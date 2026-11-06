"""Plan large indexes at module/feature granularity and retain historical research."""
from collections import Counter
import json
from pathlib import Path
import sys

from .store import atomic_write, canonical, require

# Keep the original SCC planner for genuinely small native fixtures and bounded runs.
SMALL_SCOPE = 256
FINE_KINDS = ("source_research", "scc_synthesis", "asset_discovery", "requirement_mapping")
FINE_SLOTS = ",".join("?" for _ in FINE_KINDS)
UNSTARTED = ("run=? AND status='queued' AND attempt=0 AND result IS NULL AND kind IN (" + FINE_SLOTS + ") "
             "AND (kind<>'asset_discovery' OR json_extract(data,'$.bundle.change') IS NULL)")


def use_modules(store, index, granularity):
    require(granularity in {"auto","module"}, "Choose auto or module granularity")
    if granularity == "module" or index.get("mode") in {"inventory","ecs","ecs_module"} or store.get_meta("module-queue:"+index["id"]):
        return True
    # A bounded index probe also works with old runs that have no reliable coverage counters.
    for table, field, key in (("symbols","run",index["id"]), ("tasks","run",index["id"]),
                              ("documents","snapshot",index["snapshot"]), ("assets","snapshot",index["snapshot"])):
        if store.db.execute(f"SELECT 1 FROM {table} WHERE {field}=? LIMIT 1 OFFSET ?", (key,SMALL_SCOPE)).fetchone():
            return True
    return False


def queue_report(store, run):
    groups = [dict(r) for r in store.db.execute(
        "SELECT kind,status,count(*) AS count FROM tasks WHERE run=? GROUP BY kind,status ORDER BY kind,status", (run,))]
    totals = Counter()
    for group in groups:
        totals[group["status"]] += group["count"]
    return {"by_kind_and_status":groups, "by_status":dict(totals), "total":sum(totals.values()),
            "pending":sum(totals[s] for s in ("queued","needs_research","leased")),
            "deferred":totals["deferred"], "submitted":totals["submitted"], "accepted":totals["accepted"]}


def queue_runs(store):
    rows = store.db.execute("SELECT run,snapshot,profile,count(*) AS total, "
        "sum(status='queued') AS queued,sum(status='leased') AS leased,sum(status='submitted') AS submitted,"
        "sum(status='accepted') AS accepted,sum(status='deferred') AS deferred FROM tasks "
        "GROUP BY run,snapshot,profile ORDER BY total DESC,run")
    return {"runs":[dict(row) for row in rows],"read_only":True,
            "next":"选择有历史学习任务的 run，在同一 Windows 学习工作区预览或切换。"}


def preview(store, run, granularity="auto"):
    from .study import default_module
    index = store.record("runs",run)
    require(index["status"] in {"ready","partial"}, "Use a finished index")
    strategy = "module" if use_modules(store,index,granularity) else "scc"
    plan_id = store.get_meta("plan-for:"+run)
    if plan_id:
        module_count = len(store.get_meta(plan_id)["modules"])
    else:
        selected = index.get("selected_files")
        paths = set(selected) if selected is not None else None
        repo = store.profile(index["snapshot"],index["profile"])["repository"] if paths is not None else None
        module_count = len({default_module(r["repo"], r["path"]) for r in store.db.execute(
            "SELECT repo,path FROM assets WHERE snapshot=? AND kind='source' AND status<>'excluded'", (index["snapshot"],))
            if paths is None or (r["repo"] == repo and r["path"] in paths)})
    eligible = store.db.execute("SELECT count(*) FROM tasks WHERE "+UNSTARTED, (run,*FINE_KINDS)).fetchone()[0]
    return {"run":run, "snapshot":index["snapshot"], "strategy":strategy,"module_count":module_count,
            "legacy_unstarted_upper_bound":eligible,"queue":queue_report(store,run),"read_only":True,
            "next":"在 Windows 学习工作区用 plan --run 原ID --granularity module 应用。保留在办任务需要的前置依赖。"}


