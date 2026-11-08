"""Iterative SCC planning, leased research tasks and actual evidence-read receipts."""
from __future__ import annotations

from collections import defaultdict
import json
import re
import time
import uuid
import networkx as nx

from .store import canonical, digest, identity, now, require


FUNCTIONS = {"function_decl", "cxx_method", "constructor", "destructor", "function_template",
             "conversion_function", "candidate_function"}


def scc(nodes, edges):
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from((a, b) for a, b in edges if a in graph and b in graph)
    return [sorted(group) for group in nx.strongly_connected_components(graph)]


def resolve_targets(store, run, targets):
    resolved, unknown = set(), []
    for target in targets:
        rows = store.lookup_symbols(run,target)
        if rows:
            resolved.update(r[0] for r in rows)
        else:
            unknown.append(target)
    return resolved, unknown


def create_task(store, *, snapshot, run, profile, kind, bundle, dependencies=()):
    # New accepted Wiki revisions do not force an unconditional second source walk.
    key_bundle = {k: v for k, v in bundle.items() if k != "base_knowledge_revision"}
    tid = identity("task", [snapshot, run, profile, kind, key_bundle])
    value = {"id": tid, "snapshot": snapshot, "run": run, "profile": profile, "kind": kind,
             "bundle": bundle, "created": now(), "database_execution": "not_run"}
    store.db.execute("INSERT OR IGNORE INTO tasks(id,snapshot,run,profile,kind,status,data) VALUES(?,?,?,?,?,'queued',?)",
                     (tid, snapshot, run, profile, kind, canonical(value)))
    for dep in dependencies:
        require(dep != tid, "Self-dependent task")
        store.db.execute("INSERT OR IGNORE INTO task_edges VALUES(?,?)", (tid, dep))
    return tid


