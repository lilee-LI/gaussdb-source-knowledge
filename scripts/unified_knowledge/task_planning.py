"""Evidence-bound planning proposals and bounded, repeatable task construction.

This module plans work. It never promotes lexical signals or model proposals to
accepted product knowledge. The existing task/review engine remains authoritative.
"""
from copy import deepcopy
import json

from . import study
from .planner import create_task, task_status
from .product_adapter import TOPICS
from .store import atomic_write, canonical, digest, identity, now, require

POLICY = "bounded-feature-planning/v1"


def _refs(store, plan, refs):
    require(isinstance(refs, list) and 1 <= len(refs) <= 40, "Provide 1..40 source evidence seeds")
    normalized = []
    for ref in refs:
        require(isinstance(ref, dict), "Evidence seed must be an object")
        asset = store.asset(plan["snapshot"], ref["asset"])
        require(asset["status"] == "frozen", "Evidence must use a frozen asset")
        start, end = ref.get("start"), ref.get("end")
        require(type(start) is int and type(end) is int and 1 <= start <= end and end - start < 1000, "Invalid bounded evidence range")
        lines = store.source_lines(asset.get("text_sha") or asset["sha"])
        require(end <= len(lines), "Evidence range exceeds frozen source")
        normalized.append({"asset": ref["asset"], "start": start, "end": end})
    return sorted({canonical(r): r for r in normalized}.values(), key=canonical)


def propose(store, proposal):
    """Record a planner/worker's explicit merge/split/new-lead proposal for replay.

    Each item has an explicit research question and evidence. Superseding a lead
    changes future planning only; active and accepted research is never deleted.
    """
    plan = study.current(store)
    require(plan.get("product_adapter"), "Refresh the project to bind a product adapter before planning")
    require(proposal.get("study_plan") == plan["id"], "Planning proposal belongs to another study plan")
    require(isinstance(proposal.get("author"), str) and proposal["author"].strip(), "Planning author required")
    require(isinstance(proposal.get("reason"), str) and proposal["reason"].strip(), "Planning rationale required")
    rows = proposal.get("candidates", [])
    require(isinstance(rows, list) and 1 <= len(rows) <= 100, "Provide 1..100 proposed research candidates")
    prior = store.get_meta("planning-candidates:" + plan["id"], [])
    known = {c["id"] for c in [*plan.get("candidates", []), *prior]}
    prepared = []
    for item in rows:
        require(isinstance(item, dict) and item.get("owner_module") in plan["modules"], "Unknown candidate owner")
        for key in ("title", "question", "reason"):
            require(isinstance(item.get(key), str) and 0 < len(item[key].strip()) <= 4000, "Candidate requires " + key)
        refs = _refs(store, plan, item.get("evidence"))
        owned = set(plan["modules"][item["owner_module"]]["files"])
        require(any(r["asset"] in owned for r in refs), "Candidate needs evidence in its owner module")
        supersedes = item.get("supersedes", [])
        require(isinstance(supersedes, list) and set(supersedes) <= known, "Unknown superseded candidate")
        dependencies = item.get("depends_on", [])
        require(isinstance(dependencies, list) and set(dependencies) <= known, "Dependencies must reference existing candidate IDs")
        row = {k: item[k] for k in ("title", "question", "reason", "owner_module")}
        row.update(evidence=refs, supersedes=sorted(set(supersedes)), depends_on=sorted(set(dependencies)),
                   owner_basis="planning_proposal", modules=[item["owner_module"]], design_gap=True)
        row["id"] = identity("candidate", [plan["snapshot"], plan["product_adapter"]["digest"], row])
        require(row["id"] not in row["depends_on"], "Self-dependent candidate")
        prepared.append(row)
    value = {"study_plan": plan["id"], "author": proposal["author"], "reason": proposal["reason"], "candidates": prepared,
             "parent_task": proposal.get("parent_task"), "policy": POLICY}
    if value["parent_task"]:
        parent = task_status(store, value["parent_task"])
        require(parent["snapshot"] == plan["snapshot"] and parent["bundle"].get("plan_id") == plan["id"], "Feedback task belongs to another plan")
    pid = identity("planning-proposal", value)
    with store.transaction():
        require(study.current(store)["id"] == plan["id"], "Study plan changed during proposal")
        existing = store.get_meta(pid)
        if existing:
            return existing
        latest = store.get_meta("planning-candidates:" + plan["id"], [])
        merged = {r["id"]: r for r in [*latest, *prepared]}
        _order([*plan.get("candidates", []), *merged.values()])
        value.update(id=pid, created=now(), semantic_status="unreviewed")
        store.set_meta(pid, value)
        store.set_meta("planning-candidates:" + plan["id"], sorted(merged.values(), key=lambda r: r["id"]))
        store.event("planning_proposal", {"id": pid, "study_plan": plan["id"], "parent_task": value["parent_task"]})
    return value


