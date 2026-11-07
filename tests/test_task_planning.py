"""Planning must transfer by adapter, preserve evidence, and never accept knowledge."""
from pathlib import Path
import copy
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from make_fixture import build_fixture
from unified_knowledge import ecs, study, product_adapter, task_planning, service, catalog
from unified_knowledge.store import Store


class TaskPlanningTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.src = self.root / "source"
        shutil.copytree(ROOT / "assets/ecs-fixture/source", self.src)
        self.input = self.root / "input.sqlite3"
        build_fixture(self.input)
        self.feature = self.src / "engine" / "config.cpp"
        self.feature.parent.mkdir()
        self.feature.write_text('void configure() {\n DefineCustomBoolVariable("sort_feature", "description", 0);\n palloc(10);\n#ifdef PRODUCT_FLAVOR\n ereport(ERROR, errcode(1));\n#endif\n}\n', encoding="utf8")
        self.config = {"repositories": [{"id":"server", "root":str(self.src)}],
                       "ecs_index":{"database":str(self.input), "graph_storage":"reference"}, "product_adapter":"opengauss"}
        self.store = Store(self.root / "workspace")
        self.addCleanup(self.store.close)
        ecs.connect(self.store, self.config)
        self.plan = study.current(self.store)

    def test_preview_apply_resume_and_unknown_topics(self):
        preview = task_planning.construct(self.store, max_tasks=1)
        self.assertEqual(len(preview["tasks"]), 1)
        self.assertFalse(self.store.db.execute("SELECT 1 FROM tasks WHERE kind='feature_research'").fetchone())
        topics = preview["tasks"][0]["topic_decisions"]
        self.assertTrue(topics["memory"]["evidence"])
        self.assertEqual(topics["memory"]["status"], "unknown")
        result = task_planning.construct(self.store, max_tasks=1, apply=True)
        self.assertEqual(len(result["task_results"]), 1)
        second = task_planning.construct(self.store, max_tasks=1, apply=True)
        self.assertEqual(second["tasks"], [])
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM tasks WHERE kind='feature_research'").fetchone()[0], 1)
        self.assertIsNone(self.store.get_meta("knowledge_head"))
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM main.relations").fetchone()[0], 0)

    def test_custom_product_changes_rules_without_engine_changes(self):
        self.feature.write_text('void init() { RegisterSwitch("other_mode"); }\n', encoding="utf8")
        adapter = product_adapter.load("generic")
        adapter.update(id="other-db", module_rules=[{"id":"server/sql", "patterns":["server/engine/*"]}],
            detectors=[{"id":"switch", "kind":"registration", "scope":"candidate", "topic":"guc", "extensions":[".cpp"],
                        "pattern":'RegisterSwitch\\("(?P<name>[a-z_]+)"'}])
        ecs.connect(self.store, {**self.config, "product_adapter":adapter})
        newer = study.current(self.store)
        self.assertIn("server/sql", newer["modules"])
        self.assertEqual([r["title"] for r in newer["candidates"]], ["other_mode"])
        self.assertNotEqual(newer["id"], self.plan["id"])

    def proposal(self, title="Memory spill mechanism"):
        return {"study_plan":self.plan["id"], "author":"researcher", "reason":"Source investigation found an internal mechanism",
                "candidates":[{"title":title, "question":"Who owns temporary memory and cleanup?", "reason":"Inspect ownership around allocation",
                    "owner_module":"server/engine", "evidence":[{"asset":"server/engine/config.cpp","start":2,"end":3}]}]}

    def test_feedback_deduplicates_and_preserves_dependencies(self):
        first = task_planning.propose(self.store, self.proposal())
        self.assertEqual(first, task_planning.propose(self.store, self.proposal()))
        listed = catalog.listing(self.store, study.current(self.store))
        self.assertIn(first["candidates"][0]["id"], {r["id"] for r in listed["items"]})
        next_proposal = self.proposal("Cross-module consumer")
        next_proposal["candidates"][0]["depends_on"] = [first["candidates"][0]["id"]]
        second = task_planning.propose(self.store, next_proposal)
        plan = task_planning.construct(self.store, apply=True)
        ids = {r["candidate_id"]:r["task"] for r in plan["task_results"]}
        edge = self.store.db.execute("SELECT dependency FROM task_edges WHERE task=?", (ids[second["candidates"][0]["id"]],)).fetchone()
        self.assertEqual(edge[0], ids[first["candidates"][0]["id"]])

    def test_reject_cross_version_and_invalid_source_feedback(self):
        bad = self.proposal()
        bad["study_plan"] = "old"
        with self.assertRaisesRegex(ValueError, "another study"):
            task_planning.propose(self.store, bad)
        bad = self.proposal()
        bad["candidates"][0]["evidence"][0]["end"] = 50
        with self.assertRaisesRegex(ValueError, "exceeds"):
            task_planning.propose(self.store, bad)
        self.assertFalse(self.store.get_meta("planning-candidates:" + self.plan["id"]))

    def test_adapter_update_invalidates_plan_and_conflicting_ownership_fails(self):
        before = task_planning.construct(self.store, apply=True)
        adapter = product_adapter.load("opengauss")
        adapter["version"] = "2"
        ecs.connect(self.store, {**self.config, "product_adapter":adapter})
        after = task_planning.construct(self.store, apply=True)
        self.assertNotEqual(before["study_plan"], after["study_plan"])
        self.assertNotEqual(before["task_results"][0]["task"], after["task_results"][0]["task"])
        adapter["module_rules"] = [{"id":"server/one","patterns":["server/engine/*"]}, {"id":"server/two","patterns":["server/engine/*"]}]
        with self.assertRaisesRegex(ValueError, "Ambiguous"):
            product_adapter.module_for(adapter, "server", "engine/config.cpp")

    def test_researcher_tools_only_and_manual_task_reuse(self):
        lead = self.plan["candidates"][0]
        manual = study.focus(self.store, candidate_id=lead["id"])
        result = task_planning.construct(self.store, apply=True)
        self.assertEqual(result["tasks"], [])
        self.assertEqual(result["dispositions"][0]["task"], manual["task"])
        with self.assertRaisesRegex(ValueError, "unavailable"):
            service.invoke(self.store, "plan_tasks", {"apply":True})
        result = service.invoke(self.store, "plan_tasks", {"apply":False}, role="researcher")
        self.assertEqual(result["mode"], "preview")