def plan(store, run, *, targets=None, question=None, max_symbols=12, granularity="auto"):
    require(type(max_symbols) is int and 1 <= max_symbols <= 100, "Invalid slice size")
    index = store.record("runs", run)
    require(index["status"] in {"ready", "partial"}, "Index must finish before planning")
    snapshot, profile = index["snapshot"], index["profile"]
    from .course import feature_plan, module_plan, use_modules
    if targets:
        return feature_plan(store,index,targets,question,max_symbols)
    if use_modules(store,index,granularity):
        return module_plan(store,index)
    method_digest = store.record("snapshots", snapshot).get("methods_digest")
    symbols = {r["id"]: json.loads(r["data"]) for r in store.db.execute("SELECT id,data FROM symbols WHERE run=?", (run,))}
    functions = {k: v for k, v in symbols.items() if v["kind"] in FUNCTIONS and v.get("definition")}
    pairs = [(r[0], r[1]) for r in store.db.execute("SELECT source,target FROM relations WHERE run=? AND kind='CALLS' AND resolution='resolved'", (run,))]
    unresolved = []
    groups = scc(functions, pairs)
    task_ids, owners, final_tasks, task_specs = [], {}, {}, []
    with store.transaction():
        for number, group in enumerate(groups):
            for symbol in group:
                owners[symbol] = number
            fragments = []
            for start in range(0, len(group), max_symbols):
                members = group[start:start + max_symbols]
                refs = [functions[m]["evidence"] for m in members]
                bundle = {"schema": "slice-bundle/v1", "question": question or "Explain implementation, state, contracts and boundary cases",
                          "symbol_refs": members, "source_anchor_refs": refs, "scc": identity("scc", group),
                          "scc_total_symbols": len(group), "fragment": start // max_symbols,
                          "boundary_symbols": [m for m in group if m not in members],
                          "required_views": ["implementation", "data_state", "contract", "tests", "counterexamples"],
                          "scope_digest": digest([symbols[m] for m in members]),
                          "profile_digest": index["profile_digest"], "base_knowledge_revision": store.get_meta("knowledge_head"),
                          "method_version": method_digest, "coverage": "not_started"}
                tid = create_task(store, snapshot=snapshot, run=run, profile=profile, kind="source_research", bundle=bundle)
                fragments.append(tid)
                task_ids.append(tid)
            if len(fragments) > 1:
                aggregate = create_task(store, snapshot=snapshot, run=run, profile=profile, kind="scc_synthesis",
                                        bundle={"scc": identity("scc", group), "symbol_refs": group,
                                                "question": "Reconcile fragments and cycle boundary contracts"},
                                        dependencies=fragments)
                task_ids.append(aggregate)
                final_tasks[number] = aggregate
            elif fragments:
                final_tasks[number] = fragments[0]
            task_specs.append((number, fragments))
        dependencies = defaultdict(set)
        for a, b in pairs:
            if a in owners and b in owners and owners[a] != owners[b]:
                dependencies[owners[a]].add(owners[b])
        for number, fragments in task_specs:
            for dep in sorted(dependencies[number]):
                for tid in fragments:
                    store.db.execute("INSERT OR IGNORE INTO task_edges VALUES(?,?)", (tid, final_tasks[dep]))
        if not targets:
            for row in store.db.execute("SELECT data FROM assets WHERE snapshot=? AND kind='source'", (snapshot,)).fetchall():
                asset = json.loads(row[0])
                if index.get("selected_files") is not None and asset["path"] not in index["selected_files"]:
                    continue
                if asset["status"] == "excluded":
                    continue
                # Function coverage cannot stand in for registrations, globals,
                # macros or declarations elsewhere in the same file.
                bundle = {"asset": asset["key"], "asset_sha": asset["sha"], "status": asset["status"],
                          "question": "Discover registrations, commands, types, macros, global state, tests and omitted behavior; reuse function research"}
                if asset["status"] == "frozen":
                    lines = len(store.blob(asset["sha"]).decode("utf-8", errors="replace").splitlines())
                    bundle["source_anchor_refs"] = [store.anchor(snapshot, asset["key"], start, min(start + 999, lines))["id"]
                                                    for start in range(1, lines + 1, 1000)]
                task_ids.append(create_task(store, snapshot=snapshot, run=run, profile=profile, kind="asset_discovery", bundle=bundle))
            for row in store.db.execute("SELECT data FROM documents WHERE snapshot=?", (snapshot,)).fetchall():
                document = json.loads(row[0])
                task_ids.append(create_task(store, snapshot=snapshot, run=run, profile=profile, kind="requirement_mapping",
                    bundle={"document_ref": document["id"], "source_anchor_refs": [document["anchor"]],
                            "document_status": document["document_status"], "material_kind": document["kind"],
                            "question": "Map declared behavior and conditions to implementation, contracts and test obligations"}))
        for item in index["coverage"].get("ctags", {}).get("unmatched", []):
            candidates = [v for v in functions.values() if v["asset"] == item["asset"] and v["name"] == item["name"]]
            if targets and not candidates:
                continue
            gap = create_task(store, snapshot=snapshot, run=run, profile=profile, kind="index_gap",
                bundle={"asset": item["asset"], "candidate": item["name"], "range": [item["start"], item["end"]],
                        "source_anchor_refs": [v["evidence"] for v in candidates],
                        "question": "Confirm independent definition candidate and resolve primary-parser omission"})
            task_ids.append(gap)
            for candidate in candidates:
                number = owners.get(candidate["id"])
                if number is not None:
                    for group_number, fragments in task_specs:
                        if group_number == number:
                            for tid in fragments:
                                store.db.execute("INSERT OR IGNORE INTO task_edges VALUES(?,?)", (tid, gap))
        for target in unresolved:
            task_ids.append(create_task(store, snapshot=snapshot, run=run, profile=profile, kind="unresolved_target",
                                        bundle={"target": target, "question": question or "Resolve target and missing evidence"}))
        # Candidate ownership is navigational and remains unreviewed.
        inventory = []
        snap = store.record("snapshots", snapshot)
        for row in store.db.execute("SELECT data FROM assets WHERE snapshot=? AND kind='source'", (snapshot,)):
            asset = json.loads(row[0])
            parts = asset["path"].split("/")
            declared = [r for r in snap.get("ownership", []) if asset["key"].startswith(r.get("prefix", "\0"))]
            inventory.append({"asset": asset["key"], "owner": declared[0].get("owner") if declared else None,
                              "candidate_path": [asset["repo"], *(parts[:3])],
                              "status": "declared" if declared else "candidate"})
        store.set_meta("ownership:" + run, inventory)
        store.event("plan", {"run": run, "tasks": len(set(task_ids)), "scc_groups": len(groups), "unresolved_targets": unresolved})
    return {"run": run, "tasks": sorted(set(task_ids)), "scc_groups": len(groups), "unresolved_targets": unresolved,
            "semantic_completion": "not_started", "ownership_status": "candidate_or_declared"}


