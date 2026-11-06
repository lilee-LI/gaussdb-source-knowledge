"""Real CodeWiki/Claude adapter and host-driven typed research handoff."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

from .knowledge import propose
from .planner import _check_lease, lease, submit, task_context, task_status
from .store import atomic_write, canonical, digest, identity, now, require


PROJECT = Path(__file__).resolve().parents[2]


def prepare_codewiki(store, task, worker, token, settings):
    with store.transaction():
        _check_lease(store, task, worker, token)
    context = task_context(store, task)
    require(isinstance(settings, dict), "CodeWiki runtime settings required")
    for key in ("vendor", "mcp_python", "claude", "token_cache"):
        require(settings.get(key) and Path(settings[key]).exists(), "CodeWiki runtime setting missing: " + key)
    attempt = store.db.execute("SELECT attempt FROM tasks WHERE id=?", (task,)).fetchone()[0]
    root = store.home / "worker-runs" / (task.replace(":", "-") + "-" + str(attempt))
    require(not root.exists(), "Worker attempt already prepared; use its recorded work or claim a new attempt")
    root.mkdir(parents=True)
    source = root / "source"
    source.mkdir()
    refs = context["bundle"].get("source_anchor_refs", [])
    selected = {store.record("anchors", r)["asset"] for r in refs}
    if context["bundle"].get("asset"):
        selected.add(context["bundle"]["asset"])
    # Preserve repository paths. Additional frozen ranges remain available through the evidence tools.
    for asset in selected:
        item = store.asset(context["snapshot"], asset)
        if item["kind"] == "source" and item["status"] == "frozen":
            atomic_write(source / item["repo"] / item["path"], store.blob(item["sha"]))
    if not any(source.rglob("*")):
        atomic_write(source / "scope.txt", canonical(context["bundle"]))
    background = root / "context"
    background.mkdir()
    # Bounded context avoids copying four million lines for every task.
    from .indexer import query_graph
    neighbors = query_graph(store, context["run"], context["bundle"].get("symbol_refs", []), depth=1, limit=200)
    related = selected | {n["asset"] for n in neighbors["nodes"]}
    for tu in store.record("runs", context["run"]).get("tu_results", []):
        if tu["asset"] in related:
            related.update(i["asset"] for i in tu.get("includes", []) if i["asset"])
    bounded = sorted(related)[:200]
    for asset in bounded:
        item = store.asset(context["snapshot"], asset)
        if item["kind"] == "source" and item["status"] == "frozen":
            atomic_write(background / item["repo"] / item["path"], store.blob(item["sha"]))
    manual, baseline = root / "manual", root / "baseline"
    manual.mkdir()
    baseline.mkdir()
    frozen_methods = root / "methods"
    frozen_methods.mkdir()
    method_paths = []
    enhanced_rules = None
    for row in store.db.execute("SELECT data FROM assets WHERE snapshot=? AND kind='method' AND status='frozen'", (context["snapshot"],)):
        method = json.loads(row[0])
        path = frozen_methods / method["repo"] / method["path"]
        atomic_write(path, store.blob(method["sha"]))
        method_paths.append(str(path))
        if method["repo"] == "__codewiki_enhanced_rules":
            enhanced_rules = store.blob(method["sha"])
    document_query = "SELECT data FROM assets WHERE snapshot=? AND kind='document' AND status='frozen'"
    doc_args = [context["snapshot"]]
    if context["kind"] in {"feature_research","module_survey"}:
        document_query += " AND key IN (SELECT value FROM json_each(?))"
        doc_args.append(canonical(sorted(selected)))
    for row in store.db.execute(document_query,doc_args):
        item = json.loads(row[0])
        if item.get("text_sha"):
            atomic_write(manual / (digest(item["key"])[:24] + ".md"), store.blob(item["text_sha"]))
    atomic_write(manual / "manifest.json", canonical({"snapshot": context["snapshot"], "source": "frozen material extraction"}))
    prior = store.units(ids=[c["id"] for c in context.get("reuse_candidates", [])[:30]])
    for candidate in context.get("reuse_candidates", [])[:30]:
        unit = prior[candidate["id"]]
        atomic_write(baseline / (digest(unit["id"])[:24] + ".md"), "# " + unit["title"] + "\n\n" + unit["body"])
    if not list(baseline.glob("*.md")):
        atomic_write(baseline / "scope.md", "# 尚无已审知识\n\n本页只声明研究范围，不包含语义结论。\n" + canonical(context["bundle"]))
    scope_file, module_tree = root / "scope.json", root / "module-tree.json"
    atomic_write(scope_file, canonical(context))
    atomic_write(module_tree, canonical(settings.get("module_tree_data", {"name": "research-scope", "path": str(source), "children": []})))
    work = root / "codewiki"
    cfg = {**settings, "work": str(work), "source": str(source), "context": str(background), "manual": str(manual),
           "baseline": str(baseline), "scope_file": str(scope_file), "module_tree": str(module_tree),
           "revision": context["snapshot"], "subject": context["bundle"].get("question", context["kind"]),
           "scoped_read": True, "frozen_methods_only": True, "extra_method_paths": method_paths,
           "specialist_skills": method_paths}
    cfg["extra_mcp_servers"] = {"unified": {"command": sys.executable, "args": ["-X", "utf8", str(PROJECT / "scripts/unified_kb.py"),
        "--home", str(store.home), "serve", "--transport", "stdio", "--role", "researcher"]}}
    cfg["extra_mcp_tools"] = ["mcp__unified__" + n for n in (
        "task_context", "query_graph", "create_task_evidence", "read_task_evidence", "find_knowledge", "knowledge_graph", "explain_path")]
    if settings.get("staged_submission"):
        cfg["extra_mcp_tools"] += ["mcp__unified__stage_research_unit", "mcp__unified__finish_research"]
    cfg_file = root / "codewiki-config.json"
    atomic_write(cfg_file, canonical(cfg))
    import codewiki_learning
    with contextlib.redirect_stdout(io.StringIO()):
        codewiki_learning.prepare(cfg_file)
    require(enhanced_rules is not None, "Snapshot has no frozen CodeWiki enhanced research rules")
    atomic_write(work / "enhanced-learning.md", enhanced_rules)
    lock = json.loads((work / "method-lock.json").read_text(encoding="utf-8"))
    lock["enhanced-learning.md"] = digest(enhanced_rules)
    lock["frozen_methods"] = {str(Path(p).relative_to(root)): digest(Path(p).read_bytes()) for p in method_paths}
    atomic_write(work / "method-lock.json", canonical(lock))
    with store.transaction():
        store.set_meta("worker_methods:" + task, {"digest": digest([Path(p).read_bytes().hex() for p in method_paths]),
                                                 "paths": method_paths})
    descriptor = {"task": task, "worker": worker, "attempt": attempt, "work": str(work), "root": str(root),
                  "config": str(cfg_file), "prepared": now(), "source_snapshot": context["snapshot"],
                  "driver_sha256": digest(Path(codewiki_learning.__file__).read_bytes()),
                  "status": "prepared", "semantic_approval": "not_granted", "context_assets": bounded,
                  "context_truncated": len(related) > len(bounded)}
    with store.transaction():
        _check_lease(store, task, worker, token)
        store.set_meta("worker:" + task + ":" + str(attempt), descriptor)
        store.event("codewiki_prepare", descriptor)
    return descriptor


def run_codewiki(store, task, worker, token, *, rounds=2, timeout=3600, runner=None):
    """Run the existing real executor; tests may explicitly inject a process adapter."""
    _check_lease(store, task, worker, token)
    current = task_status(store, task)
    descriptor = store.get_meta("worker:" + task + ":" + str(current["attempt"]))
    require(descriptor is not None, "Prepare CodeWiki for this task attempt first")
    command = [sys.executable, "-X", "utf8", str(PROJECT / "scripts/codewiki_learning.py"), "pipeline",
               "--work", descriptor["work"], "--max-consistency-rounds", str(rounds)]
    root = Path(descriptor["root"])
    if runner is not None:
        result = runner(command, root, timeout)
    else:
        with (root / "executor.stdout.log").open("wb") as out, (root / "executor.stderr.log").open("wb") as err:
            proc = subprocess.Popen(command, stdout=out, stderr=err,
                                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            started = time.monotonic()
            while proc.poll() is None:
                if time.monotonic() - started > timeout:
                    proc.kill()
                    proc.wait()
                    result = {"exit_code": proc.returncode, "timed_out": True}
                    break
                lease(store, task, worker, action="renew", token=token, seconds=min(86400, max(60, timeout)))
                time.sleep(1)
            else:
                result = {"exit_code": proc.returncode, "timed_out": False}
    descriptor = {**descriptor, "execution": result, "status": "generated_candidate" if result.get("exit_code") == 0 else "requires_followup",
                  "semantic_approval": "not_granted", "database_execution": "not_run"}
    with store.transaction():
        store.set_meta("worker:" + task + ":" + str(current["attempt"]), descriptor)
        store.event("codewiki_execute", descriptor)
    return descriptor


def structured_prompt(store, task, worker, token, *, staged=False):
    context = task_context(store, task)
    return (
        "你正在构建内部统一知识母库，保留源码粒度、实现关系、条件、契约和证据。"
        "此前客户包的无源码正文规则不适用于本内部研究任务。禁止运行数据库、SQL、产品编译或故障注入。"
        "已有 CodeWiki 输出只是上游候选，先读同条件的已审知识；只研究尚未回答或已经变化的问题。"
        "每一条引用必须用 mcp__unified__read_task_evidence 实际读取，截断须继续缩小原文证据范围。"
        "不得自动批准研究或发布，不得把模型新会话称为专家审阅。"
        "\n任务身份：" + canonical({"task": task, "worker": worker, "token": token}) +
        "\n冻结任务：" + canonical(context) +
        ("\n本任务采用分单元工具提交：先用 stage_research_unit 每次暂存一个 unit；全部完成后用 finish_research 提交 coverage 和最后一次返回的 drafts_digest。最终文字只简短报告状态，不输出整份 JSON。coverage 每项含 question、"
         if staged else "\n输出一个 JSON 对象，包含 coverage 数组和 units 数组。coverage 每项含 question、") +
        "status(answered/open/not_applicable)、explanation、evidence_refs。"
        "units 每项含 id、kind、title、body、conditions、counterexamples、source_refs、symbol_refs、knowledge_refs。"
        "knowledge_refs 必须是对象数组，例如 [{\"target\":\"claim:example\",\"relation\":\"DEPENDS_ON\"}]，不能是字符串数组。"
        "kind 仅允许 module/responsibility/feature/mechanism/claim/contract/flow/test_obligation/requirement/observation/decision。"
        "claim 另含 statement；contract 另含 producers、consumers(均为真实 symbol-instance id)、requires、ensures、invariants；"
        "test_obligation 另含 expected_from 对象（例如 {\"kind\":\"contract\",\"ref\":\"contract:example\"}）及 execution_status=not_run。"
        "flow 的 steps 是对象数组，kind 为 call/data_stage/state_transition/async_message，并填写实际 symbol/target。"
        "不得写入 _binding、review、content_hash 等工具保留元数据。所有 source_refs 使用本租约真正完整读取的 evidence id。"
        "责任树与特性树分开，level=1..4，跨模块通过关系连接。所有未知必须保留。"
    )


def run_structured(store, task, worker, token, *, attempt_name="structured"):
    _check_lease(store, task, worker, token)
    current = task_status(store, task)
    descriptor = store.get_meta("worker:" + task + ":" + str(current["attempt"]))
    require(descriptor, "CodeWiki runtime has not been prepared")
    root, work = Path(descriptor["root"]), Path(descriptor["work"])
    settings = json.loads(Path(descriptor["config"]).read_text(encoding="utf-8"))
    prompt = structured_prompt(store, task, worker, token, staged=settings.get("staged_submission", False))
    require(re.fullmatch(r"[A-Za-z0-9_-]+", attempt_name), "Invalid model attempt name")
    prompt_path = root / (attempt_name + ".prompt.txt")
    atomic_write(prompt_path, prompt)
    lease(store, task, worker, action="renew", token=token, seconds=min(86400, int(settings.get("timeout_seconds", 1800)) + 120))
    command = [sys.executable, "-X", "utf8", str(PROJECT / "scripts/codewiki_learning.py"), "task",
               "--work", str(work), "--name", attempt_name, "--prompt", str(prompt_path)]
    with (root / (attempt_name + ".stdout.log")).open("wb") as out, (root / (attempt_name + ".stderr.log")).open("wb") as err:
        proc = subprocess.run(command, stdout=out, stderr=err,
                              creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
    require(proc.returncode == 0, "Structured research did not complete successfully")
    return receive_structured(store, task, worker, token, attempt_name=attempt_name)


def receive_structured(store, task, worker, token, *, attempt_name="structured"):
    """Receive a completed real run without repeating a costly model invocation.

    A token-limit continuation is reconstructed only from verbatim recorded
    assistant parts and its synthetic continuation event. Raw results remain.
    """
    current = task_status(store, task)
    descriptor = store.get_meta("worker:" + task + ":" + str(current["attempt"]))
    require(descriptor, "CodeWiki runtime has not been prepared")
    require(re.fullmatch(r"[A-Za-z0-9_-]+", attempt_name), "Invalid model attempt name")
    root, work = Path(descriptor["root"]), Path(descriptor["work"])
    receipt = json.loads((work / "runs" / attempt_name / "receipt.json").read_text(encoding="utf-8"))
    require(receipt.get("exit_code") == 0 and not receipt.get("timed_out") and not receipt.get("is_error")
            and receipt.get("subtype") == "success", "Model execution has no successful receipt")
    staged = current.get("result", {}).get("capture") == "mcp_staged_units"
    if staged:
        require(current["status"] == "submitted" and current["result"]["worker"] == worker
                and current["result"]["capture_attempt"] == current["attempt"]
                and current["result"]["capture_lease_digest"] == digest(token), "Staged result identity mismatch")
        value = {"coverage": current["result"]["coverage"], "units": current["result"]["claims"]}
    else:
        _check_lease(store, task, worker, token)
        from codewiki_compare import parse_run_json
        value = parse_run_json(work / "runs" / attempt_name)
    atomic_write(root / "structured-result.json", canonical(value))
    research = current if staged else submit(store, task, worker, token, {"coverage": value["coverage"], "claims": value.get("units", [])})
    return {"task": task, "status": research["status"], "candidate_units": len(value.get("units", [])),
            "receipt": str(work / "runs" / attempt_name / "receipt.json"), "runtime_validation": "not_run"}


def propose_structured(store, task, worker):
    current = task_status(store, task)
    require(current["status"] == "accepted", "Research must be actually reviewed before knowledge proposal")
    require(current["result"]["worker"] == worker, "Research author identity mismatch")
    descriptor = store.get_meta("worker:" + task + ":" + str(current["attempt"]))
    require(descriptor and Path(descriptor["root"]).is_dir(), "Structured worker result missing")
    value = json.loads((Path(descriptor["root"]) / "structured-result.json").read_text(encoding="utf-8"))
    require(value["units"] == current["result"].get("claims", []), "Structured units changed after research submission")
    return propose(store, {"author": worker, "expected_head": store.get_meta("knowledge_head"),
                          "snapshot": current["snapshot"], "run": current["run"], "profile": current["profile"],
                          "research_tasks": [task], "units": value["units"]})
