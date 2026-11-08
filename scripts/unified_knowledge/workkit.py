"""Portable module workspaces containing frozen readings and one-hop ECS neighbors."""
import hashlib
import hmac
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile
import zipfile

from .graph_mount import readonly_uri
from .planner import create_task
from .store import Store, atomic_write, canonical, digest, identity, require
from .study import current, guide
from .team import _signed, assignment_key, open_order


def file_hash(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def make_shard(hub, shard, plan, ticket, additions):
    from .catalog import all_candidates
    leads = all_candidates(hub, plan)
    module = ticket["module"]
    info = plan["modules"][module]
    source_run = hub.record("runs", plan["run"])
    origin = ticket["source_index"] or {'provider':'workspace-sqlite/v1','run_id':source_run['id'],'snapshot':source_run['snapshot'],
                                          'profile_digest':source_run['profile_digest'],'facts_digest':source_run['facts_digest']}
    native = (plan.get("reuse_index") and origin.get("provider") == "workspace-sqlite/v1" and
              all(source_run[field] == origin[key] for field,key in (("id","run_id"),("snapshot","snapshot"),
                  ("profile_digest","profile_digest"),("facts_digest","facts_digest"))))
    require(not plan.get("worker_scope") and (source_run.get("mode") in {'ecs','inventory','source_only'} or native),
            "Export a worker kit from the coordinator's inventory or completed index")
    sid = plan["snapshot"]
    kit_run = identity("ecs-module", [source_run["id"], module, sorted(additions), ticket["id"]])
    db = shard.db
    db.execute("ATTACH DATABASE ? AS hub", ((hub.home / "knowledge.sqlite3").as_uri() + "?mode=ro",))
    linked = source_run.get("graph_storage") == "reference"
    graph = "graph_input" if linked else "hub"
    fact_run = origin["run_id"] if linked else source_run["id"]
    if linked:
        db.execute("ATTACH DATABASE ? AS graph_input", (readonly_uri(hub.graph_path),))
    try:
        with shard.transaction():
            current_assignment = db.execute("SELECT value FROM hub.meta WHERE key=?", (assignment_key(plan["id"], module),)).fetchone()
            require(current_assignment and json.loads(current_assignment[0])["id"] == ticket["id"], "Assignment has changed")
            require(json.loads(db.execute("SELECT value FROM hub.meta WHERE key='study_head'").fetchone()[0]) == plan["id"],
                    "Coordinator study plan has changed")
            db.execute("CREATE TEMP TABLE owned(key TEXT PRIMARY KEY)")
            for key in additions:
                hub.asset(sid, key)
            db.executemany("INSERT OR IGNORE INTO owned VALUES(?)", ((k,) for k in [*info["files"],*additions]))
            db.execute("CREATE TEMP TABLE seeds(id TEXT PRIMARY KEY)")
            db.execute(f"INSERT INTO seeds SELECT id FROM {graph}.symbols WHERE run=? AND asset IN (SELECT key FROM owned)", (fact_run,))
            db.execute("CREATE TEMP TABLE edges(id TEXT PRIMARY KEY)")
            for column in ("source","target"):
                db.execute(f"INSERT OR IGNORE INTO edges SELECT id FROM {graph}.relations WHERE run=? AND " +
                           column + " IN (SELECT id FROM seeds)", (fact_run,))
            legacy = None
            if linked and "call_binding" not in source_run["coverage"]:
                from .graph_facts import LegacyCalls
                legacy = LegacyCalls(hub,source_run["id"])
                for row in db.execute(f"SELECT data FROM {graph}.symbols WHERE run=? AND id IN (SELECT id FROM seeds) "
                                      "AND json_extract(data,'$.definition')=1",(fact_run,)):
                    node = json.loads(row[0])
                    for decl in legacy.matches(node,False,-1):
                        incoming = db.execute(f"SELECT id,data FROM {graph}.relations WHERE run=? AND target=? AND kind='CALLS'",
                                              (fact_run,decl["id"]))
                        for edge_id, data in incoming:
                            if legacy.rewrite(json.loads(data))["target"]==node["id"]:
                                db.execute("INSERT OR IGNORE INTO edges VALUES(?)",(edge_id,))
            db.execute(f"INSERT INTO relations SELECT ?,id,source,target,kind,resolution,data FROM {graph}.relations "
                       "WHERE run=? AND id IN (SELECT id FROM edges)", (kit_run, fact_run))
            if legacy:
                db.execute("CREATE TEMP TABLE original_calls AS SELECT id,data FROM relations WHERE kind='CALLS'")
                for prior, data in db.execute("SELECT id,data FROM original_calls"):
                    edge = legacy.rewrite(json.loads(data))
                    if prior!=edge["id"]:
                        db.execute("DELETE FROM relations WHERE run=? AND id=?",(kit_run,prior))
                        db.execute("INSERT OR IGNORE INTO relations VALUES(?,?,?,?,?,?,?)",
                                   (kit_run,edge["id"],edge["source"],edge["target"],edge["kind"],edge["resolution"],canonical(edge)))
            db.execute("INSERT OR IGNORE INTO seeds SELECT source FROM relations")
            db.execute("INSERT OR IGNORE INTO seeds SELECT target FROM relations")
            db.execute("INSERT OR IGNORE INTO seeds SELECT json_extract(data,'$.declared_target') FROM relations "
                       "WHERE json_extract(data,'$.declared_target') IS NOT NULL")
            db.execute(f"INSERT INTO symbols SELECT ?,id,logical,name,asset,kind,data FROM {graph}.symbols WHERE run=? "
                       "AND id IN (SELECT id FROM seeds)", (kit_run, fact_run))
            db.execute("INSERT OR IGNORE INTO owned SELECT DISTINCT asset FROM symbols")
            db.execute("INSERT OR IGNORE INTO owned SELECT DISTINCT json_extract(data,'$.asset') FROM relations")
            db.execute("INSERT OR IGNORE INTO owned SELECT key FROM hub.assets WHERE snapshot=? AND kind='method'", (sid,))
            candidate_assets = {r["asset"] for c in leads if c["owner_module"]==module
                                for r in c["evidence"]}
            db.executemany("INSERT OR IGNORE INTO owned VALUES(?)",((asset,) for asset in candidate_assets))
            for did in info["document_matches"]:
                row = db.execute("SELECT asset FROM hub.documents WHERE snapshot=? AND id=?", (sid,did)).fetchone()
                if row:
                    db.execute("INSERT OR IGNORE INTO owned VALUES(?)", (row[0],))
            for reference in ticket["references"].values():
                db.executemany("INSERT OR IGNORE INTO owned VALUES(?)", ((c["asset"],) for c in reference["citations"]))
            for r in hub.db.execute("SELECT data FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? AND json_extract(data,'$.bundle.module')=?",(sid,plan['id'],module)):
                b=json.loads(r[0])['bundle']
                extra=set(b.get('selected_files',[]))
                extra.update(hub.record('anchors',ref)['asset'] for ref in b.get('source_anchor_refs',[]))
                db.executemany('INSERT OR IGNORE INTO owned VALUES(?)',((key,) for key in extra))
            db.execute("INSERT INTO assets SELECT * FROM hub.assets WHERE snapshot=? AND key IN (SELECT key FROM owned)", (sid,))
            visible = {r[0] for r in db.execute("SELECT key FROM assets WHERE snapshot=?",(sid,))}
            snapshot_view = hub.record("snapshots",sid)
            snapshot_view["assets"] = [a for a in snapshot_view["assets"] if a["key"] in visible]
            snapshot_view["projection"] = {"module":module,"scope":"module_evidence","coordinator_snapshot":sid}
            for prof in snapshot_view["profiles"]:
                prof["commands"] = [c for c in prof["commands"] if prof["repository"]+"/"+c["file"] in visible]
                prof["unavailable_commands"] = []
                db.execute("INSERT INTO profiles VALUES(?,?,?,?)",(sid,prof["id"],prof["digest"],canonical(prof)))
            db.execute("INSERT INTO snapshots VALUES(?,?,?)",(sid,snapshot_view["created"],canonical(snapshot_view)))
            for schema in (["hub",graph] if linked else ["hub"]):
                db.execute(f"INSERT OR IGNORE INTO anchors SELECT a.* FROM assets s CROSS JOIN {schema}.anchors a "
                           "WHERE a.snapshot IN (?,?) AND a.asset=s.key AND s.sha=json_extract(a.data,'$.asset_sha')",
                           (sid,origin["snapshot"]))
            db.execute("INSERT INTO documents SELECT * FROM hub.documents WHERE snapshot=? AND asset IN (SELECT key FROM owned)", (sid,))
            run = {**source_run,"id":kit_run,"mode":"ecs_module","status":"partial","tu_results":[],"worker_scope":module,"source_index":origin,"graph_storage":"local_shard",
                   "facts_digest":digest([source_run["facts_digest"],module,sorted(additions)]),
                   "coverage":{"mode":"module_one_hop","global_run":ticket["source_index"]["run_id"],
                               "symbols":db.execute("SELECT count(*) FROM symbols").fetchone()[0],
                               "relations":db.execute("SELECT count(*) FROM relations").fetchone()[0],
                               "semantic_completeness":"not_certified"}}
            db.execute("INSERT INTO runs VALUES(?,?,?,?,?,?)",
                       (kit_run,sid,run["profile"],run["created"],run["status"],canonical(run)))
            task = hub.record("tasks",info["task"])
            from .course import previous_research
            history = previous_research(hub,task)
            for entry in history["tasks"]:
                prior = hub.db.execute("SELECT result FROM tasks WHERE id=?", (entry["id"],)).fetchone()
                result = json.loads(prior[0])
                entry["claim_titles"] = [str(c["title"])[:160] for c in result.get("claims",[]) if c.get("title")][:4]
            if history["tasks"]:
                shard.set_meta("coordinator-history:"+plan["id"], {"tasks":history["tasks"],"truncated":history["truncated"]})
            local_task = create_task(shard,snapshot=sid,run=kit_run,profile=run["profile"],kind="module_survey",bundle=task["bundle"])
            from .whole import current as whole_current
            program=whole_current(hub,False)
            if program:
                # Clone native tasks, not a second queue. Preserve coordinator identities for receipt/review.
                owned_tasks=[dict(r) for r in hub.db.execute("SELECT * FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? AND json_extract(data,'$.bundle.module')=?",(sid,plan['id'],module))]
                mapping={};survey_id=info['task']
                for original in owned_tasks:
                    original_data=json.loads(original['data']);bundle={**original_data['bundle'],'coordinator_task':original['id']}
                    new_id=create_task(shard,snapshot=sid,run=kit_run,profile=run['profile'],kind=original['kind'],bundle=bundle)
                    mapping[original['id']]=new_id
                    if original['status']=='accepted':
                        db.execute("UPDATE tasks SET status='accepted',result=? WHERE id=?",(original['result'],new_id))
                # Remove the legacy duplicate survey, before it can be leased.
                db.execute('DELETE FROM tasks WHERE id=?',(local_task,));local_task=mapping[survey_id]
                for original in owned_tasks:
                    for dep in hub.db.execute('SELECT dependency FROM task_edges WHERE task=?',(original['id'],)):
                        dep_id=dep[0]
                        if dep_id not in mapping:
                            dependency=hub.db.execute('SELECT * FROM tasks WHERE id=?',(dep_id,)).fetchone()
                            db.execute('INSERT OR IGNORE INTO tasks SELECT * FROM hub.tasks WHERE id=?',(dep_id,))
                            mapping[dep_id]=dep_id
                        db.execute('INSERT OR IGNORE INTO task_edges VALUES(?,?)',(mapping[original['id']],mapping[dep_id]))
                wp={**program,'worker_scope':module,'templates':[{**t,'task':mapping.get(t['task'],t['task'])} for t in program['templates'] if t['module']==module]}
                db.execute('INSERT INTO learning_programs VALUES(?,?,?,?,?)',(wp['id'],plan['id'],sid,run['profile'],canonical(wp)))
                db.execute('INSERT INTO learning_assets SELECT * FROM hub.learning_assets WHERE program=? AND module=?',(wp['id'],module))
                report_ids=[]
                for record in hub.db.execute('SELECT * FROM learning_reports WHERE program=?',(wp['id'],)):
                    data=json.loads(record['data'])
                    if data['module']!=module:continue
                    report_ids.append(record['id']);data['task']=mapping.get(data['task'],data['task'])
                    db.execute('INSERT INTO learning_reports VALUES(?,?,?,?,?)',(record['id'],wp['id'],data['task'],record['result_digest'],canonical(data)))
                for rid in report_ids:
                    db.execute('INSERT OR REPLACE INTO learning_dispositions SELECT * FROM hub.learning_dispositions WHERE report=?',(rid,))
                    db.execute('INSERT OR REPLACE INTO learning_leads SELECT * FROM hub.learning_leads WHERE report=?',(rid,))
                for meta in ('report-proposals:','approved-program-candidates:','planning-candidates:'):
                    value=hub.get_meta(meta+(wp['id'] if meta!='planning-candidates:' else plan['id']))
                    if value is not None:shard.set_meta(meta+(wp['id'] if meta!='planning-candidates:' else plan['id']),value)
                shard.set_meta('whole-for:'+plan['id'],wp['id'])
                shard.set_meta('coordinator-task-map',mapping)
            member_leads = [{**c,"evidence":[e for e in c["evidence"] if e["asset"] in visible]}
                            for c in leads if c["owner_module"]==module]
            view = {**plan,"run":kit_run,"modules":{module:{**info,"task":local_task}},"worker_scope":module,
                    "candidates":member_leads,"routes":{c["id"]:module for c in member_leads},
                    "gaps":[k for k in plan["gaps"] if db.execute("SELECT 1 FROM assets WHERE snapshot=? AND key=?", (sid,k)).fetchone()],
                    "unmapped_documents":[],"document_task":None,"documents":db.execute("SELECT count(*) FROM documents").fetchone()[0],
                    "coverage":run["coverage"]}
            shard.set_meta(plan["id"], view)
            shard.set_meta("study_head",plan["id"])
            shard.set_meta("snapshot_head",sid)
            shard.set_meta("plan-for:" + kit_run,plan["id"])
            shard.set_meta("index_head:" + sid + ":" + run["profile"],kit_run)
            shard.set_meta(assignment_key(plan["id"],module), {"id":ticket["id"],"ticket":ticket,"worker":ticket["worker"]})
            shard.set_meta("work_kit",ticket["id"])
    finally:
        if linked:
            db.execute("DETACH DATABASE graph_input")
        db.execute("DETACH DATABASE hub")
    for row in db.execute("SELECT data FROM assets"):
        asset = json.loads(row[0])
        for sha in {asset.get("sha"),asset.get("text_sha")} - {None}:
            if not shard.blob_path(sha).exists():
                shard.put_blob(hub.blob(sha))
    return run["coverage"]


def pack(hub, order, output, additions=()):
    plan = current(hub)
    ticket = json.loads(Path(order).read_text(encoding="utf-8-sig"))
    require(ticket['plan']==plan['id'],'Work order belongs to another plan')
    output = Path(output).resolve()
    require(output.suffix.lower() == ".zip" and output != Path(order).resolve(), "Use a separate .zip path for the kit")
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="module-kit-",dir=output.parent) as directory:
        folder = Path(directory) / "kit"
        with Store(folder) as shard:
            coverage = make_shard(hub,shard,plan,ticket,additions)
            shard.db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            shard.db.execute("PRAGMA journal_mode=DELETE")
        atomic_write(folder/"order.json",canonical(ticket))
        files = {"knowledge.sqlite3":folder/"knowledge.sqlite3","order.json":folder/"order.json"}
        files.update({p.relative_to(folder).as_posix():p for p in (folder/"blobs").glob("*/*")})
        spec = {"schema":"module-workspace/v1","order":ticket["id"],
                "files":{k:{"sha":file_hash(p),"bytes":p.stat().st_size} for k,p in files.items()}}
        archive = Path(directory) / "out.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=3) as zipout:
            zipout.writestr("manifest.json",canonical({"spec":spec,"signature":_signed(ticket["secret"],spec)}))
            for name,p in files.items():
                zipout.write(p,name)
        os.replace(archive,output)
    return {"file":str(output),"sha256":file_hash(output),"bytes":output.stat().st_size,
            "coverage":coverage,"worker":ticket["worker"],"module":ticket["module"]}