def task_status(store, task):
    row = store.db.execute("SELECT * FROM tasks WHERE id=?", (task,)).fetchone()
    require(row is not None, "Task missing")
    value = json.loads(row["data"])
    value.update(status=row["status"], owner=row["owner"], deadline=row["deadline"], attempt=row["attempt"])
    value["dependency_states"] = dict(store.db.execute("SELECT e.dependency,d.status FROM task_edges e "
        "LEFT JOIN tasks d ON d.id=e.dependency WHERE e.task=? ORDER BY e.dependency", (task,)))
    value["dependencies"] = list(value["dependency_states"])
    if row["result"]:
        value["result"] = json.loads(row["result"])
    return value


def next_tasks(store, run, limit=20):
    require(type(limit) is int and 1 <= limit <= 1000, "Invalid task limit")
    rows = store.db.execute("SELECT id FROM tasks t WHERE run=? AND status IN ('queued','needs_research','leased') "
                           "AND (status<>'leased' OR deadline<?) AND NOT EXISTS "
                           "(SELECT 1 FROM task_edges e JOIN tasks d ON e.dependency=d.id WHERE e.task=t.id AND d.status<>'accepted') "
                           "ORDER BY kind,id LIMIT ?", (run, time.time(), limit)).fetchall()
    return [task_status(store, r[0]) for r in rows]


def lease(store, task, worker, *, seconds=1800, action="claim", token=None, checkpoint=None):
    require(isinstance(worker, str) and worker.strip(), "Worker identity required")
    require(type(seconds) is int and 1 <= seconds <= 86400, "Invalid lease duration")
    with store.transaction():
        value = task_status(store, task)
        if action == "claim":
            b = value["bundle"]
            if b.get("module") and b.get("plan_id"):
                assignment = store.get_meta("assignment:" + b["plan_id"] + ":" + b["module"])
                require(not assignment or assignment["worker"] == worker, "Module belongs to another worker")
            require(value["status"] in {"queued", "needs_research"} or
                    (value["status"] == "leased" and value["deadline"] < time.time()), "Task is not claimable")
            require(all(v == "accepted" for v in value["dependency_states"].values()), "Task dependencies not accepted")
            token = uuid.uuid4().hex
            store.db.execute("UPDATE tasks SET status='leased',owner=?,token=?,deadline=?,attempt=attempt+1 WHERE id=?",
                             (worker, token, time.time() + seconds, task))
        else:
            _check_lease(store, task, worker, token)
            if action == "renew":
                store.db.execute("UPDATE tasks SET deadline=? WHERE id=?", (time.time() + seconds, task))
            elif action == "release":
                store.db.execute("UPDATE tasks SET status='queued',owner=NULL,token=NULL,deadline=NULL WHERE id=?", (task,))
            elif action == "checkpoint":
                store.event("checkpoint", {"task": task, "worker": worker, "token": token, "checkpoint": checkpoint})
            else:
                raise ValueError("Unknown lease action")
        store.event("task_" + action, {"task": task, "worker": worker})
    return {**task_status(store, task), "token": token}


