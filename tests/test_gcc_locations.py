"""Compiler #line labels bind only to explicit, unambiguous frozen source files."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts.unified_knowledge.gcc_frontend import decode


class GccLocations(unittest.TestCase):
    def check_mapping(self,absolute=False,ambiguous=False):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            frozen,original = base/"frozen",base/"original"
            frozen.mkdir()
            original.mkdir()
            label = str(original/"grammar.y") if absolute else "grammar.y"
            (frozen/"main.cpp").write_text('#line 1 '+json.dumps(label)+'\nint f() { return 1; }\n')
            (frozen/"grammar.y").write_text('int f() { return 1; }\n')
            # A live source differing from the frozen source must never be read.
            (original/"grammar.y").write_text("changed live source\n")
            events = []
            if ambiguous:
                other = frozen/"other"
                other.mkdir()
                (other/"grammar.y").write_text('int f() { return 2; }\n')
                (other/"header.h").write_text('#line 1 "grammar.y"\n')
                events.append({"event":"include","file":str(other/"header.h")})
            events.append({"event":"symbol","uid":1,"name":"f","spelling":"int f()","abi":"_Z1fv",
                           "type":"int()","kind":"function_decl","position":{"file":label,"line":1,"column":5},
                           "end":1,"external":True,"definition":True,"implicit":False})
            stream = base/"output.jsonl"
            stream.write_text("\n".join(json.dumps(e) for e in events))
            result = decode(stream,{"roots":{"server":str(frozen)},"original_roots":{"server":str(original)},
                                    "file":str(frozen/"main.cpp"),"unit_file":"server/main.cpp"},[])
            if ambiguous:
                self.assertEqual(result["status"],"partial")
                self.assertEqual(result["symbols"],[])
                self.assertIn("ambiguous",result["diagnostics"][0]["message"])
            else:
                self.assertEqual(result["status"],"parsed")
                self.assertEqual(result["symbols"][0]["asset"],"server/grammar.y")
                self.assertEqual(result["symbols"][0]["offset"],4)
                self.assertIn(str(frozen/"grammar.y"),[v["path"] for v in result["includes"]])

    def test_relative_line_label(self):
        self.check_mapping()

    def test_absolute_original_line_label_reads_frozen_source(self):
        self.check_mapping(absolute=True)

    def test_ambiguous_line_label_blocks_strict_export(self):
        self.check_mapping(ambiguous=True)


if __name__=="__main__":
    unittest.main()
