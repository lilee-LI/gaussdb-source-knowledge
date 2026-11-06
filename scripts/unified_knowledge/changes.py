"""Old/new material and graph comparison with explicit reverse knowledge invalidation."""
from __future__ import annotations

import json
import re

from .knowledge import content_hash, freshness
from .planner import create_task
from .store import canonical, digest, identity, now, require


def analyze_change(store, base, target, *, base_run, target_run, revision=None, enqueue=True, diff_text=None):
    old = store.record("runs", base_run)
    new = store.record("runs", target_run)
    require(old["snapshot"] == base and new["snapshot"] == target, "Change graph/snapshot binding mismatch")
    require(old["status"] in {"ready", "partial"} and new["status"] in {"ready", "partial"}, "Change needs completed indexes")
    old_assets = {r["key"]: json.loads(r["data"]) for r in store.db.execute("SELECT key,data FROM assets WHERE snapshot=?", (base,))}
    new_assets = {r["key"]: json.loads(r["data"]) for r in store.db.execute("SELECT key,data FROM assets WHERE snapshot=?", (target,))}
    changed = []
    for key in sorted(set(old_assets) | set(new_assets)):
        before, after = old_assets.get(key), new_assets.get(key)
        fields = ("sha", "status", "text_sha", "document_status", "declared_revision")
        if before is None or after is None or any(before.get(k) != after.get(k) for k in fields):
            changed.append({"asset": key, "kind": "added" if before is None else ("deleted" if after is None else "modified"),
                            "before": before and before["sha"], "after": after and after["sha"]})
    changed_keys = {x["asset"] for x in changed}
    profile_changed = old["profile_digest"] != new["profile_digest"] or old["profile"] != new["profile"]
    affected_tus = []
    for graph in (old, new):
        for tu in graph.get("tu_results", []):
            dependencies = {tu["asset"]} | {i["asset"] for i in tu.get("includes", []) if i["asset"]}
            if dependencies & changed_keys or profile_changed:
                affected_tus.append({"run": graph["id"], "context": tu["context"], "asset": tu["asset"],
                                     "reason": "profile_changed" if profile_changed else "source_or_include_changed"})
    revision = revision or store.get_meta("knowledge_head")
    units = store.units(revision) if revision else {}
    stale = {}
    for uid, unit in units.items():
        reasons = freshness(store, unit, target, target_run, units)
        if reasons:
            stale[uid] = reasons
    dependents = []
    for uid, unit in units.items():
        targets = {l["target"] for l in unit.get("knowledge_refs", [])}
        if targets & set(stale):
            dependents.append(uid)
    moved = []
    old_symbols = {r["logical"]: json.loads(r["data"]) for r in store.db.execute("SELECT logical,data FROM symbols WHERE run=?", (base_run,))}
    new_symbols = {r["logical"]: json.loads(r["data"]) for r in store.db.execute("SELECT logical,data FROM symbols WHERE run=?", (target_run,))}
    # Missing stable identity remains a candidate mapping, never an automatic equivalence.
    for logical in set(old_symbols) - set(new_symbols):
        matches = [v for v in new_symbols.values() if v["name"] == old_symbols[logical]["name"] and v["kind"] == old_symbols[logical]["kind"]]
        moved.append({"old": old_symbols[logical]["id"], "candidate_targets": [v["id"] for v in matches],
                      "resolution": "candidate" if matches else "unresolved"})
    patch = None
    if diff_text is not None:
        require(isinstance(diff_text, str) and len(diff_text) <= 2_000_000, "Invalid patch material")
        patch = {"sha": store.put_blob(diff_text.encode("utf-8")), "kind": "supplied_patch",
                 "files": re.findall(r"(?m)^\+\+\+ (?:b/)?(.+)$", diff_text), "runtime_validation": "not_run"}
    change = {"schema": "knowledge-change/v1", "base_snapshot": base, "target_snapshot": target,
              "base_run": base_run, "target_run": target_run, "knowledge_revision": revision,
              "changed_assets": changed, "profile_changed": profile_changed, "affected_tus": affected_tus,
              "stale_units": stale, "dependent_units": sorted(dependents), "symbol_mapping_candidates": moved,
              "new_unexplained_assets": [r["asset"] for r in changed if r["kind"] == "added"],
              "patch": patch, "semantic_verdict": "requires_research", "database_execution": "not_run"}
    cid = identity("change", change)
    change["id"] = cid
    tasks = []
    with store.transaction():
        if enqueue:
            for uid, reasons in sorted(stale.items()):
                tasks.append(create_task(store, snapshot=target, run=target_run, profile=new["profile"], kind="change_research",
                    bundle={"change": cid, "knowledge_id": uid, "question": "Recheck changed premises, contract and all consuming pages",
                            "reasons": reasons, "old_revision": revision}))
            for asset in change["new_unexplained_assets"]:
                tasks.append(create_task(store, snapshot=target, run=target_run, profile=new["profile"], kind="asset_discovery",
                    bundle={"change": cid, "asset": asset, "question": "Resolve newly added implementation/feature coverage"}))
        change["refresh_tasks"] = tasks
        store.db.execute("INSERT OR REPLACE INTO changes VALUES(?,?,?)", (cid, now(), canonical(change)))
        store.event("change", {"id": cid, "stale_units": len(stale), "tasks": len(tasks)})
    return change
