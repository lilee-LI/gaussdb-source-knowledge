"""Exercise the ECS handoff, two disconnected worker hosts, review and Wiki via public commands."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def exercise(root):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=False)
    engine = Path(__file__).resolve().parents[1]
    fixture = engine / "assets/ecs-fixture"
    incoming = root / "incoming"
    incoming.mkdir()
    db = incoming / "knowledge.sqlite3"
    from make_fixture import build_fixture
    build_fixture(db)
    sha = hashlib.sha256(db.read_bytes()).hexdigest()
    source = root / "hub-source"
    shutil.copytree(fixture/"source",source)
    design, manual = root/"design.md", root/"manual.md"
    design.write_text("# optimizer\nThe fixture producer returns its input plus one.\n",encoding="utf-8")
    manual.write_text("# executor\nThe fixture consumer delegates to the producer.\n",encoding="utf-8")
    ecs = json.loads((fixture/"run.json").read_text(encoding="utf-8"))
    started = time.monotonic()
    steps = []
    def dump(path, data):
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
        return path
    def run(script, *args, fail=False):
        p = subprocess.run([sys.executable,"-X","utf8",str(engine/"scripts"/script),*map(str,args)],
                           cwd=engine,capture_output=True,encoding="utf-8",timeout=120)
        steps.append({"command":str(args[2]) if len(args)>2 and args[0]=="--home" else script,"exit":p.returncode})
        if fail:
            if not p.returncode:
                raise AssertionError("Expected command failure")
            return p.stderr
        if p.returncode:
            raise RuntimeError(script+" "+str(args[:4])+": "+p.stderr[-1800:])
        return json.loads(p.stdout)
    def kb(host, *args, **kw):
        return run("unified_kb.py","--home",root/host,*args,**kw)
    paths = dump(root/"paths.json", {"source":"hub-source","design":"design.md","manual":"manual.md",
        "index_db":"incoming/knowledge.sqlite3","run_id":ecs["run_id"],"home":"hub","output":"project.json"})
    config = run("init_internal_project.py","--paths",paths)
    assert config["source_index"]["run_id"] == ecs["run_id"] and config["frontend_invocations"] == 0
    assert Path(config["study_plan"]).is_file()
    again = run("init_internal_project.py","--paths",paths)
    assert again["study_plan"] == config["study_plan"]
    hub_plan = kb("hub","guide")
    assert len(hub_plan["modules"]) == 4 and hub_plan["source_index"]["facts_digest"] == ecs["facts_digest"]
    graph = kb("hub","navigate","--symbol","cg_consume")
    calls = graph["relations"]
    assert any(e.get("target_binding") == "legacy_usr_candidate" and e["resolution"] == "candidate" for e in calls)
    leads = run("unified_kb.py","features","--paths",paths)["items"]
    lead_by_module = {v["owner_module"]:v["id"] for v in leads}
    reserved = kb("hub","focus","--candidate",lead_by_module["server/optimizer"])["task"]
    kits = []
    for host, module in (("node-a","optimizer"),("node-b","executor")):
        kit = root/(host+".zip")
        item = kb("hub","team","assign","--module","server/"+module,"--worker",host,"--kit",kit)
        assert item["kit"]["coverage"]["symbols"] >= 2
        kits.append({"host":host,"module":module,"bytes":item["kit"]["bytes"],"scope":item["kit"]["coverage"]})
    assert sha == hashlib.sha256(db.read_bytes()).hexdigest()
    # This is the isolated input copy inside this test's new root.
    db.rename(incoming/"disconnected.sqlite3")
    assert not db.exists()
    receipts = []
    for kit in kits:
        host, module = kit["host"], kit["module"]
        opened = kb(host,"team","open","--kit",root/(host+".zip"))
        assert opened["worker"] == host and Path(opened["mcp"]).is_file()
        assert not (Path(opened["reading"])/"server/tools/idle.cpp").exists()
        worker_plan = kb(host,"guide")
        assert len(worker_plan["modules"]) == 1 and worker_plan["worker_scope"] == "server/"+module
        symbol = "cg_compute" if module == "optimizer" else "cg_consume"
        scoped = kb(host,"focus","--module","server/"+module,"--symbol",symbol,"--candidate",lead_by_module["server/"+module])
        assert scoped["ecs_run_id"] == ecs["run_id"] and scoped["frontend_invocations"] == 0
        task = scoped["task"]
        token = kb(host,"task","claim","--id",task,"--worker",host)["token"]
        ctx = kb(host,"task","context","--id",task)
        evidence = ctx["evidence"][0]["id"]
        body = kb(host,"task","read","--id",task,"--worker",host,"--token",token,"--evidence",evidence)
        assert body["snapshot"] == ecs["snapshot"] and symbol in body["text"] and not body["truncated"]
        doc_asset = ("design/design.md" if host == "node-a" else "manual/manual.md")
        doc = kb(host,"task","anchor","--id",task,"--worker",host,"--token",token,"--asset",doc_asset,"--start","1","--end","2")["id"]
        kb(host,"task","read","--id",task,"--worker",host,"--token",token,"--evidence",doc)
        unit = {"id":"ecs-fixture-"+module,"kind":"claim","title":symbol,"statement":symbol+" is defined in the fixture.",
                "body":"Synthetic software test: inspected "+symbol+" and its document.",
                "conditions":["Bound ECS fixture"],"counterexamples":["Other builds require review"],
                "symbol_refs":[scoped["symbols"][0]["id"]],"source_refs":[evidence,doc]}
        if module == "executor":
            neighbors = kb(host,"navigate","--symbol","cg_consume")
            producer = next(n for n in neighbors["nodes"] if n["name"]=="cg_compute" and n["definition"])
            cited = kb(host,"task","read","--id",task,"--worker",host,"--token",token,"--evidence",producer["evidence"])
            assert "return value + 1" in cited["text"] and "return cg_compute(value)" in body["text"]
            unit.update(kind="contract",title="cg_consume forwards the bounded cg_compute result",
                body="The producer adds one. The executor directly returns the call result in the source inspected.",
                conditions=["Fixture build, int value with representable value + 1"],counterexamples=["INT_MAX is outside this contract"],
                producers=[producer["id"]],consumers=[scoped["symbols"][0]["id"]],
                requires=["value + 1 is representable as int"],ensures=["Return value equals input plus one"],
                invariants=["The consumer forwards its input once"],symbol_refs=[producer["id"],scoped["symbols"][0]["id"]],
                source_refs=[evidence,producer["evidence"],doc])
        staged = kb(host,"task","stage","--id",task,"--worker",host,"--token",token,"--input",dump(root/(host+".unit"),unit))
        if module == "executor":
            obligation = {"id":"ecs-fixture-boundary-test","kind":"test_obligation","title":"cg_consume(0) boundary",
                "body":"For input zero, check the predicted result one in the fixture build. Execution is pending.",
                "expected_from":{"kind":"contract","ref":unit["id"]},"execution_status":"not_run","symbol_refs":unit["symbol_refs"],
                "source_refs":unit["source_refs"]}
            staged = kb(host,"task","stage","--id",task,"--worker",host,"--token",token,"--input",dump(root/(host+".test-unit"),obligation))
        cov = [{"question":"What is the source evidence?","status":"answered","explanation":"Read source and document.",
                "evidence_refs":unit["source_refs"]}]
        kb(host,"task","finish","--id",task,"--worker",host,"--token",token,"--input",dump(root/(host+".coverage"),cov),
           "--drafts-digest",staged["drafts_digest"])
        packet = root/(host+".result.gz")
        kb(host,"team","export","--task",task,"--out",packet)
        rec = kb("hub","team","receive","--input",packet)
        if module=="optimizer":
            assert rec["task"]==reserved
        assert rec["source_index"] == hub_plan["source_index"] and rec["frontend_invocations"]==0 and rec["status"]=="submitted"
        assert kb("hub","team","receive","--input",packet)["replayed"]
        receipts.append(rec)
    assert kb("hub","status")["knowledge_revision"] is None
    for receipt in receipts:
        dec = {"reviewer":"fixture-reviewer","mode":"independent_review","verdict":"accept",
               "notes":"Synthetic protocol actors; software check only."}
        kb("hub","task","review","--id",receipt["task"],"--input",
           dump(root/"task-review.json",{**dec,"result_digest":receipt["result_digest"]}))
        proposal = kb("hub","team","propose","--task",receipt["task"])
        ctx = kb("hub","knowledge","review-context","--id",proposal["id"],"--reviewer","fixture-reviewer")
        rev = kb("hub","knowledge","review","--id",proposal["id"],"--input",
                 dump(root/"review.json",{**dec,"proposal_digest":ctx["proposal_digest"]}))
        receipt["knowledge_revision"] = rev["id"]
    plan = kb("hub","guide")
    assert sum(m["published_tasks"] for m in plan["modules"]) == 2
    accepted_leads = run("unified_kb.py","features","--paths",paths,"--state","published")
    assert accepted_leads["total"]==2
    wiki = run("unified_kb.py","wiki","--paths",paths)
    assert Path(wiki["portable_wiki"]).is_dir()
    merged = kb("hub","integrate")
    contexts = {}
    for role in ("coding","test_generation","review"):
        request = {"task":role,"source_snapshot":plan["snapshot"],"build_profile":plan["profile"],"index_run":merged["id"],
                   "targets":["cg_compute","cg_consume"],"query":"fixture","token_budget":30000}
        pack = kb("hub","context","--input",dump(root/(role+".json"),request))
        contexts[role] = len(pack["constraints"])
        assert contexts[role] and pack["evidence"]
        normal = run("unified_kb.py","ask","--paths",paths,"--role",role,"--symbol","cg_compute","--question","fixture")
        assert normal["scope"]["knowledge_revision"]==wiki["revision"] and normal["test_obligations"]
        contract = next(c for c in pack["constraints"] if c.get("kind")=="contract")
        assert contract["producers"] and contract["consumers"]
    release = root/"internal-release"
    kb("hub","publish","--output",release,"--allow-partial")
    verified = kb("hub","verify","--output",release,"--require-current")
    assert verified["status"]=="verified" and (release/"wiki").is_dir()
    report = {"result":"passed","validation":"v1.1 synthetic Clang index; coordinator and two isolated worker directories on one machine",
        "ecs_input_sha256":sha,"ecs_input_unchanged":True,"ecs_disconnected_before_worker_start":True,
        "ecs_run_id":ecs["run_id"],"source_snapshot":ecs["snapshot"],"study_snapshot":plan["snapshot"],
        "worker_kits":kits,"receipts":receipts,"contexts":contexts,"wiki_release":verified["id"],"cross_module_contract":"ecs-fixture-executor",
        "test_obligation":"ecs-fixture-boundary-test",
        "legacy_cross_file_binding":calls[0]["target_binding"],"frontend_invocations":0,"external_model_calls":0,
        "database_execution":"not_run","commands":len(steps),"steps":steps,"seconds":round(time.monotonic()-started,2)}
    dump(root/"report.json",report)
    return {"result":"passed","report":str(root/"report.json"),"seconds":report["seconds"],"commands":len(steps)}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    print(json.dumps(exercise(parser.parse_args().output),ensure_ascii=False,indent=2))
