"""Inventory-first study plans, bounded TU selection and reviewed module work."""
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
import json
import time

from .indexer import build_index
from . import catalog, product_adapter
from .materials import CPP, ingest
from .navigation import available, navigate
from .planner import create_task, task_status
from .store import atomic_write, canonical, digest, identity, now, require


STAGES = [
    "从设计、手册、注册和测试列出候选特性，记录缺少设计的历史行为。",
    "选一个行为，定位入口、状态生产者、消费者、宏条件和反例，按需解析相关 TU。",
    "将源码证据、公共机制、跨模块接口及测试依据提交审阅，回读开发、测试与 review 上下文。",
]
ALIASES = {"optimizer": ("优化器", "优化", "规划"), "executor": ("执行器", "执行计划"),
           "storage": ("存储",), "transaction": ("事务",), "parser": ("语法", "解析")}


def default_module(repo, path):
    dirs = list(PurePosixPath(path).parts[:-1])
    if not dirs:
        return repo + "/@root"
    start = 0
    for marker in ("gausskernel", "common", "include", "src"):
        if marker in dirs:
            start = dirs.index(marker) + 1
            break
    end = min(len(dirs), start + 1)
    if end and dirs[end - 1] in {"runtime", "storage"}:
        end = min(len(dirs), end + 1)
    return "/".join([repo, *dirs[:end]])


def material_signature(snap):
    # Absolute checkout paths are intentionally absent from the transfer contract.
    facts = [(a["key"], a["kind"], a["status"], a.get("sha"), a.get("text_sha"),
              a.get("document_status"), a.get("declared_revision")) for a in snap["assets"]]
    repos = [(m["id"], m.get("git_head")) for m in snap["materials"] if m["kind"] == "source"]
    return digest([snap["product"], snap["revision"], sorted(repos), sorted(facts), snap["methods_digest"], snap.get("source_index")])


