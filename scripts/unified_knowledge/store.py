"""Persistent, transaction-bound metadata and immutable content-addressed objects."""
from __future__ import annotations

import contextlib
from collections import OrderedDict
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else canonical(value).encode("utf-8")).hexdigest()


def identity(prefix, value):
    return prefix + ":" + digest(value)[:32]


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = data.encode("utf-8") if isinstance(data, str) else data
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".pending-")
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def require(condition, message):
    if not condition:
        raise ValueError(message)


SCHEMA = """
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS snapshots(id TEXT PRIMARY KEY,created TEXT NOT NULL,data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS assets(
 snapshot TEXT NOT NULL,key TEXT NOT NULL,repo TEXT NOT NULL,path TEXT NOT NULL,
 sha TEXT,kind TEXT NOT NULL,status TEXT NOT NULL,data TEXT NOT NULL,
 PRIMARY KEY(snapshot,key));
CREATE INDEX IF NOT EXISTS asset_scope ON assets(snapshot,repo,path);
CREATE TABLE IF NOT EXISTS profiles(
 snapshot TEXT NOT NULL,id TEXT NOT NULL,digest TEXT NOT NULL,data TEXT NOT NULL,
 PRIMARY KEY(snapshot,id));
CREATE TABLE IF NOT EXISTS anchors(
 id TEXT PRIMARY KEY,snapshot TEXT NOT NULL,asset TEXT NOT NULL,sha TEXT NOT NULL,
 start INTEGER NOT NULL,end INTEGER NOT NULL,data TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS anchor_asset ON anchors(snapshot,asset);
CREATE TABLE IF NOT EXISTS documents(
 snapshot TEXT NOT NULL,id TEXT NOT NULL,kind TEXT NOT NULL,asset TEXT NOT NULL,data TEXT NOT NULL,
 PRIMARY KEY(snapshot,id));
CREATE TABLE IF NOT EXISTS runs(
 id TEXT PRIMARY KEY,snapshot TEXT NOT NULL,profile TEXT NOT NULL,created TEXT NOT NULL,
 status TEXT NOT NULL,data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS graph_bindings(study TEXT PRIMARY KEY,upstream TEXT NOT NULL,snapshot TEXT NOT NULL,digest TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS symbols(
 run TEXT NOT NULL,id TEXT NOT NULL,logical TEXT NOT NULL,name TEXT NOT NULL,
 asset TEXT NOT NULL,kind TEXT NOT NULL,data TEXT NOT NULL,PRIMARY KEY(run,id));
CREATE INDEX IF NOT EXISTS symbol_logical ON symbols(run,logical);
CREATE INDEX IF NOT EXISTS symbol_name ON symbols(run,name);
CREATE INDEX IF NOT EXISTS symbol_file ON symbols(run,asset);
CREATE TABLE IF NOT EXISTS relations(
 run TEXT NOT NULL,id TEXT NOT NULL,source TEXT NOT NULL,target TEXT NOT NULL,
 kind TEXT NOT NULL,resolution TEXT NOT NULL,data TEXT NOT NULL,PRIMARY KEY(run,id));
CREATE INDEX IF NOT EXISTS relation_source ON relations(run,source,kind);
CREATE INDEX IF NOT EXISTS relation_target ON relations(run,target,kind);
CREATE TABLE IF NOT EXISTS tu_cache(key TEXT PRIMARY KEY,data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tasks(
 id TEXT PRIMARY KEY,snapshot TEXT NOT NULL,run TEXT NOT NULL,profile TEXT NOT NULL,
 kind TEXT NOT NULL,status TEXT NOT NULL,owner TEXT,token TEXT,deadline REAL,attempt INTEGER NOT NULL DEFAULT 0,
 data TEXT NOT NULL,result TEXT);
CREATE INDEX IF NOT EXISTS task_status ON tasks(snapshot,status);
CREATE INDEX IF NOT EXISTS task_run_queue ON tasks(run,status,kind,id);
CREATE INDEX IF NOT EXISTS task_plan_scope ON tasks(snapshot,json_extract(data,'$.bundle.plan_id'))
 WHERE json_extract(data,'$.bundle.plan_id') IS NOT NULL;
CREATE TABLE IF NOT EXISTS task_edges(task TEXT NOT NULL,dependency TEXT NOT NULL,
 PRIMARY KEY(task,dependency));
CREATE INDEX IF NOT EXISTS task_reverse_edge ON task_edges(dependency,task);
CREATE TABLE IF NOT EXISTS proposals(id TEXT PRIMARY KEY,created TEXT NOT NULL,status TEXT NOT NULL,data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS revisions(
 id TEXT PRIMARY KEY,parent TEXT,snapshot TEXT NOT NULL,run TEXT NOT NULL,
 profile TEXT NOT NULL,created TEXT NOT NULL,data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS unit_versions(hash TEXT PRIMARY KEY,data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS revision_units(
 revision TEXT NOT NULL,id TEXT NOT NULL,hash TEXT NOT NULL,PRIMARY KEY(revision,id));
CREATE INDEX IF NOT EXISTS unit_revision_hash ON revision_units(hash);
CREATE TABLE IF NOT EXISTS alignments(
 revision TEXT NOT NULL,unit TEXT NOT NULL,symbol TEXT,anchor TEXT,data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS vectors(
 revision TEXT NOT NULL,unit TEXT NOT NULL,space TEXT NOT NULL,data TEXT NOT NULL,
 PRIMARY KEY(revision,unit,space));
CREATE TABLE IF NOT EXISTS semantic_edges(
 revision TEXT NOT NULL,source TEXT NOT NULL,target TEXT NOT NULL,kind TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS semantic_source ON semantic_edges(revision,source);
CREATE INDEX IF NOT EXISTS semantic_target ON semantic_edges(revision,target);
CREATE TABLE IF NOT EXISTS unit_dependencies(
 revision TEXT NOT NULL,unit TEXT NOT NULL,kind TEXT NOT NULL,ref TEXT NOT NULL,fingerprint TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS dependency_lookup ON unit_dependencies(revision,kind,ref);
CREATE TABLE IF NOT EXISTS lexical_cache(hash TEXT PRIMARY KEY,text TEXT NOT NULL,vector TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS changes(id TEXT PRIMARY KEY,created TEXT NOT NULL,data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS releases(id TEXT PRIMARY KEY,created TEXT NOT NULL,data TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,created TEXT NOT NULL,
 kind TEXT NOT NULL,data TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS evidence_task ON events(kind,json_extract(data,'$.task'),
 json_extract(data,'$.worker'),json_extract(data,'$.token'));
"""