def defer_unstarted(store, run):
    """Caller holds the writer transaction. Keep the entire prerequisite closure of live work."""
    require(store.db.in_transaction, "Queue changes require a transaction")
    if not store.db.execute("SELECT 1 FROM tasks WHERE "+UNSTARTED+" LIMIT 1", (run,*FINE_KINDS)).fetchone():
        return 0
    before = store.db.total_changes
    store.db.execute("WITH RECURSIVE candidates(id) AS MATERIALIZED (SELECT id FROM tasks WHERE "+UNSTARTED+"), "
        "needed(id) AS (SELECT e.dependency FROM candidates c JOIN task_edges e ON e.dependency=c.id "
        "JOIN tasks parent ON parent.id=e.task LEFT JOIN candidates p ON p.id=e.task "
        "WHERE p.id IS NULL AND parent.status IN ('queued','needs_research','leased','submitted') UNION "
        "SELECT e.dependency FROM needed n JOIN task_edges e ON e.task=n.id JOIN candidates c ON c.id=e.dependency) "
        "UPDATE tasks SET status='deferred' WHERE id IN (SELECT id FROM candidates EXCEPT SELECT id FROM needed)",
        (run,*FINE_KINDS))
    return store.db.total_changes - before


def module_plan(store, index):
    from .study import guide, inventory
    run = index["id"]
    head = store.get_meta("snapshot_head")
    require(not head or head == index["snapshot"], "Choose the run for the current learning snapshot")
    plan_id = store.get_meta("plan-for:"+run)
    if plan_id:
        with store.transaction():
            require(store.get_meta("snapshot_head") in (None,index["snapshot"]), "Learning snapshot changed")
            parked = defer_unstarted(store,run)
            store.set_meta("module-queue:"+run, True)
            store.set_meta("study_head",plan_id)
            if parked:
                store.event("defer_fine_tasks", {"run":run,"count":parked})
        result = guide(store,plan_id)
    else:
        report = inventory(store, {}, snapshot=index["snapshot"], existing_run=index, module_queue=True)
        result, parked = report["study_plan"], report["newly_deferred"]
    ids = [m["survey_task"] for m in result["modules"]]
    if result.get("document_task"):
        ids.append(result["document_task"])
    mcp = Path(result["plan_file"]).with_name("researcher.mcp.json")
    script = Path(__file__).resolve().parents[1] / "unified_kb.py"
    atomic_write(mcp, canonical({"mcpServers":{"gaussdb_knowledge":{"command":sys.executable,
        "args":["-X","utf8",str(script),"--home",str(store.home),"serve","--transport","stdio","--role","researcher"]}}}))
    return {**result,"run":run,"strategy":"module","tasks":ids,"mcp":str(mcp),
            "module_count":len(result["modules"]), "newly_deferred":parked,"queue":queue_report(store,run),
            "semantic_completion":"not_certified","next":"guide 查看模块，focus --module 指定模块 --question 具体特性 为一个问题建一个任务。"}