def inventory(store, config, profile=None, snapshot=None, existing_run=None, module_queue=False, source_only=False):
    started = time.monotonic()
    adapter = product_adapter.load(config.get("product_adapter"))
    snap = store.record("snapshots", snapshot) if snapshot else ingest(store, config)
    configured = [p["id"] for p in snap["profiles"] if p["id"] != "unknown"]
    profile = existing_run["profile"] if existing_run else profile or (configured[0] if configured else "unknown")
    binding = store.profile(snap["id"], profile)
    rid = existing_run["id"] if existing_run else identity("index", ["source-only/v1" if source_only else "inventory/v2", snap["id"], binding["digest"]])
    prefixes = sorted(set(config.get("module_prefixes", [])), key=len, reverse=True)
    sources = [a for a in snap["assets"] if a["kind"] == "source"]
    if existing_run and not existing_run.get("source_index") and existing_run.get("selected_files") is not None:
        selected = set(existing_run["selected_files"])
        sources = [a for a in sources if a["repo"] == binding["repository"] and a["path"] in selected]
    for prefix in prefixes:
        require(isinstance(prefix, str) and any(a["key"] == prefix or a["key"].startswith(prefix.rstrip("/") + "/") for a in sources),
                "Module prefix does not match source: " + str(prefix))
    groups = defaultdict(list)
    for asset in sources:
        if asset["status"] == "excluded":
            continue
        module = next((p for p in prefixes if asset["key"] == p or asset["key"].startswith(p.rstrip("/") + "/")), None)
        groups[module or product_adapter.module_for(adapter, asset["repo"], asset["path"])].append(asset["key"])
    docs = [json.loads(r[0]) for r in store.db.execute("SELECT data FROM documents WHERE snapshot=? ORDER BY id", (snap["id"],))]
    units = Counter(binding["repository"] + "/" + c["file"] for c in binding["commands"])
    by_key = {a["key"]: a for a in snap["assets"]}
    aliases = adapter.get("aliases", {})
    candidates = catalog.discover(store, snap, groups, docs, aliases, adapter)
    topic_signals, signal_gaps = product_adapter.signals(store, snap, groups, adapter)
    plan_id = identity("study-plan", [rid, sorted(prefixes), adapter["digest"]])
    coverage = {"mode": "inventory", "assets": len(sources), "available_tus": len(binding["commands"]),
                "translation_units": 0, "parsed_tus": 0, "partial_tus": 0, "failed_tus": 0,
                "deferred_tus": len(binding["commands"]), "invalid_commands": len(binding.get("unavailable_commands", [])), "semantic_completeness": "not_certified"}
    run = {"id": rid, "snapshot": snap["id"], "profile": profile, "profile_digest": binding["digest"],
           "created": now(), "status": "partial", "mode": "inventory", "coverage": coverage, "tu_results": [],
           "completed_tus": [], "frontend_invocations": 0, "cache_hits": 0,
           "facts_digest": digest(coverage), "database_execution": "not_run"}
    stages = list(STAGES)
    if existing_run:
        stages[0] = "盘点本模块的特性清单。每项记录行为、入口、文档或注册位置及待核问题，同一行为的多个函数合在一起。"
        stages[1] = "一次选择一个特性，用已有索引追入口、状态、跨模块消费者。按需建一个研究任务，阅读冻结源码并核对反例。"
        run = existing_run
        coverage = {**existing_run["coverage"], "mode":"ecs" if existing_run.get("source_index") else "existing_index", "frontend_invocations":0,
                    "available_tus":len(binding["commands"]), "assets":len(sources)}
    if source_only:
        run["mode"] = coverage["mode"] = "source_only"
        stages[1] = "按特性读取冻结源码和设计，记录调用位置、条件及反例。编译配置未知的关系留待 ECS 验证。"
    modules = {}
    original_head = store.get_meta("snapshot_head")
    previous = store.get_meta(plan_id,{})
    routes = previous.get("routes",{})
    for lead in candidates:
        if lead["id"] in routes and routes[lead["id"]] in groups:
            lead["owner_module"] = routes[lead["id"]]
            lead["owner_basis"] = "coordinator"
            lead["modules"] = sorted(set(lead["modules"]) | {lead["owner_module"]})
    parked = 0
    with store.transaction():
        if module_queue:
            from .course import defer_unstarted
            require(store.get_meta("snapshot_head") == original_head, "Learning snapshot changed during planning")
            parked = defer_unstarted(store,rid)
            store.set_meta("module-queue:"+rid,True)
            if parked:
                store.event("defer_fine_tasks",{"run":rid,"count":parked})
        store.db.execute("INSERT OR IGNORE INTO runs VALUES(?,?,?,?,?,?)",
                         (rid, snap["id"], profile, run["created"], "partial", canonical(run)))
        for module, keys in sorted(groups.items()):
            keys = sorted(keys)
            token = module.split("/")[-1].casefold()
            terms = (token, *aliases.get(token, ()))
            matches = [d for d in docs if any(t in (d["title"] + " " + d["asset"]).casefold() for t in terms)]
            # Only supply a bounded first source excerpt; deeper evidence is read on demand.
            example = next((k for k in keys if PurePosixPath(k).suffix.lower() in CPP and by_key[k].get("bytes")), None)
            anchors = [d["anchor"] for d in matches[:3]]
            if example:
                prior = None
                if existing_run:
                    prior = store.db.execute("SELECT id FROM anchors WHERE snapshot=? AND asset=? ORDER BY start,id LIMIT 1",
                                             (snap["id"],example)).fetchone()
                if prior:
                    anchors.append(prior[0])
                elif not existing_run or store.blob_path(by_key[example]["sha"]).is_file():
                    count = len(store.source_lines(by_key[example]["sha"]))
                    if count:
                        anchors.append(store.anchor(snap["id"], example, 1, min(40, count))["id"])
            previous_task = previous.get("modules",{}).get(module,{}).get("task")
            task = previous_task or create_task(store, snapshot=snap["id"], run=rid, profile=profile, kind="module_survey",
                bundle={"module": module, "plan_id": plan_id, "scope_digest": digest(keys), "assets": len(keys),
                        "source_anchor_refs": anchors, "question": module + " 有哪些特性、入口、公共机制和跨模块消费者？"})
            modules[module] = {"files": keys, "available_tus": sum(units[k] for k in keys),
                               "document_matches": [d["id"] for d in matches], "task": task}
            records = [by_key[k] for k in keys]
            tu_states = Counter()
            for a in records:
                tu_states.update(a.get("tu_status",{}))
            modules[module]["graph_coverage"] = {
                "checkout_files":sum(a.get("inventory_origin")!="ecs_only" for a in records),
                "ecs_manifest_files":sum(a.get("inventory_origin") in {"checkout_and_ecs","ecs_only"} for a in records),
                "checkout_only_files":sum(a.get("inventory_origin")=="checkout_only" for a in records),
                "ecs_only_files":sum(a.get("inventory_origin")=="ecs_only" for a in records),
                "tu_observations":dict(tu_states), "command_entries":modules[module]["available_tus"]}
        for lead in candidates:
            if lead["owner_module"]:
                matches = modules[lead["owner_module"]]["document_matches"]
                for ref in lead["evidence"]:
                    if ref.get("document") and ref["document"] not in matches:
                        matches.append(ref["document"])
        mapped = {d for m in modules.values() for d in m["document_matches"]}
        unmapped = [d for d in docs if d["id"] not in mapped]
        mapping_task = None
        if unmapped:
            mapping_task = create_task(store, snapshot=snap["id"], run=rid, profile=profile, kind="document_survey",
                bundle={"plan_id": plan_id, "source_anchor_refs": [d["anchor"] for d in unmapped[:8]],
                        "question": "将未归属的设计和手册章节映射到特性，保留文码差异。"})
        gaps = [a["key"] for a in snap["assets"] if a["status"] == "failed" or a.get("extraction_error")]
        plan = {"id": plan_id, "snapshot": snap["id"], "run": rid, "profile": profile,
                "product_adapter": adapter, "topic_signals": topic_signals, "signal_gaps": signal_gaps,
                "catalog_version":2,"candidates":candidates,"routes":routes,
                "profiles": configured, "module_prefixes": sorted(prefixes), "material_signature": material_signature(snap),
                "modules": modules, "documents": len(docs),
                "navigation": {r["id"]: ("ecs-index" if existing_run else "codegraph" if available(r["root"]) else "scoped-tree-sitter")
                               for r in snap["materials"] if r["kind"] == "source"}, "unmapped_documents": [d["id"] for d in unmapped],
                "document_task": mapping_task, "gaps": gaps, "stages": stages, "coverage": coverage}
        if source_only:
            plan["source_only"] = True
            plan["navigation"] = {r["id"]:"source-text" for r in snap["materials"] if r["kind"]=="source"}
        if existing_run:
            plan["reuse_index"] = True
            origin = existing_run.get("source_index")
            if not origin:
                require(existing_run.get("facts_digest"), "A completed graph digest is required for module learning")
                origin = {"provider":"workspace-sqlite/v1", "run_id":rid, "snapshot":snap["id"], "profile":profile,
                          "profile_digest":existing_run["profile_digest"], "facts_digest":existing_run["facts_digest"]}
            plan["source_index"] = origin
            provider = "workspace-index" if origin["provider"] == "workspace-sqlite/v1" else "ecs-index"
            plan["navigation"] = {r["id"]:provider for r in snap["materials"] if r["kind"]=="source"}
            store.set_meta("snapshot_head", snap["id"])
        store.set_meta(plan_id, plan)
        store.set_meta("study_head", plan_id)
        store.set_meta("plan-for:" + rid, plan_id)
        index_head = "index_head:" + snap["id"] + ":" + profile
        if existing_run or not store.get_meta(index_head):
            store.set_meta(index_head, rid)
    summary = guide(store, plan_id)
    return {"snapshot": snap["id"], "newly_deferred":parked, "batches": [{"index": run, "plan": summary}], "study_plan": summary,
            "seconds": round(time.monotonic() - started, 3), "status": "awaiting_actual_research_and_review",
            "automatic_semantic_completion": False, "database_execution": "not_run"}


