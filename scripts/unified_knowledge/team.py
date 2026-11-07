"""Offline module work orders. Each host uses its own checkout, Python and SQLite."""
import gzip
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
    return {r for c in result["coverage"] for r in c.get("evidence_refs", [])} | {
        r for c in result.get("claims", []) for r in c.get("source_refs", [])}


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


def export_result(store, order, task, output):
    local = open_order(store, order)
    ticket = store.get_meta("local-order:" + local["assignment"])["ticket"]
    if ticket.get("source_index"):
        require(Path(output).suffix.lower() == ".gz", "Use a .gz file for the result packet")
    t = task_status(store, task)
    require(t["snapshot"] == local["local_snapshot"] and t["bundle"].get("module") == ticket["module"] and
            t["status"] in {"submitted", "accepted"}, "Export a submitted research task for the assigned module")
    result = t["result"]
    require(result["worker"] == ticket["worker"] and t["profile"] == ticket["profile"], "Worker or profile mismatch")
    run = store.record("runs", t["run"])
    require(run.get("mode") in {"inventory", "selected", "ecs", "ecs_module"}, "Work orders return bounded module results")
    evidence = {r: store.record("anchors", r) for r in _refs(result)}
    for ref, anchor in evidence.items():
        receipt = store.db.execute("SELECT 1 FROM events WHERE kind='evidence_read' AND json_extract(data,'$.task')=? "
            "AND json_extract(data,'$.worker')=? AND json_extract(data,'$.evidence')=? "
            "AND json_extract(data,'$.quote_sha256')=? AND json_extract(data,'$.truncated')=0",
            (task, result["worker"], ref, anchor["quote_sha256"])).fetchone()
        require(receipt and store.evidence_in_scope(anchor, t["snapshot"]), "Missing worker evidence receipt")
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


def _check_conflicts(store, ticket, claims):
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
    for uid in ids:
        require((content_hash(base[uid]) if uid in base else None) == (content_hash(current[uid]) if uid in current else None),
                "Knowledge changed since assignment; reconcile unit: " + uid)


def receive(store, path, jobs=2):
    with gzip.open(path, "rb") as stream:
        raw = stream.read(256 * 1024 * 1024 + 1)
    require(len(raw) <= 256 * 1024 * 1024, "Split this result into smaller research batches")
    packet = json.loads(raw)
    data = packet["data"]
    key = store.get_meta(data["order"])
    active = store.get_meta(key) if key else None
    require(active and active["id"] == data["order"], "Unknown or superseded assignment")
    ticket = active["ticket"]
    require(data.get("schema") == "module-result/v1" and hmac.compare_digest(packet["hmac"], _signed(ticket["secret"], data)),
            "Module result is damaged or belongs to a different work order")
    plan = current(store)
    require(ticket["plan"] == plan["id"] and ticket["snapshot"] == store.get_meta("snapshot_head") and
            ticket["worker"] == data["worker"] and ticket["profile"] == data["profile"], "Stale plan, worker or profile")
    receipt_id = identity("module-receipt", data)
    existing = store.get_meta(receipt_id)
    if existing:
        return {**existing, "replayed": True}
    require(not active.get("received_task"), "A different result was received; issue a new work order for the next batch")
    _check_conflicts(store, ticket, data["claims"])
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
        require(not active.get("received_task"), "Another result won the assignment")
        _check_conflicts(store, ticket, data["claims"])
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
            mapping[ref] = mapped["id"]
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
            lead = candidate(plan,cid,store)
            require(lead["owner_module"] in (None,ticket["module"]),"Candidate belongs to a different module")
            other = store.db.execute("SELECT id,status,attempt,data FROM tasks WHERE snapshot=? AND json_extract(data,'$.bundle.plan_id')=? "
                        "AND json_extract(data,'$.bundle.candidate_id')=?",(snapshot,plan["id"],cid)).fetchone()
            if other:
                require(other["status"]=="queued" and other["attempt"]==0 and
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
        if cid and other:
            tid = other["id"]
            prior = json.loads(other["data"])
            prior["bundle"].update(bundle)
            store.db.execute("UPDATE tasks SET data=? WHERE id=?",(canonical(prior),tid))
        else:
            tid = create_task(store,snapshot=snapshot,run=run["id"],profile=profile,kind="remote_module_research",bundle=bundle)
        result = {"worker": data["worker"], "task": tid, "submitted": now(), "coverage": coverage, "claims": claims,
                  "remote_submission": data["submission_digest"], "origin_task": data["origin_task"],
                  "read_provenance": "worker_receipts_rebound_to_coordinator_evidence", "database_execution": "not_run"}
        store.db.execute("UPDATE tasks SET status='submitted',owner=?,result=? WHERE id=?", (data["worker"], canonical(result), tid))
        active["received_task"] = tid
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
        require(active["id"] == order_id and active["received_task"] == task and
                active["ticket"]["snapshot"] == store.get_meta("snapshot_head"), "Assignment superseded")
        _check_conflicts(store, active["ticket"], t["result"]["claims"])
    return propose(store, {"author": t["result"]["worker"], "expected_head": expected_head,
                           "snapshot": t["snapshot"], "run": t["run"], "profile": t["profile"],
                           "research_tasks": [task], "units": t["result"]["claims"], "remote_order": order_id})
