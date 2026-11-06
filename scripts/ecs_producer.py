"""Build the version-bound ECS graph from a real Linux compilation database."""

import argparse
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile

from unified_knowledge.compile_db import capture, prepare
from unified_knowledge.store import SCHEMA, Store, atomic_write, require


def sha256(path):
    value = hashlib.sha256()
    with path.open("rb") as file:
        for buf in iter(lambda: file.read(1024 * 1024), b""):
            value.update(buf)
    return value.hexdigest()


def export(store, snapshot, run, args, adaptation):
    from unified_knowledge.graph_mount import inspect_input

    dest = args.output.resolve()
    require(
        not dest.exists(),
        "Output already exists; keep sealed deliveries and choose a new --output",
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=dest.parent, prefix=".handoff-") as staging:
        delivery = Path(staging) / "delivery"
        delivery.mkdir()
        file = delivery / "knowledge.sqlite3"
        sid, rid = snapshot["id"], run["id"]
        with closing(sqlite3.connect(file.as_uri() + "?mode=rwc", uri=True)) as db:
            db.executescript(SCHEMA)
            db.execute(
                "ATTACH DATABASE ? AS producer",
                ((store.home / "knowledge.sqlite3").as_uri() + "?mode=ro",),
            )
            with db:
                for table, field, key in (
                    ("snapshots", "id", sid),
                    ("profiles", "snapshot", sid),
                    ("assets", "snapshot", sid),
                    ("runs", "id", rid),
                    ("symbols", "run", rid),
                    ("relations", "run", rid),
                ):
                    db.execute(
                        "INSERT INTO main."
                        + table
                        + " SELECT * FROM producer."
                        + table
                        + " WHERE "
                        + field
                        + "=?",
                        (key,),
                    )
                db.execute("CREATE TEMP TABLE refs(id TEXT PRIMARY KEY) WITHOUT ROWID")
                for table in ("symbols", "relations"):
                    db.execute(
                        "INSERT OR IGNORE INTO refs SELECT json_extract(data,'$.evidence') FROM main."
                        + table
                    )
                db.execute(
                    "INSERT INTO main.anchors SELECT a.* FROM refs JOIN producer.anchors a ON a.id=refs.id"
                )
                require(
                    db.execute("SELECT count(*) FROM anchors").fetchone()
                    == db.execute("SELECT count(*) FROM refs").fetchone(),
                    "Exported graph contains an unavailable source anchor",
                )
            require(
                db.execute("PRAGMA quick_check").fetchone()[0] == "ok",
                "SQLite handoff failed integrity check",
            )
        inspect_input(file, rid, check_indexes=True)
        tracked = set()
        git = subprocess.run(
            ["git", "-C", str(args.source), "ls-files", "-z", "--", "."],
            capture_output=True,
        )
        if git.returncode == 0:
            tracked = set(os.fsdecode(git.stdout).split("\0"))
        extra = 0
        observed = set(run["evidence_assets"])
        for asset in snapshot["assets"]:
            if (
                asset["key"] not in observed
                or asset["status"] != "frozen"
                or (asset["path"] in tracked and not asset.get("link_target"))
            ):
                continue
            sha = asset["sha"]
            target = delivery / "blobs" / sha[:2] / sha
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(store.blob_path(sha), target)
                extra += 1
        info = {
            "schema": "gausskb-ecs-handoff/v1",
            "run_id": rid,
            "snapshot": sid,
            "profile": run["profile"],
            "graph": "knowledge.sqlite3",
            "bytes": file.stat().st_size,
            "sha256": sha256(file),
            "facts": run["native_facts"],
            "facts_digest": run["facts_digest"],
            "status": run["status"],
            "coverage": run["coverage"],
            "generated_or_untracked_blobs": extra,
            "compile_database": adaptation,
            "tu_results": run["tu_results"],
        }
        atomic_write(
            delivery / "run.json", json.dumps(info, ensure_ascii=False, indent=2)
        )
        delivery.rename(dest)
    return {
        k: info[k] for k in ("run_id", "status", "facts", "bytes", "sha256", "coverage")
    } | {"output": str(dest)}


def progress(done, total, asset, status):
    if done == 1 or done == total or done % 25 == 0 or status != "parsed":
        print(f"[{done}/{total}] {status} {asset}", file=sys.stderr, flush=True)