def current(store, plan_id=None):
    key = plan_id or store.get_meta("study_head")
    result = store.get_meta(key) if key else None
    require(result, "Configure project paths to generate the study plan first")
    return result


def route(store, cid, module):
    with store.transaction():
        plan = current(store)
        require(not plan.get("worker_scope") and module in plan["modules"],"请在协调端选择一个有效模块")
        lead = catalog.candidate(plan,cid,store)
        active = store.db.execute("SELECT 1 FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? "
                                  "AND json_extract(data,'$.bundle.candidate_id')=?",(plan["snapshot"],plan["id"],cid)).fetchone()
        require(not active or lead["owner_module"]==module,"该候选已有研究任务，请先处理现有任务")
        lead["owner_module"] = module
        lead["owner_basis"] = "coordinator"
        lead["modules"] = sorted(set(lead["modules"]) | {module})
        plan.setdefault("routes",{})[cid] = module
        extra = store.get_meta("planning-candidates:" + plan["id"], [])
        if any(c["id"] == cid for c in extra):
            store.set_meta("planning-candidates:" + plan["id"], [lead if c["id"] == cid else c for c in extra])
        docs = plan["modules"][module]["document_matches"]
        docs.extend(d for d in dict.fromkeys(r.get("document") for r in lead["evidence"]) if d and d not in docs)
        store.set_meta(plan["id"],plan)
    return {"candidate":cid,"owner_module":module,"plan":guide(store)["plan_file"],
            "next":"派发或更新该模块工作包，成员可用候选 ID 领取。"}

