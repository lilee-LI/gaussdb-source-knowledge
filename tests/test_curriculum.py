"""Semantic curriculum boundary checks on synthetic source, never product QA."""
from copy import deepcopy
from pathlib import Path, PurePosixPath
import tempfile
import unittest
from unittest.mock import patch

from platform_fixture import workspace, accept
from unified_knowledge import curriculum, ecs, implementation, knowledge, planner, study, team, whole
from unified_knowledge.store import canonical, digest


class CurriculumTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store, _, self.initial = workspace(self.root)
        self.addCleanup(self.store.close)
        source = self.root / "source"
        (source / "optimizer" / "uncalled.cpp").write_text(
            "#ifdef SYNTHETIC_FEATURE\nstatic int never_called() { return 9; }\n#else\n"
            "static int never_called() { return 3; }\n#endif\n", encoding="utf8")
        for name in ("a", "b", "c"):
            (source / "optimizer" / ("cost_" + name + ".cpp")).write_text(
                "// Synthetic cost region, not a database semantic fixture\n" * 44 +
                "static int cost_" + name + "(int input) { return input; }\n", encoding="utf8")
        (source / "optimizer" / "large.cpp").write_text(
            "// A large synthetic file must retain every physical region obligation.\n" * 420, encoding="utf8")
        (source / "optimizer" / "empty.cpp").write_bytes(b"")
        ecs.connect(self.store, {"repositories": [{"id": "server", "root": str(source)}],
            "product_adapter": "opengauss", "ecs_index": {"database": str(self.root / "input.sqlite3"), "graph_storage": "reference"}})
        self.plan = study.current(self.store)
        policy = whole.policy("generic")
        policy["templates"] = []
        self.program = whole.ensure(self.store, policy)
        self.inputs = {"features": [{"id": "history:increment", "name": "Synthetic increment",
            "module_hint": "server/optimizer", "aliases": [], "status": "valid"}], "summary": {"feature_rows": 1}, "issues": []}
        self.inputs["digest"] = digest(self.inputs)
        self.options = {"max_files": 2, "max_source_bytes": 10000, "region_lines": 20}
        self.course = curriculum.ensure(self.store, self.inputs, self.options)
        self.module = "server/optimizer"

    def review(self, task, result_digest, *, publish=False):
        planner.review_task(self.store, task, {"reviewer": "synthetic-research-reviewer", "mode": "independent_review",
            "verdict": "accept", "notes": "Synthetic protocol evidence review; no real product acceptance", "result_digest": result_digest})
        if publish:
            self.publish(task)

    def publish(self, task):
        proposal = team.propose_task(self.store, task)
        context = knowledge.review_context(self.store, proposal["id"], "synthetic-knowledge-reviewer", max_chars=1000000)
        knowledge.review(self.store, proposal["id"], {"reviewer": "synthetic-knowledge-reviewer", "mode": "independent_review",
            "verdict": "accept", "notes": "Synthetic reviewed source fixture only", "proposal_digest": context["proposal_digest"]})

    def inventory(self, *, complete=True, original=True):
        task = self.plan["modules"][self.module]["task"]
        if not original:
            with self.store.transaction():
                task = planner.create_task(self.store, snapshot=self.plan["snapshot"], run=self.plan["run"], profile=self.plan["profile"],
                    kind="module_survey", bundle={"plan_id": self.plan["id"], "module": self.module,
                        "question": "Complete the synthetic inventory", "inventory_revision": 2, "source_anchor_refs": []})
        lease = planner.lease(self.store, task, "synthetic-learner")
        read = whole.read_source(self.store, task, "synthetic-learner", lease["token"], "server/optimizer/producer.cpp", 1, 400)
        files = self.plan["modules"][self.module]["files"]
        rows = [{"asset": key, "disposition": "deferred", "reason": "Inventoried for later mechanism learning", "evidence_refs": [], "unit_ids": []}
                for key in (files if complete else files[:-1])]
        progress = whole.stage_progress(self.store, task, "synthetic-learner", lease["token"], {"inventory_complete": complete, "assets": rows})
        result = planner.finish_research(self.store, task, "synthetic-learner", lease["token"],
            [{"question": "Is this the synthetic scope?", "status": "answered", "explanation": "Frozen seed and all inventory entries checked",
              "evidence_refs": [read["id"]]}], progress_digest=progress["progress_digest"])
        self.review(task, result["result_digest"])
        return task

    def feature_task(self, *, selected=None, suffix="mechanism"):
        with self.store.transaction():
            return planner.create_task(self.store, snapshot=self.plan["snapshot"], run=self.plan["run"], profile=self.plan["profile"],
                kind="feature_research", bundle={"module": self.module, "plan_id": self.plan["id"], "program_id": self.program["id"],
                    "question": "Synthetic " + suffix, "selected_files": selected or ["server/optimizer/producer.cpp"], "source_anchor_refs": []},
                dependencies=[self.plan["modules"][self.module]["task"]])

    @staticmethod
    def analysis():
        return {"behavior": "Compute the synthetic input plus one", "conditions": "The integer result must be representable",
            "state": "Input is by value and the result is returned", "consumers": "The source consumer receives the returned value",
            "cleanup": "No allocation occurs in this frozen two-line function", "test_basis": "Use zero and negative inputs; exclude overflowing INT_MAX"}

    def test_all_cpp_macros_uncalled_files_and_budgets_remain_in_plan(self):
        planned = {key for item in self.course["packages"] for key in item["files"]}
        owned = {key for row in self.plan["modules"].values() for key in row["files"]}
        self.assertEqual(planned, owned)
        self.assertIn("server/optimizer/uncalled.cpp", planned)
        regions = implementation.listing(self.store, asset="server/optimizer/uncalled.cpp")["items"]
        self.assertTrue(any("SYNTHETIC_FEATURE" in hint["text"] for row in regions for hint in row["hints"]))
        self.assertEqual(self.store.db.execute("SELECT count(*) FROM symbols WHERE run=? AND asset=?",
            (self.plan["run"], "server/optimizer/uncalled.cpp")).fetchone()[0], 0)
        expected_cpp = {key for key in owned if PurePosixPath(key).suffix == ".cpp"}
        self.assertEqual(implementation.audit(self.store)["cpp_files"], len(expected_cpp))
        for package in self.course["packages"]:
            self.assertLessEqual(len(package["files"]), 2)
            if package["budget"]["source_bytes"] > self.options["max_source_bytes"]:
                self.assertEqual(len(package["files"]), 1)
                self.assertTrue(package["budget"]["large_file_requires_chunks"])
        self.assertFalse(self.store.db.execute("SELECT 1 FROM tasks WHERE kind IN ('source_research','scc_synthesis') AND run=?",
                                             (self.plan["run"],)).fetchone())
        self.assertFalse(curriculum.advance(self.store)["created_or_reused"])
        self.assertEqual(curriculum.status(self.store)["unassigned_cpp"], [])

    def test_refinement_preserves_every_file_and_enforces_revision(self):
        owned = self.plan["modules"][self.module]["files"]
        packages = [{"id": "scope-" + str(n), "title": "Synthetic mechanism batch " + str(n),
            "question": "Explain the frozen source behavior", "files": owned[n:n + 2]} for n in range(0, len(owned), 2)]
        bad = deepcopy(packages)
        bad[-1]["files"] = bad[-1]["files"][:-1]
        if not bad[-1]["files"]:
            bad.pop()
        with self.assertRaisesRegex(ValueError, "preserve every"):
            curriculum.refine(self.store, self.module, bad, "synthetic-planner", self.course["revision"])
        duplicate = deepcopy(packages)
        duplicate[0]["files"] = [owned[0], owned[0]]
        with self.assertRaisesRegex(ValueError, "Repeated package file"):
            curriculum.refine(self.store, self.module, duplicate, "synthetic-planner", self.course["revision"])
        unknown = deepcopy(packages)
        unknown[0]["feature_ids"] = ["invented:feature"]
        with self.assertRaisesRegex(ValueError, "Unknown historical"):
            curriculum.refine(self.store, self.module, unknown, "synthetic-planner", self.course["revision"])
        result = curriculum.refine(self.store, self.module, packages, "synthetic-planner", self.course["revision"])
        self.assertNotEqual(result["revision"], self.course["revision"])
        with self.assertRaisesRegex(ValueError, "Curriculum changed"):
            curriculum.refine(self.store, self.module, packages, "synthetic-planner", self.course["revision"])
        self.assertEqual(curriculum.status(self.store, self.module)["unassigned_assets"], [])

    def test_reviewed_complete_inventory_is_required_not_accepted_task_status(self):
        original = self.plan["modules"][self.module]["task"]
        lease = planner.lease(self.store, original, "synthetic-inventory-check")
        incomplete = [{"asset": key, "disposition": "deferred", "reason": "Inventory row", "evidence_refs": [], "unit_ids": []}
                      for key in self.plan["modules"][self.module]["files"][:-1]]
        with self.assertRaisesRegex(ValueError, "EVERY asset"):
            whole.stage_progress(self.store, original, "synthetic-inventory-check", lease["token"],
                                 {"inventory_complete": True, "assets": incomplete})
        planner.lease(self.store, original, "synthetic-inventory-check", action="release", token=lease["token"])
        survey = self.inventory(complete=False)
        self.assertEqual(planner.task_status(self.store, survey)["status"], "accepted")
        self.assertFalse(curriculum.inventory_ready(self.store, self.module))
        task = self.feature_task()
        self.assertIn("inventory_incomplete", canonical(curriculum.prerequisites(self.store, planner.task_status(self.store, task))))
        with self.assertRaisesRegex(ValueError, "knowledge prerequisites"):
            planner.lease(self.store, task, "synthetic-feature-learner")
        self.inventory(complete=True, original=False)
        self.assertTrue(curriculum.inventory_ready(self.store, self.module))
        lease = planner.lease(self.store, task, "synthetic-feature-learner")
        self.assertEqual(lease["status"], "leased")
        self.assertEqual(implementation.audit(self.store, self.module)["cpp_files_closed"], 0)

    def test_advance_is_bounded_by_module_and_ignores_obsolete_plan_work(self):
        self.inventory()
        with self.store.transaction():
            planner.create_task(self.store, snapshot=self.plan["snapshot"], run=self.plan["run"], profile=self.plan["profile"],
                kind="feature_research", bundle={"module": self.module, "plan_id": "obsolete-plan", "question": "Old scope is preserved"})
        first = curriculum.advance(self.store, max_tasks=1)
        self.assertEqual(len(first["created_or_reused"]), 1)
        task = planner.task_status(self.store, first["created_or_reused"][0]["task"])
        self.assertEqual(task["kind"], "feature_research")
        self.assertEqual(task["bundle"]["module"], self.module)
        self.assertLessEqual(len(task["bundle"]["selected_files"]), self.options["max_files"])
        self.assertEqual(task["dependencies"], [self.plan["modules"][self.module]["task"]])
        self.assertFalse(curriculum.advance(self.store, max_tasks=1)["created_or_reused"])
        owned = self.plan["modules"][self.module]["files"]
        refined = [{"id": str(n), "title": "Changed scope", "question": "Another mechanism", "files": owned[n:n + 2]}
                   for n in range(0, len(owned), 2)]
        with self.assertRaisesRegex(ValueError, "Refine before execution"):
            curriculum.refine(self.store, self.module, refined, "synthetic-planner", curriculum.current(self.store)["revision"])

    def test_advance_resolves_inventory_once_across_many_packages(self):
        # Preserve the real scope, with many independent proposed work packages
        # before the ready module. This guards query/parse counts, not machine
        # speed: the old per-package inventory_ready implementation fails at
        # the first prohibited call instead of hanging the test for minutes.
        scaled = deepcopy(self.course)
        unready = next(p for p in scaled["packages"] if p["module"] != self.module)
        extras = [{**deepcopy(unready), "id": "synthetic-scale-package:" + str(i)} for i in range(1000)]
        scaled["packages"] = extras + scaled["packages"]
        with self.store.transaction():
            self.store.set_meta(scaled["id"], scaled)
        with patch.object(curriculum, "ready_modules", wraps=curriculum.ready_modules) as ready, \
                patch.object(curriculum, "inventory_ready", side_effect=AssertionError("Per-package inventory resolution is unbounded")), \
                patch.object(whole, "_rows", side_effect=AssertionError("No ready module should require coverage evaluation")), \
                patch.object(implementation, "evaluated", side_effect=AssertionError("No ready module should require region evaluation")):
            self.assertFalse(curriculum.advance(self.store, max_tasks=1)["created_or_reused"])
            ready.assert_called_once()
        self.inventory()
        with patch.object(curriculum, "ready_modules", wraps=curriculum.ready_modules) as ready, \
                patch.object(curriculum, "inventory_ready", side_effect=AssertionError("Per-package inventory resolution is unbounded")), \
                patch.object(whole, "_report_state", wraps=whole._report_state) as report_reads, \
                patch.object(study, "current", wraps=study.current) as plan_reads:
            result = curriculum.advance(self.store, max_tasks=1)
        self.assertEqual(len(result["created_or_reused"]), 1)
        task = planner.task_status(self.store, result["created_or_reused"][0]["task"])
        self.assertEqual(task["bundle"]["module"], self.module)
        ready.assert_called_once()
        report_reads.assert_called_once()
        self.assertLessEqual(plan_reads.call_count, 8)

    def test_open_questions_stay_in_reviewed_gaps_without_question_tasks(self):
        questions = ["Synthetic unresolved mechanism " + str(i) for i in range(5)]
        for manual_gap in (False, True):
            with self.subTest(manually_staged_gap=manual_gap):
                task = self.plan["modules"][self.module]["task"]
                if manual_gap:
                    with self.store.transaction():
                        task = planner.create_task(self.store, snapshot=self.plan["snapshot"], run=self.plan["run"],
                            profile=self.plan["profile"], kind="module_survey", bundle={"plan_id": self.plan["id"],
                                "module": self.module, "question": "Review explicitly staged and implicit unknowns", "inventory_revision": 3})
                lease = planner.lease(self.store, task, "synthetic-gap-learner")
                token = lease["token"]
                read = whole.read_source(self.store, task, "synthetic-gap-learner", token, "server/optimizer/producer.cpp", 1, 400)
                report = {"inventory_complete": True, "assets": [{"asset": key, "disposition": "deferred",
                    "reason": "Scope inventoried; mechanisms require later learning", "unit_ids": [], "evidence_refs": []}
                    for key in self.plan["modules"][self.module]["files"]]}
                if manual_gap:
                    report["gaps"] = [{"question": questions[0], "reason": "Preserve this explicitly investigated explanation",
                                       "evidence_refs": [read["id"]]}]
                progress = whole.stage_progress(self.store, task, "synthetic-gap-learner", token, report)
                coverage = [{"question": "Synthetic module scope", "status": "answered", "explanation": "Frozen seed checked",
                             "evidence_refs": [read["id"]]}] + [{"question": question, "status": "open",
                    "explanation": "Keep this uncertainty for mechanism-level follow-up " + str(i)} for i, question in enumerate(questions)]
                coverage.append(dict(coverage[1]))  # Repeated wording must not multiply ledger entries.
                before = self.store.db.execute("SELECT count(*) FROM tasks").fetchone()[0]
                finished = planner.finish_research(self.store, task, "synthetic-gap-learner", token,
                                                   coverage, progress_digest=progress["progress_digest"])
                submitted = planner.task_status(self.store, task)["result"]
                gaps = submitted["progress"]["gaps"]
                self.assertEqual({gap["question"] for gap in gaps}, set(questions))
                self.assertEqual(len(gaps), len(questions))
                self.assertEqual(finished["result_digest"], digest(submitted))
                if manual_gap:
                    explicit = next(gap for gap in gaps if gap["question"] == questions[0])
                    self.assertEqual(explicit["reason"], report["gaps"][0]["reason"])
                    self.assertEqual(explicit["evidence_refs"], [read["id"]])
                else:
                    self.assertNotIn("gaps", report)
                    self.assertEqual(gaps[0]["reason"], coverage[1]["explanation"])
                tampered = deepcopy(submitted)
                tampered["progress"]["gaps"] = []
                with self.assertRaisesRegex(ValueError, "fingerprint mismatch"):
                    planner.review_task(self.store, task, {"reviewer": "synthetic-research-reviewer", "mode": "independent_review",
                        "verdict": "accept", "notes": "A signature omitting auto-preserved gaps must fail", "result_digest": digest(tampered)})
                self.review(task, finished["result_digest"])
                self.assertEqual(self.store.db.execute("SELECT count(*) FROM tasks").fetchone()[0], before)
                self.assertFalse(self.store.db.execute("SELECT 1 FROM tasks WHERE kind='gap_research' AND run=?",
                                                       (self.plan["run"],)).fetchone())
                reports, _, _ = whole._report_state(self.store, self.program)
                accepted = next(row for row in reports if row["task"] == task)
                self.assertEqual(accepted["progress"]["gaps"], gaps)
                self.assertTrue(curriculum.inventory_ready(self.store, self.module))
        blockers = [row for row in whole.audit(self.store, self.module)["blockers"] if row["kind"] == "open_gap"]
        self.assertEqual({row["question"] for row in blockers}, set(questions))
        advanced = curriculum.advance(self.store, max_tasks=1)
        self.assertEqual(len(advanced["created_or_reused"]), 1)
        mechanism = planner.task_status(self.store, advanced["created_or_reused"][0]["task"])
        self.assertEqual(mechanism["kind"], "feature_research")
        self.assertIn("package_id", mechanism["bundle"])
        self.assertLessEqual(len(mechanism["bundle"]["selected_files"]), self.options["max_files"])

    def test_reading_and_published_module_label_do_not_close_implementation(self):
        task = self.plan["modules"][self.module]["task"]
        lease = planner.lease(self.store, task, "synthetic-learner")
        token = lease["token"]
        refs, assets = [], []
        for asset in self.plan["modules"][self.module]["files"]:
            meta = self.store.asset(self.plan["snapshot"], asset)
            local = []
            if meta.get("bytes"):
                start = 1
                while start is not None:
                    read = whole.read_source(self.store, task, "synthetic-learner", token, asset, start, 400)
                    refs.append(read["id"])
                    local.append(read["id"])
                    start = read["next_line"]
            assets.append({"asset": asset, "disposition": "studied" if local else "supporting",
                "reason": "Full synthetic source inventory only", "evidence_refs": local, "unit_ids": ["module:synthetic-label"]})
        unit = {"id": "module:synthetic-label", "kind": "module", "title": "Synthetic source module",
            "body": "The module contains these inventoried files; no mechanism explanation is supplied.", "source_refs": refs}
        draft = planner.stage_research_unit(self.store, task, "synthetic-learner", token, unit)
        region = implementation.listing(self.store, asset="server/optimizer/producer.cpp")["items"][0]
        with self.assertRaisesRegex(ValueError, "substantive mechanism"):
            implementation.validate(self.store, self.program, planner.task_status(self.store, task), [{"item": region["id"],
                "state": "explained", "reason": "A module label is insufficient", "analysis": self.analysis(),
                "unit_ids": [unit["id"]], "evidence_refs": refs}], {unit["id"]: unit}, set(refs))
        progress = whole.stage_progress(self.store, task, "synthetic-learner", token, {"inventory_complete": True, "assets": assets})
        finished = planner.finish_research(self.store, task, "synthetic-learner", token,
            [{"question": "Inventory scope", "status": "answered", "explanation": "Every frozen source was read", "evidence_refs": refs}],
            draft["drafts_digest"], progress["progress_digest"])
        self.review(task, finished["result_digest"], publish=True)
        state = whole.status(self.store, self.module)["modules"][0]
        self.assertTrue(state["inventory_reviewed"])
        self.assertFalse(state["source_knowledge_closed"])
        self.assertGreater(state["unexplained_cpp_regions"], 0)
        self.assertIn("implementation_explanation", {b["kind"] for b in whole.audit(self.store, self.module)["blockers"]})

    def test_region_requires_full_evidence_analysis_publication_and_current_hash(self):
        self.inventory()
        task = self.feature_task()
        lease = planner.lease(self.store, task, "synthetic-learner")
        token = lease["token"]
        region = implementation.listing(self.store, asset="server/optimizer/producer.cpp")["items"][0]
        partial = whole.read_source(self.store, task, "synthetic-learner", token, region["asset"], 1, 1)
        unit = {"id": "mechanism:synthetic-region", "kind": "mechanism", "title": "Synthetic increment implementation",
            "body": "The frozen function returns its integer input plus one and performs no allocation.", "source_refs": [partial["id"]]}
        draft = planner.stage_research_unit(self.store, task, "synthetic-learner", token, unit)
        row = {"item": region["id"], "state": "explained", "reason": "Explain the exact synthetic region", "analysis": self.analysis(),
            "unit_ids": [unit["id"]], "evidence_refs": [partial["id"]]}
        with self.assertRaisesRegex(ValueError, "fully supported"):
            whole.stage_progress(self.store, task, "synthetic-learner", token, {"implementations": [row]})
        read = whole.read_source(self.store, task, "synthetic-learner", token, region["asset"], 1, 400)
        unit = {**unit, "source_refs": [read["id"]]}
        draft = planner.stage_research_unit(self.store, task, "synthetic-learner", token, unit, draft["unit_hash"])
        row["evidence_refs"] = [read["id"]]
        bad = {**row, "analysis": {**row["analysis"], "cleanup": ""}}
        with self.assertRaisesRegex(ValueError, "Explain behavior"):
            whole.stage_progress(self.store, task, "synthetic-learner", token, {"implementations": [bad]})
        progress = whole.stage_progress(self.store, task, "synthetic-learner", token, {"implementations": [row]})
        finished = planner.finish_research(self.store, task, "synthetic-learner", token,
            [{"question": "Increment implementation", "status": "answered", "explanation": "Full frozen source and boundary checked", "evidence_refs": [read["id"]]}],
            draft["drafts_digest"], progress["progress_digest"])
        self.assertEqual(implementation.evaluated(self.store, self.program)[region["id"]]["state"], "unreviewed")
        self.review(task, finished["result_digest"])
        self.assertEqual(implementation.evaluated(self.store, self.program)[region["id"]]["state"], "pending_knowledge")
        self.publish(task)
        self.assertEqual(implementation.evaluated(self.store, self.program)[region["id"]]["state"], "explained")
        changed = {**unit, "body": unit["body"] + " Revised synthetic interpretation requires coverage re-review."}
        accept(self.store, changed)
        self.assertEqual(implementation.evaluated(self.store, self.program)[region["id"]]["state"], "pending_knowledge")

    def test_empty_source_closes_only_by_reviewed_exact_hash_disposition(self):
        self.inventory()
        task = self.feature_task(selected=["server/optimizer/empty.cpp"], suffix="empty file scope")
        lease = planner.lease(self.store, task, "synthetic-learner")
        token = lease["token"]
        item = implementation.listing(self.store, asset="server/optimizer/empty.cpp")["items"][0]
        self.assertEqual(item["kind"], "empty_source")
        row = {"item": item["id"], "state": "no_implementation", "reason": "Frozen bytes are empty; no implementation exists", "sha256": item["sha256"]}
        for bad in ({**row, "sha256": "0" * 64}, {**row, "unknowns": ["Classification remains uncertain"]}):
            with self.assertRaises(ValueError):
                whole.stage_progress(self.store, task, "synthetic-learner", token, {"implementations": [bad]})
        normal = implementation.listing(self.store, asset="server/optimizer/producer.cpp")["items"][0]
        with self.assertRaisesRegex(ValueError, "actual frozen empty"):
            whole.stage_progress(self.store, task, "synthetic-learner", token, {"implementations": [{**row, "item": normal["id"], "sha256": normal["sha256"]}]})
        progress = whole.stage_progress(self.store, task, "synthetic-learner", token, {"implementations": [row]})
        self.assertEqual(implementation.evaluated(self.store, self.program)[item["id"]]["state"], "unreviewed")
        result = planner.finish_research(self.store, task, "synthetic-learner", token,
            [{"question": "Does the exact frozen empty file implement behavior?", "status": "not_applicable",
              "explanation": "The immutable content has zero bytes; exact SHA-256 supplied for review"}], progress_digest=progress["progress_digest"])
        self.review(task, result["result_digest"])
        self.assertEqual(implementation.evaluated(self.store, self.program)[item["id"]]["state"], "no_implementation")
        self.assertEqual(implementation.audit(self.store, self.module)["cpp_files_closed"], 1)

    def test_missing_implementation_index_recovers_and_partition_policy_is_explicit(self):
        with self.store.transaction():
            self.store.db.execute("DELETE FROM implementation_items WHERE program=?", (self.program["id"],))
            self.store.db.execute("DELETE FROM meta WHERE key=?", ("implementation-index:" + self.program["id"],))
        curriculum.ensure(self.store, self.inputs, self.options)
        self.assertGreater(implementation.audit(self.store)["items"], 0)
        with self.assertRaisesRegex(ValueError, "immutable region partition"):
            curriculum.ensure(self.store, self.inputs, {**self.options, "region_lines": 40})

    def test_feature_mapping_cannot_use_only_module_labels(self):
        anchor = self.initial["source_refs"][0]
        task = {"bundle": {"module": self.module}}
        label = {"id": "module:label", "kind": "module", "source_refs": [anchor]}
        row = {"feature_id": "history:increment", "state": "mapped", "reason": "Synthetic mapping evidence",
            "evidence_refs": [anchor], "modules": [self.module], "unit_ids": [label["id"]]}
        with self.assertRaisesRegex(ValueError, "substantive mechanism"):
            curriculum.validate_feature_mappings(self.store, self.program, task, [row], {label["id"]: label}, {anchor})
        row["unit_ids"] = [self.initial["id"]]
        accepted = curriculum.validate_feature_mappings(self.store, self.program, task, [row], {self.initial["id"]: self.initial}, {anchor})
        self.assertEqual(accepted[0]["state"], "mapped")

    def test_four_role_acceptance_requires_fields_and_actual_test_oracle(self):
        roles = ("coding", "test_generation", "review", "operations")
        weak = whole.verify_uses(self.store, [{"id": "weak-" + role, "module": self.module, "role": role,
            "query": "Fixture increment", "required_units": [self.initial["id"]]} for role in roles])
        self.assertEqual(weak["status"], "failed")
        self.assertTrue(all(self.initial["id"] in row["delivered_ids"] for row in weak["cases"]))
        self.assertTrue(all(row["missing_required"] for row in weak["cases"]))
        symbol = self.initial["symbol_refs"][0]
        common = {"source_refs": self.initial["source_refs"], "symbol_refs": [symbol], "conditions": ["Synthetic representable integer"]}
        accept(self.store, {**common, "id": "contract:synthetic-use", "kind": "contract", "title": "Synthetic increment contract",
            "body": "The frozen synthetic function returns input plus one.", "counterexamples": ["INT_MAX overflows and is excluded"],
            "producers": [symbol], "consumers": [symbol], "requires": ["Representable result"], "ensures": ["Result is input plus one"],
            "invariants": ["No allocation or ownership transfer occurs"]})
        accept(self.store, {**common, "id": "test:synthetic-use", "kind": "test_obligation", "title": "Synthetic increment test oracle",
            "body": "Generate zero and negative cases from the synthetic contract.", "expected_from": {"kind": "contract", "ref": "contract:synthetic-use"},
            "cases": ["zero", "negative"], "execution_status": "not_run"})
        accept(self.store, {**common, "id": "observation:synthetic-use", "kind": "observation", "title": "Synthetic increment source observations",
            "body": "Source-derived fixture guidance, never observed server behavior.", "operations": {
                "symptoms": ["Excluded input would make the result unrepresentable"], "diagnostics": ["Inspect the integer input and representability"],
                "configuration": ["This frozen two-line fixture exposes no configurable control"],
                "actions": [{"when": "Input is INT_MAX", "then": "Keep this overflowing case excluded from valid-result checks"}]}})
        strong = whole.verify_uses(self.store, [{"id": "strong-" + role, "module": self.module, "role": role,
            "query": "Synthetic increment", "required_units": ["contract:synthetic-use", "test:synthetic-use", "observation:synthetic-use"]} for role in roles])
        self.assertEqual(strong["status"], "passed", canonical(strong))
        self.assertTrue(all(row["role_status"] == "complete" for row in strong["cases"]))
        # Additional legitimate knowledge may clip redundant role-view rows.
        # Required source facts and exact requested units must still be usable.
        for index in range(5):
            accept(self.store,{**common,'id':'mechanism:redundant-view-'+str(index),'kind':'mechanism',
                'title':'Synthetic increment source facet '+str(index),'body':'Synthetic protocol facet of the same cited fixture.',
                'state':['The synthetic integer input is unchanged'],'consumers':['Synthetic fixture caller'],
                'invariants':['The cited source owns no allocation']})
        clipped=whole.verify_uses(self.store,[{'id':'clipped-usable','module':self.module,'role':'coding',
            'query':'Synthetic increment','required_units':['contract:synthetic-use']}])
        self.assertEqual(clipped['cases'][0]['role_status'],'partial')
        self.assertFalse(clipped['cases'][0]['missing_required'])
        self.assertTrue(clipped['cases'][0]['required_content_satisfied'])
        self.assertEqual(clipped['status'],'passed')
        blockers = next(b for b in whole.audit(self.store, self.module)["blockers"] if b["kind"] == "implementation_explanation")
        self.assertGreater(blockers["count"], 0)


if __name__ == "__main__":
    unittest.main()
