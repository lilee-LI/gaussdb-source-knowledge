"""Join scoped module graphs at an explicit integration point without reparsing C++."""
from collections import Counter
import json
from pathlib import Path

from .graph_facts import link_calls
from .store import canonical, digest, identity, now, require


def merge_occurrences(old, incoming, *, native=False):
    """Keep a physical occurrence's type observations bound to their TU contexts."""
    require(old["evidence"] == incoming["evidence"],
            "Conflicting symbol evidence in this build profile")
    merged = dict(incoming)
    merged["contexts"] = sorted(set(old["contexts"]) | set(incoming["contexts"]))
    if old.get("type") == incoming.get("type") and not (
            old.get("type_observations") or incoming.get("type_observations")):
        return merged
    require(native, "Conflicting symbol occurrences in this build profile")
    observations = {}
    context_types = {}
    for item in (old, incoming):
        for observation in item.get("type_observations") or [
                {"type":item.get("type"), "contexts":item["contexts"]}]:
            value = observation["type"]
            for context in observation["contexts"]:
                require(context not in context_types or context_types[context] == value,
                        "Conflicting symbol types in the same TU context")
                context_types[context] = value
                observations.setdefault(value, set()).add(context)
    merged["type"] = None
    merged["type_resolution"] = "context_dependent"
    merged["type_observations"] = sorted(
        ({"type":kind,"contexts":sorted(contexts)} for kind,contexts in observations.items()),
        key=canonical)
    return merged


def integrate(store, run_ids=(), profile=None, *, snapshot=None, retry_failed=False):
    if snapshot:
        plan = {"snapshot":snapshot,"profile":profile}
    else:
        from .study import current
        plan = current(store)
    profile = profile or plan["profile"]
    if not run_ids:
        run_ids = [r[0] for r in store.db.execute(
            "SELECT id FROM runs WHERE snapshot=? AND profile=? AND status IN ('ready','partial') "
            "AND json_extract(data,'$.mode')='selected' ORDER BY id", (plan["snapshot"], profile))]
    require(run_ids, "No module graphs to integrate; use focus or receive a module result first")
    inputs = [store.record("runs", k) for k in sorted(set(run_ids))]
    require(all(r["snapshot"] == plan["snapshot"] and r["profile"] == profile and r["status"] in {"ready", "partial"}
                and r.get("mode") in {"selected", "full"} for r in inputs), "Incompatible module graph scope")
    native = {r.get("native_facts") for r in inputs}
    native_inputs = len(native)==1 and None not in native
    scope = ["assemble/v3" if native_inputs else "assemble/v2", [(r["id"], r["facts_digest"]) for r in inputs]]
    if retry_failed:
        scope.append({"retry_failed":True})
    rid = identity("assembled", scope)
    units, files = {}, set()
    for run in inputs:
        files.update(run.get("selected_files") or [])
        for tu in run["tu_results"]:
            proof = (tu.get("cache_key"), tu["status"], sorted((d.get("asset") or d["path"], d["sha"]) for d in tu.get("includes", [])))
            previous = units.get(tu["context"])
            if retry_failed and previous and previous[1]["status"] != tu["status"] and "failed" in {previous[1]["status"],tu["status"]}:
                failed = previous[1] if previous[1]["status"]=="failed" else tu
                successful = tu if previous[1]["status"]=="failed" else previous[1]
                require(failed.get("cache_key") in {None,successful.get("cache_key")},
                        "Failed TU retry changed its frontend inputs")
                if tu["status"]=="failed":
                    continue
                previous = None
            require(not previous or previous[0] == proof, "Conflicting TU inputs; supply current compatible runs explicitly")
            units[tu["context"]] = (proof, tu)
    with store.transaction():
        head = "index_head:" + plan["snapshot"] + ":" + profile
        exists = store.db.execute("SELECT 1 FROM runs WHERE id=?", (rid,)).fetchone()
        if exists:
            store.set_meta(head, rid)
            return store.record("runs", rid)
        for run in inputs:
            if retry_failed:
                failed = [t["context"] for t in run["tu_results"] if t["status"]=="failed"]
                require(not store.db.execute("SELECT 1 FROM relations WHERE run=? AND json_extract(data,'$.context') IN "
                    "(SELECT value FROM json_each(?)) LIMIT 1",(run["id"],canonical(failed))).fetchone(),
                    "A failed TU contains facts; replace only empty failed attempts")
                if failed:
                    require(not store.db.execute("SELECT 1 FROM symbols s,json_each(s.data,'$.contexts') c WHERE s.run=? "
                        "AND c.value IN (SELECT value FROM json_each(?)) LIMIT 1",(run["id"],canonical(failed))).fetchone(),
                        "A failed TU contains symbols; replace only empty failed attempts")
            for row in store.db.execute("SELECT data FROM symbols WHERE run=?", (run["id"],)):
                s = json.loads(row[0])
                prior = store.db.execute("SELECT data FROM symbols WHERE run=? AND id=?", (rid, s["id"])).fetchone()
                if prior:
                    old = json.loads(prior[0])
                    s = merge_occurrences(old, s, native=native_inputs)
                store.db.execute("INSERT OR REPLACE INTO symbols VALUES(?,?,?,?,?,?,?)",
                                 (rid, s["id"], s["logical"], s["name"], s["asset"], s["kind"], canonical(s)))
            store.db.execute("INSERT OR IGNORE INTO relations SELECT ?,id,source,target,kind,resolution,data FROM relations WHERE run=?", (rid, run["id"]))
        links = link_calls(store, rid)
        available = store.profile(plan["snapshot"], profile)
        counts = Counter(t["status"] for _, t in units.values())
        coverage = {"available_tus": len(available["commands"]), "translation_units": len(units),
                    "deferred_tus": len(available["commands"]) - len(units), "parsed_tus": counts["parsed"],
                    "failed_tus": counts["failed"], "partial_tus": counts["partial"], "call_binding": links,
                    "symbols": store.db.execute("SELECT count(*) FROM symbols WHERE run=?", (rid,)).fetchone()[0],
                    "relations": store.db.execute("SELECT count(*) FROM relations WHERE run=?", (rid,)).fetchone()[0],
                    "semantic_completeness": "not_certified"}
        ready = units and counts["parsed"] == len(available["commands"]) and not available.get("unavailable_commands")
        record = {"id": rid, "snapshot": plan["snapshot"], "profile": profile, "profile_digest": available["digest"],
                  "status": "ready" if ready else "partial", "created": now(), "mode": "assembled",
                  "inputs": [r["id"] for r in inputs], "selected_files": sorted(files), "coverage": coverage,
                  "tu_results": [tu for _, tu in units.values()], "frontend_invocations": 0,
                  "facts_digest": digest([rid, links]), "database_execution": "not_run"}
        if native_inputs:
            record["native_facts"] = next(iter(native))
            record["evidence_assets"] = sorted({a for r in inputs for a in r["evidence_assets"]})
            record["coverage"]["source_evidence_files"] = len(record["evidence_assets"])
            record["tools"] = {"assembly":digest(Path(__file__).read_bytes()),
                               "inputs":{r["id"]:r.get("tools",{}) for r in inputs}}
            record["upstream_frontend_invocations"] = sum(r.get("frontend_invocations",0) for r in inputs)
        store.db.execute("INSERT INTO runs VALUES(?,?,?,?,?,?)",
                         (rid, plan["snapshot"], profile, record["created"], record["status"], canonical(record)))
        store.set_meta(head, rid)
        store.event("graphs_integrated", {"run": rid, "inputs": record["inputs"], "binding": links})
    return record
