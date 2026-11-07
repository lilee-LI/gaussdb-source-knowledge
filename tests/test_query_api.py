"""Bounded pagination must not hide unknowns, leak TU payloads, or mix versions."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from make_fixture import build_fixture
from unified_knowledge import ecs, study, query_api
from unified_knowledge.store import Store, canonical


class QueryApiTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        source = self.root / "source"
        shutil.copytree(ROOT / "assets/ecs-fixture/source", source)
        incoming = self.root / "input.sqlite3"
        build_fixture(incoming)
        self.store = Store(self.root / "home")
        self.addCleanup(self.store.close)
        ecs.connect(self.store, {"repositories":[{"id":"server","root":str(source)}], "ecs_index":{"database":str(incoming),"graph_storage":"reference"}})
        self.plan = study.current(self.store)
        self.run = self.plan["run"]
        self.symbol = query_api.lookup_symbols(self.store, self.run, "cg_consume")["items"][0]["id"]

    def test_compact_pagination_and_cursor_scope(self):
        with self.store.transaction():
            for i in range(8):
                value = {"id":f"test-edge:{i:03}", "source":self.symbol,"target":self.symbol,"kind":"CALLS","resolution":"unresolved",
                         "evidence":None,"contexts":["large TU payload" * 10000]}
                self.store.db.execute("INSERT INTO main.relations VALUES(?,?,?,?,?,?,?)",(self.run,value["id"],self.symbol,self.symbol,"CALLS","unresolved",canonical(value)))
        ids, cursor = [], None
        for _ in range(20):
            page = query_api.neighbors(self.store, self.run, self.symbol, limit=2, cursor=cursor)
            self.assertNotIn("contexts", canonical(page))
            self.assertLess(len(canonical(page).encode()), 32768)
            ids.extend(r["id"] for r in page["relations"])
            cursor = page["next_cursor"]
            if cursor is None:
                break
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(f"test-edge:{i:03}" for i in range(8)) <= set(ids))
        first = query_api.neighbors(self.store, self.run, self.symbol, limit=1)
        minimum = query_api.neighbors(self.store, self.run, self.symbol, max_bytes=2048)
        self.assertLessEqual(len(canonical(minimum).encode()), 2048)
        with self.assertRaisesRegex(ValueError, "another query"):
            query_api.neighbors(self.store, self.run, self.symbol, direction="reverse", cursor=first["next_cursor"])

    def test_legacy_resolution_is_not_upgraded(self):
        result = query_api.neighbors(self.store, self.run, self.symbol)
        self.assertTrue(result["relations"])
        self.assertTrue(all(r["resolution"] != "resolved" for r in result["relations"]))
        self.assertFalse(result["runtime_trace"])

    def test_invalid_limits_missing_symbols_and_versioned_evidence(self):
        with self.assertRaises(ValueError):
            query_api.lookup_symbols(self.store, self.run, "x", limit=0)
        with self.assertRaisesRegex(ValueError, "not found"):
            query_api.neighbors(self.store, self.run, "missing-symbol")
        hit = query_api.lookup_symbols(self.store, self.run, "cg_consume")["items"][0]
        value = query_api.evidence(self.store, self.plan["snapshot"], hit["evidence"])
        self.assertIn("cg_consume", value["text"])
        with self.assertRaisesRegex(ValueError, "another source"):
            query_api.evidence(self.store, "another-snapshot", hit["evidence"])
