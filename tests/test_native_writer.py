"""Durable TU ownership and one-time symbol materialization regressions."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from unified_knowledge.materials import ingest
from unified_knowledge.native_writer import NativeWriter, prepare, prune
from unified_knowledge.store import Store


class NativeWriterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root/"source"
        self.source.mkdir()
        (self.source/"unit.cpp").write_text("int shared() { return 1; }\nint private_fn() { return shared(); }\n",encoding="utf-8")
        self.store = Store(self.root/"work")
        self.addCleanup(self.store.close)
        snap = ingest(self.store,{"repositories":[{"id":"server","root":str(self.source)}]})
        self.snapshot = snap["id"]
        prepare(self.store)

    def payload(self, private=False, type="int ()"):
        shared = {"logical":"logical:shared","name":"shared","asset":"server/unit.cpp","kind":"function_decl",
                  "definition":True,"linkage":"EXTERNAL","usr":"shared","type":type,"resolution":"resolved","start":1,"end":1}
        symbols = [shared]
        if private:
            symbols.append({**shared,"logical":"logical:private","name":"private_fn","usr":"private_fn","start":2,"end":2})
        edges = [{"source":"logical:private" if private else "logical:shared","target":"logical:shared", "kind":"CALLS",
                  "resolution":"resolved","asset":"server/unit.cpp","start":2 if private else 1,"end":2 if private else 1}]
        return {"symbols":symbols,"relations":edges}

    def test_shared_symbol_is_materialized_once_not_per_tu(self):
        writer = NativeWriter(self.store,"run",self.snapshot,"native")
        updates = []
        self.store.db.set_trace_callback(lambda sql:updates.append(sql) if sql.startswith("UPDATE symbols") else None)
        for i in range(100):
            with self.store.transaction():
                writer.persist(self.payload(type="int () noexcept" if i%2 else "int ()"),"tu:"+str(i))
        self.assertEqual([],updates)
        with self.store.transaction():
            stats = writer.finish()
        self.assertEqual(1,len(updates))
        self.assertEqual(1,stats["symbol_base_inserts"])
        self.assertEqual(100,stats["symbol_context_memberships"])
        value = json.loads(self.store.db.execute("SELECT data FROM symbols").fetchone()[0])
        self.assertEqual(100,len(value["contexts"]))
        self.assertIsNone(value["type"])
        self.assertEqual(2,len(value["type_observations"]))
        self.assertEqual(100,self.store.db.execute("SELECT count(*) FROM relations").fetchone()[0])

    def test_interruption_and_retry_preserve_other_tu_ownership(self):
        writer = NativeWriter(self.store,"run",self.snapshot,"native")
        with self.store.transaction():
            writer.persist(self.payload(),"tu:keep")
            writer.persist(self.payload(private=True),"tu:retry")
        self.store.close()
        self.store = Store(self.root/"work")
        self.addCleanup(self.store.close)
        with self.store.transaction():
            prune(self.store,"run",{"tu:retry"})
        self.assertEqual(1,self.store.db.execute("SELECT count(*) FROM symbols").fetchone()[0])
        self.assertEqual(1,self.store.db.execute("SELECT count(*) FROM relations").fetchone()[0])
        resumed = NativeWriter(self.store,"run",self.snapshot,"native")
        with self.store.transaction():
            resumed.persist(self.payload(),"tu:retry")
            resumed.finish()
        value = json.loads(self.store.db.execute("SELECT data FROM symbols").fetchone()[0])
        self.assertEqual(["tu:keep","tu:retry"],value["contexts"])
        self.assertEqual(2,self.store.db.execute("SELECT count(*) FROM relations").fetchone()[0])

    def test_transaction_rollback_has_no_partial_memberships(self):
        writer = NativeWriter(self.store,"run",self.snapshot,"native")
        with self.assertRaises(RuntimeError):
            with self.store.transaction():
                writer.persist(self.payload(),"tu:failed")
                raise RuntimeError("interrupted")
        self.assertEqual(0,self.store.db.execute("SELECT count(*) FROM native_memberships").fetchone()[0])
        self.assertEqual(0,self.store.db.execute("SELECT count(*) FROM symbols").fetchone()[0])

    def test_compiler_cannot_publish_different_frozen_header_bytes(self):
        writer=NativeWriter(self.store,"run",self.snapshot,"native")
        payload=self.payload()
        payload["includes"]=[{"asset":"server/unit.cpp","sha":"0"*64}]
        with self.assertRaisesRegex(ValueError,"frozen input contract"):
            with self.store.transaction():writer.persist(payload,"tu:changed")
        self.assertEqual(0,self.store.db.execute("SELECT count(*) FROM symbols").fetchone()[0])


if __name__=="__main__":
    unittest.main()
