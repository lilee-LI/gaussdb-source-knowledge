"""Attach a completed ECS index to a locally owned learning workspace."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3
from collections import Counter, defaultdict

from .graph_mount import readonly_uri
from .materials import ingest
from .store import canonical, digest, identity, now, require


def index_path(path, home):
    path = Path(path).expanduser().resolve()
    home = Path(home).expanduser().resolve()
    require(path.is_file(), "ECS knowledge.sqlite3 is missing: " + str(path))
    destination = home / "knowledge.sqlite3"
    require(path != destination and not (destination.exists() and path.samefile(destination)),
            "Use a separate learning --home; the ECS database is read-only input")
    return path


class CompletedIndex:
    def __init__(self, db, path, run_id):
        self.db, self.path = db, path
        self.restored_text_files = 0
        row = db.execute("SELECT snapshot,profile,status,data FROM runs WHERE id=?", (run_id,)).fetchone()
        require(row, "ECS run_id was not found: " + run_id)
        self.run = json.loads(row["data"])
        require(row["status"] in {"ready", "partial"} and self.run.get("status") == row["status"] and
                self.run.get("id") == run_id and self.run.get("facts_digest"),
                "Select a completed ECS run with a facts_digest")
        require(self.run.get("mode") not in {"inventory","ecs_module"},
                "Select the ECS analysis run, not an inventory-only plan or a portable module run")
        require(self.run["snapshot"] == row["snapshot"] and self.run["profile"] == row["profile"],
                "Inconsistent ECS run binding")
        snap = db.execute("SELECT data FROM snapshots WHERE id=?", (row["snapshot"],)).fetchone()
        require(snap, "Source snapshot for the ECS run is missing")
        self.snapshot = json.loads(snap[0])
        require(self.snapshot["id"] == row["snapshot"], "ECS snapshot identity mismatch")
        self.origin = {"provider":"ecs-sqlite/v1", "run_id":run_id, "snapshot":row["snapshot"],
                       "profile":row["profile"], "profile_digest":self.run["profile_digest"],
                       "facts_digest":self.run["facts_digest"]}
        binding = next((p for p in self.snapshot["profiles"] if p["id"] == row["profile"]), None)
        require(binding and binding["digest"] == self.origin["profile_digest"], "ECS profile digest mismatch")
        self.tu_status = defaultdict(Counter)
        for tu in self.run.get("tu_results", []):
            self.tu_status[tu.get("asset")][tu.get("status", "unknown")] += 1

    def freeze(self, store, sha):
        require(isinstance(sha, str) and len(sha) == 64, "Invalid ECS material digest")
        existing = store.blob_path(sha)
        if existing.is_file():
            store.blob(sha)
            return
        frozen = self.path.parent / "blobs" / sha[:2] / sha
        require(frozen.is_file(), "Missing frozen material. Supply the matching source/documents or ECS blobs: " + sha)
        raw = frozen.read_bytes()
        require(digest(raw) == sha, "Material differs from the ECS snapshot: " + str(frozen))
        store.put_blob(raw)

    def source_assets(self, repository):
        keys = set(self.run["evidence_assets"]) if "evidence_assets" in self.run else None
        return {asset["path"]: asset for asset in self.snapshot["assets"]
                if asset["kind"] == "source" and asset["repo"] == repository and (keys is None or asset["key"] in keys)}

    def bind_asset(self, store, asset, path):
        row = {**asset, "inventory_origin": "checkout_and_ecs" if path else "ecs_only",
               "tu_status": dict(self.tu_status.get(asset["key"], {}))}
        if asset["status"] == "frozen":
            if path is None:
                self.freeze(store, asset["sha"])
            else:
                # Verify the checkout even when a previous snapshot already cached this blob.
                raw = path.read_bytes()
                if digest(raw) != asset["sha"] and b"\0" not in raw:
                    lf = raw.replace(b"\r\n", b"\n")
                    for candidate in (lf, lf.replace(b"\n", b"\r\n")):
                        if digest(candidate) == asset["sha"]:
                            raw = candidate
                            self.restored_text_files += 1
                            break
                require(digest(raw) == asset["sha"], "Material differs from the ECS snapshot: " + str(path))
                store.put_blob(raw)
        return row

    def inherited_documents(self, store, supplied):
        specs = [r for r in self.snapshot["materials"] if r["kind"] == "document" and r["id"] not in supplied]
        ids = {s["id"] for s in specs}
        rows = [r for r in self.snapshot["assets"] if r["kind"] == "document" and r["repo"] in ids]
        keys = {r["key"] for r in rows}
        for row in rows:
            for sha in (row.get("sha"), row.get("text_sha")):
                if sha:
                    self.freeze(store, sha)
        docs = []
        for row in self.db.execute("SELECT data FROM documents WHERE snapshot=?", (self.origin["snapshot"],)):
            d = json.loads(row[0])
            if d["asset"] in keys:
                docs.append({k:d[k] for k in ("asset","start","end","text_sha","kind","title","document_status")})
        return specs, rows, docs


def _adopt_graph(store, path, index, snapshot):
    """Bulk-copy only this run. IDs from the ECS graph continue to identify its original facts."""
    rid = identity("ecs-study", [snapshot, index.origin])
    with store.transaction():
        present = store.db.execute("SELECT data FROM runs WHERE id=?", (rid,)).fetchone()
        if present:
            return json.loads(present[0])
    store.db.execute("ATTACH DATABASE ? AS ecs_input", (readonly_uri(path),))
    try:
        with store.transaction():
            row = store.db.execute("SELECT status,data FROM ecs_input.runs WHERE id=?", (index.origin["run_id"],)).fetchone()
            require(row and row[0] in {"partial", "ready"} and json.loads(row[1]).get("facts_digest") == index.origin["facts_digest"],
                    "ECS run changed during import; retry using a completed run")
            if store.db.execute("SELECT 1 FROM runs WHERE id=?", (rid,)).fetchone():
                return store.record("runs", rid)
            params = (rid, index.origin["run_id"])
            store.db.execute("INSERT INTO symbols SELECT ?,id,logical,name,asset,kind,data FROM ecs_input.symbols WHERE run=?", params)
            store.db.execute("INSERT INTO relations SELECT ?,id,source,target,kind,resolution,data FROM ecs_input.relations WHERE run=?", params)
            store.db.execute("INSERT OR IGNORE INTO anchors SELECT a.* FROM ecs_input.anchors a "
                             "JOIN main.assets m ON m.snapshot=? AND m.key=a.asset AND m.kind='source' AND m.sha=a.sha "
                             "WHERE a.snapshot=?", (snapshot, index.origin["snapshot"]))
            coverage = dict(index.run.get("coverage", {}))
            for table in ("symbols", "relations"):
                count = store.db.execute("SELECT count(*) FROM " + table + " WHERE run=?", (rid,)).fetchone()[0]
                require(table not in coverage or coverage[table] == count, "ECS graph count mismatch: " + table)
                coverage[table] = count
                missing = store.db.execute("SELECT 1 FROM " + table + " t LEFT JOIN anchors a "
                    "ON a.id=json_extract(t.data,'$.evidence') WHERE t.run=? AND a.id IS NULL LIMIT 1", (rid,)).fetchone()
                require(not missing, "ECS graph contains an unbound source anchor: " + table)
            from .graph_facts import link_calls
            coverage["call_binding"] = link_calls(store, rid, legacy_candidates=True)
            run = {"id":rid, "snapshot":snapshot, "profile":index.origin["profile"], "profile_digest":index.origin["profile_digest"],
                   "mode":"ecs", "source_index":index.origin, "status":row[0], "created":now(),
                   "facts_digest":digest(["ecs-study-link/v1",index.origin["facts_digest"],coverage["call_binding"]]), "coverage":coverage,
                   "tu_results":[], "cache_hits":0, "frontend_invocations":0, "database_execution":"not_run"}
            store.db.execute("INSERT INTO runs VALUES(?,?,?,?,?,?)",
                             (rid, snapshot, run["profile"], run["created"], run["status"], canonical(run)))
        return run
    finally:
        store.db.execute("DETACH DATABASE ecs_input")


def connect(store, config, requested_profile=None):
    """No compiler, TU cache, product binary or mutation of the source database."""
    from .study import inventory
    spec = config["ecs_index"]
    path = index_path(spec["database"], store.home)
    from .graph_mount import inspect_input, register
    storage = spec.get("graph_storage", "auto")
    require(storage in {"auto","reference","copy"}, "graph_storage 取 auto、reference 或 copy")
    if storage == "auto":
        storage = "reference" if path.stat().st_size >= 256 * 1024**2 else "copy"
    require(not store.graph_path or storage=="reference", "当前工作区使用只读挂接模式，请继续使用 graph_storage=reference")
    details = inspect_input(path,spec.get("run_id"),check_indexes=storage=="reference")
    with closing(sqlite3.connect(readonly_uri(path), uri=True)) as upstream:
        upstream.row_factory = sqlite3.Row
        upstream.execute("BEGIN")
        try:
            index = CompletedIndex(upstream, path, details["run_id"])
            require(not requested_profile or requested_profile == index.origin["profile"], "The ECS run belongs to a different profile")
            source_repos = [r for r in index.snapshot["materials"] if r["kind"] == "source"]
            local = config["repositories"]
            require(len(local) == len(source_repos), "Supply a local path for each ECS source repository")
            # The single-repository shortcut adopts the ID used on the ECS.
            other_ids = {r["id"] for r in local[1:]}
            primary = [r for r in source_repos if r["id"] not in other_ids]
            require(len(primary) == 1, "Use repository_roots for additional ECS repositories")
            local = [{**local[0],"id":primary[0]["id"]}, *local[1:]]
            require({r["id"] for r in local} == {r["id"] for r in source_repos}, "ECS repository IDs do not match local roots")
            effective = {**config, "repositories":local, "profiles":[],
                         "product":index.snapshot["product"], "revision":index.snapshot["revision"]}
            snapshot = ingest(store, effective, imported=index)
            if storage == "reference":
                rid = identity("ecs-study-reference", [snapshot["id"],index.origin])
                run = register(store,path,index,snapshot["id"],rid)
            else:
                run = _adopt_graph(store, path, index, snapshot["id"])
        except sqlite3.DatabaseError as error:
            raise ValueError("Incompatible or unreadable ECS knowledge.sqlite3: " + str(error)) from error
    report = inventory(store, effective, snapshot=snapshot["id"], existing_run=run, module_queue=True)
    report["graph"] = {**details,"storage":storage,"restored_text_files":index.restored_text_files}
    return report


def focus_existing(store, plan, module, files, limit, question, symbol, profile, extend, lead=None):
    """Create a study task over already indexed symbols and original ECS evidence."""
    from .planner import create_task
    require(not profile or profile == plan["profile"], "Choose the plan bound to the requested ECS profile")
    origin = plan.get("source_index") or {}
    require(not extend or extend in {plan["run"],origin.get("run_id")}, "Focus uses the bound index run")
    info = plan["modules"][module]
    owned = set(info["files"])
    repo = module.split("/", 1)[0]
    explicit = {p if p.startswith(repo + "/") else repo + "/" + p for p in files}
    if lead and not explicit:
        explicit = set(dict.fromkeys(r["asset"] for r in lead["evidence"] if r["asset"] in owned))
        explicit = set(sorted(explicit)[:limit])
    require(len(explicit) <= limit, "File selection exceeds the reading budget")
    for key in explicit:
        store.asset(plan["snapshot"], key)
    matched = []
    text_hits = {}
    if symbol and not plan.get("source_only"):
        matched = [json.loads(r["data"]) for r in store.lookup_symbols(plan["run"],symbol,assets=explicit or owned,limit=101)]
        matched.sort(key=lambda r:(r["asset"],r["id"]))
        require(len(matched)<=100, "Ambiguous symbol in this module; choose its exact symbol ID")
    text_symbol = symbol
    if lead and not explicit and not symbol:
        import re
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*",lead["title"]):
            text_symbol = lead["title"]
    if text_symbol and not matched:
        import re
        needle = re.compile(r"(?<!\w)" + re.escape(text_symbol) + r"(?!\w)",0 if symbol else re.IGNORECASE)
        for key in sorted(explicit or owned, key=lambda k:(Path(k).suffix.lower() not in {".c",".cpp",".cc",".cxx"},k)):
            asset = store.asset(plan["snapshot"], key)
            if asset["status"] == "frozen" and Path(key).suffix.lower() in {".c",".cc",".cpp",".cxx",".h",".hpp"}:
                for n,line in enumerate(store.source_lines(asset["sha"]),1):
                    if needle.search(line):
                        text_hits[key] = n
                        break
            if len(text_hits)>=limit:
                break
        require(text_hits or not symbol, "当前模块冻结源码中未命中该标识符，可用 --file 选择准确的相对路径。")
    seeds = sorted({s["asset"] for s in matched if s["asset"] in owned})
    if explicit:
        selected = sorted(explicit)
    elif text_hits:
        selected = sorted(text_hits)
    elif seeds:
        selected = seeds[:limit]
    elif matched:
        raise ValueError("Symbol outside this module; choose its owner or an explicit consumer file")
    else:
        import re
        words = [w.casefold() for w in re.findall(r"[A-Za-z_][A-Za-z_0-9]+", question or "")]
        selected = sorted(owned, key=lambda k:(-sum(w in k.casefold() for w in words),
            Path(k).suffix.lower() not in {".c",".cpp",".cc",".cxx"}, k))[:limit]
    require(selected and owned.intersection(selected), "Select an implementation file from the assigned module")
    if not matched:
        rows = store.db.execute("SELECT data FROM symbols WHERE run=? AND asset IN (" + ",".join("?" for _ in selected) +
            ") AND kind IN ('function_decl','candidate_function','cxx_method') AND json_extract(data,'$.definition')=1 "
            "ORDER BY asset,name LIMIT 12", (plan["run"], *selected))
        matched = [json.loads(r[0]) for r in rows]
    matches = [s for s in matched if s["asset"] in selected][:12]
    anchors = [s["evidence"] for s in matches]
    with store.transaction():
        if lead:
            from .catalog import candidate
            require(store.get_meta("study_head")==plan["id"],"学习计划已换版，请重新选择候选")
            require(candidate(store.get_meta(plan["id"]),lead["id"],store)["owner_module"] in (None,module),
                    "候选责任模块已变更，请刷新清单")
            prior = store.db.execute("SELECT id,data FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? "
                "AND json_extract(data,'$.bundle.candidate_id')=? ORDER BY rowid LIMIT 1",
                (plan["snapshot"],plan["id"],lead["id"])).fetchone()
            if prior:
                bundle = json.loads(prior["data"])["bundle"]
                require(bundle["module"] == module,"此候选已由其他模块负责："+bundle["module"])
                return {"module":module,"task":prior["id"],"run":plan["run"],"frontend_invocations":0,
                        "candidate_id":lead["id"],"question":bundle.get("question",question),"reused":True}
            for ref in lead["evidence"]:
                if ref.get("document"):
                    row = store.db.execute("SELECT json_extract(data,'$.anchor') FROM documents WHERE snapshot=? AND id=?",
                                           (plan["snapshot"],ref["document"])).fetchone()
                    if row:
                        anchors.append(row[0])
                else:
                    anchors.append(store.anchor(plan["snapshot"],ref["asset"],ref["start"],ref["end"])["id"])
        for key in selected:
            if any(s["asset"] == key for s in matches):
                continue
            a = store.asset(plan["snapshot"], key)
            if a["status"] == "frozen":
                n = len(store.source_lines(a["sha"]))
                if n:
                    first = max(1,text_hits.get(key,1)-3)
                    anchors.append(store.anchor(plan["snapshot"], key, first, min(first+39,n))["id"])
        doc_refs = [r[0] for doc in info["document_matches"][:3] for r in store.db.execute(
            "SELECT json_extract(data,'$.anchor') FROM documents WHERE snapshot=? AND id=?", (plan["snapshot"],doc))]
        anchors.extend(doc_refs)
        task = create_task(store, snapshot=plan["snapshot"], run=plan["run"], profile=plan["profile"], kind="feature_research",
            bundle={"module":module,"plan_id":plan["id"],"selected_files":selected,"source_index":plan.get("source_index"),
                    **({"candidate_id":lead["id"]} if lead else {}),
                    "question":question or module + " 的入口、状态、消费者和测试依据是什么？",
                    "symbol_refs":[s["id"] for s in matches],"source_anchor_refs":list(dict.fromkeys(anchors))})
    return {"module":module,"task":task,"run":plan["run"],"index_run_id":origin.get("run_id"),
            "ecs_run_id":origin.get("run_id") if origin.get("provider") == "ecs-sqlite/v1" else None,
            "profile":plan["profile"],"selected_files":selected,"symbols":[{"id":s["id"],"name":s["name"],"asset":s["asset"]} for s in matches],
            "frontend_invocations":0,"candidate_id":lead and lead["id"],"question":question,
            "evidence_mode":"indexed" if matches and not text_hits else "source_text", "next":"领取任务、读取证据并提交。"}
