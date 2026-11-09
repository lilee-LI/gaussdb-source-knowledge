"""Offline module work orders. Each host uses its own checkout, Python and SQLite."""
import gzip
from copy import deepcopy
import hashlib
import hmac
import json
from pathlib import Path
import platform
import secrets

from . import tu_cache
from .indexer import build_index, compiler_arguments, tool_identity
from .knowledge import _validate_unit, content_hash, propose
from .planner import create_task, task_status
from .store import atomic_write, canonical, digest, identity, now, read_json, require
from .study import current


def assignment_key(plan, module):
    return "assignment:" + plan + ":" + module


def reference_context(store, plan, module, requested):
    revision = store.get_meta("knowledge_head")
    require(revision or not requested, "There is no accepted knowledge revision for these references")
    if not revision:
        return {}
    require(len(requested) <= 24, "At most 24 explicit references per work order")
    files = set(plan["modules"][module]["files"])
    ids = set(requested)
    for row in store.db.execute("SELECT DISTINCT a.unit,e.asset FROM alignments a JOIN anchors e ON e.id=a.anchor "
                                "WHERE a.revision=? ORDER BY a.unit", (revision,)):
        if row["asset"] in files and len(ids) < max(12, len(requested)):
            ids.add(row["unit"])
    units = store.units(revision, ids=sorted(ids))
    require(set(requested) <= set(units), "Unknown reference knowledge ID")
    refs = {}
    for uid, unit in units.items():
        item = {k: unit.get(k) for k in ("id", "kind", "title", "body", "conditions", "counterexamples", "knowledge_refs")}
        item["binding"] = {k: unit.get("_binding", {}).get(k) for k in ("snapshot", "profile", "run")}
        item["content_hash"] = content_hash(unit)
        item["citations"] = [{k: a[k] for k in ("asset", "start", "end", "asset_sha", "quote_sha256")}
                             for r in unit.get("source_refs", []) for a in [store.record("anchors", r)]]
        refs[uid] = item
    return refs


def assign(store, module, worker, output, replace=False, references=()):
    plan = current(store)
    require(module in plan["modules"] and worker.strip(), "Choose a listed module and a named worker")
    if plan.get("source_index"):
        require(Path(output).suffix.lower() == ".json", "Use a .json file for the work order")
    key = assignment_key(plan["id"], module)
    with store.transaction():
        old = store.get_meta(key)
        if old and old["worker"] == worker and not replace:
            ticket = old["ticket"]
            require(set(references) <= set(ticket["references"]), "Changed references require a new work order (--replace)")
        else:
            require(not old or replace, "Module already assigned; reassignment requires --replace")
            ticket = {"schema": "module-order/v1", "plan": plan["id"], "snapshot": plan["snapshot"],
                      "module": module, "worker": worker, "material_signature": plan["material_signature"],
                      "membership": digest(plan["modules"][module]["files"]), "profile": plan["profile"],
                      "source_index":plan.get("source_index"),
                      "base_revision": store.get_meta("knowledge_head"),
                      "references": reference_context(store, plan, module, references),
                      "secret": secrets.token_hex(32)}
            ticket["id"] = identity("assignment", ticket)
            store.set_meta(key, {"id": ticket["id"], "worker": worker, "ticket": ticket})
            store.set_meta(ticket["id"], key)
            store.event("module_assigned", {"plan": plan["id"], "module": module, "worker": worker,
                                            "id": ticket["id"], "previous": old and old["id"]})
    atomic_write(output, canonical(ticket))
    return {"assignment": ticket["id"], "module": module, "worker": worker, "order_file": str(output),
            "next": ("把模块包交给成员，在独立工作目录执行 team open --kit。" if plan.get("source_index") else
                     "在工作服务器配置相同版本的本地材料，执行 team open --order 工作单。")}


def open_order(store, order):
    ticket = read_json(order)
    expected = dict(ticket)
    tid = expected.pop("id")
    require(ticket.get("schema") == "module-order/v1" and identity("assignment", expected) == tid,
            "Work order fingerprint mismatch")
    plan = current(store)
    module = ticket["module"]
    require(plan["material_signature"] == ticket["material_signature"], "Worker source/documents/methods differ from work order")
    require(module in plan["modules"] and digest(plan["modules"][module]["files"]) == ticket["membership"],
            "Worker module partition differs from coordinator; configure matching module prefixes")
    require(plan["profile"] == ticket["profile"] and plan.get("source_index") == ticket.get("source_index"),
            "Worker build profile or ECS run differs from work order")
    with store.transaction():
        store.set_meta("local-order:" + tid, {"ticket": ticket, "plan": plan["id"]})
        store.set_meta("order-references:" + plan["id"] + ":" + module + ":" + ticket["worker"], ticket["references"])
    return {"assignment": tid, "module": module, "worker": ticket["worker"], "task": plan["modules"][module]["task"],
            "local_snapshot": plan["snapshot"], "base_revision": ticket["base_revision"], "reference_units": list(ticket["references"]),
            "next": ("用 guide --module 查看入口，用 focus 在已有 ECS 索引上选择特性，使用工作单身份领取任务并提交。" if plan.get("source_index") else
                     "可直接研究模块清单，也可用 focus 选择 TU。使用工作单上的 worker 身份领取任务并提交研究。")}


def _refs(result):
    refs={r for c in result["coverage"] for r in c.get("evidence_refs", [])} | {
        r for c in result.get("claims", []) for r in c.get("source_refs", [])}
    refs.update(r for section in result.get('progress',{}).values() if isinstance(section,list)
                for item in section if isinstance(item,dict) for r in item.get('evidence_refs',[]))
    return refs


def _environment(store, snapshot, profile):
    snap = store.record("snapshots", snapshot)
    roots = {m["id"]: Path(m["root"]) for m in snap["materials"] if m["kind"] == "source"}
    return roots, store.profile(snapshot, profile), tool_identity()


def _tu_signature(entry, args, roots, binding, tools):
    def portable_path(path):
        value = Path(path)
        for repo, root in sorted(roots.items(), key=lambda i: -len(str(i[1]))):
            if value.is_relative_to(root):
                return "@repo/" + repo + "/" + value.relative_to(root).as_posix()
        return path
    portable = []
    path_next = False
    for arg in args:
        if path_next:
            portable.append(portable_path(arg))
            path_next = False
        elif arg.startswith("-I") and len(arg) > 2:
            portable.append("-I" + portable_path(arg[2:]))
        elif arg.startswith("--sysroot="):
            portable.append("--sysroot=" + portable_path(arg.split("=", 1)[1]))
        else:
            portable.append(arg)
            path_next = arg in {"-I", "-isystem", "-iquote", "-include", "-imacros", "-isysroot", "--sysroot"}
    return digest([entry["file"], portable, entry["arguments"][:1],
                   binding.get("toolchain"), tools["clang_worker"], tools["libclang"],
                   platform.system(), platform.machine(), tu_cache.environment()])