def previous_research(store, task):
    """Show applicable old task results separately from accepted Wiki units."""
    b = task["bundle"]
    files = set(b.get("selected_files", []))
    module = b.get("module")
    if not files and module and b.get("plan_id"):
        plan = store.get_meta(b["plan_id"], {})
        files.update(plan.get("modules", {}).get(module, {}).get("files", []))
    if not files:
        files.update(r[0] for r in store.db.execute("SELECT asset FROM anchors WHERE id IN (SELECT value FROM json_each(?))",
                                                    (canonical(b.get("source_anchor_refs", [])),)))
    rows = list(store.db.execute(
        "WITH files(asset) AS MATERIALIZED (SELECT value FROM json_each(?)) "
        "SELECT t.id,t.kind,t.status FROM tasks t WHERE t.run=? AND t.id<>? AND t.status IN ('accepted','submitted') "
        "AND t.result IS NOT NULL AND (json_extract(t.data,'$.bundle.module')=? OR json_extract(t.data,'$.bundle.asset') IN (SELECT asset FROM files) "
        "OR EXISTS (SELECT 1 FROM json_each(t.data,'$.bundle.source_anchor_refs') r JOIN anchors a ON a.id=r.value "
        "WHERE a.asset IN (SELECT asset FROM files))) ORDER BY t.status,t.id LIMIT 21",
        (canonical(sorted(files)),task["run"],task["id"],module)))
    result = {"tasks":[dict(r) for r in rows[:20]],"truncated":len(rows)>20,
              "next":"用 task context 查看关联历史结果。submitted 仍需审阅，当前结论仍需读取对应版本证据。"}
    if b.get("plan_id"):
        remote = store.get_meta("coordinator-history:" + b["plan_id"])
        if remote:
            result["coordinator_at_dispatch"] = remote
            result["coordinator_note"] = "工作包派发时的历史研究索引。原始结果和最新审阅状态可按 ID 在协调端查询。"
    return result


def feature_plan(store, index, targets, question, limit):
    """One explicitly requested behavior, bounded seeds and one-hop evidence. Never visit the full connected component."""
    from .indexer import query_graph
    from .planner import create_task
    from .study import default_module
    targets = sorted(set(targets))
    require(0 < len(targets) <= limit, "Too many targets for one feature; narrow the question or adjust --max-symbols")
    run = index["id"]
    seeds, missing = {}, []
    for target in targets:
        rows = store.lookup_symbols(run,target,limit=limit+1)
        if not rows:
            missing.append(target)
        seeds.update((r["id"],r) for r in rows)
        require(len(seeds) <= limit, "Ambiguous feature seeds exceed --max-symbols; use exact symbol IDs")
    if not seeds:
        return {"strategy":"feature","run":run,"tasks":[],"unresolved_targets":missing}
    graph = query_graph(store,run,seeds,kinds=["CALLS"],direction="both",depth=1,limit=limit)
    nodes = {n["id"]:n for n in graph["nodes"]}
    nodes.update((key,json.loads(row["data"])) for key,row in seeds.items())
    chosen = [*sorted(seeds), *sorted(set(nodes)-seeds.keys())]
    plan_id = store.get_meta("plan-for:"+run)
    first = next(iter(seeds.values()))["asset"]
    repo, path = first.split("/",1)
    module = default_module(repo,path)
    if plan_id:
        view = store.get_meta(plan_id)
        require(not view.get("worker_scope") or any(r["asset"] in view["modules"][view["worker_scope"]]["files"] for r in seeds.values()),
                "Choose a feature seed in the assigned module")
        module = view.get("worker_scope") or next((m for m,v in view["modules"].items() if first in v["files"]),module)
    bundle = {"module":module,"plan_id":plan_id,"seed_targets":targets,"seed_symbol_refs":sorted(seeds),"unresolved_targets":missing,
              "question":question or "核对这些入口的行为、生产者、消费者和一个边界条件。",
              "symbol_refs":chosen[:limit],"source_anchor_refs":list(dict.fromkeys(nodes[k]["evidence"] for k in chosen[:limit])),
              "selected_files":sorted({r["asset"] for r in seeds.values()}),
              "graph_depth":1,"graph_truncated":graph["truncated"] or len(chosen)>limit,"scope":"bounded_feature"}
    with store.transaction():
        task = create_task(store,snapshot=index["snapshot"],run=run,profile=index["profile"],kind="feature_research",bundle=bundle)
    return {"strategy":"feature","run":run,"tasks":[task],"unresolved_targets":missing,"graph_truncated":bundle["graph_truncated"],
            "evidence_count":len(bundle["source_anchor_refs"]),"semantic_completion":"not_started"}
