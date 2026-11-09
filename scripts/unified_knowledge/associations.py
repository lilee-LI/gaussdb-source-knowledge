"""Read-only projections of explicitly reviewed feature/mainline associations.

These links do not alter knowledge units or attest semantic completion. Current
planning reports are never applied to a historical knowledge revision.
"""
import json

from .knowledge import UnitMap, content_hash, freshness
from .query_api import execution_budget
from .store import digest, require


def collect(store, *, snapshot=None, run=None, revision=None, selectors=None, units=None,
            max_rows=20000, max_units=2000):
    require(type(max_rows) is int and 1 <= max_rows <= 50000 and type(max_units) is int and 1 <= max_units <= 10000,
            "Invalid association projection bounds")
    selectors = selectors or {}
    require(not set(selectors) - {"feature", "mainline"}, "Unknown association selector")
    for values in selectors.values():
        require(isinstance(values, list) and len(values) <= 100 and all(isinstance(value, str) for value in values),
                "Association selectors must contain at most 100 IDs")
    key = store.get_meta("study_head")
    plan = store.get_meta(key, {}) if key else {}
    head = store.get_meta("knowledge_head")
    revision = revision or head
    snapshot, run = snapshot or plan.get("snapshot"), run or plan.get("run")
    scope = {"source_snapshot": snapshot, "index_run": run, "knowledge_revision": revision, "study_plan": plan.get("id")}
    result = {"schema": "reviewed-associations/v1", "scope": scope, "navigation": {"feature": {}, "mainline": {}},
              "associations": [], "truncated": False, "limits": {"rows": max_rows, "units": max_units}, "read_only": True}
    course_key = store.get_meta("curriculum_head")
    course = store.get_meta(course_key, {}) if course_key else {}
    program = store.get_meta("whole-for:" + str(plan.get("id")))
    eligible = bool(revision and revision == head and course and
        (snapshot, run) == (plan.get("snapshot"), plan.get("run")) and
        (course.get("plan_id"), course.get("snapshot"), course.get("run"), course.get("profile"), course.get("program")) ==
        (plan.get("id"), snapshot, run, plan.get("profile"), program))
    if not eligible:
        result["current_projection"] = False
        result["fingerprint"] = digest([result["schema"], scope, "no_current_report_projection"])
        return result
    scope.update(build_profile=plan["profile"], curriculum=course["id"], program=program)
    result["current_projection"] = True
    decisions, candidates, wanted, seen = [], [], set(), set()
    feature_ids = {row["id"] for row in course.get("features", [])}

    def candidate(kind, identifier, ids, hashes, provenance):
        ids = sorted(set(ids))
        decisions.append({"kind": kind, "id": identifier, "units": hashes, **provenance})
        if not ids or len(wanted | set(ids)) > max_units:
            result["truncated"] |= bool(ids)
            return
        wanted.update(ids)
        candidates.append({"kind": kind, "id": identifier, "unit_ids": ids, "unit_hashes": hashes, **provenance})

    try:
        with execution_budget(store, 2000):
            if not selectors or selectors.get("feature"):
                args = [program, snapshot, run, plan["id"]]
                where = ""
                if selectors.get("feature"):
                    where = " AND json_extract(m.value,'$.feature_id') IN (" + ",".join("?" for _ in selectors["feature"]) + ")"
                    args.extend(selectors["feature"])
                rows = store.db.execute("SELECT r.id,r.task,r.result_digest,m.value mapping FROM learning_reports r "
                    "JOIN tasks t ON t.id=r.task JOIN json_each(r.data,'$.progress.feature_mappings') m "
                    "WHERE r.program=? AND t.snapshot=? AND t.run=? AND json_extract(t.data,'$.bundle.plan_id')=? "
                    "AND t.status='accepted' AND json_extract(r.data,'$.review.verdict')='accept'" + where +
                    " ORDER BY r.rowid DESC,CAST(m.key AS INTEGER) DESC LIMIT ?", [*args, max_rows + 1]).fetchall()
                result["truncated"] |= len(rows) > max_rows
                for row in rows[:max_rows]:
                    mapping = json.loads(row["mapping"])
                    fid = mapping.get("feature_id")
                    if fid not in feature_ids or fid in seen:
                        continue
                    seen.add(fid)
                    provenance = {"report": row["id"], "task": row["task"], "result_digest": row["result_digest"], "state": mapping.get("state")}
                    if mapping.get("state") == "mapped":
                        candidate("feature", fid, mapping.get("unit_ids", []), mapping.get("unit_hashes", {}), provenance)
                    else:
                        decisions.append({"kind": "feature", "id": fid, **provenance})
            if not selectors or selectors.get("mainline"):
                for item in course.get("mainlines", [])[:100]:
                    mid = item["id"]
                    if selectors.get("mainline") and mid not in selectors["mainline"]:
                        continue
                    row = store.db.execute("SELECT id,data,json_extract(result,'$.claims') claims FROM tasks WHERE id=? "
                        "AND snapshot=? AND run=? AND profile=? AND status='accepted' AND json_extract(data,'$.bundle.plan_id')=? "
                        "AND json_extract(data,'$.bundle.program_id')=? AND json_extract(data,'$.bundle.program_item')=?",
                        (item.get("task"), snapshot, run, plan["profile"], plan["id"], program, mid)).fetchone()
                    if not row:
                        continue
                    claims = json.loads(row["claims"] or "[]")
                    hashes = {unit["id"]: content_hash(unit) for unit in claims}
                    candidate("mainline", mid, list(hashes), hashes,
                              {"task": row["id"], "via": "accepted_program_item_claims", "meaning": "associated_claims_not_mainline_completion"})
    except ValueError as exc:
        if "Query execution budget exhausted" not in str(exc):
            raise
        result["truncated"] = True
        result["stop_reason"] = "association_query_budget_exhausted"
    initial = {uid: units[uid] for uid in wanted if units is not None and uid in units}
    missing = sorted(wanted - set(initial))
    for offset in range(0, len(missing), 400):
        initial.update(store.units(revision, ids=missing[offset:offset + 400]))
    available = UnitMap(store, revision, initial)
    valid = {}
    for row in candidates:
        good = True
        for uid in row["unit_ids"]:
            expected = row["unit_hashes"].get(uid)
            unit = available.get(uid)
            check = (uid, expected)
            if check not in valid:
                valid[check] = bool(unit and expected and unit.get("review", {}).get("verdict") == "accept" and
                    content_hash(unit) == expected and not freshness(store, unit, snapshot, run, available))
            good &= valid[check]
        if good:
            result["navigation"][row["kind"]][row["id"]] = row["unit_ids"]
            result["associations"].append(row)
    result["associations"].sort(key=lambda row: (row["kind"], row["id"]))
    result["fingerprint"] = digest([result["schema"], scope, course.get("revision"), decisions,
                                    result["associations"], result["truncated"], result.get("stop_reason")])
    return result