def _signed(secret, payload):
    return hmac.new(bytes.fromhex(secret), canonical(payload).encode("utf-8"), hashlib.sha256).hexdigest()


def _read_packet(path):
    """Limit decompression without reserving 256 MiB for every tiny module packet."""
    blocks=[];length=0
    with gzip.open(path,'rb') as stream:
        while True:
            block=stream.read(1024*1024)
            if not block:break
            length+=len(block);require(length<=256*1024**2,'Split this packet into smaller module batches')
            blocks.append(block)
    return json.loads(b''.join(blocks))


def learning_projection(store, plan, module):
    """Small learning-state projection inside the existing signed kit/feedback.

    It preserves coordinator identities. Only the assigned module's packages and
    physical implementation obligations travel; no second graph or queue exists.
    """
    from . import curriculum, whole
    course = curriculum.current(store)
    program = whole.current(store, False)
    if not course or not program:
        return None
    packages = [deepcopy(p) for p in course['packages'] if p['module'] == module]
    needed = {fid for p in packages for fid in p.get('feature_ids', [])}
    selected = deepcopy(course)
    selected.update(packages=packages,
        features=[deepcopy(f) for f in course['features'] if f['id'] in needed or module in f.get('module_candidates', [])],
        mainlines=[deepcopy(m) for m in course['mainlines'] if module in m.get('modules', [])],
        worker_scope=module,
        projection={'module': module, 'coordinator_revision': course['revision'], 'coordinator_run': plan['run']})
    items = [dict(r) for r in store.db.execute('SELECT * FROM implementation_items WHERE program=? AND module=? ORDER BY asset,start', (program['id'], module))]
    dispositions = [dict(r) for r in store.db.execute('SELECT d.* FROM implementation_dispositions d JOIN implementation_items i '
        'ON i.program=d.program AND i.id=d.item JOIN learning_reports r ON r.id=d.report '
        "WHERE d.program=? AND i.module=? AND json_extract(r.data,'$.review.verdict')='accept'", (program['id'], module))]
    report_ids = {d['report'] for d in dispositions}
    reports = [dict(r) for r in store.db.execute('SELECT * FROM learning_reports WHERE program=?', (program['id'],)) if r['id'] in report_ids]
    return {'schema': 'module-learning-projection/v1', 'plan': plan['id'], 'snapshot': plan['snapshot'],
        'program': program['id'], 'module': module, 'inputs': deepcopy(store.get_meta('learning_inputs')),
        'curriculum': selected, 'implementation_items': items, 'implementation_dispositions': dispositions,
        'implementation_reports': reports,
        'implementation_index': deepcopy(store.get_meta('implementation-index:' + program['id']))}


def apply_learning_projection(store, value, plan, module, mapping):
    """Apply only coordinator-signed, module-bounded curriculum state."""
    if not value:
        return
    from . import implementation, whole
    require(value.get('schema') == 'module-learning-projection/v1' and
        (value['plan'], value['snapshot'], value['module']) == (plan['id'], plan['snapshot'], module), 'Learning projection outside assignment')
    program = whole.current(store)
    require(value['program'] == program['id'], 'Learning projection program changed')
    course = deepcopy(value['curriculum'])
    require((course['plan_id'], course['snapshot'], course['program']) == (plan['id'], plan['snapshot'], program['id']) and
        all(p['module'] == module and set(p['files']) <= set(plan['modules'][module]['files']) for p in course['packages']), 'Curriculum package outside assigned module')
    for package in course['packages']:
        package['tasks'] = [mapping.get(t, t) for t in package.get('tasks', [])]
        package['depends_on'] = [mapping.get(t, t) for t in package.get('depends_on', [])]
    for mainline in course['mainlines']:
        mainline['task'] = mapping.get(mainline.get('task'), mainline.get('task'))
    course['run'] = plan['run']
    if value.get('inputs') is not None:
        old = store.get_meta('learning_inputs')
        require(not old or old.get('digest') == value['inputs'].get('digest'), 'Learning input manifest changed; request a new kit')
        store.set_meta('learning_inputs', value['inputs'])
    for statement in implementation.SCHEMA.split(';'):
        if statement.strip():store.db.execute(statement)
    allowed = set(plan['modules'][module]['files'])
    known = set()
    for row in value['implementation_items']:
        data = json.loads(row['data'])
        require(row['program'] == program['id'] and row['module'] == module and row['asset'] in allowed and
            (data['id'], data['asset'], data['module'], data['start'], data['end']) ==
            (row['id'], row['asset'], module, row['start'], row['end']), 'Implementation item outside assignment')
        old = store.db.execute('SELECT data FROM implementation_items WHERE program=? AND id=?', (program['id'], row['id'])).fetchone()
        require(not old or old[0] == row['data'], 'Immutable implementation partition changed; request a new kit')
        store.db.execute('INSERT OR IGNORE INTO implementation_items VALUES(?,?,?,?,?,?,?)', tuple(row[k] for k in ('program','id','asset','module','start','end','data')))
        known.add(row['id'])
    reviewed = set()
    for row in value.get('implementation_reports', []):
        data = json.loads(row['data'])
        require(row['program'] == program['id'] and data['module'] == module and
            data.get('review', {}).get('verdict') == 'accept' and data['id'] == row['id'], 'Implementation report lacks coordinator review')
        data['task'] = mapping.get(data['task'], data['task'])
        store.db.execute('INSERT OR IGNORE INTO learning_reports VALUES(?,?,?,?,?)',
            (row['id'], program['id'], data['task'], row['result_digest'], canonical(data)))
        reviewed.add(row['id'])
    for row in value['implementation_dispositions']:
        require(row['program'] == program['id'] and row['item'] in known and row['report'] in reviewed, 'Implementation review outside assignment')
        store.db.execute('INSERT OR REPLACE INTO implementation_dispositions VALUES(?,?,?,?)', tuple(row[k] for k in ('program','item','report','data')))
    index = value.get('implementation_index')
    if index:
        store.set_meta('implementation-index:' + program['id'], {**index, 'items': len(known),
            'cpp_files': len({r['asset'] for r in value['implementation_items']}), 'projection': module})
    store.set_meta(course['id'], course)
    store.set_meta('curriculum_head', course['id'])


