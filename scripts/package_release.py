"""Build an offline ZIP from the Git index or an explicitly selected working tree."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
from unified_knowledge import __version__ as VERSION


def package(output, *, source="index", include=()):
    if source not in {"index","working-tree"}:
        raise ValueError("Choose index or working-tree source")
    if include and source!="working-tree":
        raise ValueError("Explicit extra files require --source working-tree")
    listing = subprocess.check_output(["git", "ls-files", "--stage", "-z"], cwd=ROOT)
    files = {}
    for record in listing.split(b"\0"):
        if not record:
            continue
        meta, name = record.split(b"\t", 1)
        mode, sha, stage = meta.split()
        path = name.decode("utf-8")
        if stage != b"0" or mode not in {b"100644", b"100755"}:
            raise ValueError(
                "Only regular tracked files in a resolved index are supported"
            )
        if path in {".gitignore", ".gitattributes"}:
            continue
        files[path] = sha.decode("ascii")
    for name in include:
        relative=Path(name)
        path=(ROOT/relative).resolve()
        allowed=(relative.parts and relative.parts[0] in {"scripts","tests","docs","adapters","assets","references","skills","engine"}) or (len(relative.parts)==1 and relative.suffix==".md")
        if relative.is_absolute() or ".." in relative.parts or not allowed or not path.is_relative_to(ROOT.resolve()) or not path.is_file() or (ROOT/relative).is_symlink():
            raise ValueError("Invalid explicit release source: "+name)
        files[relative.as_posix()]=None
    if (
        not {"README.md", "kb.cmd", "scripts/unified_kb.py", "docs/DESIGN.md"}
        <= files.keys()
    ):
        raise ValueError("Stage the release sources first")
    # Read canonical Git bytes. A Windows checkout's line endings never affect archive hashes.
    from tempfile import TemporaryDirectory

    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    head=subprocess.run(["git","rev-parse","--verify","HEAD"],cwd=ROOT,capture_output=True,text=True)
    with TemporaryDirectory(dir=output.parent) as tmp:
        if not Path(tmp).resolve().is_relative_to(output.parent):
            raise ValueError("Temporary output escaped the release directory")
        built = Path(tmp) / "release.zip"
        manifest = {
            "schema": "gaussdb-source-knowledge-release/v2",
            "version": VERSION,
            "files": {},
            "source_mode": source,
            "git_head": head.stdout.strip() if head.returncode==0 else None,
            "release_status": "working_tree_candidate" if source=="working-tree" else "index_snapshot",
        }
        prefix = "gaussdb-source-knowledge-" + VERSION + "/"

        def write(archive, name, raw):
            info = zipfile.ZipInfo(prefix + name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if name.endswith(".sh") else 0o100644) << 16
            archive.writestr(info, raw)

        with zipfile.ZipFile(built, "w") as archive:
            for name, oid in sorted(files.items()):
                if source=="working-tree":
                    path=(ROOT/name).resolve()
                    if not path.is_relative_to(ROOT.resolve()) or not path.is_file() or (ROOT/name).is_symlink():
                        raise ValueError("Invalid working-tree release source: "+name)
                    raw=path.read_bytes()
                    if name.endswith(".sh"):
                        raw=raw.replace(b"\r\n",b"\n")
                else:
                    raw = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)
                manifest["files"][name] = {
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "bytes": len(raw),
                }
                write(archive, name, raw)
            write(
                archive,
                "BUILD-MANIFEST.json",
                (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode(),
            )
        built.replace(output)
    checksum = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(".zip.sha256").write_text(
        checksum + "  " + output.name + "\n", encoding="ascii"
    )
    return {"path": str(output), "sha256": checksum, "files": len(files) + 1}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--out",
        type=Path,
        default=ROOT / "dist" / ("gaussdb-source-knowledge-" + VERSION + ".zip"),
    )
    p.add_argument("--source",choices=("index","working-tree"),default="index",help="working-tree includes tested tracked edits without staging or changing the Git index")
    p.add_argument("--include",action="append",default=[],help="Explicit new source/document file; never automatically includes untracked runtime or credentials")
    args=p.parse_args()
    print(json.dumps(package(args.out,source=args.source,include=args.include)))
