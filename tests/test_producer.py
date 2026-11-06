"""Regressions from the full native openGauss experiment."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from unified_knowledge.assembly import integrate, merge_occurrences
from unified_knowledge.indexer import _persist_payload, compiler_arguments
from unified_knowledge.materials import ingest
from unified_knowledge.store import Store, canonical, now


class NativeProducerTests(unittest.TestCase):
    def test_native_types_remain_bound_to_disjoint_contexts(self):
        old = {"evidence":"same", "type":"void () noexcept", "contexts":["tu:1"]}
        new = {"evidence":"same", "type":"void ()", "contexts":["tu:2"]}
        merged = merge_occurrences(old, new, native=True)
        self.assertIsNone(merged["type"])
        self.assertEqual("context_dependent", merged["type_resolution"])
        self.assertEqual(merged, merge_occurrences(new, old, native=True))
        self.assertEqual(merged, merge_occurrences(merged, old, native=True))
        self.assertEqual(["tu:1","tu:2"], merged["contexts"])
        self.assertEqual(2, len(merged["type_observations"]))

    def test_type_conflicts_within_one_context_are_rejected(self):
        old = {"evidence":"same", "type":"void () noexcept", "contexts":["tu:1"]}
        new = {"evidence":"same", "type":"void ()", "contexts":["tu:1"]}
        with self.assertRaisesRegex(ValueError, "same TU context"):
            merge_occurrences(old, new, native=True)
        new["contexts"] = ["tu:2"]
        with self.assertRaisesRegex(ValueError, "Conflicting symbol occurrences"):
            merge_occurrences(old, new)

    def test_native_evidence_conflicts_are_rejected(self):
        old = {"evidence":"old", "type":"void ()", "contexts":["tu:1"]}
        new = {"evidence":"new", "type":"void ()", "contexts":["tu:2"]}
        with self.assertRaisesRegex(ValueError, "symbol evidence"):
            merge_occurrences(old, new, native=True)

    def test_native_warning_suppression_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            entry = {
                "directory": str(root),
                "file": "unit.cpp",
                "arguments": [
                    "g++",
                    "-w",
                    "-DVALUE=2",
                    "-c",
                    "unit.cpp",
                    "-o",
                    "unit.o",
                ],
            }
            actual = compiler_arguments(entry, {}, {"server": root}, {"server": root})
            self.assertEqual(["-w", "-DVALUE=2"], actual)

    def test_native_brief_receipt_retry_keeps_one_context(self):
        self.check_retry(False)

    def test_native_retry_rejects_changed_inputs(self):
        self.check_retry(True)

    def test_native_retry_with_success_before_failed_input(self):
        self.check_retry(False, reverse_order=True)

    def check_retry(self, mismatch, reverse_order=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "unit.cpp").write_text("void f() {}\n", encoding="utf-8")
            cfg = {
                "repositories": [{"id": "server", "root": str(source)}],
                "profiles": [
                    {
                        "id": "native",
                        "repository": "server",
                        "commands": [
                            {
                                "directory": str(source),
                                "file": "unit.cpp",
                                "arguments": ["g++", "-w", "-c", "unit.cpp"],
                            }
                        ],
                    }
                ],
            }
            with Store(root / "work") as store:
                snap = ingest(store, cfg)
                common = {
                    "snapshot": snap["id"],
                    "profile": "native",
                    "profile_digest": store.profile(snap["id"], "native")["digest"],
                    "created": now(),
                    "native_facts": "calls",
                    "evidence_assets": ["server/unit.cpp"],
                    "tools": {},
                }
                first = {
                    **common,
                    "id": "run:z-before" if reverse_order else "run:a-before",
                    "mode": "full",
                    "status": "partial",
                    "facts_digest": "first",
                    "tu_results": [
                        {
                            "context": "tu:one",
                            "asset": "server/unit.cpp",
                            "status": "failed",
                            "cache_key": "old-key" if mismatch else None,
                        }
                    ],
                }
                retry = {
                    **common,
                    "id": "run:a-after" if reverse_order else "run:z-after",
                    "mode": "selected",
                    "status": "ready",
                    "facts_digest": "second",
                    "selected_files": ["unit.cpp"],
                    "frontend_invocations": 1,
                    "tu_results": [
                        {
                            "context": "tu:one",
                            "asset": "server/unit.cpp",
                            "status": "parsed",
                            "cache_key": "parsed-key",
                        }
                    ],
                }
                for run in (first, retry):
                    store.db.execute(
                        "INSERT INTO runs VALUES(?,?,?,?,?,?)",
                        (
                            run["id"],
                            snap["id"],
                            "native",
                            run["created"],
                            run["status"],
                            canonical(run),
                        ),
                    )
                _persist_payload(
                    store,
                    retry["id"],
                    snap["id"],
                    "native",
                    {
                        "symbols": [
                            {
                                "logical": "function:f",
                                "name": "f",
                                "asset": "server/unit.cpp",
                                "kind": "function_decl",
                                "usr": "f",
                                "linkage": "EXTERNAL",
                                "definition": True,
                                "type": "void ()",
                                "start": 1,
                                "end": 1,
                                "resolution": "resolved",
                            }
                        ],
                        "relations": [],
                    },
                    "tu:one",
                )
                store.db.commit()
                args = (store, [first["id"], retry["id"]], "native")
                if mismatch:
                    with self.assertRaisesRegex(
                        ValueError, "changed its frontend inputs"
                    ):
                        integrate(*args, snapshot=snap["id"], retry_failed=True)
                    return
                with self.assertRaisesRegex(ValueError, "Conflicting TU"):
                    integrate(*args, snapshot=snap["id"])
                result = integrate(*args, snapshot=snap["id"], retry_failed=True)
                self.assertEqual(
                    (1, 1, 0),
                    (
                        result["coverage"]["translation_units"],
                        result["coverage"]["parsed_tus"],
                        result["coverage"]["failed_tus"],
                    ),
                )
                self.assertEqual("calls", result["native_facts"])
                self.assertEqual(["server/unit.cpp"], result["evidence_assets"])
                self.assertEqual(1, result["coverage"]["symbols"])
                self.assertEqual(
                    result["id"],
                    integrate(*args, snapshot=snap["id"], retry_failed=True)["id"],
                )


if __name__ == "__main__":
    unittest.main()
