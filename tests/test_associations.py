"""Reviewed associations are shared by Agent selectors and Wiki projections."""
import json
from pathlib import Path
import tempfile
import unittest

from platform_fixture import workspace, accept
from unified_knowledge import associations, curriculum, knowledge, planner, reader_wiki, retrieval, team, whole
from unified_knowledge.store import Store, digest


class AssociationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.store, self.plan, self.unit = workspace(Path(temporary.name))
        self.addCleanup(self.store.close)
        self.old_revision = self.store.get_meta("knowledge_head")
        self.alternate = {"id": "mechanism:alternate", "kind": "mechanism", "title": "Alternate synthetic explanation",
            "body": "An alternative source-derived fixture explanation for association checks.", "source_refs": self.unit["source_refs"]}
        accept(self.store, self.alternate)
        policy = whole.policy("generic")
        policy["templates"] = [{"id": "mainline:fixture", "title": "Synthetic increment mainline", "kind": "shared_research",
            "question": "Explain the synthetic value path", "patterns": ["server/optimizer/*"], "depends_on": []}]
        self.program = whole.ensure(self.store, policy)
        manifest = {"features": [{"id": "history:increment", "name": "Synthetic historical increment", "module_hint": "server/optimizer"}]}
        manifest["digest"] = digest(manifest)
        self.course = curriculum.ensure(self.store, manifest, {"region_lines": 20})

    def review(self, task, finished):
        planner.review_task(self.store, task, {"reviewer": "association-reviewer", "mode": "independent_review", "verdict": "accept",
            "notes": "Synthetic mapping protocol review, no real product acceptance", "result_digest": finished["result_digest"]})

    def mapping(self, uid, *, revision=1):
        task = self.plan["modules"]["server/optimizer"]["task"]
        if revision != 1:
            with self.store.transaction():
                task = planner.create_task(self.store, snapshot=self.plan["snapshot"], run=self.plan["run"], profile=self.plan["profile"],
                    kind="module_survey", bundle={"plan_id": self.plan["id"], "module": "server/optimizer", "mapping_revision": revision})
        lease = planner.lease(self.store, task, "association-learner")
        ref = self.unit["source_refs"][0]
        planner.read_for_task(self.store, task, "association-learner", lease["token"], ref)
        report = {"inventory_complete": True,
            "assets": [{"asset": key, "disposition": "deferred", "reason": "Inventory only; later mechanism learning remains",
                        "evidence_refs": [], "unit_ids": []} for key in self.plan["modules"]["server/optimizer"]["files"]],
            "feature_mappings": [{"feature_id": "history:increment", "state": "mapped", "reason": "Explicit synthetic source-backed mapping",
                                  "modules": ["server/optimizer"], "evidence_refs": [ref], "unit_ids": [uid]}]}
        progress = whole.stage_progress(self.store, task, "association-learner", lease["token"], report)
        finished = planner.finish_research(self.store, task, "association-learner", lease["token"],
            [{"question": "Historical feature identity", "status": "answered", "explanation": "Explicit frozen source relationship checked",
              "evidence_refs": [ref]}], progress_digest=progress["progress_digest"])
        self.review(task, finished)
        return task

    @staticmethod
    def exported(result):
        return json.loads(Path(result["structured_knowledge"]).read_text(encoding="utf8"))

    def test_planning_only_mapping_changes_regenerate_wiki_and_match_agent_ids(self):
        revision = self.store.get_meta("knowledge_head")
        before = reader_wiki.export_wiki(self.store)
        self.assertNotIn("history:increment", self.exported(before)["navigation"]["feature"])
        self.assertNotIn("feature_ids", self.store.units(ids=[self.unit["id"]])[self.unit["id"]])
        self.mapping(self.unit["id"])
        self.assertEqual(self.store.get_meta("knowledge_head"), revision)
        context = retrieval.get_context(self.store, {"task": "coding", "feature": "history:increment", "token_budget": 16000})
        self.assertEqual(context["retrieval"]["knowledge_ids"], [self.unit["id"]])
        first = reader_wiki.export_wiki(self.store)
        self.assertNotEqual(before["portable_wiki"], first["portable_wiki"])
        self.assertNotEqual(before["projection_fingerprint"], first["projection_fingerprint"])
        self.assertEqual(first["revision"], revision)
        self.assertEqual(self.exported(first)["navigation"]["feature"]["history:increment"], [self.unit["id"]])
        self.mapping(self.alternate["id"], revision=2)
        second = reader_wiki.export_wiki(self.store)
        self.assertEqual(second["revision"], revision)
        self.assertNotEqual(first["portable_wiki"], second["portable_wiki"])
        self.assertEqual(self.exported(second)["navigation"]["feature"]["history:increment"], [self.alternate["id"]])
        context = retrieval.get_context(self.store, {"task": "coding", "feature": "history:increment", "token_budget": 16000})
        self.assertEqual(context["retrieval"]["knowledge_ids"], [self.alternate["id"]])
        old = retrieval.get_context(self.store, {"task": "coding", "feature": "history:increment", "knowledge_revision": self.old_revision,
                                                  "token_budget": 16000})
        self.assertEqual(old["retrieval"]["knowledge_ids"], [])

    def test_changed_published_unit_reopens_mapping_and_is_excluded(self):
        self.mapping(self.unit["id"])
        changed = {**self.unit, "body": self.unit["body"] + " Revised interpretation needs a fresh mapping review."}
        accept(self.store, changed)
        self.assertEqual(curriculum.feature_status(self.store)[0]["state"], "pending_knowledge")
        projected = associations.collect(self.store)
        self.assertNotIn("history:increment", projected["navigation"]["feature"])
        context = retrieval.get_context(self.store, {"task": "coding", "feature": "history:increment", "token_budget": 16000})
        self.assertEqual(context["retrieval"]["knowledge_ids"], [])
        self.assertNotIn("history:increment", self.exported(reader_wiki.export_wiki(self.store))["navigation"]["feature"])

    def test_program_item_published_claims_project_without_manual_unit_tags(self):
        self.mapping(self.unit["id"])
        old = self.store.get_meta("knowledge_head")
        task = self.program["templates"][0]["task"]
        lease = planner.lease(self.store, task, "mainline-learner")
        ref = self.unit["source_refs"][0]
        planner.read_for_task(self.store, task, "mainline-learner", lease["token"], ref)
        unit = {"id": "mechanism:mainline", "kind": "mechanism", "title": "Synthetic mainline claim",
            "body": "The frozen fixture value passes through the increment implementation.", "source_refs": [ref]}
        draft = planner.stage_research_unit(self.store, task, "mainline-learner", lease["token"], unit)
        progress = whole.stage_progress(self.store, task, "mainline-learner", lease["token"], {"templates": [
            {"id": "mainline:fixture", "state": "verified", "reason": "Synthetic source path investigated",
             "unit_ids": [unit["id"]], "evidence_refs": [ref]}]})
        finished = planner.finish_research(self.store, task, "mainline-learner", lease["token"],
            [{"question": "Synthetic value path", "status": "answered", "explanation": "Source path inspected", "evidence_refs": [ref]}],
            draft["drafts_digest"], progress["progress_digest"])
        self.review(task, finished)
        self.assertNotIn("mainline:fixture", associations.collect(self.store)["navigation"]["mainline"])
        proposal = team.propose_task(self.store, task)
        review = knowledge.review_context(self.store, proposal["id"], "mainline-knowledge-reviewer")
        knowledge.review(self.store, proposal["id"], {"reviewer": "mainline-knowledge-reviewer", "mode": "independent_review",
            "verdict": "accept", "notes": "Synthetic source-backed publication", "proposal_digest": review["proposal_digest"]})
        context = retrieval.get_context(self.store, {"task": "coding", "mainline": "mainline:fixture", "token_budget": 16000})
        self.assertEqual(context["retrieval"]["knowledge_ids"], [unit["id"]])
        exported = self.exported(reader_wiki.export_wiki(self.store))
        self.assertEqual(exported["navigation"]["mainline"]["mainline:fixture"], [unit["id"]])
        previous = retrieval.get_context(self.store, {"task": "coding", "mainline": "mainline:fixture", "knowledge_revision": old, "token_budget": 16000})
        self.assertEqual(previous["retrieval"]["knowledge_ids"], [])

    def test_association_queries_are_readonly_scoped_and_selector_bounded(self):
        self.mapping(self.unit["id"])
        with Store(self.store.home, readonly=True) as reader:
            before = reader.db.total_changes
            projected = associations.collect(reader, selectors={"feature": ["history:increment"]})
            self.assertEqual(projected["navigation"]["feature"]["history:increment"], [self.unit["id"]])
            self.assertEqual(reader.db.total_changes, before)
            self.assertFalse(associations.collect(reader, run="different-run")["current_projection"])
        with self.assertRaisesRegex(ValueError, "at most 100"):
            associations.collect(self.store, selectors={"feature": ["history:increment"] * 101})


if __name__ == "__main__":
    unittest.main()