def _task_scope(task):
    # Receipt metadata and rebound anchors may change on round-trip. Every
    # remaining native planning field (including budgets/closure issues) is scope.
    transport = {'base_knowledge_revision','coordinator_task','order','receipt','reference_epoch','source_anchor_refs'}
    return {'kind': task['kind'], 'profile': task['profile'],
            'bundle': {key:value for key,value in task['bundle'].items() if key not in transport}}


def _delegation(store, ticket, task, result, coordinator):
    if result['worker'] == ticket['worker']:
        return None
    worker = result['worker']
    auth = store.get_meta('dispatch-actor:' + worker, {})
    batch = store.get_meta('dispatch:' + auth.get('batch',''), {})
    child = next((c for c in batch.get('children', []) if c['worker'] == worker), None)
    plan = current(store)
    binding = (plan['snapshot'],plan['run'],plan['id'])
    require(child and (auth.get('active') or batch.get('closed')) and auth.get('worker') == worker and auth.get('principal_worker') == batch.get('principal_worker') == ticket['worker'] and
        auth.get('batch') == batch.get('id') and auth.get('parent_session') == batch.get('parent_session') and
        (auth.get('snapshot'),auth.get('run'),auth.get('plan')) == binding ==
        (batch.get('snapshot'),batch.get('run'),batch.get('plan')) ==
        (task['snapshot'],task['run'],task['bundle'].get('plan_id')) and
        (ticket['snapshot'],ticket['plan']) == (plan['snapshot'],plan['id']) and
        ticket['module'] in batch.get('modules', []) and task['bundle'].get('module') == ticket['module'] and
        task['id'] in auth.get('allowed_tasks', []), 'Invalid or stale persisted assignment delegate/task grant')
    # Closing a batch revokes future claims. A lease acquired before closure may
    # still finish when close did not release it; bind the claim and exact lease.
    from .assistant_session import handle_file
    path = handle_file(store.home,child['session'])
    handle = read_json(path) if path.is_file() else {}
    require(handle.get('session') == child['session'] and handle.get('worker') == worker and
        handle.get('snapshot') == task['snapshot'] and handle.get('batch') == batch['id'] and
        handle.get('parent_session') == batch['parent_session'], 'Historical delegate session binding mismatch')
    native = store.record('tasks',task['id'])
    attempt = result.get('capture_attempt')
    require(task['owner'] == worker and task['status'] in {'submitted','accepted'} and result.get('task') == task['id'] and
        result.get('capture') == 'mcp_staged_units' and type(attempt) is int and attempt == task['attempt'] and attempt > 0 and
        result.get('input_binding') == digest(native) and result.get('drafts_digest') == digest(store.get_meta('research_drafts:'+task['id']+':'+str(attempt),{})),
        'Historical delegate result lacks exact native submission/capture proof')
    submitted = result.get('submitted','')
    claim = store.db.execute("SELECT id,created,data FROM events WHERE kind='task_claim' AND json_extract(data,'$.task')=? "
        "ORDER BY id DESC LIMIT 1",(task['id'],)).fetchone()
    require(claim and json.loads(claim['data']).get('worker')==worker and
        isinstance(submitted,str) and batch['created'] <= claim['created'] <= submitted and
        (not batch.get('closed') or claim['created'] <= batch.get('closed_at','')),
        'Delegate task claim occurred outside the authorized batch lifetime')
    receipt = store.db.execute("SELECT id FROM events WHERE kind='research_submit' AND json_extract(data,'$.task')=? "
        "AND json_extract(data,'$.worker')=? AND created>=? ORDER BY id DESC LIMIT 1",(task['id'],worker,submitted)).fetchone()
    lease_digest = result.get('capture_lease_digest')
    active = handle.get('active') or {}
    token_proof = active.get('task') == task['id'] and active.get('attempt') == attempt and digest(active.get('token')) == lease_digest
    if not token_proof:
        token_proof = any(digest(json.loads(row[0]).get('token')) == lease_digest for row in store.db.execute(
            "SELECT data FROM events WHERE kind='evidence_read' AND json_extract(data,'$.task')=? AND json_extract(data,'$.worker')=?",(task['id'],worker)))
    require(receipt and isinstance(lease_digest,str) and len(lease_digest)==64 and token_proof,
        'Historical delegate native lease/submission receipt mismatch')
    return {'schema': 'module-delegation/v1', 'assignment': ticket['id'], 'principal_worker': ticket['worker'],
        'worker': worker, 'batch': batch['id'], 'parent_session': auth['parent_session'], 'child_session': child['session'],
        'active': bool(auth.get('active') and not batch.get('closed')), 'authorization':'submitted_native_result',
        'batch_created':batch['created'],'batch_closed_at':batch.get('closed_at'),
        'native_submission':{'digest':digest(result),'submitted':submitted,'capture':result['capture'],'attempt':attempt,
            'input_binding':result['input_binding'],'lease_digest':lease_digest,'drafts_digest':result['drafts_digest'],'receipt':receipt['id'],
            'claim_receipt':claim['id'],'claimed':claim['created']},
        'snapshot': ticket['snapshot'], 'plan': ticket['plan'], 'profile': ticket['profile'],
        'module': ticket['module'], 'origin_task': task['id'], 'origin_run': task['run'], 'coordinator_task': coordinator,
        'task_scope': _task_scope(task)}


def _validate_remote_actor(ticket, data):
    require(data.get('principal_worker', data['worker']) == ticket['worker'], 'Assignment principal mismatch')
    scope=data.get('task_scope')
    if scope:
        require(scope.get('kind')==data.get('task_kind') and scope.get('profile')==ticket['profile'] and
            scope.get('bundle',{}).get('plan_id')==ticket['plan'] and
            scope.get('bundle',{}).get('module')==ticket['module'], 'Native task scope outside assignment')
    if data['worker'] == ticket['worker']:
        require(not data.get('delegation'), 'Principal submission must not impersonate a delegated child')
        return
    grant = data.get('delegation') or {}
    capture=grant.get('native_submission') or {}
    submitted=capture.get('submitted','')
    require(isinstance(scope,dict) and grant.get('schema') == 'module-delegation/v1' and
        grant.get('authorization')=='submitted_native_result' and capture.get('digest')==data.get('submission_digest') and
        capture.get('capture')=='mcp_staged_units' and type(capture.get('attempt')) is int and capture['attempt']>0 and
        all(isinstance(capture.get(k),str) and len(capture[k])==64 for k in ('input_binding','lease_digest','drafts_digest')) and
        type(capture.get('receipt')) is int and capture['receipt']>0 and type(capture.get('claim_receipt')) is int and capture['claim_receipt']>0 and
        isinstance(submitted,str) and isinstance(capture.get('claimed'),str) and isinstance(grant.get('batch_created'),str) and
        grant['batch_created']<=capture['claimed']<=submitted and
        (not grant.get('batch_closed_at') or capture['claimed']<=grant['batch_closed_at']) and
        data.get('origin_snapshot') == ticket['snapshot'] and
        all(grant.get(key) == expected for key, expected in {
            'assignment':ticket['id'], 'principal_worker':ticket['worker'], 'worker':data['worker'],
            'snapshot':ticket['snapshot'], 'plan':ticket['plan'], 'profile':ticket['profile'], 'module':ticket['module'],
            'origin_task':data['origin_task'], 'origin_run':data['origin_run'], 'coordinator_task':data.get('coordinator_task'),
            'task_scope':data.get('task_scope')}.items()) and grant.get('batch') and grant.get('parent_session') and grant.get('child_session'),
        'Invalid or stale assignment delegation')