def guide(store, plan_id=None):
    plan = current(store, plan_id)
    modules = []
    work = defaultdict(list)
    for row in store.db.execute("SELECT id,run,status,json_extract(data,'$.bundle.module') module FROM tasks "
                                "WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=?", (plan["snapshot"], plan["id"])):
        if row["module"]:
            work[row["module"]].append({"task": row["id"], "run": row["run"], "status": row["status"]})
    published = {tid for row in store.db.execute("SELECT data FROM proposals WHERE status='accepted'")
                 for tid in json.loads(row[0]).get("research_tasks", [])}
    origin = plan.get("source_index")
    indexed = bool(origin or plan.get("reuse_index"))
    for name, value in plan["modules"].items():
        assignment = store.get_meta("assignment:" + plan["id"] + ":" + name, {})
        task = assignment.get("received_task") or value["task"]
        entry = {"module": name, "file_count": len(value["files"]), "tu_count": value["available_tus"],
                 "doc_candidates": len(value["document_matches"]), "task": task, "survey_task":value["task"],
                 "research_status": task_status(store, task)["status"], "worker": assignment.get("worker"),
                 "research_tasks": work[name], "published_tasks": sum(t["task"] in published for t in work[name])}
        if indexed:
            states = {t["status"] for t in entry["research_tasks"] if t["task"] not in published}
            if not entry["worker"]:
                action = "分配模块或开始特性盘点"
            elif "submitted" in states:
                action = "协调端审阅已提交的证据与结论"
            elif "accepted" in states:
                action = "协调端合并已审阅的知识"
            elif entry["published_tasks"]:
                action = "核对剩余特性和缺口，继续下一项"
            else:
                action = "成员领取任务，核对入口、消费者和边界"
            entry["next_action"] = action
        entry["graph_coverage"] = value.get("graph_coverage",{})
        modules.append(entry)
    first_batch = []
    if indexed and not plan.get("worker_scope"):
        pending = [m for m in modules if not m["worker"] and not m["published_tasks"]]
        eligible = sorted(pending, key=lambda m: (not bool(m["doc_candidates"]), not bool(m["tu_count"]), m["module"]))
        first_batch = [{"module":m["module"], "reason":("有候选设计或手册，可先对照实现" if m["doc_candidates"] else
                       "从编译记录与注册入口恢复行为" if m["tu_count"] else "先检查目录、注册、接口或测试清单")} for m in eligible[:3]]
    folder = store.home / "learning" / plan["id"].replace(":", "-")
    guide_path = folder / "PLAN.md"
    description = (f"来源索引 {origin['run_id']}，源码快照 {origin['snapshot']}。学习使用已经生成的符号和关系。"
                   if origin else f"使用已有索引 {plan['run']}，按特性研究。" if indexed else f"本次盘点启动 Clang 0 次。可按需解析 {plan['coverage']['available_tus']} 个编译单元。")
    if plan.get("source_only"):
        description = "使用冻结源码和文档学习。编译配置、跨文件调用绑定及宏分支保留为待核项。"
    lines = ["# " + ("成员模块学习计划" if plan.get("worker_scope") else "源码学习计划"), "", f"学习快照 {plan['snapshot']}，配置 {plan['profile']}。",
             description]
    coverage = plan["coverage"]
    if "candidates" in plan:
        leads = list(catalog.entries(store,plan))
        lines += ["", f"当前范围有 {sum(m['file_count'] for m in modules)} 个源码资产、{len(modules)} 个模块、{len(leads)} 个候选特性。候选清单独立于任务队列。",
                  "模块图覆盖按 ECS 源码清单和逐 TU 回执分别统计。清单内文件仍需核对具体调用边，图外模块可以直接读源码。",
                  "", "## 可领取的特性", "", "用 `features` 分页查看全部候选，用 `learn --candidate <ID>` 建一单。待归属时加 `--module`。"]
        for lead in leads[:12]:
            label = lead["title"].replace("\n"," ")[:120]
            lines.append(f"- {label} · {lead['state']} · {lead['owner_module'] or '待归属'} · `{lead['id']}`")
    if indexed:
        if plan.get("worker_scope"):
            lines += ["", f"此包覆盖 {plan['worker_scope']} 及其一跳邻居，共 {coverage['symbols']} 个符号、{coverage['relations']} 条关系。"]
        else:
            lines += ["", f"本次运行有 {coverage.get('symbols', 0)} 个符号和 {coverage.get('relations', 0)} 条关系。",
                      f"上游 TU 已解析 {coverage.get('parsed_tus', '未知')}，部分解析 {coverage.get('partial_tus', '未知')}，失败 {coverage.get('failed_tus', '未知')}。",
                      "这些数字衡量索引覆盖。每项行为、跨模块契约和宏条件仍需成员以源码验证。"]
    lines += ["", "| 模块候选 | 文件 | ECS 清单内文件 | 编译记录 | TU 实测状态 | 文档候选 | 负责人 | 调研任务状态 | 已入库任务 | 下一步 |",
              "|---|---:|---:|---:|---|---:|---|---|---:|---|"]
    for m in modules:
        graph = m["graph_coverage"]
        lines.append(f"| {m['module']} | {m['file_count']} | {graph.get('ecs_manifest_files','未知')} | {m['tu_count']} | {graph.get('tu_observations') or '无回执'} | {m['doc_candidates']} | "
                     f"{m['worker'] or '待分配'} | {dict(Counter(t['status'] for t in m['research_tasks']))} | {m['published_tasks']} | {m.get('next_action', '查看模块计划')} |")
    lines += ["", *[f"{i}. {s}" for i, s in enumerate(plan["stages"], 1)],
              "", "选模块后执行 focus --module <模块>。用模块任务单把工作分配到其他服务器。"]
    if modules and not indexed and not plan.get("source_only"):
        example = next((m for m in modules if m["tu_count"]), modules[0])
        lines.extend(["", "第一批可以从下列模块开始", "",
                      f"- 模块 {example['module']} 的盘点任务为 {example['task']}。用 guide --module 查看实际文件和资料入口。",
                      f"- 在工程 CLI 的 --home 参数后添加 focus --module {example['module']} --limit 3 可深化一个小批次。",
                      "- 需要分工时用 team assign 输出工作单，工作端用 team open，完成后 export，协调端用 receive。",
                      "- 多个模块回来后用 integrate 连接已解析的图，保留未解析目标。"])
    if origin:
        example = (first_batch[0]["module"] if first_batch else modules[0]["module"] if modules else "")
        if first_batch:
            lines += ["", "## 建议的首批可分配模块", "", *[f"- {m['module']}。{m['reason']}。" for m in first_batch]]
        if plan.get("worker_scope"):
            lines += ["", "## 当前成员的步骤", "", f"1. 用 `guide --module {example}` 查看候选入口和应答问题。",
                      f"2. 用 `focus --module {example} --symbol <入口符号>` 在现有调用图上建研究任务，记录生产者、消费者、条件和反例。",
                      "3. 按工作单身份读取源码与文档，提交研究，用 `team export` 将结果送回协调端。"]
        elif example:
            lines += ["", "## 协调端的步骤", "", f"1. 用 `guide --module {example}` 查看第一批材料和应答问题。",
                      f"2. 用 `team assign --module {example} --worker <成员名> --kit <模块>.zip` 分配工作。不同模块可并行。",
                      "3. 成员端用 `team open --kit` 打开工作包并导出研究结果。协调端用 `team receive` 验收版本和引用。",
                      "4. 分别审阅研究任务和知识提案。入库后再次执行 `guide` 查看任务状态，接着研究其余特性。"]
    if indexed:
        lines += ["", "模块盘点后，针对清单中的每个具体行为用 focus 创建任务。函数、调用边和文件作为证据保存。",
                  "历史细任务的 deferred 表示待按需核查，已接受和待审的研究仍可引用。"]
    if indexed and not origin and modules:
        lines += ["", f"先用 guide --module {modules[0]['module']} 查看入口，再按行为用 focus --module <模块> --question <特性> 创建研究任务。"]
    if plan["document_task"]:
        lines.append(f"另有 {len(plan['unmapped_documents'])} 个待映射文档片段。任务 {plan['document_task']}。")
    if plan["gaps"]:
        lines.append(f"有 {len(plan['gaps'])} 个材料读取或提取缺口，见计划 JSON 的 gaps。")
    if not store.readonly:
        atomic_write(guide_path, "\n".join(lines) + "\n")
        atomic_write(folder / "plan.json", canonical(plan))
    return {"plan_id": plan["id"], "plan_file": str(guide_path), "snapshot": plan["snapshot"],
            "profile": plan["profile"], "study_run": plan["run"], "coverage": coverage, "suggested_first_batch":first_batch, "source_index": origin, "worker_scope":plan.get("worker_scope"), "modules": modules, "stages": plan["stages"], "navigation": plan["navigation"],
            "unmapped_documents": len(plan["unmapped_documents"]), "document_task":plan["document_task"], "gaps": plan["gaps"],
            "compile_command_gaps": store.profile(plan["snapshot"], plan["profile"]).get("unavailable_commands", []),
            "next": "用 guide --module 查看入口、资料和待答问题；focus 创建研究任务，team assign 分工，guide 查看进度。"}


