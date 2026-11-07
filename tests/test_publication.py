import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from platform_fixture import workspace, accept
from unified_knowledge import publication, retrieval_pipeline, evaluation
from unified_knowledge.store import canonical


class PublicationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.store, self.plan, self.unit = workspace(self.root)
        self.addCleanup(self.store.close)

    def release(self):
        value = publication.prepare(self.store)
        publication.sync(self.store, value["id"])
        return publication.get(self.store, value["id"])

    def test_prepare_replay_activation_rollback_and_frozen_queries(self):
        first = self.release()
        self.assertEqual(publication.prepare(self.store)["id"], first["id"])
        publication.activate(self.store, first["id"])
        found = retrieval_pipeline.context(self.store, "fixture increment", max_bytes=30000)
        self.assertEqual(found["release_id"], first["id"])
        self.assertTrue(found["groups"][0]["complete"])
        self.assertTrue(found["groups"][0]["units"][0]["conditions"])
        self.assertTrue(found["groups"][0]["evidence"])
        updated = {**self.unit,"body":"The synthetic fixture returns value + 1. A new documentation revision clarifies the int bound."}
        accept(self.store, updated)
        second = self.release()
        with self.assertRaisesRegex(ValueError, "Active release changed"):
            publication.activate(self.store, second["id"])
        publication.activate(self.store, second["id"], expected_active=first["id"])
        old = retrieval_pipeline.context(self.store, "fixture increment", release_id=first["id"])
        self.assertEqual(old["groups"][0]["units"][0]["body"], self.unit["body"])
        publication.activate(self.store, first["id"], expected_active=second["id"])
        self.assertEqual(publication.get(self.store)["id"], first["id"])

    def test_staging_and_tampered_exports_cannot_activate(self):
        first = publication.prepare(self.store)
        with self.assertRaisesRegex(ValueError, "not ready"):
            publication.activate(self.store, first["id"])
        path = self.store.home / "retrieval-releases" / first["id"].replace(":", "-") / "documents" / next(iter(first["documents"].values()))["filename"]
        path.write_text("tampered", encoding="utf8")
        with self.assertRaisesRegex(ValueError, "export drift"):
            publication.sync(self.store, first["id"])
        self.assertIsNone(self.store.get_meta("active_retrieval_release"))
        self.assertFalse(self.store.get_meta("retrieval-sync-lock:" + first["id"]))

    def test_atomic_evidence_groups_and_no_answer(self):
        huge = {**self.unit,"body":"Fixture increment " + "long explanation " * 2000}
        accept(self.store, huge)
        release = self.release()
        publication.activate(self.store, release["id"])
        pack = retrieval_pipeline.context(self.store, "fixture increment", max_bytes=4096)
        self.assertEqual(pack["groups"], [])
        self.assertEqual(pack["status"], "no_answer")
        self.assertGreater(pack["omitted_count"], 0)
        self.assertLessEqual(len(canonical(pack).encode()), 4096)
        missing = retrieval_pipeline.context(self.store, "zqzq_unrelated_unknown_identifier")
        self.assertEqual(missing["status"], "no_answer")

    def test_evaluation_requires_version_and_nonleaking_mechanism_groups(self):
        release = self.release()
        publication.activate(self.store, release["id"])
        dataset = {"schema":"knowledge-evaluation/v1","release_id":release["id"],"cases":[
            {"id":"one","group":"increment","split":"acceptance","question":"fixture increment","answerable":True,
             "topics":["mechanism"],"necessary_unit_sets":[[self.unit["id"]]]},
            {"id":"two","group":"unknown","split":"acceptance","question":"zqzq_unrelated_unknown_identifier","answerable":False,
             "topics":["unknown"],"necessary_unit_sets":[]}]}
        report = evaluation.evaluate(self.store, dataset)
        self.assertEqual(report["summary"]["complete_context_rate"], 1)
        self.assertEqual(report["semantic_answer_accuracy"], "requires_separate_review")
        bad = copy.deepcopy(dataset)
        bad["cases"].append({**bad["cases"][0],"id":"three","split":"development"})
        with self.assertRaisesRegex(ValueError, "leaks"):
            evaluation.validate_cases(bad)
        with self.assertRaisesRegex(ValueError, "another release"):
            evaluation.evaluate(self.store, {**dataset,"release_id":"other"})

    def test_ragflow_retry_parse_completion_metadata_and_foreign_hits(self):
        import httpx
        docs, calls = {}, []
        ready = [False]
        def respond(request):
            path = request.url.path.removeprefix("/api/v1")
            calls.append((request.method,path))
            body = json.loads(request.content) if request.headers.get("content-type", "").startswith("application/json") else {}
            def response(data=None):
                return httpx.Response(200, json={"code":0,"data":data})
            if path == "/datasets" and request.method == "GET":
                return response([])
            if path == "/datasets" and request.method == "POST":
                return response({"id":"dataset-1","embedding_model":"test-embedding"})
            if path == "/datasets/dataset-1/documents" and request.method == "GET":
                return response({"docs":list(docs.values()),"total":len(docs)})
            if path == "/datasets/dataset-1/documents" and request.method == "POST":
                # Decode the sole multipart file, as a protocol fixture rather than a live RAGFlow engine.
                import email.parser, email.policy
                message = email.parser.BytesParser(policy=email.policy.default).parsebytes(
                    b"Content-Type: " + request.headers["content-type"].encode() + b"\r\n\r\n" + request.content)
                part = next(message.iter_parts())
                docs["doc-1"] = {"id":"doc-1","name":part.get_filename(),"run":"UNSTART","chunk_count":0,"meta_fields":{}}
                self.uploaded = part.get_payload(decode=True)
                return response([docs["doc-1"]])
            if path.endswith("/documents/doc-1") and request.method == "GET":
                return httpx.Response(200, content=self.uploaded)
            if path.endswith("/documents/doc-1") and request.method == "PATCH":
                docs["doc-1"]["meta_fields"] = body["meta_fields"]
                return response(docs["doc-1"])
            if path.endswith("/chunks"):
                docs["doc-1"].update(run="RUNNING",chunk_count=0)
                return response()
            if path == "/retrieval":
                self.assertEqual(body["dataset_ids"], ["dataset-1"])
                self.assertFalse(body["include_knowledge_compilation"])
                self.assertEqual(body["metadata_condition"]["conditions"][0]["name"], "release_id")
                return response({"chunks":[{"id":"foreign","document_id":"foreign-doc","dataset_id":"other","content":"Do not trust this text"},
                                           {"id":"hit","document_id":"doc-1","dataset_id":"dataset-1","content":"Also not authoritative"}]})
            raise AssertionError((request.method, path))
        config = {"kind":"ragflow","base_url":"http://ragflow.test","api_key_env":"KB_TEST_RAGFLOW_KEY","embedding_model":"test-embedding"}
        with patch.dict("os.environ", {"KB_TEST_RAGFLOW_KEY":"synthetic-test-key"}), httpx.Client(transport=httpx.MockTransport(respond)) as client:
            release = publication.prepare(self.store, provider=config)
            first = publication.sync(self.store, release["id"], provider_client=client)
            self.assertEqual(first["status"], "staging")
            with self.assertRaisesRegex(ValueError, "not ready"):
                publication.activate(self.store, release["id"])
            docs["doc-1"].update(run="DONE",chunk_count=1)
            second = publication.sync(self.store, release["id"], provider_client=client)
            self.assertEqual(second["status"], "ready")
            publication.activate(self.store, release["id"])
            pack = retrieval_pipeline.context(self.store, "fixture increment", provider_client=client)
            self.assertEqual(pack["groups"][0]["units"][0]["body"], self.unit["body"])
            self.assertTrue(any(u["code"] == "rejected_retrieval_candidates" for u in pack["unknowns"]))
            self.assertEqual(calls.count(("POST","/datasets/dataset-1/documents")), 1)
