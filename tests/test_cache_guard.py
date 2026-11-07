"""Cache refusal must be cheap while retaining negative include validation."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from unified_knowledge import tu_cache
from unified_knowledge.materials import ingest
from unified_knowledge.store import Store,digest


class CacheGuardTests(unittest.TestCase):
    def test_uncacheable_sdk_is_rejected_before_path_probes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory);source=root/"source";source.mkdir()
            (source/"unit.cpp").write_text('#include "local.h"\n',encoding="utf-8")
            (source/"local.h").write_text('int value;\n',encoding="utf-8")
            sdk=root/"sdk.h";sdk.write_text('#include_next <stddef.h>\n',encoding="utf-8")
            with Store(root/"work") as store:
                snap=ingest(store,{"repositories":[{"id":"server","root":str(source)}]})
                with patch.object(tu_cache,"present",side_effect=AssertionError("unnecessary path probe")):
                    guard=tu_cache.guard(store,snap["id"],"server/unit.cpp",["-I"+str(source)],{"server":source},
                        [{"path":str(sdk),"sha":digest(sdk.read_bytes()),"asset":None}])
                self.assertIsNone(guard)

    def test_new_higher_priority_include_invalidates_the_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/"source";source.mkdir()
            for name in ("priority","fallback"):(source/name).mkdir()
            (source/"unit.cpp").write_text('#include <choice.h>\n',encoding="utf-8")
            header=source/"fallback/choice.h";header.write_text('int before;\n',encoding="utf-8")
            cfg={"repositories":[{"id":"server","root":str(source)}]}
            with Store(root/"work") as store:
                snap=ingest(store,cfg)
                includes=[{"asset":"server/fallback/choice.h","sha":digest(header.read_bytes())}]
                guard=tu_cache.guard(store,snap["id"],"server/unit.cpp",
                    ["-I"+str(source/"priority"),"-I"+str(source/"fallback")],{"server":source},includes)
                payload={"lookup_guard":guard,"includes":includes}
                self.assertTrue(tu_cache.valid(store,snap["id"],payload))
                (source/"priority/choice.h").write_text('int after;\n',encoding="utf-8")
                changed=ingest(store,cfg)
                self.assertFalse(tu_cache.valid(store,changed["id"],payload))


if __name__=="__main__":unittest.main()