def ecs_neighbors(store, plan, symbol, direction, limit):
    from .planner import resolve_targets
    from .indexer import query_graph
    if plan.get("source_only"):
        return {"provider":"source-text","relations":[],"nodes":[],"run":plan["run"],"next":"本工作区按源码阅读，可用 learn --symbol 或 --file 定位，再通过证据工具读取实际行。"}
    seeds, missing = resolve_targets(store,plan["run"],[symbol])
    origin = plan.get("source_index")
    provider = "workspace-index" if not origin or origin.get("provider") == "workspace-sqlite/v1" else "ecs-index"
    return {"provider":provider,"source_index":origin,"unresolved_targets":missing,
            **query_graph(store,plan["run"],seeds,direction=direction,kinds=["CALLS"],depth=2,limit=limit,walk="dfs")}


def module_guide(store, module):
    plan = current(store)
    info = plan["modules"].get(module)
    require(info, "Unknown module; see guide")
    docs = [store.db.execute("SELECT data FROM documents WHERE id=?", (d,)).fetchone()
            for d in info["document_matches"][:8]]
    readings = [{"asset": d["asset"], "title": d["title"], "start": d["start"], "end": d["end"]}
                for row in docs if row for d in [json.loads(row[0])]]
    candidates = sorted(info["files"], key=lambda key: (PurePosixPath(key).suffix.lower() not in CPP, key))
    questions = ["从入口或注册点追到实现，列出用户可观察行为及其条件。",
                 "哪些字段或状态由本模块产生，由哪些模块消费？缺少哪些证据？",
                 "为一个边界条件给出测试预期、反例和 review 要查的代码位置。"]
    result = {**info, "module": module, "source_starting_points": candidates[:6], "document_starting_points": readings,
              "questions": questions, "survey_task": info["task"],
              "focus_command": "focus --module " + module + " --limit 3 --question 具体特性或符号"}
    if plan.get("source_index") or plan.get("reuse_index"):
        rows = store.db.execute("SELECT data FROM symbols WHERE run=? AND asset IN (SELECT value FROM json_each(?)) "
                    "AND kind IN ('function_decl','cxx_method','constructor','function_template') "
                    "AND json_extract(data,'$.definition')=1 ORDER BY asset,name,id LIMIT 6", (plan["run"],canonical(info["files"])))
        examples = [{k:s.get(k) for k in ("id","name","asset","evidence")} for row in rows for s in [json.loads(row[0])]]
        result["indexed_definitions"] = examples
        if examples:
            result["focus_command"] = "focus --module " + module + " --symbol " + examples[0]["id"]
    return result