def _check_lease(store, task, worker, token):
    row = store.db.execute("SELECT * FROM tasks WHERE id=?", (task,)).fetchone()
    require(row and row["status"] == "leased" and row["owner"] == worker and row["token"] == token
            and row["deadline"] > time.time(), "Invalid, expired or superseded task lease")
    return row


def read_for_task(store, task, worker, token, evidence, **kwargs):
    with store.transaction():
        row = _check_lease(store, task, worker, token)
        value = store.read_evidence(evidence, **kwargs)
        require(store.evidence_in_scope(value, row["snapshot"]), "Evidence belongs to another task snapshot")
        receipt = {"task": task, "worker": worker, "token": token, "evidence": evidence,
                   "quote_sha256": value["quote_sha256"], "truncated": value["truncated"],
                   "returned_chars": value["returned_chars"]}
        store.event("evidence_read", receipt)
    return value


def _complete_reads(store, task, worker, token):
    receipts = [json.loads(r[0]) for r in store.db.execute(
        "SELECT data FROM events WHERE kind='evidence_read' AND json_extract(data,'$.task')=? "
        "AND json_extract(data,'$.worker')=? AND json_extract(data,'$.token')=?", (task, worker, token))]
    return {r["evidence"] for r in receipts if not r["truncated"]}


def stage_research_unit(store, task, worker, token, unit, previous_hash=None):
    """Save one unreviewed unit through typed tool transport, within a live lease."""
    from .knowledge import KINDS, EDGES
    require(isinstance(unit, dict) and unit.get("kind") in KINDS and isinstance(unit.get("id"), str)
            and unit["id"].strip() and unit.get("title") and isinstance(unit.get("body"), str) and unit["body"].strip(),
            "Typed unit id/kind/title/body required")
    require(len(canonical(unit).encode("utf-8")) <= 80000, "Split oversized research unit")
    require(not any(k.startswith("_") for k in unit), "Reserved knowledge metadata")
    if unit['kind']=='flow':
        require(isinstance(unit.get('steps'),list) and unit['steps'],'Flow needs typed steps')
        for step in unit['steps']:
            require(isinstance(step,dict) and step.get('kind') in {'call','data_stage','state_transition','async_message'},'flow.steps uses kind (not type): call/data_stage/state_transition/async_message')
            if step['kind']=='call':require(step.get('symbol') and step.get('target'),'A call step requires real symbol and target IDs; use data_stage/state_transition for effects and stages')
    if unit["kind"] == "test_obligation":
        expected = unit.get("expected_from")
        require(isinstance(expected,dict) and expected.get("kind") in {"requirement","claim","contract","source_prediction"}
                and isinstance(expected.get("ref"),str),
                'expected_from must be one object, e.g. {"kind":"contract","ref":"contract:example"}')
    refs = unit.get("source_refs", [])
    require(isinstance(refs, list) and all(isinstance(ref, str) for ref in refs), "Evidence id list required")
    for link in unit.get("knowledge_refs", []):
        require(isinstance(link, dict) and link.get("target") and link.get("relation") in EDGES,
                "knowledge_refs requires target/relation objects")
    with store.transaction():
        row = _check_lease(store, task, worker, token)
        require(set(refs) <= _complete_reads(store, task, worker, token), "Unit references evidence not fully read with this lease")
        for ref in refs:
            require(store.evidence_in_scope(store.record("anchors", ref), row["snapshot"]), "Unit evidence snapshot mismatch")
            store.read_evidence(ref)
        key = "research_drafts:" + task + ":" + str(row["attempt"])
        drafts = store.get_meta(key, {})
        old = drafts.get(unit["id"])
        require(old is None or old == unit or previous_hash == digest(old), "Staged unit changed; previous_hash required")
        require(unit["id"] in drafts or len(drafts) < 100, "Research task unit limit exceeded")
        drafts[unit["id"]] = unit
        store.set_meta(key, drafts)
        store.event("research_unit_staged", {"task": task, "worker": worker, "attempt": row["attempt"],
                    "unit": unit["id"], "hash": digest(unit), "semantic_approval": "not_granted"})
    return {"unit": unit["id"], "unit_hash": digest(unit), "drafts_digest": digest(drafts),
            "staged_units": len(drafts), "ids": sorted(drafts), "semantic_approval": "not_granted"}


