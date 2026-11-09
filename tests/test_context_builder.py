"""Bounded graph reading order must not become a function-level task queue."""
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from platform_fixture import workspace
from unified_knowledge import context_builder
from unified_knowledge.planner import create_task
from unified_knowledge.store import Store, canonical


class ContextBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.store, cls.plan, cls.unit = workspace(Path(cls.temp.name))
        cls.files = sorted(key for module in cls.plan["modules"].values() for key in module["files"])
        cls.symbol_assets = {"synthetic:a": "server/optimizer/producer.cpp", "synthetic:b": "server/executor/consumer.cpp",
                             "synthetic:c": "server/tools/idle.cpp"}
        with cls.store.transaction():
            # Explicitly marked synthetic binding-capable graph, distinct from
            # old fixture edges that correctly remain candidate static facts.
            index = cls.store.record("runs", cls.plan["run"])
            index["coverage"]["call_binding"] = {"synthetic_protocol_fixture": True}
            cls.store.db.execute("UPDATE main.runs SET data=? WHERE id=?", (canonical(index), cls.plan["run"]))
            for uid, asset in cls.symbol_assets.items():
                node = {"id": uid, "logical": uid, "name": uid, "asset": asset, "kind": "function_decl", "definition": True,
                        "start": 1, "end": 2, "evidence": cls.unit["source_refs"][0]}
                cls.store.db.execute("INSERT INTO main.symbols VALUES(?,?,?,?,?,?,?)",
                    (cls.plan["run"], uid, uid, uid, asset, node["kind"], canonical(node)))
            for suffix, source, target in (("ab", "synthetic:a", "synthetic:b"), ("ba", "synthetic:b", "synthetic:a"),
                                           ("ac", "synthetic:a", "synthetic:c")):
                edge = {"id": "synthetic:" + suffix, "source": source, "target": target, "kind": "CALLS", "resolution": "resolved",
                        "evidence": cls.unit["source_refs"][0], "target_binding": "synthetic_exact"}
                cls.store.db.execute("INSERT INTO main.relations VALUES(?,?,?,?,?,?,?)",
                    (cls.plan["run"], edge["id"], source, target, "CALLS", "resolved", canonical(edge)))
            cls.task = create_task(cls.store, snapshot=cls.plan["snapshot"], run=cls.plan["run"], profile=cls.plan["profile"],
                kind="feature_research", bundle={"plan_id": cls.plan["id"], "selected_files": cls.files,
                    "question": "Synthetic multi-file cycle with residual source",
                    "requires_knowledge": [cls.unit["id"], "unpublished:missing"]})

    @classmethod
    def tearDownClass(cls):
        cls.store.close()
        cls.temp.cleanup()

    def test_scc_members_internal_and_cross_edges_survive(self):
        plan = context_builder.build(self.store, self.task)
        chunks = plan["graph"]["chunks"]
        cycle = next(c for c in chunks if "synthetic:a" in c["members"])
        self.assertEqual(set(cycle["members"]), {"synthetic:a", "synthetic:b"})
        self.assertEqual(set(cycle["internal_edges"]), {"synthetic:ab", "synthetic:ba"})
        self.assertIn("synthetic:ac", cycle["cross_edges"])
        callee = next(c for c in chunks if "synthetic:c" in c["members"])
        self.assertLess(chunks.index(callee), chunks.index(cycle))
        self.assertTrue(all(chunk["learning_task"] is False for chunk in chunks))
        self.assertEqual(plan["scope"]["index_run"], self.plan["run"])
        self.assertEqual(plan["graph"]["global_scc_completeness"], "not_claimed")

    def test_residual_files_prerequisites_and_actual_read_instructions(self):
        result = context_builder.build(self.store, self.task)
        self.assertEqual({r["asset"] for r in result["source_reads"]}, set(self.files))
        header = next(r for r in result["source_reads"] if r["asset"].endswith("api.h"))
        self.assertFalse(header["compiled"])
        self.assertTrue(all(r["residual_review_required"] for r in result["source_reads"]))
        self.assertTrue(all(r["read"]["action"] == "read_source" for r in result["source_reads"]))
        self.assertEqual(result["reviewed_prerequisites"][0]["id"], self.unit["id"])
        self.assertEqual(result["missing_prerequisites"][0]["id"], "unpublished:missing")
        self.assertIn("not_published_in_revision", canonical(result["missing_prerequisites"]))

    def test_pages_are_bounded_and_do_not_write_receipts_or_read_source(self):
        changes = self.store.db.total_changes
        tasks = self.store.db.execute("SELECT count(*) FROM tasks").fetchone()[0]
        events = self.store.db.execute("SELECT count(*) FROM events").fetchone()[0]
        with patch.object(self.store, "source_lines", side_effect=AssertionError("Builder may not perform source reads")):
            first = context_builder.build(self.store, self.task, limit=1)
            second = context_builder.build(self.store, self.task, offset=first["page"]["next_offset"], limit=1)
        self.assertNotEqual(first["source_reads"][0]["asset"], second["source_reads"][0]["asset"])
        self.assertEqual(first["receipts_created"], 0)
        self.assertFalse(first["automatic_semantic_approval"])
        self.assertEqual(self.store.db.total_changes, changes)
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM tasks").fetchone()[0], tasks)
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM events").fetchone()[0], events)
        for maximum in (2048, 4096, 8192):
            result = context_builder.build(self.store, self.task, max_chars=maximum)
            self.assertLessEqual(len(canonical(result).encode("utf8")), maximum)

    def test_readonly_store_and_boundary_call_survive_file_page(self):
        with Store(self.store.home, readonly=True) as reader:
            result = context_builder.build(reader, self.task, limit=1)
        self.assertTrue(result["graph"]["boundary_edges"])
        edges = {e["id"]: e for e in result["graph"]["relations"]}
        self.assertTrue(all(uid in edges for uid in result["graph"]["boundary_edges"]))
        self.assertEqual(result["read_only"], True)

    def test_cross_module_anchor_is_supporting_context_not_illegal_selection(self):
        module = next(mid for mid, row in self.plan["modules"].items() if "server/executor/consumer.cpp" in row["files"])
        with self.store.transaction():
            task = create_task(self.store, snapshot=self.plan["snapshot"], run=self.plan["run"], profile=self.plan["profile"],
                kind="feature_research", bundle={"plan_id": self.plan["id"], "module": module,
                    "selected_files": ["server/executor/consumer.cpp"], "source_anchor_refs": self.unit["source_refs"]})
        result = context_builder.build(self.store, task)
        self.assertIn("server/optimizer/producer.cpp", {r["asset"] for r in result["source_reads"]})


if __name__ == "__main__":
    unittest.main()
