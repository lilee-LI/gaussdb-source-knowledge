"""Capture real build invocations and prepare their arguments for a Linux libclang."""

from collections import Counter
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile

from .materials import _compile_entry
from .store import atomic_write, canonical, digest, require


def capture(args):
    source, output = args.source.resolve(), args.output.resolve()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    require(
        source.is_dir() and command,
        "Use capture --source DIR --output FILE -- <actual build command>",
    )
    require(not output.exists(), "Choose a new compile database path")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="gausskb-capture-") as temp:
        work = Path(temp)
        records, wrappers = work / "records", work / "bin"
        records.mkdir()
        wrappers.mkdir()
        drivers = {}
        for name in {
            "cc",
            "c++",
            "gcc",
            "g++",
            "clang",
            "clang++",
            Path(args.cc).name,
            Path(args.cxx).name,
        }:
            binary = shutil.which(name)
            if binary:
                drivers[name] = binary
        for alias, requested in (("cc", args.cc), ("c++", args.cxx)):
            binary = shutil.which(requested)
            require(binary, "Cannot locate build compiler: " + requested)
            drivers[alias] = drivers[Path(requested).name] = binary
        shim = Path(__file__).resolve().parents[1] / "capture_compiler.py"
        for name in drivers:
            dst = wrappers / name
            shutil.copyfile(shim, dst)
            dst.chmod(0o755)
        config = work / "capture.json"
        config.write_text(
            canonical({"records": str(records), "drivers": drivers}), encoding="utf-8"
        )
        env = dict(
            os.environ,
            PATH=str(wrappers) + os.pathsep + os.environ["PATH"],
            CC="cc",
            CXX="c++",
            GAUSSKB_CAPTURE_CONFIG=str(config),
        )
        subprocess.run(command, cwd=source, env=env, stdout=sys.stderr, check=True)
        unique = {}
        for file in records.glob("*.json"):
            item = json.loads(file.read_bytes())
            if (
                (Path(item["directory"]) / item["file"])
                .resolve()
                .is_relative_to(source)
            ):
                unique[canonical(item)] = item
        require(
            unique,
            "Build invoked no intercepted C/C++ compilation. Force the build target to recompile; absolute compiler paths need CMake export or Bear.",
        )
        atomic_write(output, json.dumps([unique[k] for k in sorted(unique)], indent=2))
    return {"compile_commands": str(output), "entries": len(unique)}


def expand(args, directory, seen=()):
    for arg in args:
        if not arg.startswith("@"):
            yield arg
            continue
        path = (directory / arg[1:]).resolve()
        require(
            path not in seen and len(seen) < 16,
            "Recursive compiler response file: " + str(path),
        )
        yield from expand(
            shlex.split(path.read_text(encoding="utf-8")), directory, (*seen, path)
        )


def system_paths(driver, language):
    exe = shutil.which(driver)
    require(exe, "Build compiler missing: " + driver)
    cmd = [exe, "-E", "-v", "-x", language, "-"]
    out = subprocess.run(
        cmd,
        input="",
        capture_output=True,
        text=True,
        errors="replace",
        timeout=20,
        env=dict(os.environ, LC_ALL="C"),
    )
    require(
        out.returncode == 0,
        "Cannot run build compiler "
        + driver
        + ". Load its normal build environment. "
        + out.stderr[-600:],
    )
    block = out.stderr.partition("#include <...> search starts here:")[2].partition(
        "End of search list."
    )[0]
    require(
        block.strip(),
        "Cannot discover system includes with "
        + driver
        + "; supply --no-driver-includes and explicit -isystem paths",
    )
    return [
        str(p.resolve()) for l in block.splitlines() if (p := Path(l.strip())).is_dir()
    ]


def prepare(args, work):
    """Preserve the original digest and record every omitted code-generation option."""
    raw = args.compile_db.read_bytes()
    entries = json.loads(raw.decode("utf-8-sig"))
    require(
        isinstance(entries, list) and entries,
        "compile_commands.json must be a nonempty JSON array",
    )
    root = args.source.resolve()
    rows, invalid, supported, omitted = [], [], {}, Counter()
    codegen = {
        "-fno-aggressive-loop-optimizations",
        "-freg-struct-return",
        "-fno-expensive-optimizations",
        *args.drop_arg,
    }
    resource = Path(sys.prefix) / "clang-resource"
    require(
        (resource / "include/stddef.h").is_file(), "Run the producer through sh ecs.sh"
    )
    for n, item in enumerate(entries):
        try:
            entry = _compile_entry(item, root)
            directory = Path(entry["directory"])
            require(directory.is_dir(), "Compile directory missing: " + str(directory))
            require((root / entry["file"]).is_file(), "TU missing from source checkout")
            argv = list(expand(entry["arguments"], directory))
            require(argv, "Empty compiler argv")
            cleaned = []
            for arg in argv:
                if arg in codegen:
                    omitted[arg] += 1
                else:
                    cleaned.append(arg)
            driver_idx = int(Path(cleaned[0]).name in {"ccache", "sccache", "distcc"})
            cpp = (
                Path(entry["file"]).suffix != ".c"
                or "++" in Path(cleaned[driver_idx]).name
            )
            if "-x" in cleaned:
                cpp = "++" in cleaned[cleaned.index("-x") + 1]
            flags = [*cleaned, *args.extra_arg]
            additions = []
            if not any(a.startswith("-resource-dir") for a in flags):
                additions.extend(["-resource-dir", str(resource)])
            explicit = any(
                a
                in {
                    "-nostdinc",
                    "-nostdinc++",
                    "-m32",
                    "-mx32",
                    "-target",
                    "-isysroot",
                    "--sysroot",
                }
                or a.startswith(("--target=", "--sysroot="))
                for a in flags
            )
            if not args.no_driver_includes and not explicit:
                language = "c++" if cpp else "c"
                if language not in supported:
                    supported[language] = system_paths(
                        args.cxx if cpp else args.cc, language
                    )
                # libstdc++ uses include_next to reach libc. Keep the build driver's actual order.
                if cpp:
                    additions.append("-nostdinc++")
                for path in supported[language]:
                    if "/lib/gcc/" in path and path.endswith("/include"):
                        path = str(resource / "include")
                    additions.extend(["-isystem", path])
            rows.append(
                {
                    **entry,
                    "file": str(root / entry["file"]),
                    "arguments": flags + additions,
                }
            )
        except (ValueError, OSError, IndexError, TypeError) as exc:
            invalid.append(
                {
                    "entry": n,
                    "file": item.get("file") if isinstance(item, dict) else None,
                    "reason": str(exc),
                }
            )
    require(
        rows,
        "No usable compile commands. Check this ECS checkout and working directories: "
        + str(invalid[:3]),
    )
    serialized = canonical(rows)
    adapted = work / "commands" / (digest(serialized.encode()) + ".json")
    if not adapted.exists():
        atomic_write(adapted, serialized)
    return adapted, {
        "input_sha256": digest(raw),
        "entries": len(entries),
        "invalid": invalid,
        "system_include_paths": supported,
        "dropped_arguments": dict(omitted),
        "extra_arguments": args.extra_arg,
    }
