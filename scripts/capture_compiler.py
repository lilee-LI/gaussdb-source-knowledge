#!/usr/bin/env python3
"""GCC/Clang compiler shim used only by the explicit ECS capture command."""

import json
import os
from pathlib import Path
import sys
import uuid


def main():
    ctx = json.loads(Path(os.environ["GAUSSKB_CAPTURE_CONFIG"]).read_bytes())
    driver = ctx["drivers"][Path(sys.argv[0]).name]
    args = sys.argv[1:]
    if "-c" in args or any(a.startswith("@") for a in args):
        # Preserve argv exactly. Response files can disappear when the build finishes.
        from shlex import split

        def expand(values, seen=()):
            for arg in values:
                if not arg.startswith("@"):
                    yield arg
                    continue
                path = Path(arg[1:]).resolve()
                if path in seen or len(seen) >= 16:
                    raise ValueError("Recursive compiler response file")
                yield from expand(
                    split(path.read_text(encoding="utf-8")), (*seen, path)
                )

        full = list(expand(args))
        if "-c" in full:
            inputs = []
            i = 0
            pairs = {
                "-o",
                "-I",
                "-include",
                "-isystem",
                "-iquote",
                "-imacros",
                "-MF",
                "-MT",
                "-MQ",
                "-x",
                "-D",
                "-U",
                "-target",
            }
            while i < len(full):
                arg = full[i]
                if arg in pairs:
                    i += 2
                    continue
                if not arg.startswith("-") and Path(arg).suffix.lower() in {
                    ".c",
                    ".cc",
                    ".cpp",
                    ".cxx",
                    ".c++",
                }:
                    inputs.append(arg)
                i += 1
            for name in inputs:
                row = {
                    "directory": str(Path.cwd()),
                    "file": name,
                    "arguments": [driver, *full],
                }
                out = Path(ctx["records"]) / (uuid.uuid4().hex + ".json")
                out.write_text(json.dumps(row), encoding="utf-8")
    os.execv(driver, [driver, *args])


if __name__ == "__main__":
    main()
