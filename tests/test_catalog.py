"""Regressions for planning a full checkout against a deliberately incomplete ECS run."""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from make_fixture import build_fixture
from unified_knowledge import catalog, ecs, study, team, workkit
from unified_knowledge.store import Store


class FeatureCatalogTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.src = self.root / "src"
        shutil.copytree(ROOT / "assets/ecs-fixture/source", self.src)
        self.incoming = self.root / "input.sqlite3"
        build_fixture(self.incoming)
        self.extra = self.src / "history" / "extension.cpp"
        self.extra.parent.mkdir()
        self.extra.write_text(
            'void register_feature() {\n DefineCustomBoolVariable("old_feature", "description", 0);\n}\n',
            encoding="utf8",
        )
        tests = self.src / "tests" / "regress" / "sql"
        tests.mkdir(parents=True)
        (tests / "partial_sort.sql").write_text("select 1;\n")
        self.docs = self.root / "manual.md"
        self.docs.write_text(
            "# old_feature\nToggle an extension.\n# Unassigned chapter\nEvidence needs an owner.\n",
            encoding="utf8",
        )
        self.config = {
            "repositories": [{"id": "server", "root": str(self.src)}],
            "materials": [
                {"id": "manual", "path": str(self.docs), "material_kind": "manual"}
            ],
            "ecs_index": {"database": str(self.incoming), "graph_storage": "reference"},
        }
        self.store = Store(self.root / "home")
        self.addCleanup(self.store.close)
        self.report = ecs.connect(self.store, self.config)
        self.plan = study.current(self.store)
        self.lead = next(
            x for x in self.plan["candidates"] if x["title"] == "old_feature"
        )

    def test_partial_graph_complete_checkout_and_no_task_per_candidate(self):
        info = self.plan["modules"]["server/history"]
        self.assertEqual(info["graph_coverage"]["checkout_only_files"], 1)
        self.assertEqual(info["graph_coverage"]["ecs_manifest_files"], 0)
        self.assertEqual(
            self.plan["modules"]["server/optimizer"]["graph_coverage"][
                "tu_observations"
            ],
            {"parsed": 1},
        )
        self.assertEqual(
            {e["kind"] for e in self.lead["evidence"]}, {"manual", "registration"}
        )
        self.assertEqual(self.lead["evidence"][1]["start"], 2)
        self.assertTrue(self.lead["design_gap"])
        self.assertTrue(
            any(r["title"] == "partial_sort" for r in self.plan["candidates"])
        )
        self.assertFalse(
            self.store.db.execute(
                "select 1 from tasks where kind='feature_research'"
            ).fetchone()
        )
        first = study.focus(self.store, candidate_id=self.lead["id"])
        self.assertEqual(first["evidence_mode"], "source_text")
        self.assertEqual(first["frontend_invocations"], 0)
        self.assertEqual(
            first["task"], study.focus(self.store, candidate_id=self.lead["id"])["task"]
        )
        found = catalog.listing(
            self.store, self.plan, module="server/history", state="queued"
        )
        self.assertEqual(found["total"], 1)
        by_text = study.focus(
            self.store, "server/history", symbol="register_feature", question="where?"
        )
        self.assertEqual(by_text["evidence_mode"], "source_text")
        self.assertEqual(
            self.store.db.execute("select count(*) from main.relations").fetchone()[0],
            0,
        )

    def test_route_then_disconnected_member_receives_only_module_leads(self):
        unowned = next(
            c for c in self.plan["candidates"] if c["title"] == "Unassigned chapter"
        )
        with self.assertRaisesRegex(ValueError, "归属"):
            study.focus(self.store, candidate_id=unowned["id"])
        study.route(self.store, unowned["id"], "server/history")
        # Idempotent re-planning retains the explicit decision.
        ecs.connect(self.store, self.config)
        self.assertEqual(
            catalog.candidate(study.current(self.store), unowned["id"])["owner_module"],
            "server/history",
        )
        order = self.root / "order.json"
        kit = self.root / "history.zip"
        worker = self.root / "worker"
        team.assign(self.store, "server/history", "reader", order)
        workkit.pack(self.store, order, kit)
        workkit.open_kit(worker, kit)
        with Store(worker) as s:
            plan = study.current(s)
            visible = {r[0] for r in s.db.execute("select key from assets")}
            self.assertEqual(
                {a["key"] for a in s.record("snapshots", plan["snapshot"])["assets"]},
                visible,
            )
            self.assertNotIn("server/tools/idle.cpp", visible)
            result = catalog.listing(s, study.current(s))
            self.assertEqual(
                {r["id"] for r in result["items"]}, {self.lead["id"], unowned["id"]}
            )
            chosen = study.focus(s, candidate_id=self.lead["id"])
            self.assertEqual(chosen["evidence_mode"], "source_text")
            self.assertEqual(chosen["module"], "server/history")

    def test_refresh_checks_checkout_even_with_cached_blob(self):
        src = self.src / "optimizer/producer.cpp"
        src.write_text("int not_the_same(){return 9;}\n", encoding="utf8")
        with self.assertRaisesRegex(ValueError, "differs"):
            ecs.connect(self.store, self.config)
        self.assertEqual(study.current(self.store)["id"], self.plan["id"])

    def test_new_snapshot_retains_candidate_identity_not_old_research_state(self):
        before = study.focus(self.store, candidate_id=self.lead["id"])
        self.extra.write_text(
            self.extra.read_text() + "// new revision\n", encoding="utf8"
        )
        ecs.connect(self.store, self.config)
        newer = study.current(self.store)
        self.assertNotEqual(newer["snapshot"], self.plan["snapshot"])
        row = next(
            r for r in catalog.entries(self.store, newer) if r["id"] == self.lead["id"]
        )
        self.assertEqual(row["state"], "available")
        self.assertNotEqual(
            study.focus(self.store, candidate_id=self.lead["id"])["task"],
            before["task"],
        )
