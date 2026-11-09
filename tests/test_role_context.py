"""Roles compose actual reviewed fields, keep IDs/provenance and expose gaps."""
from pathlib import Path
import json
import tempfile
import unittest

from platform_fixture import workspace, accept
from unified_knowledge import retrieval, reader_wiki, role_context
from unified_knowledge.store import canonical


class RoleContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.store, cls.plan, cls.unit = workspace(Path(cls.temp.name))
        common = {"source_refs": cls.unit["source_refs"], "symbol_refs": cls.unit["symbol_refs"],
                  "conditions": ["Synthetic representable integer"], "counterexamples": ["INT_MAX excluded"],
                  "feature_ids": ["feature:increment"], "mainline_ids": ["mainline:fixture"],
                  "knowledge_refs": [{"target": cls.unit["id"], "relation": "DEPENDS_ON"}]}
        accept(cls.store, {**common, "id": "fixture:interface", "kind": "contract", "title": "Fixture increment interface",
            "body": "Returns the synthetic input plus one.", "producers": cls.unit["symbol_refs"],
            "consumers": cls.unit["symbol_refs"], "requires": ["Representable result"], "ensures": ["Result = input + 1"],
            "invariants": ["No ownership transfer"]})
        accept(cls.store, {**common, "id": "fixture:test", "kind": "test_obligation", "title": "Fixture increment tests",
            "body": "Check synthetic zero and negative inputs.", "expected_from": {"kind": "contract", "ref": "fixture:interface"},
            "execution_status": "not_run", "cases": ["zero", "negative"]})
        accept(cls.store, {**common, "id": "fixture:flow", "kind": "flow", "title": "Fixture increment flow",
            "body": "Synthetic state passes through increment.", "steps": [{"kind": "data_stage", "meaning": "value -> result"}]})
        accept(cls.store, {"source_refs": cls.unit["source_refs"], "conditions": ["Synthetic fixture only"],
            "id": "fixture:ops", "kind": "observation", "title": "Fixture operational observations",
            "body": "Synthetic source-derived observation; no server execution.", "operations": {
                "symptoms": ["Fixture symptom in this test only"], "diagnostics": ["Inspect fixture input"],
                "configuration": ["Test fixture configuration"], "actions": [{"when": "Fixture input excluded", "then": "Use representable input"}]}})

    @classmethod
    def tearDownClass(cls):
        cls.store.close()
        cls.temp.cleanup()

    def test_default_scope_and_semantic_selectors(self):
        asset = self.store.record("anchors", self.unit["source_refs"][0])["asset"]
        module = next(mid for mid, row in self.plan["modules"].items() if asset in row["files"])
        for key, value in (("feature", "feature:increment"), ("mainline", "mainline:fixture"),
                           ("module", module)):
            result = retrieval.get_context(self.store, {"task": "coding", key: value, "token_budget": 24000})
            self.assertEqual(result["scope"]["source_snapshot"], self.plan["snapshot"])
            self.assertIn("fixture:interface", result["retrieval"]["knowledge_ids"])
            self.assertEqual(result["retrieval"]["selectors"][key], [value])

    def test_roles_have_different_requirements_and_real_oracles(self):
        packs = {role: retrieval.get_context(self.store, {"task": role, "feature": "feature:increment", "token_budget": 30000})
                 for role in ("coding", "test_generation", "review", "operations")}
        self.assertIn("interface_or_state", packs["coding"]["role_context"]["sections"])
        tests = packs["test_generation"]["role_context"]
        self.assertEqual(tests["sections"]["test_oracle"][0]["value"], {"kind": "contract", "ref": "fixture:interface"})
        self.assertIn("invariants", packs["review"]["role_context"]["sections"])
        operations = packs["operations"]["role_context"]
        self.assertEqual(operations["status"], "partial")
        self.assertIn("conditional_actions", operations["missing_required"])
        self.assertNotIn("observations", operations["sections"])
        for pack in packs.values():
            delivered = {r["id"] for field in ("constraints", "paths", "test_obligations") for r in pack[field]}
            self.assertEqual(set(pack["role_context"]["knowledge_ids"]), delivered)
            for rows in pack["role_context"]["sections"].values():
                self.assertTrue(all(row["unit"] in delivered for row in rows))
            self.assertEqual(pack["runtime_validation"], "not_run")

    def test_operational_fields_are_not_invented_from_contracts(self):
        result = retrieval.get_context(self.store, {"task": "operations", "query": "Fixture operational observations", "token_budget": 30000})
        view = result["role_context"]
        self.assertTrue(all(view["sections"].get(k) for k in ("observations", "diagnostic_evidence", "configuration", "conditional_actions")))
        self.assertTrue(all(row["unit"] == "fixture:ops" for key in ("observations", "diagnostic_evidence", "configuration", "conditional_actions")
                            for row in view["sections"][key]))

    def test_role_ordering_and_small_budget_remain_bounded(self):
        coding = retrieval.search(self.store, {"task": "coding", "feature": "feature:increment"})
        testing = retrieval.search(self.store, {"task": "test_generation", "feature": "feature:increment"})
        self.assertEqual(coding["hits"][0]["id"], "fixture:interface")
        self.assertEqual(testing["hits"][0]["id"], "fixture:test")
        for budget in (512, 2048, 5000):
            result = retrieval.get_context(self.store, {"task": "review", "feature": "feature:increment", "token_budget": budget})
            self.assertLessEqual(len(canonical(result).encode("utf8")), budget)

    def test_wiki_and_agent_views_share_revision_and_units(self):
        result = reader_wiki.export_wiki(self.store)
        exported = json.loads(Path(result["structured_knowledge"]).read_text(encoding="utf8"))
        self.assertEqual(exported["knowledge_revision"], result["revision"])
        self.assertIn("mainline:fixture", exported["navigation"]["mainline"])
        self.assertIn("feature:increment", exported["navigation"]["feature"])
        self.assertEqual(set(exported["provenance"]), {u["id"] for u in exported["units"]})
        view = json.loads(Path(result["role_views"]["test_generation"]).read_text(encoding="utf8"))
        self.assertEqual(view["knowledge_revision"], result["revision"])
        self.assertEqual(view["sections"]["test_oracle"][0]["unit"], "fixture:test")

    def test_manual_citation_is_not_implementation_evidence(self):
        unit = {"id": "synthetic:manual", "kind": "claim", "statement": "Documented behavior", "body": "Manual only",
                "source_refs": ["synthetic:manual-anchor"], "conditions": ["Document scope"]}
        view = role_context.compose({"constraints": [unit]}, {unit["id"]: unit}, "coding",
                                    evidence_kinds={"synthetic:manual-anchor": "document"})
        self.assertIn("implementation_evidence", view["missing_required"])
        self.assertEqual(view["status"], "partial")

    def test_source_only_consumers_are_useful_without_fabricating_contract_symbols(self):
        unit={'id':'synthetic:source-consumer','kind':'mechanism','body':'State is passed to the next planner stage.',
              'conditions':['Source-only conditional behavior'],'source_refs':['source-anchor'],
              'state':['Planner-owned result'],'consumers':['optimizer/path consumes the result'],
              'affected_modules':['optimizer/plan']}
        pack={'constraints':[unit]}
        view=role_context.compose(pack,{unit['id']:unit},'coding',evidence_kinds={'source-anchor':'source'})
        self.assertEqual(view['status'],'complete')
        self.assertEqual(view['sections']['consumers'][0]['field'],'consumers')
        self.assertNotIn('producers/consumers',str(view))
        manual=role_context.compose(pack,{unit['id']:unit},'coding',evidence_kinds={'source-anchor':'document'})
        self.assertIn('consumers',manual['missing_required'])

    def test_publishing_prose_consumers_does_not_create_false_symbol_bindings(self):
        from unified_knowledge.knowledge import knowledge_graph
        unit={'id':'fixture:text-consumer','kind':'mechanism','title':'Source-backed textual consumer',
              'body':'The fixture forwards its output to the named consumer under a stated source condition.',
              'source_refs':self.unit['source_refs'],'conditions':['Synthetic source only'],
              'state':['Source-backed output'],'consumers':['optimizer/path consumes the output']}
        accept(self.store,unit)
        published=self.store.units(ids=[unit['id']])[unit['id']]
        self.assertTrue(any(d['type']=='asset' for d in published['_binding']['dependencies']))
        self.assertFalse(any(d['type']=='symbol' for d in published['_binding']['dependencies']))
        self.assertFalse(any(link['knowledge']==unit['id'] for link in knowledge_graph(self.store)['source_links']))
        self.assertEqual(published['consumers'],unit['consumers'])

    def test_answered_topic_sections_use_real_profile_names_and_keep_open_gaps(self):
        unit = {"id": "synthetic:guc", "kind": "mechanism", "body": "Source-derived configuration",
                "source_refs": [], "topic_extensions": {"guc": {"coverage": [
                    {"check": "parameter_definition", "status": "answered"},
                    {"check": "consumers_and_observation", "status": "open"}], "details": {
                        "parameter_definition": [{"name": "synthetic_switch", "context": "session"}],
                        "consumers_and_observation": [{"observations": ["Unreviewed suggestion"]}]}}}}
        view = role_context.compose({"constraints": [unit]}, {unit["id"]: unit}, "operations")
        self.assertEqual(view["sections"]["configuration"][0]["field"], "topic_extensions.guc.details.parameter_definition")
        self.assertIn("observations", view["missing_required"])


if __name__ == "__main__":
    unittest.main()