def build(args):
    import fcntl
    from unified_knowledge.indexer import build_index
    from unified_knowledge.materials import ingest

    source, work, dest = (
        args.source.resolve(),
        args.work.resolve(),
        args.output.resolve(),
    )
    require(
        source.is_dir() and args.compile_db.is_file(),
        "Provide the ECS checkout and its compile_commands.json",
    )
    require(
        not dest.exists(), "Choose a new --output directory for this sealed delivery"
    )
    for a, b in ((source, work), (source, dest), (work, dest)):
        require(
            not a.is_relative_to(b) and not b.is_relative_to(a),
            "Source, work and delivery must be separate directories",
        )
    require(
        1 <= args.jobs <= 128 and args.timeout > 0,
        "Use --jobs 1..128 and a positive --timeout",
    )
    work.mkdir(parents=True, exist_ok=True)
    with (work / ".producer.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("Another producer owns this work directory") from None
        adapted, audit = prepare(args, work)
        require(
            not audit["invalid"] or args.allow_partial,
            "Invalid compile entries, first examples: " + str(audit["invalid"][:3]),
        )
        selected = []
        for requested in args.tu:
            file = (source / requested).resolve()
            require(
                file.is_relative_to(source),
                "Selected TU is outside the checkout: " + requested,
            )
            selected.append(file.relative_to(source).as_posix())
        print("Freezing code and build inputs ...", file=sys.stderr, flush=True)
        cfg = {
            "product": "GaussDB",
            "repositories": [
                {
                    "id": "server",
                    "root": str(source),
                    "native_sources": True,
                    "additional_files": args.include_file,
                }
            ],
            "profiles": [
                {
                    "id": args.profile,
                    "repository": "server",
                    "compile_commands": str(adapted),
                    "toolchain": audit,
                }
            ],
        }
        with Store(work) as store:
            require(not store.graph_path, "Use a dedicated ECS work directory")
            snapshot = ingest(store, cfg)
            run = build_index(
                store,
                snapshot["id"],
                args.profile,
                timeout=args.timeout,
                jobs=args.jobs,
                resume=True,
                files=selected or None,
                native_facts=args.facts,
                progress=progress,
                owns_producer_lock=True,
            )
            problems = [r for r in run["tu_results"] if r["status"] != "parsed"]
            summary = {
                "run_id": run["id"],
                "coverage": run["coverage"],
                "compile_database": audit,
                "tu_results": run["tu_results"],
            }
            atomic_write(
                work / "last-build.json",
                json.dumps(summary, ensure_ascii=False, indent=2),
            )
            require(
                run["coverage"]["parsed_tus"] > 0
                and (not problems or args.allow_partial),
                "Build has incomplete TUs. Inspect "
                + str(work / "last-build.json")
                + " and fix flags/includes; --allow-partial permits a delivery with at least one clean TU.",
            )
            return export(store, snapshot, run, args, audit)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    actions = p.add_subparsers(dest="action", required=True)
    actions.add_parser("doctor", help="Verify the offline Linux frontend and SQLite")
    scan = actions.add_parser(
        "capture", help="Capture an actual Make/GCC or Clang build"
    )
    make = actions.add_parser(
        "build", help="Parse TUs in parallel and produce a Windows-ready delivery"
    )
    for cmd in (scan, make):
        cmd.add_argument("--source", type=Path, required=True)
        cmd.add_argument("--output", type=Path, required=True)
        cmd.add_argument("--cc", default="cc")
        cmd.add_argument("--cxx", default="c++")
    scan.add_argument("command", nargs=argparse.REMAINDER)
    make.add_argument("--compile-db", type=Path, required=True)
    make.add_argument("--work", type=Path, required=True)
    make.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1))
    make.add_argument("--timeout", type=int, default=300, help="Seconds per TU")
    make.add_argument("--profile", default="linux-native")
    make.add_argument(
        "--tu",
        action="append",
        default=[],
        help="One repo-relative TU; repeat for a pilot, omit for the whole database",
    )
    make.add_argument("--facts", choices=["calls", "full"], default="calls")
    make.add_argument("--extra-arg", action="append", default=[])
    make.add_argument("--drop-arg", action="append", default=[])
    make.add_argument("--no-driver-includes", action="store_true")
    make.add_argument("--allow-partial", action="store_true")
    make.add_argument(
        "--include-file",
        action="append",
        default=[],
        help="Additional repository-relative header with a nonstandard suffix",
    )
    args = p.parse_args()
    if args.action == "doctor":
        import importlib.metadata
        from clang.cindex import Index

        Index.create()
        with closing(sqlite3.connect(":memory:")) as db:
            db.execute("SELECT json_extract('{}','$.ok')")
        result = {
            "status": "ready",
            "python": sys.version.split()[0],
            "libclang": importlib.metadata.version("libclang"),
            "sqlite": sqlite3.sqlite_version,
            "git": shutil.which("git"),
            "compiler": shutil.which("c++"),
        }
    else:
        result = capture(args) if args.action == "capture" else build(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