def read_research_drafts(store,task,worker,token,ids=None,offset=0,limit=5):
    row=_check_lease(store,task,worker,token)
    require(type(offset) is int and offset>=0 and type(limit) is int and 1<=limit<=10,'Read 1..10 drafts per page')
    drafts=store.get_meta('research_drafts:'+task+':'+str(row['attempt']),{})
    keys=sorted(set(ids)) if ids is not None else sorted(drafts)
    require(set(keys)<=set(drafts),'Unknown draft knowledge ID')
    out=[];size=0
    for uid in keys[offset:offset+limit]:
        u=drafts[uid];length=len(canonical(u))
        if out and size+length>250000:break
        out.append({'unit':u,'unit_hash':digest(u)});size+=length
    return {'items':out,'total':len(keys),'next_offset':offset+len(out) if offset+len(out)<len(keys) else None,
            'drafts_digest':digest(drafts),'semantic_approval':'not_granted'}


def finish_research(store, task, worker, token, coverage, drafts_digest=None, progress_digest=None):
    """Validate staged structure/evidence and submit for actual semantic review."""
    from .knowledge import _validate_unit
    row = _check_lease(store, task, worker, token)
    key = "research_drafts:" + task + ":" + str(row["attempt"])
    drafts = store.get_meta(key, {})
    progress_key='progress-draft:'+task+':'+str(row['attempt'])
    progress=store.get_meta(progress_key)
    require((drafts or progress) and (not drafts or digest(drafts)==drafts_digest), "Research drafts changed or empty; use latest drafts_digest")
    require(not progress or digest(progress)==progress_digest,'Progress changed; use latest progress_digest')
    bundle = json.loads(row["data"])["bundle"]
    references = store.get_meta("order-references:" + str(bundle.get("plan_id")) + ":" + str(bundle.get("module")) + ":" + worker, {})
    from .whole import reference_units
    wanted={link['target'] for u in drafts.values() for link in u.get('knowledge_refs',[])}
    wanted.update(u['parent'] for u in drafts.values() if u.get('parent'))
    available = {**references, **reference_units(store,wanted), **store.units(), **drafts}
    binding = {"snapshot": row["snapshot"], "run": row["run"], "profile": row["profile"]}
    for unit in drafts.values():
        _validate_unit(store, unit, binding, available)
    result = submit(store, task, worker, token, {"coverage": coverage, "claims": [drafts[k] for k in sorted(drafts)],
        "capture": "mcp_staged_units", "capture_attempt": row["attempt"], "capture_lease_digest": digest(token),
        "drafts_digest": digest(drafts),**({'progress':progress} if progress else {})},
        expected_drafts=(key,digest(drafts)),expected_progress=(progress_key,progress_digest) if progress else None)
    return {"task": task, "status": result["status"], "units": len(drafts),
            "result_digest": digest(result["result"]), "semantic_approval": "not_granted"}