def export_result(store, order, task, output):
    local = open_order(store, order)
    ticket = store.get_meta("local-order:" + local["assignment"])["ticket"]
    if ticket.get("source_index"):
        require(Path(output).suffix.lower() == ".gz", "Use a .gz file for the result packet")
    t = task_status(store, task)
    require(t["snapshot"] == local["local_snapshot"] and t["bundle"].get("module") == ticket["module"] and
            t["status"] in {"submitted", "accepted"}, "Export a submitted research task for the assigned module")
    result = t["result"]
    require(t["profile"] == ticket["profile"], "Worker profile mismatch")
    from .curriculum import current as curriculum_current
    course = curriculum_current(store)
    require(not course or not course.get('projection') or course['revision'] == course['projection']['coordinator_revision'],
            'Local curriculum refinements require coordinator reconciliation; sync the coordinator plan before exporting')
    coordinator = t['bundle'].get('coordinator_task') or next((k for k,v in store.get_meta('coordinator-task-map',{}).items() if v==task),None)
    delegation = _delegation(store, ticket, t, result, coordinator)
    run = store.record("runs", t["run"])
    require(run.get("mode") in {"inventory", "selected", "ecs", "ecs_module",'source_only'}, "Work orders return bounded module results")
    evidence = {r: store.record("anchors", r) for r in _refs(result)}
    for ref, anchor in evidence.items():
        receipt = store.db.execute("SELECT 1 FROM events WHERE kind='evidence_read' AND json_extract(data,'$.task')=? "
            "AND json_extract(data,'$.worker')=? AND json_extract(data,'$.evidence')=? "
            "AND json_extract(data,'$.quote_sha256')=? AND json_extract(data,'$.truncated')=0",
            (task, result["worker"], ref, anchor["quote_sha256"])).fetchone()
        reuse={r for item in result.get('progress',{}).get('assets',[]) if item.get('reuse') for r in item.get('evidence_refs',[])}
        require((receipt or ref in reuse) and store.evidence_in_scope(anchor, t["snapshot"]), "Missing worker evidence receipt")
    symbols = {}
    stack = list(result.get("claims", []))
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
        elif isinstance(value, str) and value.startswith(("symbol-instance:", "symbol:", "syntax:")) and value not in symbols:
            rows = store.lookup_symbols(run["id"],value,names=False,limit=1)
            require(rows, "Unknown research symbol " + value)
            symbols[value] = rows[0]["logical"]
    if not ticket.get("source_index"):
        roots, binding, tools = _environment(store, t["snapshot"], t["profile"])
        commands = {identity("tu", [binding["repository"], e]): e for e in binding["commands"]}
    parts = []
    for tu in ([] if ticket.get("source_index") else run["tu_results"]):
        entry = commands[tu["context"]]
        args = compiler_arguments(entry, binding, roots, roots)
        signature = _tu_signature(entry, args, roots, binding, tools)
        row = store.db.execute("SELECT data FROM tu_cache WHERE key=?", (tu.get("cache_key"),)).fetchone()
        parts.append({"signature": signature, "file": entry["file"], "facts": json.loads(row[0]) if row else None})
    data = {"schema": "module-result/v1", "order": ticket["id"], "origin_task": task, "worker": result["worker"],
            "origin_snapshot": t["snapshot"], "origin_run": run["id"], "profile": t["profile"],
            "selected_files": t["bundle"].get("selected_files", []) if ticket.get("source_index") else run.get("selected_files") or [],
            "source_index":ticket.get("source_index"), "parts": parts, "symbols": symbols,
            "evidence": evidence, "coverage": result["coverage"], "claims": result.get("claims", []),
            **({"candidate_id":t["bundle"]["candidate_id"]} if t["bundle"].get("candidate_id") else {}),
            "submission_digest": digest(result)}
    data.update(task_kind=t['kind'],coordinator_task=coordinator,program_item=t['bundle'].get('program_item'),
                question=t['bundle'].get('question'),progress=result.get('progress'),
                reference_epoch=store.get_meta('synced-references:'+ticket['id'],{}).get('epoch'),
                principal_worker=ticket['worker'],delegation=delegation,task_scope=_task_scope(t),
                curriculum_revision=course and course.get('projection',{}).get('coordinator_revision',course['revision']))
    packet = {"data": data, "hmac": _signed(ticket["secret"], data)}
    atomic_write(output, gzip.compress(canonical(packet).encode("utf-8"), mtime=0))
    return {"file": str(output), "module": ticket["module"], "claims": len(data["claims"]),
            "result_digest": digest(data), "next": "将结果文件交给协调端，执行 team receive。"}


def _translate(value, mapping):
    if isinstance(value, dict):
        return {k: _translate(v, mapping) for k, v in value.items()}
    if isinstance(value, list):
        return [_translate(v, mapping) for v in value]
    if isinstance(value, str):
        if value in mapping:
            return mapping[value]
        require(not value.startswith(("symbol-instance:", "evidence:")), "Unmapped worker reference: " + value)
    return value


def _check_conflicts(store, ticket, claims, epoch=None):
    ids = {c["id"] for c in claims}
    for unit in claims:
        ids.update(link["target"] for link in unit.get("knowledge_refs", []))
        if unit.get("parent"):
            ids.add(unit["parent"])
        expected = unit.get("expected_from", {})
        if expected and expected.get("kind") != "source_prediction":
            ids.add(expected["ref"])
    base = store.units(ticket["base_revision"], ids=sorted(ids)) if ticket["base_revision"] else {}
    current = store.units(ids=sorted(ids))
    issued=store.get_meta('issued-reference:'+ticket['id']+':'+str(epoch)) if epoch else None
    require(not epoch or issued,'Unknown coordinator reference epoch')
    for uid in ids:
        expected=issued['hashes'].get(uid) if issued and uid in issued['hashes'] else content_hash(base[uid]) if uid in base else None
        require(expected == (content_hash(current[uid]) if uid in current else None),
                "Knowledge changed since assignment; reconcile unit: " + uid)


