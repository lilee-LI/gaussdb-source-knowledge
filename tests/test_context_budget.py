"""Large source excerpts must not displace reviewed interface contracts."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from platform_fixture import workspace, accept
from unified_knowledge import retrieval
from unified_knowledge.store import canonical


class ContextBudgetTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store, self.plan, self.unit = workspace(Path(temp.name))
        self.addCleanup(self.store.close)
        anchor = self.store.record("anchors", self.unit["source_refs"][0])
        with self.store.transaction():
            refs = [self.store.anchor(self.plan["snapshot"], anchor["asset"], first, last)["id"]
                    for first, last in ((1, 1), (1, 2), (2, 2))]
        self.contracts = set()
        for number, ref in enumerate(refs):
            uid = "fixture:contract-" + str(number)
            self.contracts.add(uid)
            accept(self.store, {
                "id": uid, "kind": "contract", "title": "Fixture increment interface " + str(number),
                "body": "The fixture increment keeps its input/output contract.",
                "conditions": ["Representable input"], "counterexamples": ["INT_MAX is excluded"],
                "source_refs": [ref], "symbol_refs": self.unit["symbol_refs"],
                "producers": self.unit["symbol_refs"], "consumers": self.unit["symbol_refs"],
                "requires": ["Input plus one is representable"], "ensures": ["Return input plus one"],
                "invariants": ["No pointer ownership transfer"],
            })

    def context(self, budget):
        return retrieval.get_context(self.store, {
            "task": "coding", "query": "fixture increment interface", "targets": ["cg_compute"],
            "source_snapshot": self.plan["snapshot"], "build_profile": self.plan["profile"],
            "index_run": self.plan["run"], "token_budget": budget,
        })

    def test_excerpts_are_deferred_before_contracts(self):
        original = self.store.read_evidence
        def large_excerpt(ref, **kwargs):
            return {**original(ref, **kwargs), "text": "source excerpt " * 300, "truncated": True}
        with patch.object(self.store, "read_evidence", side_effect=large_excerpt):
            pack = self.context(11000)
        self.assertTrue(self.contracts <= {u["id"] for u in pack["constraints"]})
        self.assertIn("evidence", pack["budget"]["omitted_kinds"])
        self.assertTrue(all(u["source_refs"] for u in pack["constraints"]))
        self.assertLessEqual(len(canonical(pack).encode("utf-8")), 11000)

    def test_delivered_ids_do_not_claim_omitted_bodies(self):
        for uid in sorted(self.contracts):
            unit = self.store.units(self.store.get_meta("knowledge_head"))[uid]
            unit = {k: v for k, v in unit.items() if k not in {"_binding", "review", "content_hash"}}
            accept(self.store, {**unit, "body": "fixture increment detail " * 400})
        pack = self.context(16000)
        delivered = {u["id"] for field in ("constraints", "paths", "test_obligations") for u in pack[field]}
        self.assertEqual(set(pack["retrieval"]["knowledge_ids"]), delivered)
        self.assertLess(len(delivered), pack["retrieval"]["matched_knowledge_count"])
        self.assertLessEqual(len(canonical(pack).encode("utf-8")), 16000)


if __name__ == "__main__":
    unittest.main()
