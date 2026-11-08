"""Complete internal knowledge snapshots, integrity verification and activation."""
from __future__ import annotations

from html import escape
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess

from .knowledge import freshness, knowledge_files, knowledge_graph
from .store import Store, atomic_write, canonical, digest, identity, now, require


def file_sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()


def status(store, *, run=None):
    result = {"schema": "unified-status/v1", "source_snapshot": store.get_meta("snapshot_head"),
              "knowledge_revision": store.get_meta("knowledge_head"), "active_release": store.get_meta("active_release"),
              "database_execution": "not_run", "automatic_semantic_approval": False}
    result["counts"] = {table: store.db.execute("SELECT count(*) FROM main." + table).fetchone()[0]
                        for table in ("snapshots", "assets", "runs", "symbols", "relations", "tasks", "revisions")}
    if store.graph_path:
        # Imported graph counts are upper-run metadata, never scan a multi-GB input just to display status.
        result["referenced_graphs"] = [dict(r) for r in store.db.execute("SELECT b.study,b.upstream,"
            "json_extract(r.data,'$.coverage.symbols') symbols,json_extract(r.data,'$.coverage.relations') relations "
            "FROM graph_bindings b JOIN main.runs r ON r.id=b.study")]
        result["counts_scope"] = "local_tables"
    where, args = (" WHERE run=?", (run,)) if run else ("", ())
    result["tasks"] = dict(store.db.execute("SELECT status,count(*) FROM tasks" + where + " GROUP BY status", args))
    if run:
        record = store.record("runs", run)
        result["index"] = record
        ownership = store.get_meta("ownership:" + run, [])
        result["ownership"] = {"assets": len(ownership), "unassigned": sum(x["owner"] is None for x in ownership)}
    return result


def doctor(store, *, repair_git=False, verify_blobs=False):
    import importlib.metadata
    result = {"schema": "unified-doctor/v1", "database_integrity": store.db.execute("PRAGMA integrity_check").fetchone()[0],
              "sqlite_fts5": store.fts, "source_only": True, "checks": [], "optional_dependencies": {}}
    packages = ("networkx", "pypdf") if (Path(__file__).resolve().parents[2]/"ECS-EDITION").is_file() else ("libclang", "tree-sitter", "tree-sitter-cpp", "pypdf", "networkx")
    for package in packages:
        try:
            result["optional_dependencies"][package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            result["optional_dependencies"][package] = "unavailable"
    head = store.get_meta("knowledge_head")
    if head:
        revision = store.record("revisions", head)
        units = store.units(head)
        result["checks"].append({"name": "unit_hashes", "passed": bool(units)})
        directory = store.home / "revisions" / head.replace(":", "-")
        files_ok = all((directory / path).is_file() and digest((directory / path).read_bytes()) == sha
                       for path, sha in revision["files"].items())
        if (store.home / "release.json").exists():
            # Published bundles use wiki/ for the formal readable projection.
            files_ok = all((store.home / "wiki" / path).is_file() and digest((store.home / "wiki" / path).read_bytes()) == sha
                           for path, sha in revision["files"].items())
        result["checks"].append({"name": "wiki_files", "passed": files_ok})
        if not store.readonly:
            git_dir = store.home / "wiki.git"
            proc = subprocess.run(["git", "--git-dir", str(git_dir), "rev-parse", "refs/heads/knowledge"],
                                  capture_output=True, timeout=30)
            actual = proc.stdout.decode().strip() if proc.returncode == 0 else None
            expected = revision["git_commit"]
            if actual != expected and repair_git:
                proc = subprocess.run(["git", "--git-dir", str(git_dir), "update-ref", "refs/heads/knowledge", expected],
                                      capture_output=True, timeout=30)
                require(proc.returncode == 0, "Cannot repair Git mirror")
                actual = expected
            result["checks"].append({"name": "git_mirror", "passed": actual == expected})
    if verify_blobs:
        count = 0
        for p in (store.home / "blobs").glob("*/*"):
            require(p.is_file() and digest(p.read_bytes()) == p.name, "Frozen material corruption: " + p.name)
            count += 1
        result["checks"].append({"name": "blob_hashes", "passed": True, "files": count})
    result["passed"] = result["database_integrity"] == "ok" and all(c["passed"] for c in result["checks"])
    return result


def _reader(units, stale):
    sections = []
    for uid, unit in sorted(units.items()):
        mark = "待核：依赖已变化" if uid in stale else unit["review"]["mode"]
        sections.append('<article id="' + digest(uid)[:24] + '"><h2>' + escape(unit["title"]) +
                        '</h2><p class="meta">' + escape(unit["kind"] + " · " + mark) + '</p><pre>' +
                        escape(unit["body"]) + '</pre><h3>适用条件</h3><pre>' +
                        escape(canonical(unit.get("conditions", []))) + '</pre><details><summary>证据与接口</summary><pre>' +
                        escape(json.dumps(unit, ensure_ascii=False, indent=2)) + '</pre></details></article>')
    return ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            '<title>Wiki 与源码分析统一知识库</title><style>body{max-width:1100px;margin:40px auto;padding:0 24px;'
            'font:16px/1.6 system-ui,"Microsoft YaHei",sans-serif;color:#172033}article{padding:22px 0;border-top:1px solid #d6dce5}'
            'pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f8;padding:14px}.meta{color:#596577}</style>'
            '<h1>Wiki 与源码分析统一知识库</h1><p>本包为内部统一知识快照，包含源码证据。运行验证另记；待核条目不作为当前结论。</p>'
            + "".join(sections) + '</html>')


