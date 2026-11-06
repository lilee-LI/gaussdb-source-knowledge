"""Build the offline ZIP from the exact files in a Git revision or index."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.0.0"


def package(output):
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
    if (
        not {"README.md", "kb.cmd", "scripts/unified_kb.py", "docs/DESIGN.md"}
        <= files.keys()
    ):
        raise ValueError("Stage the release sources first")
    # Read canonical Git bytes. A Windows checkout's line endings never affect archive hashes.
    from tempfile import TemporaryDirectory

    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as tmp:
        built = Path(tmp) / "release.zip"
        manifest = {
            "schema": "gaussdb-source-knowledge-release/v2",
            "version": VERSION,
            "files": {},
        }
        prefix = "gaussdb-source-knowledge-" + VERSION + "/"

        def write(archive, name, raw):
            info = zipfile.ZipInfo(prefix + name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if name.endswith(".sh") else 0o100644) << 16
            archive.writestr(info, raw)

        with zipfile.ZipFile(built, "w") as archive:
            for name, oid in sorted(files.items()):
                raw = subprocess.check_output(
                    ["git", "cat-file", "blob", oid], cwd=ROOT
                )
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
    print(json.dumps(package(p.parse_args().out)))
