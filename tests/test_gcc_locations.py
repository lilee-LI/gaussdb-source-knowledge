"""Compiler #line labels bind only to explicit, unambiguous frozen source files."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts.unified_knowledge.gcc_frontend import decode


class GccLocations(unittest.TestCase):
    def check_mapping(self,absolute=False,ambiguous=False,virtual_line=1):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            frozen,original = base/"frozen",base/"original"
            frozen.mkdir()
            original.mkdir()
            label = str(original/"grammar.y") if absolute else "grammar.y"
            (frozen/"main.cpp").write_text('#line '+str(virtual_line)+' '+json.dumps(label)+'\nint f() { return 1; }\n')
            (frozen/"grammar.y").write_text('int f() { return 1; }\n')
            # A live source differing from the frozen source must never be read.
            (original/"grammar.y").write_text("changed live source\n")
            events = []
            if ambiguous:
                other = frozen/"other"
                other.mkdir()
                (other/"grammar.y").write_text('int f() { return 2; }\n')
                (other/"header.h").write_text('#line 1 "grammar.y"\nint f() { return 2; }\n')
                events.append({"event":"include","file":str(other/"header.h")})
            events.append({"event":"symbol","uid":1,"name":"f","spelling":"int f()","abi":"_Z1fv",
                           "type":"int()","kind":"function_decl","position":{"file":label,"line":virtual_line,"column":5},
                           "end":virtual_line,"external":True,"definition":True,"implicit":False})
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
                self.assertEqual(result["symbols"][0]["asset"],"server/main.cpp")
                self.assertEqual(result["symbols"][0]["start"],2)
                self.assertEqual(result["symbols"][0]["offset"],(frozen/"main.cpp").read_bytes().index(b"f()"))
                self.assertEqual(result["symbols"][0]["expansion_location"]["presumed_location"]["asset"],"server/grammar.y")
                self.assertIn(str(frozen/"main.cpp"),[v["path"] for v in result["includes"]])

    def test_relative_line_label(self):
        self.check_mapping()

    def test_absolute_original_line_label_reads_frozen_source(self):
        self.check_mapping(absolute=True)

    def test_ambiguous_line_label_blocks_strict_export(self):
        self.check_mapping(ambiguous=True)

    def test_flex_line_past_original_eof_uses_compiled_file(self):
        self.check_mapping(virtual_line=2153)


if __name__=="__main__":
    unittest.main()
