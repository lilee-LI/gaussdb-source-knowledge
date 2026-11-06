"""Check every distributed file before installing an offline release."""

import hashlib
import json
from pathlib import Path


def verify(package, *, allow_local_runtime=False):
    root = Path(package).resolve()
    manifest = root / "BUILD-MANIFEST.json"
    if not manifest.exists():
        if (root / ".git").exists() and (root / "scripts/package_release.py").is_file():
            return {"manifest_sha256": None, "source": "working_copy"}
        raise ValueError(
            "Missing release manifest; use a Git checkout or the complete offline ZIP."
        )
    content = json.loads(manifest.read_bytes())
    for name, item in content["files"].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path.is_symlink():
            raise ValueError("Missing or invalid release member: " + name)
        if (
            path.stat().st_size != item["bytes"]
            or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]
        ):
            raise ValueError("Release file differs: " + name)
    import os

    actual = set()
    for parent, folders, names in os.walk(root):
        rel = Path(parent).relative_to(root)
        folders[:] = [
            d
            for d in folders
            if not (
                allow_local_runtime
                and (
                    d == "__pycache__"
                    or (not rel.parts and d in {".venv", "local", "state"})
                )
            )
        ]
        actual.update((rel / n).as_posix() for n in names)
    if actual != set(content["files"]) | {"BUILD-MANIFEST.json"}:
        raise ValueError(
            "Unexpected files in release directory; keep workspaces outside the installation."
        )
    return {
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "source": "release",
    }