def submit(store, task, worker, token, result, *, expected_drafts=None, expected_progress=None):
    require(isinstance(result, dict) and isinstance(result.get("coverage"), list) and result["coverage"],
            "Research must account for its questions")
    with store.transaction():
        row = _check_lease(store, task, worker, token)
        if expected_drafts:
            require(digest(store.get_meta(expected_drafts[0], {})) == expected_drafts[1], "Research drafts changed during submission")
        if expected_progress:
            require(digest(store.get_meta(expected_progress[0]))==expected_progress[1],'Progress changed during submission')
        evidence = set()
        for item in result["coverage"]:
            require(isinstance(item,dict) and item.get("status") in {"answered", "open", "not_applicable"} and item.get("question"),
                    "Invalid coverage entry")
            require(item.get("explanation"), "Question explanation or concrete next step required")
            refs = item.get("evidence_refs", [])
            require(isinstance(refs,list) and all(isinstance(ref,str) for ref in refs),"coverage.evidence_refs must be a list of evidence IDs")
            if item["status"] == "answered":
                require(refs, "Answered question needs actual evidence")
            evidence.update(refs)
        for item in result.get("claims", []):
            evidence.update(item.get("source_refs", []))
        complete = _complete_reads(store, task, worker, token)
        if result.get('progress'):
            from .whole import validate_progress
            result={**result,'progress':validate_progress(store,task_status(store,task),result['progress'],
                    {u['id']:u for u in result.get('claims',[])},complete)}
        require(evidence <= complete, "Research references evidence not fully read with this lease")
        for ref in evidence:
            value = store.record("anchors", ref)
            require(store.evidence_in_scope(value, row["snapshot"]), "Research evidence snapshot mismatch")
            store.read_evidence(ref)
        result = {**result, "worker": worker, "task": task, "submitted": now(),
                  "database_execution": "not_run", "input_binding": digest(json.loads(row["data"]))}
        store.db.execute("UPDATE tasks SET status='submitted',result=?,token=NULL,deadline=NULL WHERE id=?",
                         (canonical(result), task))
        store.event("research_submit", {"task": task, "worker": worker})
    return task_status(store, task)


def review_task(store, task, review):
    require(review.get("mode") in {"self_reviewed", "independent_review"}, "Actual review mode required")
    require(review.get("verdict") in {"accept", "reject"} and review.get("reviewer") and review.get("notes"),
            "Actual review decision and notes required")
    with store.transaction():
        value = task_status(store, task)
        require(value["status"] == "submitted", "Task is not awaiting review")
        result = value["result"]
        require(review.get("result_digest") == digest(result), "Review result fingerprint mismatch")
        if review["mode"] == "independent_review":
            require(review["reviewer"] != result["worker"], "Independent review requires a different actor")
        status = "accepted" if review["verdict"] == "accept" else "needs_research"
        store.db.execute("UPDATE tasks SET status=? WHERE id=?", (status, task))
        store.event("research_review", {"task": task, **review})
        followups = []
        if status == "accepted":
            if result.get('progress'):
                from .whole import apply_reviewed_locked
                apply_reviewed_locked(store,value,result,review)
            for item in result["coverage"]:
                if item["status"] == "open":
                    followups.append(create_task(store, snapshot=value["snapshot"], run=value["run"], profile=value["profile"],
                        kind="gap_research", bundle={"parent": task, "module": value["bundle"].get("module"),
                                                    "plan_id": value["bundle"].get("plan_id"), "question": item["question"],
                                                    "next_step": item["explanation"], "source_anchor_refs": item.get("evidence_refs", [])}))
    return {**task_status(store, task), "followups": followups}