def focus(store, module=None, *, files=(), limit=12, jobs=2, extend=None, question=None, profile=None, symbol=None, candidate_id=None):
    plan = current(store)
    lead = None
    if candidate_id:
        lead = catalog.candidate(plan,candidate_id,store)
        module = module or lead["owner_module"]
        require(module,"该候选待归属，请用 --module 指定责任模块")
        require(not lead["owner_module"] or module==lead["owner_module"],"该候选属于 "+str(lead["owner_module"]))
        question = question or lead["question"]
    require(module in plan["modules"], "Unknown module; see guide")
    require(1 <= limit <= 100, "Reading budget must be from 1 to 100")
    info = plan["modules"][module]
    if plan.get("source_index") or plan.get("reuse_index") or plan.get("source_only"):
        from .ecs import focus_existing
        return focus_existing(store, plan, module, files, limit, question, symbol, profile, extend, lead)
    profile = profile or plan["profile"]
    binding = store.profile(plan["snapshot"], profile)
    repo = binding["repository"] or module.split("/", 1)[0]
    available = {c["file"] for c in binding["commands"]}
    if profile == "unknown":
        available = {r[0] for r in store.db.execute(
            "SELECT path FROM assets WHERE snapshot=? AND repo=? AND status='frozen'", (plan["snapshot"], repo))
                     if PurePosixPath(r[0]).suffix.lower() in CPP}
    module_files = set(info["files"])
    inside = {p for p in available if repo + "/" + p in module_files}
    prior = set()
    if extend:
        old = store.record("runs", extend)
        require(old["snapshot"] == plan["snapshot"] and old["profile"] == profile and old.get("mode") == "selected",
                "Extension requires a selected run from this snapshot and profile")
        prior.update(old["selected_files"])
    requested = {PurePosixPath(p.replace("\\", "/")).as_posix().removeprefix(repo + "/") for p in files}
    navigation = None
    if symbol:
        navigation = navigate(store, plan["snapshot"], symbol, repository=repo)
        require(navigation["matches"], "CodeGraph did not identify this symbol")
        suggestions = {n["asset"].split("/", 1)[1] for n in navigation["matches"] + navigation["neighbors"]
                       if n["status"] == "candidate"} & available
        if not requested:
            candidates = suggestions or inside
        else:
            candidates = requested
    else:
        candidates = requested if requested else inside - prior
    require(not (candidates - available), "No matching TU/source file: " + ", ".join(sorted(candidates - available)))
    weights = Counter(c["file"] for c in binding["commands"])
    def cost(path):
        return weights.get(path, 1)
    require(not requested or sum(cost(p) for p in requested - prior) <= limit,
            "Selected files have more compile commands than the TU budget; increase --limit or narrow the scope")
    ranked = sorted(candidates - prior)
    if question and not requested:
        import re
        words = {w.casefold() for w in re.findall(r"[A-Za-z_][A-Za-z_0-9]+|[\u4e00-\u9fff]{2,}", question)}
        def rank(path):
            asset = store.asset(plan["snapshot"], repo + "/" + path)
            text = store.blob(asset["sha"]).decode("utf-8", errors="replace").casefold() if asset["sha"] else ""
            return (-sum(5 * (w in path.casefold()) + min(3, text.count(w)) for w in words), path)
        ranked.sort(key=rank)
    new_files, remaining_budget = [], limit
    for p in ranked:
        if cost(p) <= remaining_budget:
            new_files.append(p)
            remaining_budget -= cost(p)
        if not remaining_budget:
            break
    selection = sorted(prior | set(new_files))
    require(selection, "No TU fits this module/budget; use its survey task, raise --limit or select a consumer TU")
    require(inside.intersection(selection) or not inside, "Select at least one TU from the module")
    run = build_index(store, plan["snapshot"], profile, files=selection, jobs=jobs, resume=True)
    symbols = [json.loads(r[0]) for r in store.db.execute(
        "SELECT data FROM symbols WHERE run=? ORDER BY asset,name", (run["id"],))]
    selected_assets = {repo + "/" + p for p in selection}
    first = [s for s in symbols if s.get("definition") and s["asset"] in selected_assets
             and s["kind"] in {"function_decl", "candidate_function", "cxx_method"}][:12]
    with store.transaction():
        task = create_task(store, snapshot=plan["snapshot"], run=run["id"], profile=profile, kind="feature_research",
            bundle={"module": module, "plan_id": plan["id"], "selected_files": selection,
                    "question": question or module + " 的入口、生产者、消费者、边界与测试依据是什么？",
                    "symbol_refs": [s["id"] for s in first], "source_anchor_refs": [s["evidence"] for s in first]})
    return {"module": module, "task": task, "run": run["id"], "profile": profile, "selected_files": selection,
            "added_files": new_files, "navigation": navigation, "remaining_module_files": len(inside - set(selection)),
            "coverage": run["coverage"], "cache_hits": run["cache_hits"], "frontend_invocations": run["frontend_invocations"],
            "next": "领取研究任务并读取冻结证据；下一批可使用 focus --extend 当前 run。"}
