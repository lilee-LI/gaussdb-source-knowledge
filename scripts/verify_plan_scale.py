"""Replay an old SCC queue in a disposable workspace. Measures planning, never model learning."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import time

from unified_knowledge import course, planner, study
from unified_knowledge.store import Store, canonical, require


def seed_history(store, index, count, accepted):
    # Same persisted fields as the old planner. The payloads are explicitly synthetic.
    run, snap, profile = index["id"], index["snapshot"], index["profile"]
    symbol = json.loads(store.db.execute("SELECT data FROM symbols WHERE run=? AND name='cg_compute' LIMIT 1",
                                         (run,)).fetchone()[0])

    def rows():
        for i in range(count):
            tid = "task:scale-%07d" % i
            value = {"id":tid, "snapshot":snap, "run":run, "profile":profile, "kind":"source_research",
                     "bundle":{"scc":"scale-%07d"%i, "symbol_refs":[symbol["id"]], "source_anchor_refs":[symbol["evidence"]]}}
            result = canonical({"fixture":True, "worker_note":i}) if i < accepted else None
            yield (tid,snap,run,profile,"source_research","accepted" if result else "queued",
                   int(result is not None),canonical(value),result)

    with store.transaction():
        store.db.executemany("INSERT INTO tasks(id,snapshot,run,profile,kind,status,attempt,data,result) VALUES(?,?,?,?,?,?,?,?,?)",rows())
        store.db.executemany("INSERT INTO task_edges(task,dependency) VALUES(?,?)",
                             (("task:scale-%07d"%i, "task:scale-%07d"%(i-1)) for i in range(1,count)))


def accepted_fingerprint(store, run):
    hasher = hashlib.sha256()
    for row in store.db.execute("SELECT * FROM tasks WHERE run=? AND status='accepted' ORDER BY id", (run,)):
        hasher.update(canonical(dict(row)).encode())
    return hasher.hexdigest()


def verify(work, count=220000, accepted=80):
    require(0 < accepted < count, "Choose 0 < accepted < tasks")
    work = Path(work).resolve()
    work.mkdir(parents=True,exist_ok=False)
    fixture = Path(__file__).resolve().parents[1]/"assets/ecs-fixture"
    run = json.loads((fixture/"run.json").read_text("utf-8"))["run_id"]
    home = work/"windows-study"
    home.mkdir()
    db = home/"knowledge.sqlite3"
    from make_fixture import build_fixture
    build_fixture(db)
    with Store(home) as store:
        for source in (fixture/"source").rglob("*"):
            if source.is_file():
                store.put_blob(source.read_bytes())
        index = store.record("runs",run)
        seed_history(store,index,count,accepted)
        fingerprint = accepted_fingerprint(store,run)
    # Real v1.3 workspaces have none of the new scheduling indexes. Include their one-time build in the timing.
    with sqlite3.connect(db) as legacy:
        for name in ("task_run_queue","task_plan_scope","task_reverse_edge"):
            legacy.execute("DROP INDEX IF EXISTS " + name)
    started = time.perf_counter()
    with Store(home,readonly=True) as reader:
        runs = course.queue_runs(reader)
        check = course.preview(reader,run)
        require(check["queue"]["total"] == count and runs["runs"][0]["run"] == run, "Preview lost history")
        require(check["legacy_unstarted_upper_bound"] == count-accepted and check["strategy"] == "module", "Preview disagrees")
        require(not reader.get_meta("study_head"), "Preview mutated the learning plan")
    preview_seconds = time.perf_counter()-started
    started = time.perf_counter()
    with Store(home) as store:
        first = planner.plan(store,run)
        switch_seconds = time.perf_counter()-started
        queue = first["queue"]
        require(first["newly_deferred"] == count-accepted and queue["accepted"] == accepted, "Wrong migration counts")
        require(first["module_count"] == 4 and len(first["tasks"]) == queue["pending"] == 4, "Unexpected fixture plan")
        require(accepted_fingerprint(store,run) == fingerprint, "Old accepted results changed")
        require(store.db.execute("SELECT count(*) FROM task_edges").fetchone()[0] == count-1, "Lost old dependencies")
        require(store.record("runs",run)["facts_digest"] == index["facts_digest"], "Index binding changed")
        repeat = planner.plan(store,run)
        require(repeat["tasks"] == first["tasks"] and repeat["newly_deferred"] == 0, "Re-plan duplicated work")
        started = time.perf_counter()
        focus = study.focus(store,"server/optimizer",symbol="cg_compute",question="哪个跨文件消费者依赖计算结果？")
        context = planner.task_context(store,focus["task"])
        ready = planner.next_tasks(store,run)
        focus_seconds = time.perf_counter()-started
        require(focus["frontend_invocations"] == 0 and context["previous_research"]["tasks"], "Missing history or reran frontend")
        require(set(r["kind"] for r in ready) == {"module_survey","feature_research"} and len(ready)==5, "Deferred work still dispatches")
        require(planner.plan(store,run,targets=["cg_compute"],question="单个特性")["strategy"] == "feature", "Wrong targeted plan")
    report = {"result":"passed", "scope":"synthetic old task queue over the shipped four-module, 3-TU C++ fixture",
              "legacy_tasks":count, "legacy_task_dependencies":count-1, "accepted_preserved":accepted,
              "accepted_rows_sha256":fingerprint,"deferred":first["newly_deferred"],"module_surveys":first["module_count"],
              "pending_after_switch":queue["pending"], "pending_after_one_focus":len(ready), "second_switch_changes":0,
              "upstream_symbols":index["coverage"]["symbols"],"upstream_relations":index["coverage"]["relations"],
              "frontend_invocations":focus["frontend_invocations"], "model_calls":0, "preview_seconds":round(preview_seconds,3),
              "switch_with_schema_upgrade_seconds":round(switch_seconds,3),"focus_context_and_next_seconds":round(focus_seconds,3)}
    (work/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True,help="A new directory for synthetic data")
    parser.add_argument("--tasks",type=int,default=220000)
    parser.add_argument("--accepted",type=int,default=80)
    args=parser.parse_args()
    print(json.dumps(verify(args.output,args.tasks,args.accepted),ensure_ascii=False,indent=2))