class Store:
    def __init__(self, home, *, readonly=False, graph_override=None):
        self.home = Path(home).expanduser().resolve()
        self.readonly = readonly
        self._line_cache = OrderedDict()
        self._evidence_origins = {}
        require(readonly or not (self.home / "release.json").is_file(), "Published release is read-only; queue updates in a live workspace")
        if readonly:
            require((self.home / "knowledge.sqlite3").is_file(), "Workspace database missing")
            uri = (self.home / "knowledge.sqlite3").as_uri() + "?mode=ro"
            if (self.home / "release.json").is_file():
                uri += "&immutable=1"
            self.db = sqlite3.connect(uri, uri=True, timeout=30)
        else:
            self.home.mkdir(parents=True, exist_ok=True)
            self.db = sqlite3.connect((self.home / "knowledge.sqlite3").as_uri() + "?mode=rwc", uri=True, timeout=30)
            self.db.executescript(SCHEMA)
            self.db.execute("PRAGMA journal_mode=WAL")
            self.db.execute("PRAGMA synchronous=FULL")
            self.db.commit()
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA busy_timeout=30000")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.fts = True
        if not readonly:
            try:
                self.db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS search_fts USING fts5(revision UNINDEXED,unit UNINDEXED,text)")
                self.db.commit()
            except sqlite3.OperationalError:
                self.fts = False
        else:
            self.fts = bool(self.db.execute("SELECT 1 FROM sqlite_master WHERE name='search_fts'").fetchone())

        self.graph_path = None
        location = self.get_meta("external_graph")
        if location:
            from .graph_mount import attach
            try:
                attach(self, graph_override or self.home/Path(location))
            except BaseException:
                self.db.close()
                raise

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    @contextlib.contextmanager
    def transaction(self):
        require(not self.readonly, "Read-only workspace")
        require(not self.db.in_transaction, "Nested transaction is not supported")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise

    def event(self, kind, data):
        self.db.execute("INSERT INTO events(created,kind,data) VALUES(?,?,?)", (now(), kind, canonical(data)))

    def get_meta(self, key, default=None):
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else default

    def set_meta(self, key, value):
        self.db.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (key, canonical(value)))

    def blob_path(self, sha):
        require(isinstance(sha, str) and len(sha) == 64 and all(c in "0123456789abcdef" for c in sha),
                "Invalid content digest")
        return self.home / "blobs" / sha[:2] / sha

    def put_blob(self, raw):
        sha = digest(raw)
        path = self.blob_path(sha)
        if path.exists():
            require(digest(path.read_bytes()) == sha, "Stored blob was modified")
        else:
            atomic_write(path, raw)
        return sha

    def blob(self, sha):
        raw = self.blob_path(sha).read_bytes()
        require(digest(raw) == sha, "Evidence hash mismatch")
        return raw

    def source_lines(self, sha):
        # Bounded cache is used only to create anchors during one controller
        # operation. Evidence reads and freshness checks still rehash raw blobs.
        if sha not in self._line_cache:
            self._line_cache[sha] = self.blob(sha).decode("utf-8", errors="replace").splitlines(keepends=True)
            while len(self._line_cache) > 4:
                self._line_cache.popitem(last=False)
        self._line_cache.move_to_end(sha)
        return self._line_cache[sha]

    def record(self, table, key):
        require(table in {"snapshots", "runs", "tasks", "proposals", "revisions", "changes", "releases", "anchors"},
                "Unsupported record type")
        row = self.db.execute("SELECT data FROM " + table + " WHERE id=?", (key,)).fetchone()
        require(row is not None, table + " record missing: " + str(key))
        return json.loads(row[0])

    def asset(self, snapshot, key):
        row = self.db.execute("SELECT data FROM assets WHERE snapshot=? AND key=?", (snapshot, key)).fetchone()
        require(row is not None, "Asset not present in snapshot: " + str(key))
        return json.loads(row[0])

    def lookup_symbols(self, run, term, *, names=True, assets=None, limit=None):
        # Separate B-tree seeks. An OR across these columns can scan every symbol in the run.
        found = {}
        for column in (("id","logical","name") if names else ("id","logical")):
            rows = self.db.execute("SELECT id,logical,asset,data FROM symbols WHERE run=? AND "+column+"=?", (run,term))
            for row in rows:
                if assets is None or row["asset"] in assets:
                    found[row["id"]] = row
                    if limit is not None and len(found) >= limit:
                        return list(found.values())
        return list(found.values())

    def profile(self, snapshot, profile):
        row = self.db.execute("SELECT data FROM profiles WHERE snapshot=? AND id=?", (snapshot, profile)).fetchone()
        require(row is not None, "Build profile missing: " + str(profile))
        return json.loads(row[0])

    def units(self, revision=None, ids=None):
        revision = revision or self.get_meta("knowledge_head")
        if not revision:
            return {}
        if ids is not None and not ids:
            return {}
        query = "SELECT r.id,r.hash,v.data FROM revision_units r JOIN unit_versions v ON r.hash=v.hash WHERE r.revision=?"
        parameters = [revision]
        if ids is not None:
            query += " AND r.id IN (" + ",".join("?" for _ in ids) + ")"
            parameters.extend(ids)
        result = {}
        for r in self.db.execute(query, parameters):
            value = json.loads(r["data"])
            require(digest(value) == r["hash"], "Stored knowledge content was modified")
            result[r["id"]] = value
        return result

    def anchor(self, snapshot, asset, start, end, *, text_sha=None):
        item = self.asset(snapshot, asset)
        require(item["status"] == "frozen", "Cannot anchor unavailable asset")
        sha = text_sha or item["sha"]
        lines = self.source_lines(sha)
        require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines), "Invalid evidence range")
        quote_sha = digest("".join(lines[start - 1:end]).encode("utf-8"))
        value = {"snapshot": snapshot, "asset": asset, "sha": sha, "asset_sha": item["sha"],
                 "start": start, "end": end, "quote_sha256": quote_sha, "view": "extracted" if text_sha else "source"}
        aid = identity("evidence", value)
        value["id"] = aid
        self.db.execute("INSERT OR IGNORE INTO main.anchors VALUES(?,?,?,?,?,?,?)",
                        (aid, snapshot, asset, sha, start, end, canonical(value)))
        return value

    def evidence_in_scope(self, anchor, snapshot):
        if anchor["snapshot"] == snapshot:
            return True
        if anchor.get("view") != "source":
            return False
        if snapshot not in self._evidence_origins:
            row = self.db.execute("SELECT json_extract(data,'$.source_index.snapshot') FROM snapshots WHERE id=?", (snapshot,)).fetchone()
            if not row:
                return False
            self._evidence_origins[snapshot] = row[0]
        if self._evidence_origins[snapshot] != anchor["snapshot"]:
            return False
        asset = self.asset(snapshot, anchor["asset"])
        return asset["kind"] == "source" and asset["sha"] == anchor["sha"] == anchor["asset_sha"]

    def read_evidence(self, evidence_id, *, expected_hash=None, max_chars=30000):
        require(type(max_chars) is int and 1 <= max_chars <= 1000000, "Invalid evidence read budget")
        value = self.record("anchors", evidence_id)
        if expected_hash is not None:
            require(expected_hash in {value["sha"], value["quote_sha256"]}, "Expected evidence hash mismatch")
        raw = self.blob(value["sha"])
        lines = raw.decode("utf-8", errors="replace").splitlines(keepends=True)
        text = "".join(lines[value["start"] - 1:value["end"]])
        require(digest(text.encode("utf-8")) == value["quote_sha256"], "Evidence range mismatch")
        return {**value, "text": text[:max_chars], "truncated": len(text) > max_chars,
                "returned_chars": min(len(text), max_chars), "total_chars": len(text)}