def _readable_materials(store, directory, snapshot):
    for row in store.db.execute("SELECT data FROM assets WHERE snapshot=? AND status='frozen' AND kind IN ('source','document')", (snapshot,)):
        asset = json.loads(row[0])
        key = PurePosixPath(asset["key"])
        require(not key.is_absolute() and ".." not in key.parts, "Invalid reading path")
        path = (directory / key.as_posix()).resolve()
        require(path.is_relative_to(directory.resolve()), "Reading path leaves workspace")
        if asset.get("text_sha"):
            path = path.with_name(path.name + ".extracted.txt")
        atomic_write(path,store.blob(asset.get("text_sha") or asset["sha"]))


def open_kit(home, archive):
    home, archive = Path(home).resolve(), Path(archive).resolve()
    home.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as source:
        manifest = json.loads(source.read("manifest.json"))
        spec = manifest["spec"]
        ticket = json.loads(source.read("order.json"))
        require(spec.get("schema") == "module-workspace/v1" and ticket["id"] == spec["order"] and
                hmac.compare_digest(manifest["signature"],_signed(ticket["secret"],spec)), "Invalid module kit binding")
        require(len(source.namelist()) == len(set(source.namelist())) and
                set(source.namelist()) == {"manifest.json",*spec["files"]} and
                {"order.json","knowledge.sqlite3"} <= spec["files"].keys(), "Invalid module kit inventory")
        if (home/"knowledge.sqlite3").is_file():
            with Store(home, readonly=True) as old:
                require(old.get_meta("work_kit") == ticket["id"], "Use a new worker directory for this assignment")
        else:
            require(not home.exists() or (home.is_dir() and not any(home.iterdir())), "Worker directory must be new or empty")
            with tempfile.TemporaryDirectory(prefix=".opening-kit-",dir=home.parent) as temp:
                stage = Path(temp) / "work"
                stage.mkdir()
                for name, prop in spec["files"].items():
                    require(name in {"order.json","knowledge.sqlite3"} or
                            re.fullmatch(r"blobs/[0-9a-f]{2}/[0-9a-f]{64}",name), "Unexpected kit file")
                    dest = stage / name
                    dest.parent.mkdir(parents=True,exist_ok=True)
                    require(source.getinfo(name).file_size == prop["bytes"], "Kit file size mismatch")
                    with source.open(name) as inp, dest.open("xb") as out:
                        shutil.copyfileobj(inp,out)
                    require(file_hash(dest) == prop["sha"], "Damaged kit file: " + name)
                with Store(stage) as local:
                    require(local.db.execute("PRAGMA quick_check").fetchone()[0] == "ok" and
                            local.get_meta("work_kit") == ticket["id"], "Invalid worker database")
                    opened = open_order(local,stage/"order.json")
                    _readable_materials(local,stage/"reading",opened["local_snapshot"])
                if home.exists():
                    home.rmdir()  # Only an empty, explicitly supplied destination can be removed.
                os.rename(stage,home)
    with Store(home) as local:
        result = open_order(local,home/"order.json")
        plan_file = guide(local)["plan_file"]
    script = Path(__file__).resolve().parents[1] / "unified_kb.py"
    mcp = {"mcpServers":{"gaussdb_knowledge":{"command":sys.executable,"args":["-X","utf8",str(script),"--home",str(home),
                                                                               "serve","--transport","stdio","--role","researcher"]}}}
    atomic_write(home/"worker.mcp.json",canonical(mcp))
    return {**result,"order":str(home/"order.json"),"reading":str(home/"reading"),"plan":plan_file,
            "mcp":str(home/"worker.mcp.json"),"frontend_invocations":0}
