"""Install the Linux producer offline, independently of the learning environment."""

import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import venv

from verify_unified_bundle import verify


def install(root):
    if sys.platform != "linux" or sys.version_info < (3, 9):
        raise ValueError(
            "ECS requires Linux, Python 3.9 or newer with venv/ensurepip, and Git"
        )
    arch = {"x86_64": "x64", "aarch64": "arm64"}.get(platform.machine())
    if not arch or not shutil.which("git"):
        raise ValueError("Provide Linux x86_64/aarch64 with Git on PATH")
    wheels = root / "wheels" / ("ecs-linux-" + arch)
    resource = root / "wheels/ecs-resource/clang18-headers.tar.xz"
    target = root / ".venv-ecs"
    python = target / "bin/python"
    stamp = target / ".installed.json"
    local = root / "local"
    local.mkdir(exist_ok=True)
    with (local / "ecs-install.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        version = [
            arch,
            sys.version.split()[0],
            hashlib.sha256((wheels / "requirements.lock").read_bytes()).hexdigest(),
            hashlib.sha256(resource.read_bytes()).hexdigest(),
        ]
        if (
            stamp.is_file()
            and python.is_file()
            and json.loads(stamp.read_bytes()) == version
        ):
            return
        verify(root, allow_local_runtime=True)
        venv.EnvBuilder(with_pip=True).create(target)
        subprocess.run(
            [
                str(python),
                "-I",
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-index",
                "--only-binary=:all:",
                "--require-hashes",
                "--find-links",
                str(wheels),
                "-r",
                str(wheels / "requirements.lock"),
            ],
            check=True,
        )
        dest = target / "clang-resource"
        with tarfile.open(resource, "r:xz") as tar:
            for entry in tar:
                path = (dest / entry.name).resolve()
                if (
                    not entry.isfile()
                    or not path.is_relative_to(dest)
                    or not entry.name.startswith("include/")
                ):
                    raise ValueError("Unexpected resource header: " + entry.name)
                path.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(entry) as reader, path.open("wb") as writer:
                    shutil.copyfileobj(reader, writer)
        subprocess.run(
            [str(python), "-I", "-c", "from clang.cindex import Index; Index.create()"],
            check=True,
        )
        temporary = stamp.with_suffix(".tmp")
        temporary.write_text(json.dumps(version), encoding="utf-8")
        os.replace(temporary, stamp)


if __name__ == "__main__":
    install(Path(sys.argv[1]).resolve())
