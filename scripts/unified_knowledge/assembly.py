"""Join scoped module graphs at an explicit integration point without reparsing C++."""
from collections import Counter
import json

from .graph_facts import link_calls
from .store import canonical, digest, identity, now, require
from .study import current


def integrate(store, run_ids=(), profile=None):
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
    rid = identity("assembled", ["assemble/v2", [(r["id"], r["facts_digest"]) for r in inputs]])
    units, files = {}, set()
    for run in inputs:
        files.update(run.get("selected_files") or [])
        for tu in run["tu_results"]:
            proof = (tu.get("cache_key"), tu["status"], sorted((d.get("asset") or d["path"], d["sha"]) for d in tu["includes"]))
            previous = units.get(tu["context"])
            require(not previous or previous[0] == proof, "Conflicting TU inputs; supply current compatible runs explicitly")
            units[tu["context"]] = (proof, tu)
    with store.transaction():
        head = "index_head:" + plan["snapshot"] + ":" + profile
        exists = store.db.execute("SELECT 1 FROM runs WHERE id=?", (rid,)).fetchone()
        if exists:
            store.set_meta(head, rid)
            return store.record("runs", rid)
        for run in inputs:
            for row in store.db.execute("SELECT data FROM symbols WHERE run=?", (run["id"],)):
                s = json.loads(row[0])
                prior = store.db.execute("SELECT data FROM symbols WHERE run=? AND id=?", (rid, s["id"])).fetchone()
                if prior:
                    old = json.loads(prior[0])
                    require(old["evidence"] == s["evidence"] and old.get("type") == s.get("type"),
                            "Conflicting symbol occurrences in this build profile")
                    s["contexts"] = sorted(set(old["contexts"]) | set(s["contexts"]))
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
        store.db.execute("INSERT INTO runs VALUES(?,?,?,?,?,?)",
                         (rid, plan["snapshot"], profile, record["created"], record["status"], canonical(record)))
        store.set_meta(head, rid)
        store.event("graphs_integrated", {"run": rid, "inputs": record["inputs"], "binding": links})
    return record