def publish(store, output, *, revision=None, allow_partial=False):
    output = Path(output).expanduser().resolve()
    require(not output.exists(), "Release output must be a new directory")
    require(not output.is_relative_to(store.home) and not store.home.is_relative_to(output),
            "Release directory must be separate from workspace")
    revision = revision or store.get_meta("knowledge_head")
    require(revision, "No accepted knowledge to publish")
    record = store.record("revisions", revision)
    units = store.units(revision)
    require(units, "Cannot publish empty knowledge")
    require(doctor(store)["passed"], "Workspace integrity/Git mirror check failed")
    index = store.record("runs", record["run"])
    from . import whole
    program=whole.current(store,False)
    coverage=whole.audit(store) if program else None
    require(allow_partial or not coverage or coverage['status']=='accepted','Whole-repository coverage is not accepted; inspect coverage, or explicitly publish a partial scope with --allow-partial')
    stale = {uid: reasons for uid, unit in units.items()
             if (reasons := freshness(store, unit, record["snapshot"], record["run"], units))}
    tasks = dict(store.db.execute("SELECT status,count(*) FROM tasks WHERE run=? GROUP BY status", (record["run"],)))
    partial = bool(stale or index["status"] != "ready" or any(k != "accepted" and v for k, v in tasks.items()) or coverage and coverage['status']!='accepted')
    require(allow_partial or not partial, "Scope has pending knowledge/index/tasks; explicit allow_partial is required")
    output.mkdir(parents=True)
    try:
        with store.transaction():
            # A second connection backs up a committed WAL snapshot while the
            # controller holds a writer lease. No inconsistent file-copy of SQLite.
            source = sqlite3.connect(store.home / "knowledge.sqlite3", timeout=30)
            destination = sqlite3.connect(output / "knowledge.sqlite3")
            try:
                source.backup(destination)
                destination.execute("PRAGMA journal_mode=DELETE")
                if store.graph_path:
                    graph_dir = output/"source-index"
                    graph_dir.mkdir()
                    from contextlib import closing
                    from .graph_mount import readonly_uri
                    with closing(sqlite3.connect(readonly_uri(store.graph_path),uri=True)) as upstream, \
                         closing(sqlite3.connect(graph_dir/"knowledge.sqlite3")) as frozen:
                        upstream.backup(frozen)
                        frozen.execute("PRAGMA journal_mode=DELETE")
                    destination.execute("UPDATE meta SET value=? WHERE key='external_graph'",(canonical("source-index/knowledge.sqlite3"),))
                destination.execute("INSERT OR REPLACE INTO meta VALUES('knowledge_head',?)", (canonical(revision),))
                destination.execute("INSERT OR REPLACE INTO meta VALUES('snapshot_head',?)", (canonical(record["snapshot"]),))
                destination.commit()
            finally:
                source.close()
                destination.close()
            # All content-addressed material remains available for history and
            # source-level read/graph queries. Build caches and credentials are excluded.
            if (store.home / "blobs").is_dir():
                for p in (store.home / "blobs").glob("*/*"):
                    require(p.is_file() and digest(p.read_bytes()) == p.name, "Blob integrity failure")
                    atomic_write(output / "blobs" / p.parent.name / p.name, p.read_bytes())
            files = knowledge_files(units)
            for path, raw in files.items():
                atomic_write(output / "wiki" / path, raw)
            atomic_write(output / "index.html", _reader(units, stale))
            atomic_write(output / "knowledge-graph.json", canonical(knowledge_graph(store, revision)))
            release = {"schema": "unified-release/v1", "knowledge_revision": revision,
                       "source_snapshot": record["snapshot"], "profile": record["profile"], "index_run": record["run"],
                       "git_commit": record["git_commit"], "created": now(), "scope_status": "partial" if partial else "bounded",
                       "stale_units": stale, "tasks": tasks, "database_execution": "not_run",
                       "projection": "complete_internal_mother", "external_projection": "not_applied"}
            release["id"] = identity("release", release)
            atomic_write(output / "release.json", canonical(release))
            contents = {p.relative_to(output).as_posix(): file_sha(p) for p in sorted(output.rglob("*")) if p.is_file()}
            atomic_write(output / "CONTENTS.json", canonical({"schema": "release-manifest/v1", "files": contents}))
            store.db.execute("INSERT INTO releases VALUES(?,?,?)", (release["id"], release["created"],
                             canonical({**release, "path": str(output), "manifest_sha256": digest((output / "CONTENTS.json").read_bytes())})))
            store.event("release", {"id": release["id"], "revision": revision})
        return {**release, "path": str(output), "files": len(contents) + 1}
    except BaseException:
        # Keep any incomplete output reviewable; it never becomes active.
        atomic_write(output / "INCOMPLETE.json", canonical({"status": "failed_publication", "active": False}))
        raise