def receive(store, path, jobs=2):
    packet = _read_packet(path)
    data = packet["data"]
    key = store.get_meta(data["order"])
    active = store.get_meta(key) if key else None
    require(active and active["id"] == data["order"], "Unknown or superseded assignment")
    ticket = active["ticket"]
    require(data.get("schema") == "module-result/v1" and hmac.compare_digest(packet["hmac"], _signed(ticket["secret"], data)),
            "Module result is damaged or belongs to a different work order")
    plan = current(store)
    require(ticket["plan"] == plan["id"] and ticket["snapshot"] == store.get_meta("snapshot_head") and
            ticket["profile"] == data["profile"], "Stale plan, worker or profile")
    _validate_remote_actor(ticket, data)
    from . import curriculum
    course = curriculum.current(store)
    require(not course or data.get('curriculum_revision') == course['revision'], 'Curriculum changed; synchronize coordinator feedback before importing research')
    receipt_id = identity("module-receipt", data)
    existing = store.get_meta(receipt_id)
    if existing:
        return {**existing, "replayed": True}
    _check_conflicts(store, ticket, data["claims"],data.get('reference_epoch'))
    snapshot, profile = plan["snapshot"], plan["profile"]
    run = store.record("runs", plan["run"])
    files = data["selected_files"]
    if plan.get("source_index"):
        require(ticket.get("source_index") == data.get("source_index") == plan["source_index"] and
                data["origin_snapshot"] == ticket["snapshot"] and not data["parts"],
                "Worker result must use the assigned ECS graph")
    elif files:
        require(len(files) <= 100 and len(set(files)) == len(files), "Invalid TU selection")
        roots, binding, tools = _environment(store, snapshot, profile)
        available = {}
        if profile != "unknown":
            for entry in (e for e in binding["commands"] if e["file"] in files):
                args = compiler_arguments(entry, binding, roots, roots)
                sig = _tu_signature(entry, args, roots, binding, tools)
                available[sig] = entry, args
            require(set(available) == {p["signature"] for p in data["parts"]}, "Worker compilation settings or frontend differ")
        with store.transaction():
            for part in data["parts"]:
                entry, args = available[part["signature"]]
                facts = part["facts"]
                if facts and facts["status"] == "parsed" and tu_cache.valid(store, snapshot, facts):
                    src = store.asset(snapshot, binding["repository"] + "/" + entry["file"])
                    cache_id = tu_cache.parse_key(binding["repository"], entry, args, binding, tools, src["sha"])
                    store.db.execute("INSERT OR IGNORE INTO tu_cache VALUES(?,?)", (cache_id, canonical(facts)))
        run = build_index(store, snapshot, profile, files=files, jobs=jobs, resume=True)
    with store.transaction():
        require(store.get_meta("snapshot_head") == snapshot and store.get_meta("study_head") == ticket["plan"],
                "Coordinator inputs changed during receipt")
        active = store.get_meta(key)
        require(active["id"] == ticket["id"], "Assignment changed during receipt")
        if store.get_meta(receipt_id):
            return {**store.get_meta(receipt_id), "replayed": True}
        _check_conflicts(store, ticket, data["claims"],data.get('reference_epoch'))
        mapping = {}
        for ref, a in data["evidence"].items():
            require(a["id"] == ref and (a["snapshot"] == data["origin_snapshot"] or (plan.get("source_index") and
                    a["snapshot"] == plan["source_index"]["snapshot"] and a["view"] == "source")), "Worker evidence binding mismatch")
            asset = store.asset(snapshot, a["asset"])
            require(asset["sha"] == a["asset_sha"], "Source version mismatch: " + a["asset"])
            expected = asset.get("text_sha") if a["view"] == "extracted" else None
            require(a["sha"] == (expected or asset["sha"]), "Evidence view mismatch")
            mapped = store.anchor(snapshot, a["asset"], a["start"], a["end"], text_sha=expected)
            require(mapped["quote_sha256"] == a["quote_sha256"], "Evidence excerpt mismatch")
            # Kits share the coordinator snapshot/global ECS origin. Preserve an
            # already valid content-addressed anchor identity so round-trip
            # reference hashes do not change merely because of canonicalization.
            if store.evidence_in_scope(a,snapshot) and identity('evidence',{k:v for k,v in a.items() if k!='id'})==ref:
                store.db.execute('INSERT OR IGNORE INTO main.anchors VALUES(?,?,?,?,?,?,?)',(ref,a['snapshot'],a['asset'],a['sha'],a['start'],a['end'],canonical(a)))
                mapping[ref]=ref
            else:mapping[ref] = mapped["id"]
        for sid, logical in data["symbols"].items():
            if plan.get("source_index"):
                # A module kit keeps ECS instance IDs. One logical symbol may have multiple definitions or declarations.
                row = store.db.execute("SELECT 1 FROM symbols WHERE run=? AND logical=? AND (id=? OR logical=?) LIMIT 1",
                                       (run["id"],logical,sid,sid)).fetchone()
                require(row, "Worker ECS symbol binding differs from coordinator: " + sid)
                mapping[sid] = sid
                continue
            row = store.db.execute("SELECT id FROM symbols WHERE run=? AND logical=? LIMIT 1", (run["id"],logical)).fetchone()
            require(row, "Worker symbol missing from coordinator graph: " + logical)
            mapping[sid] = row[0]
        claims = _translate(data["claims"], mapping)
        cid = data.get("candidate_id")
        if cid:
            from .catalog import candidate
            lead=candidate(plan,cid,store)
        prior_origin=active.get('origins',{}).get(data['origin_task'])
        other=None
        target=data.get('coordinator_task') or (prior_origin or {}).get('task')
        if not target and data.get('task_kind')=='module_survey':target=plan['modules'][ticket['module']]['task']
        if not target and data.get('program_item'):
            target=next((t['id'] for t in (dict(r) for r in store.db.execute("SELECT id,data FROM tasks WHERE snapshot=?",(snapshot,)))
                         if json.loads(t['data'])['bundle'].get('plan_id')==plan['id'] and json.loads(t['data'])['bundle'].get('program_item')==data['program_item']),None)
        if not target and data.get('task_scope',{}).get('bundle',{}).get('program_id'):
            for row in store.db.execute("SELECT id FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? "
                "AND json_extract(data,'$.bundle.module')=?",(snapshot,plan['id'],ticket['module'])):
                if _task_scope(task_status(store,row['id']))==data['task_scope']:
                    target=row['id'];break
            require(target or cid,'Coordinator has not scheduled this native learning task; advance the coordinator plan and synchronize feedback before exporting local continuations')
        if target:
            other=store.db.execute('SELECT id,status,attempt,data FROM tasks WHERE id=?',(target,)).fetchone()
            require(other and other['status'] in {'queued','needs_research'} and json.loads(other['data'])['bundle'].get('module')==ticket['module'],
                    'Coordinator task is active, submitted, accepted, or outside this module')
            if data.get('task_scope'):
                require(_task_scope(task_status(store,target)) == data['task_scope'], 'Worker native task identity/scope differs from coordinator')
        elif cid:
            from .catalog import candidate
            lead = candidate(plan,cid,store)
            require(lead["owner_module"] in (None,ticket["module"]),"Candidate belongs to a different module")
            other = store.db.execute("SELECT id,status,attempt,data FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? "
                        "AND json_extract(data,'$.bundle.candidate_id')=?",(snapshot,plan["id"],cid)).fetchone()
            if other:
                require(other["status"] in {'queued','needs_research'} and
                        json.loads(other["data"])["bundle"]["module"]==ticket["module"],
                        "Candidate already has active or reviewed work; resolve it before importing another result")
        coverage = _translate(data["coverage"], mapping)
        require(coverage and all(c.get("question") and c.get("explanation") and c.get("status") in
            {"answered","open","not_applicable"} and (c["status"] != "answered" or c.get("evidence_refs")) for c in coverage),
            "Invalid remote research coverage")
        available = {**store.units(), **{c["id"]: c for c in claims}}
        require(len(set(c["id"] for c in claims)) == len(claims), "Duplicate imported unit")
        for c in claims:
            _validate_unit(store, c, {"snapshot": snapshot, "run": run["id"]}, available)
        bundle={"module":ticket["module"],"plan_id":plan["id"],"order":ticket["id"],"receipt":receipt_id,
                **({"candidate_id":cid} if cid else {}),"question":lead["question"] if cid else "审阅模块发现、跨模块边界和缺口",
                "source_anchor_refs":list(mapping[r] for r in data["evidence"])}
        if data.get('program_item'):bundle['program_item']=data['program_item']
        bundle['reference_epoch']=data.get('reference_epoch')
        if other:
            tid = other["id"]
            prior = json.loads(other["data"])
            bundle['question'] = prior['bundle'].get('question', bundle['question'])
            prior["bundle"].update(bundle)
            store.db.execute("UPDATE tasks SET data=? WHERE id=?",(canonical(prior),tid))
        else:
            tid = create_task(store,snapshot=snapshot,run=run["id"],profile=profile,kind=data.get('task_kind') or "remote_module_research",bundle=bundle)
        result = {"worker": data["worker"], "task": tid, "submitted": now(), "coverage": coverage, "claims": claims,
                  "remote_submission": data["submission_digest"], "origin_task": data["origin_task"],
                  "read_provenance": "worker_receipts_rebound_to_coordinator_evidence", "database_execution": "not_run"}
        if data.get('delegation'):
            result.update(principal_worker=ticket['worker'], delegation=data['delegation'])
        if data.get('progress'):
            from .whole import validate_progress
            result['progress']=validate_progress(store,task_status(store,tid),_translate(data['progress'],mapping),
                       {u['id']:u for u in claims},set(mapping[r] for r in data['evidence']),imported=True)
        require(not store.db.execute("SELECT 1 FROM task_edges e JOIN tasks d ON e.dependency=d.id WHERE e.task=? AND d.status<>'accepted'",(tid,)).fetchone(),
                'Coordinator prerequisites are not accepted; import and review upstream work first')
        require(not curriculum.prerequisites(store,task_status(store,tid)),
                'Coordinator knowledge prerequisites are not published/applicable; publish upstream work first')
        store.db.execute("UPDATE tasks SET status='submitted',owner=?,result=? WHERE id=?", (data["worker"], canonical(result), tid))
        active["received_task"] = tid
        active.setdefault('received_tasks',[])
        if tid not in active['received_tasks']:active['received_tasks'].append(tid)
        active.setdefault('origins',{})[data['origin_task']]={'task':tid,'submission':data['submission_digest']}
        store.set_meta(key, active)
        receipt = {"task": tid, "run": run["id"], "status": "submitted", "result_digest": digest(result),
                   "worker": data["worker"], "claims": len(claims), "semantic_approval": "pending_review",
                   "source_index":plan.get("source_index"), "cache_hits": run.get("cache_hits", 0), "frontend_invocations": run.get("frontend_invocations", 0)}
        store.set_meta(receipt_id, receipt)
        store.event("module_received", {**receipt, "order": ticket["id"], "receipt": receipt_id})
    return receipt


