"""ECS handoff, frozen evidence and disconnected module workspace regressions (no compiler)."""
from contextlib import closing
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import unittest
import zipfile

ENGINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE / "scripts"))

from unified_knowledge import ecs, study, team, workkit
from unified_knowledge.materials import ingest
from unified_knowledge.store import Store, canonical, digest, identity, now


class ECSStudyTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        fixture = ENGINE / "assets/ecs-fixture"
        self.db = self.root / "incoming" / "knowledge.sqlite3"
        self.db.parent.mkdir()
        from make_fixture import build_fixture
        build_fixture(self.db)
        self.source = self.root / "source"
        shutil.copytree(fixture / "source", self.source)
        self.origin = json.loads((fixture / "run.json").read_text("utf-8"))
        self.config = {"product":"fixture", "revision":"fixture", "repositories":[{"id":"server","root":str(self.source)}],
                       "materials":[], "methods":[], "profiles":[], "ownership":[],
                       "ecs_index":{"database":str(self.db),"run_id":self.origin["run_id"]}}
        self.hub = Store(self.root / "hub")
        self.addCleanup(self.hub.close)

    def connect(self):
        return ecs.connect(self.hub,self.config)["study_plan"]

    def test_readonly_graph_cross_file_calls_and_disconnected_kit(self):
        original = hashlib.sha256(self.db.read_bytes()).hexdigest()
        self.config["ecs_index"]["graph_storage"] = "reference"
        self.config["ecs_index"].pop("run_id")
        plan = self.connect()
        self.assertEqual(plan["coverage"]["frontend_invocations"],0)
        for table in ("symbols","relations"):
            self.assertEqual(self.hub.db.execute("SELECT count(*) FROM main."+table).fetchone()[0],0)
        with Store(self.hub.home,readonly=True) as reopened:
            for name,direction in (("cg_consume","forward"),("cg_compute","reverse")):
                g = study.ecs_neighbors(reopened,study.current(reopened),name,direction,20)
                self.assertTrue(any(e.get("target_binding")=="legacy_usr_candidate" and e["resolution"]=="candidate" for e in g["relations"]))
        order, kit = self.root/"order.json", self.root/"worker.zip"
        team.assign(self.hub,"server/optimizer","opt-a",order)
        workkit.pack(self.hub,order,kit)
        self.hub.close()
        self.db.rename(self.root/"detached.sqlite3")
        worker = self.root/"worker"
        workkit.open_kit(worker,kit)
        with Store(worker) as isolated:
            g = study.ecs_neighbors(isolated,study.current(isolated),"cg_compute","reverse",20)
            self.assertTrue(any(e.get("target_binding")=="legacy_usr_candidate" for e in g["relations"]))
        self.assertEqual(hashlib.sha256((self.root/"detached.sqlite3").read_bytes()).hexdigest(), original)

    def test_malformed_draft_reports_tool_error_and_same_mcp_connection_continues(self):
        from io import StringIO
        from unified_knowledge import planner, service
        self.config["ecs_index"]["graph_storage"] = "reference"
        self.connect()
        task = study.focus(self.hub,"server/optimizer",symbol="cg_compute")["task"]
        token = planner.lease(self.hub,task,"member")["token"]
        bad = {"id":"test:bad","kind":"test_obligation","title":"bad","body":"expected boundary",
               "source_refs":[],"expected_from":["contract:expected"]}
        args = {"task":task,"worker":"member","token":token}
        # Old clients could have saved the malformed unit before upgrading.
        staged = {bad["id"]:bad}
        with self.hub.transaction():
            self.hub.set_meta("research_drafts:"+task+":1",staged)
        incoming = [{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"finish_research","arguments":{
                    **args,"coverage":[],"drafts_digest":digest(staged)}}},
                    {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"stage_research_unit","arguments":{**args,"unit":bad}}},
                    {"jsonrpc":"2.0","id":3,"method":"ping"}]
        out = StringIO()
        service.stdio(self.hub.home,"researcher",StringIO("".join(json.dumps(r)+"\n" for r in incoming)),out)
        responses = [json.loads(line) for line in out.getvalue().splitlines()]
        self.assertEqual([r["id"] for r in responses],[1,2,3])
        for response in responses[:2]:
            self.assertTrue(response["result"]["isError"])
            self.assertIn("expected_from",response["result"]["content"][0]["text"])
        self.assertEqual(planner.task_status(self.hub,task)["status"],"leased")

    def test_path_entry_source_only_does_not_mask_bad_ecs(self):
        from unified_knowledge import project, reader_wiki
        spec = {"source":str(self.source),"home":str(self.root/"text-study"),"repository_roots":{}}
        first = project.start(spec,False)
        self.assertEqual(first["mode"],"source_only")
        self.assertEqual(project.start(spec,False)["plan_id"],first["plan_id"])
        with Store(Path(spec["home"])) as text_store:
            result = study.focus(text_store,"server/optimizer",symbol="cg_compute",question="Find producer")
            self.assertEqual(result["evidence_mode"],"source_text")
            self.assertEqual(result["frontend_invocations"],0)
            self.assertEqual(len([r for r in text_store.db.execute("SELECT id FROM tasks WHERE kind='feature_research'")]),1)
            with self.assertRaisesRegex(ValueError,"已审"):
                reader_wiki.export_wiki(text_store)
        with self.assertRaisesRegex(ValueError,"missing"):
            project.check({**spec,"index_db":str(self.root/"absent.sqlite3")})

    def test_exact_cross_platform_text_and_incompatible_input(self):
        from unified_knowledge.graph_mount import inspect_input
        file = self.source/"optimizer/producer.cpp"
        file.write_bytes(file.read_bytes().replace(b"\r\n",b"\n").replace(b"\n",b"\r\n"))
        self.config["ecs_index"]["graph_storage"] = "reference"
        self.connect()
        broken = self.root/"foreign.sqlite3"
        with closing(sqlite3.connect(broken)) as foreign:
            foreign.execute("CREATE TABLE nodes(id INTEGER PRIMARY KEY)")
        with self.assertRaisesRegex(ValueError,"格式不匹配"):
            inspect_input(broken)

    def test_wrong_run_incomplete_run_and_overlapping_files(self):
        self.config["ecs_index"]["run_id"] = "index:no-such-run"
        with self.assertRaisesRegex(ValueError, "not found"):
            self.connect()
        self.config["ecs_index"]["run_id"] = self.origin["run_id"]
        with closing(sqlite3.connect(self.db)) as upstream:
            upstream.execute("UPDATE runs SET data=json_set(data,'$.facts_digest','') WHERE id=?", (self.origin["run_id"],))
            upstream.commit()
        with self.assertRaisesRegex(ValueError, "completed ECS run"):
            self.connect()
        with self.assertRaisesRegex(ValueError, "separate learning"):
            ecs.index_path(self.db,self.db.parent)
        self.assertIsNone(self.hub.get_meta("study_head"))

    def test_unmatched_checkout_cannot_create_current_plan(self):
        p = self.source / "optimizer/producer.cpp"
        p.write_text("int different_version();\n",encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs from the ECS snapshot"):
            self.connect()
        self.assertIsNone(self.hub.get_meta("snapshot_head"))

    def test_repeated_binding_and_new_manual_preserve_ecs_provenance(self):
        original = hashlib.sha256(self.db.read_bytes()).hexdigest()
        first = self.connect()
        again = self.connect()
        self.assertEqual((first["plan_id"],first["study_run"]), (again["plan_id"],again["study_run"]))
        self.assertEqual(first["coverage"]["frontend_invocations"],0)
        self.assertTrue(first["suggested_first_batch"])
        definitions = study.module_guide(self.hub,"server/optimizer")["indexed_definitions"]
        self.assertTrue(any(d["name"]=="cg_compute" and d["evidence"] for d in definitions))
        manual = self.root / "manual.md"
        manual.write_text("# optimizer\nA new optimizer document\n",encoding="utf-8")
        self.config["materials"] = [{"id":"manual","path":str(manual),"material_kind":"manual","status":"unreviewed"}]
        revised = self.connect()
        self.assertEqual(first["source_index"],revised["source_index"])
        self.assertNotEqual(first["snapshot"],revised["snapshot"])
        self.assertNotEqual(first["plan_id"],revised["plan_id"])
        self.assertEqual(4,len(revised["modules"]))
        self.assertEqual(hashlib.sha256(self.db.read_bytes()).hexdigest(), original)
        graph = study.ecs_neighbors(self.hub,study.current(self.hub),"cg_consume","forward",10)
        linked = [r for r in graph["relations"] if r.get("target_binding")=="legacy_usr_candidate"]
        self.assertTrue(linked)
        self.assertTrue(all(r["resolution"]=="candidate" for r in linked))

    def test_documents_already_in_ecs_are_inherited_once(self):
        original = self.root / "design.md"
        original.write_text("# optimizer\nFrozen design inside the upstream snapshot.\n",encoding="utf-8")
        upstream_config = {**self.config, "materials":[{"id":"design","path":str(original),"material_kind":"design"}]}
        with Store(self.db.parent) as upstream:
            snap = ingest(upstream,upstream_config)
            binding = upstream.profile(snap["id"],"unknown")
            run = {"id":identity("index",[snap["id"],"docs-fixture"]), "snapshot":snap["id"],"profile":"unknown",
                   "profile_digest":binding["digest"],"status":"partial","created":now(),"facts_digest":digest([]),
                   "coverage":{"symbols":0,"relations":0,"parsed_tus":0,"semantic_completeness":"not_certified"}}
            with upstream.transaction():
                upstream.db.execute("INSERT INTO runs VALUES(?,?,?,?,?,?)",
                                    (run["id"],snap["id"],run["profile"],run["created"],run["status"],canonical(run)))
        original.rename(self.root/"old-location.md")
        self.config["ecs_index"]["run_id"] = run["id"]
        plan = self.connect()
        rows = list(self.hub.db.execute("SELECT data FROM documents WHERE snapshot=?", (plan["snapshot"],)))
        self.assertEqual(len(rows),1)
        evidence = self.hub.read_evidence(json.loads(rows[0][0])["anchor"])
        self.assertIn("Frozen design",evidence["text"])
        self.assertEqual(study.current(self.hub)["documents"],1)

    def test_worker_scope_and_corrupt_kit(self):
        self.connect()
        order = self.root / "opt.json"
        team.assign(self.hub,"server/optimizer","a",order)
        kit = self.root / "opt.zip"
        workkit.pack(self.hub,order,kit)
        worker = self.root / "worker"
        self.db.rename(self.root / "input-offline.sqlite3")
        opened = workkit.open_kit(worker,kit)
        self.assertTrue((Path(opened["reading"])/"server/optimizer/producer.cpp").is_file())
        self.assertFalse((Path(opened["reading"])/"server/tools/idle.cpp").exists())
        with Store(worker) as isolated:
            self.assertEqual(list(study.current(isolated)["modules"]),["server/optimizer"])
            with self.assertRaisesRegex(ValueError,"Unknown module"):
                study.focus(isolated,"server/tools")
            self.assertEqual(study.focus(isolated,"server/optimizer",symbol="cg_compute")["frontend_invocations"],0)
        damaged = self.root / "damaged.zip"
        with zipfile.ZipFile(kit) as good, zipfile.ZipFile(damaged,"w") as out:
            for name in good.namelist():
                content = good.read(name)
                if name.startswith("blobs/"):
                    content = bytes([content[0] ^ 1])+content[1:] if content else b"bad"
                out.writestr(name,content)
        with self.assertRaisesRegex(ValueError, "Damaged kit|size mismatch"):
            workkit.open_kit(self.root/"damaged-worker",damaged)
        self.assertFalse((self.root/"damaged-worker").exists())

    def test_tampered_and_reassigned_results(self):
        self.connect()
        order = self.root / "worker.json"
        ticket = team.assign(self.hub,"server/optimizer","a",order)
        with self.assertRaisesRegex(ValueError, "already assigned"):
            team.assign(self.hub,"server/optimizer","b",order)
        result = self.root / "tampered.gz"
        with gzip.open(result,"wt",encoding="utf-8") as file:
            json.dump({"data":{"schema":"module-result/v1","order":ticket["assignment"]},"hmac":"bad"},file)
        with self.assertRaisesRegex(ValueError,"damaged"):
            team.receive(self.hub,result)
        team.assign(self.hub,"server/optimizer","b",order,replace=True)
        with self.assertRaisesRegex(ValueError,"superseded"):
            team.receive(self.hub,result)
        self.assertIsNone(self.hub.get_meta("knowledge_head"))


    def test_compaction_retains_live_work_dependencies_and_history(self):
        from unified_knowledge import course, planner
        view = self.connect()
        run = view["study_run"]
        anchor = self.hub.db.execute("SELECT id FROM anchors WHERE asset LIKE '%/producer.cpp' LIMIT 1").fetchone()[0]
        def task(label, kind="source_research", deps=(), other=None, **extra):
            return planner.create_task(self.hub,snapshot=view["snapshot"],run=other or run,profile=view["profile"],
                kind=kind,bundle={"name":label,"source_anchor_refs":[anchor],**extra},dependencies=deps)
        held_results = canonical({"coverage":[],"claims":[{"title":"historical contract"}]})
        with self.hub.transaction():
            keep = {state:task(state) for state in ("leased","submitted","accepted","needs_research")}
            for state,tid in keep.items():
                self.hub.db.execute("UPDATE tasks SET status=?,attempt=1,owner='prior',result=? WHERE id=?",
                    (state,held_results if state in {"accepted","submitted","needs_research"} else None,tid))
            retried = task("retried")
            self.hub.db.execute("UPDATE tasks SET attempt=1 WHERE id=?",(retried,))
            changed = task("change","asset_discovery",change="delta:1")
            grand = task("grand")
            direct = task("direct",deps=[grand])
            # Include a cross-run live consumer and a prerequisite cycle.
            task("active consumer","gap_research",deps=[direct],other="other-run")
            self.hub.db.execute("INSERT INTO task_edges VALUES(?,?)",(grand,direct))
            unrelated = task("unrelated",other="other-run")
            for_drop = [task("unstarted",kind) for kind in course.FINE_KINDS]
            self.hub.set_meta("research_drafts:"+keep["leased"]+":1",{"draft":"kept"})
        with Store(self.hub.home,readonly=True) as reader:
            before = course.preview(reader,run)
            self.assertEqual(before["legacy_unstarted_upper_bound"],len(for_drop)+2)
            self.assertTrue(course.queue_runs(reader)["read_only"])
        applied = planner.plan(self.hub,run)
        self.assertEqual(applied["newly_deferred"],len(for_drop))
        self.assertEqual(planner.plan(self.hub,run)["newly_deferred"],0)
        for tid in for_drop:
            self.assertEqual(planner.task_status(self.hub,tid)["status"],"deferred")
        for tid in (grand,direct,changed,retried,unrelated):
            self.assertEqual(planner.task_status(self.hub,tid)["status"],"queued")
        for state,tid in keep.items():
            value = planner.task_status(self.hub,tid)
            self.assertEqual((value["status"],value["owner"],value["attempt"]),(state,"prior",1))
            if state in {"submitted","accepted","needs_research"}:
                self.assertEqual(canonical(value["result"]),held_results)
        self.assertEqual(self.hub.get_meta("research_drafts:"+keep["leased"]+":1"),{"draft":"kept"})
        feature = study.focus(self.hub,"server/optimizer",symbol="cg_compute",question="旧的计算契约是什么？")
        context = planner.task_context(self.hub,feature["task"])
        self.assertTrue(any(edge["resolution"]=="candidate" and edge["evidence"] for edge in context["call_sites"]["relations"]))
        history = context["previous_research"]["tasks"]
        self.assertEqual({h["id"] for h in history},{keep["accepted"],keep["submitted"]})
        cfg = json.loads(Path(applied["mcp"]).read_text("utf-8"))["mcpServers"]["gaussdb_knowledge"]
        self.assertEqual(cfg["command"],sys.executable)
        self.assertIn(str(self.hub.home),cfg["args"])
        order = self.root/"opt-history.json"
        team.assign(self.hub,"server/optimizer","opt-a",order)
        kit = self.root/"with-history.zip"
        workkit.pack(self.hub,order,kit)
        workkit.open_kit(self.root/"opt",kit)
        with Store(self.root/"opt") as isolated:
            local = study.focus(isolated,"server/optimizer",symbol="cg_compute")
            packet = planner.task_context(isolated,local["task"])["previous_research"]["coordinator_at_dispatch"]
            self.assertEqual({e["id"] for e in packet["tasks"]},{keep["accepted"],keep["submitted"]})
            self.assertTrue(all(e["claim_titles"]==["historical contract"] for e in packet["tasks"]))

    def test_fresh_large_native_index_uses_modules_and_bounds_explicit_targets(self):
        from unified_knowledge import planner
        from unittest.mock import patch
        with Store(self.db.parent) as local:
            for source in [*self.source.rglob("*"), ENGINE/"scripts/unified_knowledge/research_contract.md",
                           ENGINE/"integrations/codewiki/enhanced-learning.md"]:
                if source.is_file():
                    local.put_blob(source.read_bytes())
            run = self.origin["run_id"]
            symbol = json.loads(local.db.execute("SELECT data FROM symbols WHERE run=? AND name='cg_compute' LIMIT 1",(run,)).fetchone()[0])
            with local.transaction():
                for i in range(300):
                    sid = "symbol:extra-"+str(i)
                    obj = {**symbol,"id":sid,"logical":sid,"name":"many_defs"}
                    local.db.execute("INSERT INTO symbols VALUES(?,?,?,?,?,?,?)",
                                     (run,sid,sid,obj["name"],obj["asset"],obj["kind"],canonical(obj)))
                    rel = {"id":"edge:"+sid,"source":symbol["id"],"target":sid,"kind":"CALLS","resolution":"candidate","evidence":symbol["evidence"]}
                    local.db.execute("INSERT INTO relations VALUES(?,?,?,?,?,?,?)",
                                     (run,rel["id"],rel["source"],sid,rel["kind"],rel["resolution"],canonical(rel)))
            with patch.object(planner,"scc",side_effect=AssertionError("Whole graph SCC traversal")):
                overview = planner.plan(local,run)
                self.assertEqual((overview["strategy"],overview["module_count"],overview["queue"]["pending"]),("module",4,4))
                specific = planner.plan(local,run,targets=[symbol["id"],"missing"],max_symbols=4,question="cross-file consumer")
                self.assertTrue(specific["graph_truncated"])
                self.assertEqual((len(specific["tasks"]),specific["unresolved_targets"]),(1,["missing"]))
                b = planner.task_status(local,specific["tasks"][0])["bundle"]
                self.assertLessEqual(len(b["symbol_refs"]),4)
                self.assertEqual(planner.plan(local,run,targets=[symbol["id"],"missing"],max_symbols=4,question="cross-file consumer")["tasks"],specific["tasks"])
                with self.assertRaisesRegex(ValueError,"Ambiguous"):
                    planner.plan(local,run,targets=["many_defs"],max_symbols=4)
            order = self.root/"native-order.json"
            team.assign(local,"server/optimizer","b",order)
            archive = self.root/"native-kit.zip"
            workkit.pack(local,order,archive)
            workkit.open_kit(self.root/"native-member",archive)
            with Store(self.root/"native-member") as member:
                feature = study.focus(member,"server/optimizer",symbol="cg_compute")
                self.assertEqual((feature["frontend_invocations"],feature["index_run_id"]),(0,run))
                self.assertEqual(study.ecs_neighbors(member,study.current(member),"cg_compute","forward",4)["provider"],"workspace-index")


if __name__ == "__main__":
    unittest.main()