def task_context(store, task):
    value = task_status(store, task)
    refs = value["bundle"].get("source_anchor_refs", [])
    value["evidence"] = [store.record("anchors", ref) for ref in refs]
    value["known_revision"] = store.get_meta("knowledge_head")
    b = value["bundle"]
    attempt=value.get('attempt',0)
    drafts=store.get_meta('research_drafts:'+task+':'+str(attempt),{})
    progress=store.get_meta('progress-draft:'+task+':'+str(attempt))
    value['active_drafts']={'ids':sorted(drafts),'drafts_digest':digest(drafts),'read_with':'read_research_drafts returns full units and previous unit_hash values'}
    value['active_progress']={'report':progress,'progress_digest':digest(progress)} if progress else None
    value['review_feedback']=[json.loads(r[0]) for r in store.db.execute("SELECT data FROM events WHERE kind IN ('research_review','coordinator_review_synced') AND json_extract(data,'$.task')=? ORDER BY id DESC LIMIT 2",(task,))]
    value["coordinator_references"] = store.get_meta("order-references:" + str(b.get("plan_id")) + ":"
        + str(b.get("module")) + ":" + str(value.get("owner")), {})
    if store.get_meta('work_kit'):
        synced=store.get_meta('synced-references:'+store.get_meta('work_kit'),{})
        units=list(synced.get('units',{}).values())
        value['synced_reference_units']=[{k:u.get(k) for k in ('id','kind','title','conditions','source_refs','knowledge_refs')} for u in units[:100]]
        value['synced_references_truncated']=len(units)>100
        value['supplemental_materials']=synced.get('extra_materials',[])
    if value["kind"] in {"feature_research","module_survey"}:
        from .course import previous_research
        value["previous_research"] = previous_research(store,value)
    value["methods"] = []
    for row in store.db.execute("SELECT data FROM assets WHERE snapshot=? AND kind='method'", (value["snapshot"],)):
        method = json.loads(row[0])
        value["methods"].append({"asset": method["key"], "sha256": method["sha"], "status": method["status"]})
    candidates = set()
    for symbol in value["bundle"].get("symbol_refs", []):
        row = store.db.execute("SELECT logical FROM symbols WHERE run=? AND id=?", (value["run"], symbol)).fetchone()
        if row:
            candidates.update(r[0] for r in store.db.execute(
                "SELECT unit FROM unit_dependencies WHERE revision=? AND kind='symbol' AND ref=? LIMIT 201",
                (value["known_revision"], row[0])))
    value["reuse_candidates_truncated"] = len(candidates) > 200
    prior = store.units(value["known_revision"], ids=sorted(candidates)[:200])
    value["reuse_candidates"] = [{"id": u["id"], "kind": u["kind"], "title": u["title"]} for u in prior.values()]
    value["research_contract"] = {
        "required": ["coverage of each research question", "actual evidence reads", "conditions", "counterexamples", "open questions"],
        "tools": ["query_graph", "read_evidence", "find_knowledge", "explain_path"],
        "semantic_approval": "requires_actual_review", "runtime_validation": "not_run"}
    if store.get_meta('whole-for:'+str(b.get('plan_id'))):
        from .whole import guidance
        value['whole_learning']=guidance(store,value)
    if value["kind"] == "feature_research" and b.get("symbol_refs"):
        from .indexer import query_graph
        seeds = b.get("seed_symbol_refs", b["symbol_refs"])[:12]
        graph = query_graph(store,value["run"],seeds,kinds=["CALLS"],direction="both",depth=1,limit=12)
        value["call_sites"] = {"depth":1,"truncated":graph["truncated"],
            "symbols":[{k:n.get(k) for k in ("id","name","asset")} for n in graph["nodes"]],
            "relations":[{k:e.get(k) for k in ("source","target","asset","evidence","resolution","target_binding")} for e in graph["relations"]]}
    if value["kind"] == "module_survey":
        value["research_contract"]["required"].append("按用户可观察行为列候选特性、入口、源码/手册线索和遗漏项。后续用 focus_module 按特性建任务。")
    value["dependency_results"] = []
    for dep in value["dependencies"]:
        child = task_status(store, dep)
        if child.get("result"):
            result = child["result"]
            value["dependency_results"].append({"task": dep, "status": child["status"], "result_digest": digest(result),
                "coverage": result["coverage"], "claims": result.get("claims", []),
                "expand_with": {"tool": "task_context", "task": dep}})
    return value


def create_task_evidence(store, task, worker, token, asset, start, end):
    with store.transaction():
        row = _check_lease(store, task, worker, token)
        material = store.asset(row["snapshot"], asset)
        result = store.anchor(row["snapshot"], asset, start, end, text_sha=material.get("text_sha"))
        store.event("task_evidence_anchor", {"task": task, "worker": worker, "evidence": result["id"]})
    return result
