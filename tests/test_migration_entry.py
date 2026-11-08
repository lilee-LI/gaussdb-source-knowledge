"""Portable Claude entry, lease recovery and explicit working-tree packaging."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from platform_fixture import workspace
from unified_knowledge import project, service, study
from unified_knowledge.store import Store
import package_release


class MigrationEntryTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name).resolve()
        self.store,self.plan,self.unit=workspace(self.root)
        self.addCleanup(self.store.close)

    def test_mcp_lease_recovery_preserves_attempt_and_enforces_token(self):
        task=study.focus(self.store,"server/optimizer",symbol="cg_compute",question="migration lease regression")["task"]
        args={"task":task,"worker":"learner"}
        first=service.invoke(self.store,"claim_task",{**args,"seconds":60},role="researcher")
        args["token"]=first["token"]
        renewed=service.invoke(self.store,"renew_task",{**args,"seconds":14400},role="researcher")
        self.assertEqual(renewed["attempt"],first["attempt"])
        self.assertEqual(renewed["token"],first["token"])
        self.assertGreater(renewed["deadline"],first["deadline"])
        service.invoke(self.store,"checkpoint_task",{**args,"checkpoint":{"covered":["entry"],"open":["consumer"]}},role="researcher")
        with self.assertRaises(ValueError):
            service.invoke(self.store,"renew_task",{**args,"token":"wrong"},role="researcher")
        with self.assertRaisesRegex(ValueError,"unavailable"):
            service.invoke(self.store,"renew_task",args,role="query")
        released=service.invoke(self.store,"release_task",args,role="researcher")
        self.assertEqual(released["status"],"queued")
        second=service.invoke(self.store,"claim_task",{"task":task,"worker":"learner"},role="researcher")
        self.assertNotEqual(first["token"],second["token"])
        with self.assertRaises(ValueError):
            service.invoke(self.store,"renew_task",args,role="researcher")

    def test_path_entry_generates_query_config_and_concrete_prompt(self):
        paths=self.root/"paths.json"
        paths.write_text(json.dumps({"product":"GaussDB","product_adapter":"gaussdb","source":"source",
            "index_db":"input.sqlite3","home":"portable-home","graph_storage":"reference"}),encoding="utf8")
        # platform_fixture names its input consistently; assert the real path used here.
        self.assertTrue((self.root/"input.sqlite3").is_file())
        spec=project.settings(paths)
        first=project.start(spec,False)
        query=Path(first["query_mcp"])
        config=json.loads(query.read_text(encoding="utf8"))
        args=next(iter(config["mcpServers"].values()))["args"]
        self.assertEqual(args[args.index("--role")+1],"query")
        query.unlink()
        resumed=project.start(spec,False)
        self.assertEqual(resumed["plan_id"],first["plan_id"])
        self.assertTrue(query.is_file())
        with Store(Path(spec["home"]),readonly=True) as reader:
            self.assertEqual(study.current(reader)["product_adapter"]["id"],"gaussdb-centralized")
        request=argparse.Namespace(action="learn",paths=paths,candidate=None,module="server/optimizer",question="Who owns the copied buffer?",
                                  symbol="cg_compute",file=[],worker="learner")
        work=project.execute(request)
        self.assertEqual(Path(work["prompt_file"]).read_text(encoding="utf8").strip(),work["prompt"])
        self.assertIn("renew_task",work["prompt"])
        self.assertIn("expected_from",work["prompt"])
        self.assertIn(work["task"],work["prompt"])
        self.assertEqual(work["worker"],"learner")


class WorkingTreePackageTests(unittest.TestCase):
    def test_explicit_candidate_contains_current_bytes_and_leaves_git_index_unchanged(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root=Path(temp.name).resolve()
        for name in ("README.md","kb.cmd","scripts/unified_kb.py","docs/DESIGN.md","ecs.sh"):
            path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b"staged\n")
        def git(*args):
            return subprocess.check_output(["git",*args],cwd=root,stderr=subprocess.DEVNULL)
        git("init","-q");git("add",".")
        before=git("ls-files","--stage","-z")
        (root/"scripts/unified_kb.py").write_bytes(b"tested working tree\n")
        (root/"ecs.sh").write_bytes(b"#!/bin/sh\r\necho ok\r\n")
        (root/"MIGRATE.md").write_text("new migration guide",encoding="utf8")
        with patch.object(package_release,"ROOT",root):
            archive=root/"out/candidate.zip"
            package_release.package(archive,source="working-tree",include=["MIGRATE.md"])
            with zipfile.ZipFile(archive) as z:
                prefix="gaussdb-source-knowledge-"+package_release.VERSION+"/"
                self.assertEqual(z.read(prefix+"scripts/unified_kb.py"),b"tested working tree\n")
                self.assertEqual(z.read(prefix+"ecs.sh"),b"#!/bin/sh\necho ok\n")
                self.assertIn(prefix+"MIGRATE.md",z.namelist())
                manifest=json.loads(z.read(prefix+"BUILD-MANIFEST.json"))
                self.assertEqual(manifest["source_mode"],"working-tree")
                self.assertEqual(manifest["release_status"],"working_tree_candidate")
            package_release.package(root/"out/index.zip")
            with zipfile.ZipFile(root/"out/index.zip") as z:
                self.assertEqual(z.read(prefix+"scripts/unified_kb.py"),b"staged\n")
            with self.assertRaisesRegex(ValueError,"working-tree"):
                package_release.package(root/"out/invalid.zip",include=["MIGRATE.md"])
            with self.assertRaisesRegex(ValueError,"Invalid explicit"):
                package_release.package(root/"out/invalid.zip",source="working-tree",include=["../outside.md"])
        self.assertEqual(before,git("ls-files","--stage","-z"))


if __name__=="__main__":unittest.main()