def propose_task(store, task):
    t = task_status(store, task)
    require(t["status"] == "accepted" and t.get("result", {}).get("claims"), "Review the task and its claims first")
    expected_head = store.get_meta("knowledge_head")
    order_id = t["bundle"].get("order")
    if order_id:
        active = store.get_meta(store.get_meta(order_id))
        require(active["id"] == order_id and task in active.get('received_tasks',[active.get('received_task')]) and
                active["ticket"]["snapshot"] == store.get_meta("snapshot_head"), "Assignment superseded")
        _check_conflicts(store, active["ticket"], t["result"]["claims"],t['bundle'].get('reference_epoch'))
    return propose(store, {"author": t["result"]["worker"], "expected_head": expected_head,
                           "snapshot": t["snapshot"], "run": t["run"], "profile": t["profile"],
                           "research_tasks": [task], "units": t["result"]["claims"], "remote_order": order_id})


def feedback(store,order,output,additions=()):
    """Signed review outcomes and exact accepted reference versions for continuing work."""
    import base64
    ticket=read_json(order);active=store.get_meta(assignment_key(ticket['plan'],ticket['module']))
    require(active and active['id']==ticket['id'] and ticket['snapshot']==store.get_meta('snapshot_head'),'Superseded feedback order')
    plan=current(store)
    learning=learning_projection(store,plan,ticket['module'])
    outcomes=[];ids=set(ticket.get('references',{}))
    if learning:
        ids.update(uid for row in learning['implementation_dispositions'] for uid in json.loads(row['data']).get('unit_ids',[]))
    for origin,item in active.get('origins',{}).items():
        t=task_status(store,item['task'])
        reviews=[json.loads(r[0]) for r in store.db.execute("SELECT data FROM events WHERE kind='research_review' AND json_extract(data,'$.task')=? ORDER BY id DESC LIMIT 1",(t['id'],))]
        outcomes.append({'origin_task':origin,'hub_task':t['id'],'submission_digest':item['submission'],'status':t['status'],
                         'review':reviews[0] if reviews else None})
        if t['status']=='accepted':ids.update(u['id'] for u in t.get('result',{}).get('claims',[]))
    dependencies=[]
    for row in store.db.execute("SELECT DISTINCT d.id,d.status,d.result FROM tasks t JOIN task_edges e ON e.task=t.id JOIN tasks d ON d.id=e.dependency WHERE t.snapshot=? AND json_extract(t.data,'$.bundle.plan_id')=? AND json_extract(t.data,'$.bundle.module')=?",(ticket['snapshot'],ticket['plan'],ticket['module'])):
        dependencies.append({'task':row['id'],'status':row['status'],
            'result':json.loads(row['result']) if row['status']=='accepted' and row['result'] else None})
        if row['status']=='accepted' and row['result']:ids.update(u['id'] for u in json.loads(row['result']).get('claims',[]))
    task_delta=[]
    for row in store.db.execute("SELECT id,kind,status,data FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? AND json_extract(data,'$.bundle.module')=? AND status IN ('queued','needs_research') ORDER BY id",(ticket['snapshot'],ticket['plan'],ticket['module'])):
        task_delta.append({'id':row['id'],'kind':row['kind'],'status':row['status'],'bundle':json.loads(row['data'])['bundle'],
                           'dependencies':[r[0] for r in store.db.execute('SELECT dependency FROM task_edges WHERE task=?',(row['id'],))]})
    require(len(task_delta)<=500,'Split the module before synchronizing more than 500 pending tasks')
    stubs=[]
    for did in {d for t in task_delta for d in t['dependencies']}:
        dep=task_status(store,did)
        stubs.append({k:dep[k] for k in ('id','kind','status','bundle')})
    from .whole import current as whole_current
    program=whole_current(store,False)
    required={d['task'] for d in dependencies if d['status']=='accepted'}
    prerequisite_reports=[dict(r) for r in store.db.execute('SELECT * FROM learning_reports WHERE program=?',(program['id'],))
        if r['task'] in required] if program else []
    # Pin the transitive knowledge context, including hierarchy and test oracles.
    units={};pending=set(ids)
    while pending:
        found=store.units(ids=sorted(pending));pending=set()
        units.update(found);require(len(units)<=1000,'Split reference synchronization into smaller module work orders')
        for u in found.values():
            wanted={x['target'] for x in u.get('knowledge_refs',[])}
            if u.get('parent'):wanted.add(u['parent'])
            if u.get('expected_from',{}).get('kind') not in (None,'source_prediction'):wanted.add(u['expected_from']['ref'])
            pending.update(wanted-set(units))
    anchors={r:store.record('anchors',r) for u in units.values() for r in u.get('source_refs',[])}
    anchors.update({r:store.record('anchors',r) for t in task_delta for r in t['bundle'].get('source_anchor_refs',[])})
    assets={a['asset']:store.asset(ticket['snapshot'],a['asset']) for a in anchors.values()}
    require(len(set(additions))<=40,'At most 40 extra frozen materials per feedback packet')
    for key in additions:
        material=store.asset(ticket['snapshot'],key)
        require(material['kind'] in {'source','document'} and material['status']=='frozen','Choose a frozen product material: '+key)
        assets[key]=material
    blobs={sha:base64.b64encode(store.blob(sha)).decode('ascii') for a in assets.values() for sha in {a.get('sha'),a.get('text_sha')}-{None}}
    require(sum(len(v) for v in blobs.values())<=240*1024**2,'Reference material too large; narrow the order')
    hashes={u:content_hash(v) for u,v in units.items()}
    from .knowledge import freshness,UnitMap
    bound=UnitMap(store,store.get_meta('knowledge_head'),units)
    applicable={uid:hashes[uid] for uid,u in units.items() if not freshness(store,u,ticket['snapshot'],plan['run'],bound)}
    epoch=identity('reference-epoch',[ticket['id'],store.get_meta('knowledge_head'),hashes,outcomes,dependencies,task_delta,learning,[(k,a['sha'],a.get('text_sha')) for k,a in sorted(assets.items())]])
    data={'schema':'module-feedback/v1','order':ticket['id'],'snapshot':ticket['snapshot'],'profile':ticket['profile'],
          'worker':ticket['worker'],'epoch':epoch,'revision':store.get_meta('knowledge_head'),'units':units,'anchors':anchors,
          'source_index':plan.get('source_index'),'applicable_hashes':applicable,
          'assets':assets,'extra_materials':sorted(set(additions)),'blobs':blobs,'outcomes':outcomes,'dependencies':dependencies,
          'task_delta':task_delta,'dependency_stubs':stubs,'prerequisite_reports':prerequisite_reports,
          'learning_projection':learning,'created':now()}
    with store.transaction():
        store.set_meta('issued-reference:'+ticket['id']+':'+epoch,{'hashes':hashes,'revision':data['revision']})
    atomic_write(output,gzip.compress(canonical({'data':data,'hmac':_signed(ticket['secret'],data)}).encode('utf-8'),mtime=0))
    return {'file':str(output),'epoch':epoch,'units':len(units),'outcomes':len(outcomes),'next':'成员执行 team sync --input 此反馈包，再 whole advance / whole next。'}