def _order(candidates):
    rows = {c["id"]: c for c in candidates}
    seen, visiting, ordered = set(), set(), []
    def visit(cid):
        require(cid in rows, "Missing candidate dependency: " + cid)
        require(cid not in visiting, "Cyclic planning dependencies")
        if cid in seen:
            return
        visiting.add(cid)
        for other in sorted(rows[cid].get("depends_on", [])):
            visit(other)
        visiting.remove(cid)
        seen.add(cid)
        ordered.append(rows[cid])
    for cid in sorted(rows):
        visit(cid)
    return ordered


def candidates(store, plan):
    extra = store.get_meta("planning-candidates:" + plan["id"], [])
    return _order([*plan.get("candidates", []), *extra])


def construct(store, *, modules=None, max_tasks=20, files_per_task=12, apply=False):
    require(type(max_tasks) is int and 1 <= max_tasks <= 500, "max_tasks must be 1..500")
    require(type(files_per_task) is int and 1 <= files_per_task <= 40, "files_per_task must be 1..40")
    plan = study.current(store)
    require(plan.get("product_adapter"), "Refresh the project to bind a product adapter before planning")
    scope = sorted(set(modules or plan["modules"]))
    require(set(scope) <= set(plan["modules"]), "Unknown module in planning scope")
    leads = candidates(store, plan)
    superseded = {cid for c in leads for cid in c.get("supersedes", [])}
    # Referenced prerequisites cannot disappear merely because another candidate supersedes them.
    needed = {cid for c in leads for cid in c.get("depends_on", [])}
    existing = {r["cid"]: r["id"] for r in store.db.execute(
        "SELECT id,json_extract(data,'$.bundle.candidate_id') cid FROM tasks WHERE snapshot=? "
        "AND json_extract(data,'$.bundle.plan_id')=? AND json_extract(data,'$.bundle.candidate_id') IS NOT NULL ORDER BY rowid",
        (plan["snapshot"], plan["id"]))}
    eligible, gaps, dispositions = [], [], []
    for lead in leads:
        cid, owner = lead["id"], lead.get("owner_module")
        if cid in superseded and cid not in needed:
            dispositions.append({"candidate": cid, "state": "superseded", "existing_task": existing.get(cid)})
        elif owner is None:
            gaps.append({"candidate": cid, "reason": "unassigned_module"})
        elif owner in scope:
            if cid in existing:
                dispositions.append({"candidate": cid, "state": "existing_task", "task": existing[cid]})
            else:
                eligible.append(lead)
    specs, selected_ids = [], set(existing)
    for lead in eligible:
        if len(specs) >= max_tasks:
            break
        dependencies = lead.get("depends_on", [])
        if not set(dependencies) <= selected_ids:
            gaps.append({"candidate": lead["id"], "reason": "prerequisite_outside_batch_or_scope", "dependencies": dependencies})
            continue
        owner = lead["owner_module"]
        owned = plan["modules"][owner]["files"]
        refs = [{"asset": r["asset"], "start": r["start"], "end": r["end"]} for r in lead["evidence"][:40]]
        selected = list(dict.fromkeys([r["asset"] for r in refs if r["asset"] in owned]))[:files_per_task]
        if not selected:
            selected = owned[:files_per_task]
        # A document-only lead remains a question; these file seeds do not claim a resolved entry.
        topics = deepcopy(plan.get("topic_signals", {}).get(owner, {}))
        for topic in TOPICS:
            topics.setdefault(topic, {"status": "unknown", "reason": "Requires source research", "evidence": []})
        specs.append({"candidate_id": lead["id"], "module": owner, "question": lead["question"], "selected_files": selected,
                      "evidence_seeds": refs, "candidate_dependencies": dependencies, "topic_decisions": topics,
                      "reason": lead.get("reason") or "Material-backed candidate: " + lead["title"],
                      "expected_outputs": ["mechanism_and_conditions", "typed_calls_and_data_stages", "topic_applicability", "counterexamples", "open_gaps"],
                      "acceptance": ["same_snapshot_evidence", "actual_read_receipts", "explicit_unknowns", "separate_semantic_review"],
                      "budget": {"initial_files": files_per_task, "expansion_requires_feedback": True}})
        selected_ids.add(lead["id"])
    value = {"schema": "research-task-plan/v1", "study_plan": plan["id"], "snapshot": plan["snapshot"],
             "run": plan["run"], "profile": plan["profile"], "adapter_digest": plan["product_adapter"]["digest"],
             "policy": POLICY, "modules": scope, "tasks": specs, "dispositions": dispositions,
             "gaps": [*gaps, *plan.get("signal_gaps", [])], "candidate_count": len(leads),
             "deferred_by_budget": max(0, len(eligible) - len(specs)), "semantic_completeness": "not_certified"}
    value["id"] = identity("research-task-plan", value)
    if not apply:
        return {**value, "mode": "preview"}
    created = []
    with store.transaction():
        require(study.current(store)["id"] == plan["id"], "Study plan changed during planning")
        # Serialize with every producer, including manual focus, before checking candidate uniqueness.
        latest = {r["cid"]: r["id"] for r in store.db.execute(
            "SELECT id,json_extract(data,'$.bundle.candidate_id') cid FROM tasks WHERE snapshot=? "
            "AND json_extract(data,'$.bundle.plan_id')=? ORDER BY rowid", (plan["snapshot"], plan["id"]))}
        for item in specs:
            cid = item["candidate_id"]
            if cid in latest:
                created.append({"candidate_id": cid, "task": latest[cid], "reused": True})
                continue
            anchors = []
            for ref in item["evidence_seeds"]:
                asset = store.asset(plan["snapshot"], ref["asset"])
                anchors.append(store.anchor(plan["snapshot"], ref["asset"], ref["start"], ref["end"], text_sha=asset.get("text_sha"))["id"])
            if not anchors:
                for key in item["selected_files"][:3]:
                    asset = store.asset(plan["snapshot"], key)
                    if asset.get("sha"):
                        length = len(store.source_lines(asset["sha"]))
                        if length:
                            anchors.append(store.anchor(plan["snapshot"], key, 1, min(40, length))["id"])
            bundle = {**item, "plan_id": plan["id"], "planning_id": value["id"], "policy": POLICY,
                      "adapter_digest": value["adapter_digest"], "source_index": plan.get("source_index"),
                      "source_anchor_refs": sorted(set(anchors)), "symbol_refs": []}
            deps = [latest[c] for c in item["candidate_dependencies"]]
            tid = create_task(store, snapshot=plan["snapshot"], run=plan["run"], profile=plan["profile"],
                              kind="feature_research", bundle=bundle, dependencies=deps)
            latest[cid] = tid
            created.append({"candidate_id": cid, "task": tid, "reused": False})
        value.update(mode="applied", created=now(), task_results=created)
        store.set_meta(value["id"], value)
        store.set_meta("task_planning_head:" + plan["id"], value["id"])
        store.event("task_plan_applied", {"id": value["id"], "tasks": len(created)})
    export(store, value)
    return value


def export(store, value=None):
    plan = study.current(store)
    value = value or store.get_meta(store.get_meta("task_planning_head:" + plan["id"], ""))
    require(value, "No applied task plan")
    folder = store.home / "planning" / value["id"].replace(":", "-")
    atomic_write(folder / "plan.json", canonical(value) + "\n")
    rows = ["# Research task plan", "", "Source snapshot: " + value["snapshot"], "", "Semantic completeness: not certified", "",
            "| Module | Question | Candidate |", "| --- | --- | --- |"]
    rows.extend("| " + " | ".join(str(item[k]).replace("|", "\\|").replace("\n", " ") for k in ("module", "question", "candidate_id")) + " |" for item in value["tasks"])
    rows.extend(["", "## Gaps", "", "```json", json.dumps(value["gaps"], ensure_ascii=False, indent=2), "```"])
    atomic_write(folder / "PLAN.md", "\n".join(rows) + "\n")
    return {"plan": str(folder / "plan.json"), "readable": str(folder / "PLAN.md")}