def verify(output, *, current_store=None, require_current=False):
    output = Path(output).resolve()
    manifest = json.loads((output / "CONTENTS.json").read_text(encoding="utf-8"))
    require(manifest.get("schema") == "release-manifest/v1" and isinstance(manifest.get("files"), dict), "Invalid release manifest")
    expected = set(manifest["files"]) | {"CONTENTS.json"}
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    require(actual == expected, "Release has missing or unregistered files")
    for name, sha in manifest["files"].items():
        p = (output / name).resolve()
        require(p.is_relative_to(output) and not (output / name).is_symlink(), "Invalid release file path")
        require(file_sha(p) == sha, "Release hash mismatch: " + name)
    release = json.loads((output / "release.json").read_text(encoding="utf-8"))
    with Store(output, readonly=True) as frozen:
        require(frozen.get_meta("knowledge_head") == release["knowledge_revision"], "Release knowledge binding mismatch")
        frozen.units(release["knowledge_revision"])
    current = None
    if current_store is not None:
        current = (current_store.get_meta("knowledge_head") == release["knowledge_revision"]
                   and current_store.get_meta("snapshot_head") == release["source_snapshot"])
    require(not require_current or current is True, "Release is not the current material/knowledge version")
    return {"status": "verified", "id": release["id"], "files": len(expected), "current": current,
            "scope_status": release["scope_status"], "database_execution": "not_run"}


def activate(store, output):
    verified = verify(output)
    release = json.loads((Path(output) / "release.json").read_text(encoding="utf-8"))
    require(store.db.execute("SELECT 1 FROM revisions WHERE id=?", (release["knowledge_revision"],)).fetchone(),
            "Release does not belong to this workspace")
    with store.transaction():
        store.set_meta("active_release", {"id": release["id"], "path": str(Path(output).resolve()),
                                        "knowledge_revision": release["knowledge_revision"]})
        store.event("activate_release", {"id": release["id"]})
    return verified
