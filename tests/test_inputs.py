"""Four-input discovery does not invoke compilers, shells or model clients."""
import json
from pathlib import Path
import tempfile
import unittest

from platform_fixture import ROOT
from unified_knowledge import inputs, materials
from unified_knowledge.store import Store


class InputPreparationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name); self.source = self.root / "source"
        (self.source / "src/optimizer").mkdir(parents=True)
        (self.source / "src/optimizer/cost.cpp").write_text("int cost(int n) { return n + 1; }\n", encoding="utf8")
        self.spec = {"product": "FixtureDB", "source": str(self.source)}

    def write(self, name, value):
        path = self.root / name
        path.write_text(value if isinstance(value, str) else json.dumps(value), encoding="utf8")
        return str(path)

    def prepare(self, **extra):
        return inputs.prepare({**self.spec, **extra}, self.root / "home/setup")

    def test_name_only_csv_duplicates_stable_ids_and_provenance(self):
        path = self.write("features.csv", "name,aliases,module_hint\nSQLPatch,sql_patch|补丁,optimizer\nSQLPatch,,optimizer\nGEQO,,optimizer\n")
        first = self.prepare(features=path); second = self.prepare(features=path)
        self.assertEqual(first, second)
        self.assertEqual(first["summary"]["features"], 2)
        self.assertEqual(first["summary"]["feature_rows"], 3)
        self.assertEqual(first["summary"]["duplicates"], 1)
        self.assertEqual(first["features"][0]["source_line"], 2)
        self.assertEqual(first["features"][0]["aliases"], ["sql_patch", "补丁"])
        self.assertEqual(first["features"][1]["status"], "duplicate")
        reordered = self.write("reordered.csv", "name\nGEQO\nSQLPatch\n")
        other = self.prepare(features=reordered)
        self.assertEqual({r["name"]: r["id"] for r in first["features"]}, {r["name"]: r["id"] for r in other["features"]})
        self.assertTrue(Path(first["manifest_path"]).is_file())

    def test_external_identity_collision_is_ambiguous_and_rows_retained(self):
        path = self.write("features.json", {"features": [{"id": "F1", "name": "Alpha"}, {"id": "F1", "name": "Beta"}]})
        value = self.prepare(features=path)
        self.assertEqual(value["summary"]["ambiguous"], 2)
        self.assertEqual({r["status"] for r in value["features"]}, {"ambiguous"})
        self.assertEqual(value["features"][1]["source_pointer"], "/features/1")
        self.assertTrue(any(r["kind"] == "ambiguous_feature_identity" for r in value["issues"]))

    def test_txt_and_markdown_names_with_no_required_design_fields(self):
        a = self.prepare(features=self.write("names.txt", "SQLPatch\nGEQO\n"))
        b = self.prepare(features=self.write("names.md", "# Features\n- SQLPatch\n- GEQO\n"))
        self.assertEqual([r["id"] for r in a["features"]], [r["id"] for r in b["features"]])
        c = self.prepare(features=self.write("table.md", "| 特性编号 | 名称 | 模块 |\n| --- | --- | --- |\n| F1 | SQLPatch | optimizer |\n"))
        self.assertEqual(c["features"][0]["external_id"], "F1")
        self.assertEqual(c["features"][0]["module_hint"], "optimizer")

    def test_multiple_contexts_preserve_macros_and_never_execute_commands(self):
        db = self.write("compile_commands.json", [
            {"directory": "/ecs/build", "file": "/ecs/repo/src/optimizer/cost.cpp", "arguments": ["g++", "-I", "../include", "-DROW=1", "-c", "/ecs/repo/src/optimizer/cost.cpp"]},
            {"directory": "/ecs/build", "file": "/ecs/repo/src/optimizer/cost.cpp", "command": "g++ -DVECTOR=1 -c /ecs/repo/src/optimizer/cost.cpp $(MUST_NOT_EXECUTE)"},
            {"directory": "/ecs/build", "file": "/ecs/repo/missing.cpp", "arguments": ["g++", "-c", "/ecs/repo/missing.cpp"]},
        ])
        value = self.prepare(compile_db=db)
        self.assertEqual(value["summary"]["compile_contexts"], 3)
        self.assertEqual(value["summary"]["mapped_contexts"], 2)
        self.assertEqual(value["summary"]["source_files_in_compile_db"], 1)
        self.assertEqual(value["compile_contexts"][0]["asset"], "server/src/optimizer/cost.cpp")
        self.assertEqual(value["compile_contexts"][0]["defines"], ["ROW=1"])
        self.assertEqual(value["compile_contexts"][0]["includes"], ["../include"])
        self.assertEqual(value["compile_contexts"][1]["analysis_status"], "not_run")
        self.assertIn("$(MUST_NOT_EXECUTE)", value["compile_contexts"][1]["original_arguments"])
        self.assertNotEqual(value["compile_contexts"][0]["id"], value["compile_contexts"][1]["id"])
        descriptor = json.loads(Path(value["normalized_compile_db"]).read_text(encoding="utf8"))
        self.assertEqual(len(descriptor), 2)
        for entry in descriptor:
            replay = materials._compile_entry(entry, self.source.resolve())
            self.assertEqual(replay["file"], "src/optimizer/cost.cpp")

    def test_ambiguous_suffix_unlocated_invalid_and_explicit_mapping(self):
        other = self.source / "other/cost.cpp"; other.parent.mkdir(); other.write_text("int cost2();\n", encoding="utf8")
        db = self.write("compile_commands.json", [
            {"directory": "/foreign", "file": "cost.cpp", "arguments": ["g++", "-c", "cost.cpp"]},
            {"directory": "/foreign", "file": "missing.cpp", "arguments": ["g++", "-c", "missing.cpp"]},
            {"directory": "/foreign", "file": "bad.cpp", "arguments": "not-an-array"},
        ])
        value = self.prepare(compile_db=db)
        self.assertEqual([r["status"] for r in value["compile_contexts"]], ["ambiguous", "unlocated", "invalid"])
        self.assertIsNone(value["normalized_compile_db"])
        mapped = self.prepare(compile_db=db, path_maps=[{"from": "/foreign", "to": str(self.source / "src/optimizer")}])
        self.assertEqual(mapped["compile_contexts"][0]["mapping_method"], "explicit_path_map")
        self.assertEqual(mapped["summary"]["mapped_contexts"], 1)

    def test_malformed_input_is_actionable_and_no_inputs_is_valid(self):
        self.assertEqual(self.prepare()["summary"]["compile_contexts"], 0)
        for value in ("{}", "[broken"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):self.prepare(compile_db=self.write("compile.json", value))
        with self.assertRaisesRegex(ValueError, "name column"):
            self.prepare(features=self.write("bad.csv", "foo,bar\na,b\n"))

    def test_feature_and_compile_originals_are_freezable_documents(self):
        feature = self.write("features.csv", "name\nSQLPatch\n")
        db = self.write("compile_commands.json", [{"directory": str(self.source), "file": "src/optimizer/cost.cpp", "arguments": ["g++", "-c", "src/optimizer/cost.cpp"]}])
        value = self.prepare(features=feature, compile_db=db)
        with Store(self.root / "knowledge") as store:
            snapshot = materials.ingest(store, {"repositories": [{"id": "server", "root": str(self.source)}], "materials": value["materials"]})
            docs = [r for r in snapshot["assets"] if r["kind"] == "document"]
            self.assertEqual(len(docs), 2)
            self.assertTrue(all(r.get("text_sha") and not r.get("extraction_error") for r in docs))
            self.assertEqual({r["material_kind"] for r in docs}, {"feature_catalog", "build_context"})

    def test_html_navigation_omitted_but_main_and_nested_paragraphs_remain(self):
        html = b'<html><body><aside><div>Sidebar feature</div></aside><nav><p>Nav</p></nav><main><h1>Real feature</h1><p>First <b>important</b> paragraph.</p><div>Second</div></main><footer>Footer</footer><script>unsafe()</script><p>Last</p></body></html>'
        text, _, _ = materials.extract(html, ".html")
        for item in ("Real feature", "First important paragraph.", "Second", "Last"):self.assertIn(item, text)
        for item in ("Sidebar", "Nav", "Footer", "unsafe"):self.assertNotIn(item, text)
        void = b'<aside><input type="text"><br>skip</aside><article><p>keep</p></article>'
        self.assertIn("keep", materials.extract(void, ".html")[0])

    def test_worktree_git_file_is_recorded_as_explicit_exclusion(self):
        (self.source / ".git").write_text("gitdir: /a/private/path\n", encoding="utf8")
        found = {p.relative_to(self.source).as_posix(): reason for p, reason in materials.walk(self.source)}
        self.assertEqual(found[".git"], "tool_metadata_file")
        with Store(self.root / "knowledge") as store:
            snap = materials.ingest(store, {"repositories": [{"id": "server", "root": str(self.source)}]})
            meta = next(r for r in snap["assets"] if r["key"] == "server/.git")
            self.assertEqual(meta["status"], "excluded")
            self.assertIsNone(meta["sha"])


if __name__ == "__main__":unittest.main()