def sync_feedback(store,path):
    import base64
    packet=_read_packet(path);data=packet['data'];local=store.get_meta('local-order:'+data['order'])
    require(local and data.get('schema')=='module-feedback/v1','Unknown feedback order')
    ticket=local['ticket'];plan=current(store)
    require(hmac.compare_digest(packet['hmac'],_signed(ticket['secret'],data)) and data['worker']==ticket['worker'] and
            data['snapshot']==ticket['snapshot']==plan['snapshot'] and data['profile']==ticket['profile'] and ticket['plan']==plan['id'],
            'Invalid feedback binding/signature')
    receipt='feedback-receipt:'+data['epoch']
    if store.get_meta(receipt):return {**store.get_meta(receipt),'replayed':True}
    old=store.get_meta('synced-references:'+ticket['id'],{})
    require(not old or data['created']>=old.get('created',''),'Older feedback cannot roll back references')
    from .curriculum import current as curriculum_current
    local_course=curriculum_current(store)
    require(not local_course or not local_course.get('projection') or
        local_course['revision']==local_course['projection']['coordinator_revision'],
        'Local curriculum refinements require coordinator reconciliation before synchronization; request a reconciled kit')
    with store.transaction():
        for sha,encoded in data['blobs'].items():require(store.put_blob(base64.b64decode(encoded,validate=True))==sha,'Feedback blob hash mismatch')
        for key,a in data['assets'].items():
            require(key==a['key'] and a.get('sha') in data['blobs'] or key==a['key'] and a['status']=='excluded','Feedback asset binding mismatch')
            existing=store.db.execute('SELECT sha FROM assets WHERE snapshot=? AND key=?',(plan['snapshot'],key)).fetchone()
            require(not existing or existing[0]==a['sha'],'Feedback source changed')
            store.db.execute('INSERT OR IGNORE INTO assets VALUES(?,?,?,?,?,?,?,?)',(plan['snapshot'],key,a['repo'],a['path'],a['sha'],a['kind'],a['status'],canonical(a)))
        for ref,a in data['anchors'].items():
            mapped=store.anchor(plan['snapshot'],a['asset'],a['start'],a['end'],text_sha=a['sha'] if a['view']=='extracted' else None)
            require(a['id']==ref and mapped['quote_sha256']==a['quote_sha256'] and store.evidence_in_scope(a,plan['snapshot']),'Feedback evidence mismatch')
            store.db.execute('INSERT OR IGNORE INTO anchors VALUES(?,?,?,?,?,?,?)',(ref,a['snapshot'],a['asset'],a['sha'],a['start'],a['end'],canonical(a)))
        require(all(u['id']==uid and u.get('review',{}).get('verdict')=='accept' for uid,u in data['units'].items()),'Feedback reference was not accepted')
        require(data.get('source_index')==plan.get('source_index'),'Feedback global graph changed')
        store.set_meta('synced-references:'+ticket['id'],{**{k:data[k] for k in ('units','epoch','revision','created','source_index','applicable_hashes')},
            'extra_materials':sorted(set(old.get('extra_materials',[]))|set(data.get('extra_materials',[])))})
        store._coverage_freshness={}
        for dependency in data.get('dependencies',[]):
            # External prerequisite stubs may advance only by the signed coordinator outcome.
            row=store.db.execute('SELECT data FROM tasks WHERE id=?',(dependency['task'],)).fetchone()
            if row and json.loads(row[0])['bundle'].get('module')!=ticket['module'] and dependency['status']=='accepted':
                store.db.execute("UPDATE tasks SET status='accepted',result=? WHERE id=?",
                    (canonical(dependency['result']) if dependency.get('result') else None,dependency['task']))
        mapping=store.get_meta('coordinator-task-map',{})
        for item in data.get('task_delta',[]):
            b=item['bundle'];require(b.get('module')==ticket['module'] and b.get('plan_id')==plan['id'],'Task delta outside assigned scope')
            cid=b.get('candidate_id');local_id=mapping.get(item['id'])
            if not local_id and cid:
                row=store.db.execute("SELECT id FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? AND json_extract(data,'$.bundle.candidate_id')=?",(plan['snapshot'],plan['id'],cid)).fetchone()
                local_id=row[0] if row else None
            if not local_id:
                scope={'kind':item['kind'],'profile':plan['profile'],'bundle':b}
                expected=_task_scope(scope)
                for row in store.db.execute("SELECT id FROM tasks WHERE snapshot=? AND run=? AND json_extract(data,'$.bundle.plan_id')=? "
                    "AND json_extract(data,'$.bundle.module')=?",(plan['snapshot'],plan['run'],plan['id'],ticket['module'])):
                    if _task_scope(task_status(store,row['id']))==expected:
                        local_id=row['id'];break
            if not local_id:local_id=create_task(store,snapshot=plan['snapshot'],run=plan['run'],profile=plan['profile'],kind=item['kind'],bundle={**b,'coordinator_task':item['id']})
            mapping[item['id']]=local_id
        for stub in data.get('dependency_stubs',[]):
            if stub['id'] not in mapping:
                # Coordinator-only prerequisites remain read-only stubs for scheduling.
                value={'id':stub['id'],'snapshot':plan['snapshot'],'run':plan['run'],'profile':plan['profile'],'kind':stub['kind'],'bundle':stub['bundle'],'created':data['created']}
                store.db.execute('INSERT OR IGNORE INTO tasks(id,snapshot,run,profile,kind,status,data) VALUES(?,?,?,?,?,?,?)',
                    (stub['id'],plan['snapshot'],plan['run'],plan['profile'],stub['kind'],'accepted' if stub['status']=='accepted' else 'blocked_external',canonical(value)))
                mapping[stub['id']]=stub['id']
            dependency=next((d for d in data.get('dependencies',[]) if d['task']==stub['id']),None)
            if dependency and stub['bundle'].get('module')!=ticket['module'] and dependency['status']=='accepted' and dependency.get('result'):
                store.db.execute("UPDATE tasks SET result=? WHERE id=?",(canonical(dependency['result']),mapping[stub['id']]))
        for item in data.get('task_delta',[]):
            for dep in item['dependencies']:store.db.execute('INSERT OR IGNORE INTO task_edges VALUES(?,?)',(mapping[item['id']],mapping[dep]))
        store.set_meta('coordinator-task-map',mapping)
        from .whole import current as whole_current
        program=whole_current(store,False)
        required={d['task'] for d in data.get('dependencies',[]) if d['status']=='accepted'}
        for row in data.get('prerequisite_reports',[]):
            report=json.loads(row['data'])
            require(program and row['program']==program['id'] and row['task'] in required and
                report.get('review',{}).get('verdict')=='accept','Invalid prerequisite review proof')
            report['task']=mapping.get(row['task'],row['task'])
            store.db.execute('INSERT OR IGNORE INTO learning_reports VALUES(?,?,?,?,?)',
                (row['id'],row['program'],report['task'],row['result_digest'],canonical(report)))
        updated=[]
        for item in data['outcomes']:
            t=task_status(store,item['origin_task'])
            require(t.get('result') and digest(t['result'])==item['submission_digest'],'Feedback does not describe this local submission')
            if item['status'] not in {'accepted','needs_research'}:continue
            require(item['review'] and item['review'].get('verdict')==('accept' if item['status']=='accepted' else 'reject'),'Missing coordinator research review')
            require(t['status'] in {'submitted',item['status']},'Local work changed after remote review')
            store.db.execute('UPDATE tasks SET status=? WHERE id=?',(item['status'],t['id']))
            if item['status']=='accepted' and t['result'].get('progress'):
                from .whole import apply_reviewed_locked
                apply_reviewed_locked(store,t,t['result'],item['review'])
            store.event('coordinator_review_synced',{'task':t['id'],'hub_task':item['hub_task'],'review':item['review'],'epoch':data['epoch']})
            updated.append({'task':t['id'],'status':item['status']})
        apply_learning_projection(store,data.get('learning_projection'),plan,ticket['module'],mapping)
        result={'epoch':data['epoch'],'updated':updated,'reference_units':len(data['units']),'extra_materials':data.get('extra_materials',[]),'review_source':'coordinator_signed_feedback'}
        store.set_meta(receipt,result)
    return result
