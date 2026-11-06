"""Version-filtered lexical/vector/graph retrieval and bounded task ContextPacks."""
from __future__ import annotations

from collections import Counter
import heapq
import json
import math
import re

from .indexer import query_graph
from .knowledge import UnitMap, content_hash, freshness, knowledge_graph
from .planner import resolve_targets
from .store import canonical, digest, identity, require


LEXICAL_SPACE = "lexical-hash-charword/v1/256"


def terms(text):
    words = re.findall(r"[A-Za-z_][A-Za-z_0-9]*", text.lower())
    for chunk in re.findall(r"[\u3400-\u9fff]+", text):
        words.extend(chunk)
        words.extend(chunk[i:i + 2] for i in range(len(chunk) - 1))
    return words


def embedding(text, dimensions=256):
    vector = [0.0] * dimensions
    for word, count in Counter(terms(text)).items():
        hashed = int(digest(word)[:16], 16)
        vector[hashed % dimensions] += (1 if hashed & 0x10000 else -1) * (1 + math.log(count))
    norm = math.sqrt(sum(v * v for v in vector)) or 1
    return [v / norm for v in vector]


def cosine(a, b):
    require(len(a) == len(b) and a and all(type(v) in {int, float} and math.isfinite(v) for v in [*a, *b]),
            "Embedding dimension/value mismatch")
    norm = math.sqrt(sum(v * v for v in a) * sum(v * v for v in b))
    return sum(x * y for x, y in zip(a, b)) / norm if norm else 0.0


def import_vectors(store, revision, space, vectors):
    require(isinstance(space, str) and space.strip() and space != LEXICAL_SPACE, "Named external embedding space required")
    units = store.units(revision)
    require(units and isinstance(vectors, list) and vectors, "Vector records required")
    dimensions = None
    prepared = []
    for row in vectors:
        uid = row.get("unit")
        require(uid in units and row.get("content_hash") == content_hash(units[uid]), "Vector refers to different knowledge content")
        vector = row.get("vector")
        require(isinstance(vector, list) and 1 <= len(vector) <= 16384, "Invalid vector dimension")
        cosine(vector, vector)
        dimensions = dimensions or len(vector)
        require(dimensions == len(vector), "Mixed embedding dimensions")
        prepared.append((revision, uid, space, canonical(row)))
    with store.transaction():
        prior = store.db.execute("SELECT data FROM vectors WHERE revision=? AND space=? LIMIT 1", (revision, space)).fetchone()
        if prior:
            require(len(json.loads(prior[0])["vector"]) == dimensions, "Embedding space dimension changed")
        store.db.executemany("INSERT OR REPLACE INTO vectors VALUES(?,?,?,?)", prepared)
        store.event("vectors_import", {"revision": revision, "space": space, "records": len(prepared), "dimensions": dimensions})
    return {"revision": revision, "space": space, "records": len(prepared), "dimensions": dimensions}


def _bound_scope(store, request):
    snapshot = request.get("source_snapshot")
    require(isinstance(snapshot, str), "source_snapshot is required")
    store.record("snapshots", snapshot)
    profile = request.get("build_profile", "unknown")
    store.profile(snapshot, profile)
    run = request.get("index_run") or store.get_meta("index_head:" + snapshot + ":" + profile)
    require(run is not None, "No completed index for this snapshot/profile")
    index = store.record("runs", run)
    require(index["snapshot"] == snapshot and index["profile"] == profile and index["status"] in {"ready", "partial"},
            "Index scope mismatch")
    revision = request.get("knowledge_revision", "latest_compatible")
    if revision == "latest_compatible":
        # Revisions can retain unchanged units; applicability is checked per unit below.
        rows = store.db.execute("SELECT id FROM revisions WHERE profile=? AND snapshot=? ORDER BY rowid DESC",
                                (profile, snapshot)).fetchall()
        if not rows:
            rows = store.db.execute("SELECT id FROM revisions WHERE profile=? ORDER BY rowid DESC", (profile,)).fetchall()
        revision = rows[0][0] if rows else None
    elif revision is not None:
        store.record("revisions", revision)
    return snapshot, profile, run, revision


def search(store, request, *, limit=12):
    require(type(limit) is int and 1 <= limit <= 100, "Search limit out of range")
    snapshot, profile, run, revision = _bound_scope(store, request)
    query = request.get("query", "")
    require(isinstance(query, str) and len(query) <= 50000, "Invalid query")
    targets = request.get("targets", [])
    require(isinstance(targets, list) and all(isinstance(v, str) for v in targets), "targets must be strings")
    targets = list(targets)
    if request.get("diff_ref"):
        change = store.record("changes", request["diff_ref"])
        require(snapshot in {change["base_snapshot"], change["target_snapshot"]}, "Diff belongs to another source scope")
        for item in change["changed_assets"]:
            targets.extend(r[0] for r in store.db.execute("SELECT id FROM symbols WHERE run=? AND asset=?",
                                                        (run, item["asset"])))
    seeds, unresolved = resolve_targets(store, run, targets)
    seed_logicals = set()
    for seed in seeds:
        seed_logicals.add(store.db.execute("SELECT logical FROM symbols WHERE run=? AND id=?", (run, seed)).fetchone()[0])
    query_terms = set(terms(query))
    qvec = embedding(query)
    fts_ranks = {}
    if store.fts and query_terms and revision:
        expression = " OR ".join('"' + word.replace('"', '""') + '"' for word in sorted(query_terms)[:100])
        try:
            rows = store.db.execute("SELECT unit FROM search_fts WHERE revision=? AND search_fts MATCH ? ORDER BY bm25(search_fts) LIMIT 100",
                                    (revision, expression)).fetchall()
            fts_ranks = {r[0]: i for i, r in enumerate(rows, 1)}
        except Exception as error:
            # Do not hide the fallback mode; character/word retrieval remains available.
            fts_ranks = {}
    external = {}
    if request.get("query_vector") is not None:
        space = request.get("embedding_space")
        require(isinstance(space, str) and space != LEXICAL_SPACE, "query_vector needs its named embedding_space")
        ranked = []
        for r in store.db.execute("SELECT unit,data FROM vectors WHERE revision=? AND space=?", (revision, space)):
            value = json.loads(r["data"])
            ranked.append((cosine(request["query_vector"], value["vector"]), r["unit"], value))
        external = {uid: value for score, uid, value in heapq.nlargest(100, ranked, key=lambda x: (x[0], x[1]))}
        require(external, "No matching embedding space for this revision")
    candidate_ids = set(fts_ranks) | set(external)
    for logical in seed_logicals:
        candidate_ids.update(r[0] for r in store.db.execute(
            "SELECT unit FROM unit_dependencies WHERE revision=? AND kind='symbol' AND ref=?", (revision, logical)))
    # Chinese substrings and code identifiers are checked by SQLite, then only
    # bounded candidates are decoded/ranked in Python.
    selected_terms = sorted(query_terms, key=lambda x: (-len(x), x))[:24]
    if selected_terms and revision:
        predicates = " OR ".join("instr(lower(c.text),?)>0" for _ in selected_terms)
        sql = ("SELECT r.id FROM revision_units r JOIN unit_versions v ON v.hash=r.hash "
               "JOIN lexical_cache c ON c.hash=json_extract(v.data,'$.content_hash') WHERE r.revision=? AND (" +
               predicates + ") ORDER BY r.id LIMIT 1000")
        candidate_ids.update(r[0] for r in store.db.execute(sql, [revision, *selected_terms]))
    candidate_truncated = len(candidate_ids) > 5000
    candidate_ids = set(sorted(candidate_ids, key=lambda uid: (uid not in fts_ranks, fts_ranks.get(uid, 0), uid))[:5000])
    units = UnitMap(store, revision, store.units(revision, ids=sorted(candidate_ids)) if revision else {})
    hits, stale = [], []
    for uid in sorted(candidate_ids):
        unit = units.get(uid)
        if unit is None:
            continue
        text = unit["title"] + "\n" + unit["body"] + "\n" + canonical(unit.get("conditions", []))
        unit_terms = set(terms(text))
        lexical = len(query_terms & unit_terms) / (len(query_terms) or 1)
        logicals = {d["ref"] for d in unit.get("_binding", {}).get("dependencies", []) if d["type"] == "symbol"}
        aligned = bool(seed_logicals & logicals)
        cache = store.db.execute("SELECT vector FROM lexical_cache WHERE hash=?", (unit["content_hash"],)).fetchone()
        vector = json.loads(cache[0]) if cache else embedding(text)
        score = lexical * 4 + max(0, cosine(qvec, vector)) + (10 if aligned else 0)
        if uid in fts_ranks:
            score += 1 / (1 + fts_ranks[uid])
        modes = ["character_word", "lexical_hash"]
        if uid in external:
            record = external[uid]
            require(record["content_hash"] == content_hash(unit), "Stored vector content drift")
            score += 2 * max(0, cosine(request["query_vector"], record["vector"]))
            modes.append("external_embedding")
        if not (lexical or aligned or uid in fts_ranks or uid in external):
            continue
        reasons = freshness(store, unit, snapshot, run, units)
        item = {"id": uid, "score": round(score, 6), "kind": unit["kind"], "title": unit["title"],
                "retrieval_modes": modes + (["symbol_alignment"] if aligned else [])}
        if reasons:
            stale.append({**item, "reasons": reasons})
        else:
            hits.append(item)
    hits.sort(key=lambda h: (-h["score"], h["id"]))
    return {"snapshot": snapshot, "profile": profile, "run": run, "knowledge_revision": revision,
            "hits": hits[:limit], "stale_candidates": sorted(stale, key=lambda x: -x["score"])[:limit],
            "seed_symbols": sorted(seeds), "unresolved_targets": unresolved, "truncated": len(hits) > limit or candidate_truncated,
            "vector_baseline": LEXICAL_SPACE, "semantic_embedding": request.get("embedding_space")}


def get_context(store, request):
    require(request.get("task") in {"coding", "test_generation", "review", "operations"}, "Unknown task type")
    budget = request.get("token_budget", 8192)
    require(type(budget) is int and 512 <= budget <= 128000, "token_budget must be an integer from 512 to 128000")
    found = search(store, request)
    snapshot, profile, run, revision = found["snapshot"], found["profile"], found["run"], found["knowledge_revision"]
    units = UnitMap(store, revision, store.units(revision, ids=[h["id"] for h in found["hits"]]) if revision else {})
    selected = {h["id"] for h in found["hits"]}
    # Expand explicit semantic dependencies/consumers, independently of lexical scores.
    frontier = set(selected)
    for _ in range(2):
        following = set()
        for uid in frontier:
            for row in store.db.execute("SELECT source,target FROM semantic_edges WHERE revision=? AND (source=? OR target=?)",
                                        (revision, uid, uid)):
                following.update(row)
        following -= selected
        selected.update(following)
        frontier = following
    constraints, paths, tests, evidence, unknowns, impacts = [], [], [], {}, [], {"confirmed_dependencies": [], "candidate_risks": [], "unresolved": []}
    omitted = []
    used = set()
    for uid in sorted(selected, key=lambda k: (units[k]["kind"] != "contract", k)):
        unit = units[uid]
        reasons = freshness(store, unit, snapshot, run, units)
        if reasons:
            unknowns.append({"code": "stale_knowledge", "id": uid, "reasons": reasons})
            continue
        if unit["kind"] in {"claim", "contract", "requirement", "mechanism", "module", "feature", "responsibility", "decision", "observation"}:
            item = {"id": uid, "kind": unit["kind"], "title": unit["title"], "body": unit["body"],
                    "conditions": unit.get("conditions", []), "counterexamples": unit.get("counterexamples", []),
                    "source_refs": unit.get("source_refs", []), "review_mode": unit["review"]["mode"]}
            if unit["kind"] == "contract":
                item.update({k: unit[k] for k in ("requires", "ensures", "invariants", "producers", "consumers")})
            constraints.append(item)
        elif unit["kind"] == "flow":
            paths.append({"id": uid, "body": unit["body"], "steps": unit.get("steps", []), "source_refs": unit.get("source_refs", [])})
        elif unit["kind"] == "test_obligation":
            tests.append({"id": uid, "body": unit["body"], "expected_from": unit["expected_from"],
                          "execution_status": "not_run", "conditions": unit.get("conditions", []), "source_refs": unit.get("source_refs", [])})
        if unit["kind"] == "contract":
            impacts["confirmed_dependencies"].append({"contract": uid, "producers": unit["producers"],
                "consumers": unit["consumers"], "conditions": unit["conditions"], "source_refs": unit.get("source_refs", []),
                "meaning": "reviewed dependency; actual change effect requires diff analysis"})
        for ref in unit.get("source_refs", []):
            try:
                evidence[ref] = store.read_evidence(ref, max_chars=min(4000, budget))
            except (ValueError, OSError) as error:
                unknowns.append({"code": "hash_mismatch_or_unavailable", "evidence": ref, "reason": str(error)})
        used.add(uid)
    graph = query_graph(store, run, found["seed_symbols"], depth=1, limit=60)
    if graph["relations"]:
        impacts["candidate_risks"] = [{"relation": e["kind"], "source": e["source"], "target": e["target"],
            "evidence": e["evidence"], "resolution": e["resolution"], "semantic_verdict": "requires_review"}
            for e in graph["relations"]]
    if profile == "unknown":
        unknowns.append({"code": "profile_unknown", "meaning": "Raw/source evidence; no arbitrary-build applicability"})
    index = store.record("runs", run)
    if index["status"] == "partial":
        unknowns.append({"code": "index_partial", "coverage": index["coverage"]})
    for target in found["unresolved_targets"]:
        unknowns.append({"code": "relation_unresolved", "target": target})
    unknowns.extend({"code": "stale_knowledge", "id": x["id"], "reasons": x["reasons"]} for x in found["stale_candidates"])
    if not used:
        unknowns.append({"code": "knowledge_insufficient", "meaning": "No applicable reviewed knowledge found"})
    if found["truncated"] or graph["truncated"]:
        unknowns.append({"code": "retrieval_partial", "meaning": "Additional knowledge or graph neighbors were not expanded"})
    pack = {"schema": "context-pack/v1", "scope": {"source_snapshot": snapshot, "build_profile": profile,
            "index_run": run, "knowledge_revision": revision}, "task": request["task"], "constraints": constraints,
            "paths": paths, "impacts": impacts, "test_obligations": tests, "evidence": list(evidence.values()),
            "unknowns": unknowns, "refresh_tasks": [], "retrieval": {"seed_symbols": found["seed_symbols"],
            "knowledge_ids": sorted(used), "modes": sorted({m for h in found["hits"] for m in h["retrieval_modes"]}),
            "semantic_embedding": found["semantic_embedding"]}, "truncated": False, "runtime_validation": "not_run"}
    if request.get("diff_ref"):
        change = store.record("changes", request["diff_ref"])
        pack["scope"]["diff_ref"] = change["id"]
        pack["impacts"]["registered_change"] = {
            "base_snapshot": change["base_snapshot"], "target_snapshot": change["target_snapshot"],
            "changed_assets": change["changed_assets"], "stale_units": sorted(change["stale_units"]),
            "semantic_verdict": "requires_diff_review"}
        pack["refresh_tasks"] = change.get("refresh_tasks", [])
    if any(e["truncated"] for e in pack["evidence"]):
        pack["unknowns"].append({"code": "evidence_partial", "meaning": "Expand cited evidence to read its complete range"})
    # Conservative UTF-8 byte bound. No model-specific tokenizer is pretended.
    def size():
        return len(canonical(pack).encode("utf-8"))
    while size() > max(256, budget - 700):
        pack["truncated"] = True
        # Preserve a usable contract, cited source and test oracle before speculative graph neighbors.
        if pack["impacts"]["candidate_risks"]:
            item=pack["impacts"]["candidate_risks"].pop()
            omitted.append({"kind":"candidate_risk","id":item["evidence"]})
        elif len(pack["constraints"])>1:
            item=pack["constraints"].pop()
            omitted.append({"kind":"constraint","id":item["id"]})
            pack["impacts"]["confirmed_dependencies"]=[x for x in pack["impacts"]["confirmed_dependencies"] if x["contract"]!=item["id"]]
        elif len(pack["evidence"])>1:
            item=pack["evidence"].pop()
            omitted.append({"kind":"evidence","id":item["id"]})
        elif pack["constraints"] and pack["constraints"][0]["kind"]=="contract" and pack["constraints"][0]["body"]:
            # The structured preconditions and guarantees remain available, with original citations.
            item=pack["constraints"][0]
            item["body"]=""
            item["body_omitted_for_budget"]=True
            omitted.append({"kind":"contract_body","id":item["id"]})
        elif pack["impacts"]["confirmed_dependencies"]:
            item=pack["impacts"]["confirmed_dependencies"].pop()
            omitted.append({"kind":"dependency_summary","id":item["contract"]})
        elif pack["evidence"]:
            item=pack["evidence"].pop()
            omitted.append({"kind":"evidence","id":item["id"]})
        elif pack["constraints"]:
            item=pack["constraints"].pop()
            omitted.append({"kind":"constraint","id":item["id"]})
        elif pack["test_obligations"]:
            omitted.append({"kind": "test_obligation", "id": pack["test_obligations"].pop()["id"]})
        elif pack["paths"]:
            omitted.append({"kind": "path", "id": pack["paths"].pop()["id"]})
        elif len(pack["unknowns"]) > 1:
            pack["unknowns"].pop()
        elif pack["retrieval"]:
            pack["retrieval"] = {}
        else:
            break
    pack["budget"] = {"requested_tokens": budget, "counting": "conservative_utf8_bytes",
                      "omitted_items": len(omitted), "evidence_read_truncated": any(e["truncated"] for e in pack["evidence"])}
    if pack["truncated"]:
        pack["status"] = "budget_partial"
        # The small summary avoids itself exceeding a narrow response budget.
        pack["budget"]["omitted_kinds"] = sorted({x["kind"] for x in omitted})
    else:
        pack["status"] = "partial" if unknowns else "ok"
    pack["budget"]["returned_utf8_bytes"] = len(canonical(pack).encode("utf-8"))
    if len(canonical(pack).encode("utf-8")) > budget:
        pack = {"schema": "context-pack/v1", "scope": {"source_snapshot": snapshot, "build_profile": profile,
                "knowledge_revision": revision}, "task": request["task"], "status": "budget_partial",
                "truncated": True, "unknowns": [{"code": "budget_insufficient_for_complete_pack"}],
                "budget": {"requested_tokens": budget, "counting": "conservative_utf8_bytes"}}
    for _ in range(3):
        pack["budget"]["returned_utf8_bytes"] = len(canonical(pack).encode("utf-8"))
    return pack


def request_refresh(store, request):
    from .planner import create_task, resolve_targets
    snapshot, profile, run, revision = _bound_scope(store, request)
    require(request.get("query") or request.get("targets"), "Refresh needs a concrete question or target")
    symbols, unresolved = resolve_targets(store, run, request.get("targets", []))
    refs = [json.loads(r[0])["evidence"] for symbol in symbols for r in store.db.execute(
        "SELECT data FROM symbols WHERE run=? AND id=?", (run, symbol))]
    with store.transaction():
        task = create_task(store, snapshot=snapshot, run=run, profile=profile, kind="context_gap",
            bundle={"question": request.get("query", "Resolve task targets"), "targets": request.get("targets", []),
                    "symbol_refs": sorted(symbols), "source_anchor_refs": refs, "unresolved_targets": unresolved,
                    "knowledge_revision": revision, "reason": "online_context_gap", "required_views": ["contract", "evidence", "tests"]})
        store.event("online_refresh_requested", {"task": task, "snapshot": snapshot, "revision": revision})
    return {"refresh_tasks": [task], "status": "queued_or_existing", "automatic_semantic_approval": False}


def knowledge_delta(store, base_revision, target_revision):
    store.record("revisions", base_revision)
    store.record("revisions", target_revision)
    before, after = store.units(base_revision), store.units(target_revision)
    common = set(before) & set(after)
    return {"base_revision": base_revision, "target_revision": target_revision,
            "added": sorted(set(after) - set(before)), "removed": sorted(set(before) - set(after)),
            "content_changed": sorted(uid for uid in common if content_hash(before[uid]) != content_hash(after[uid])),
            "bindings_changed": sorted(uid for uid in common if before[uid].get("_binding") != after[uid].get("_binding")),
            "runtime_validation": "not_run"}


def explain_path(store, request):
    snapshot, profile, run, revision = _bound_scope(store, request)
    targets, unresolved = resolve_targets(store, run, request.get("targets", []))
    return {"scope": {"snapshot": snapshot, "profile": profile, "run": run, "knowledge_revision": revision},
            "code_graph": query_graph(store, run, targets, depth=request.get("depth", 2), limit=request.get("limit", 100)),
            "knowledge_graph": knowledge_graph(store, revision), "unresolved": unresolved,
            "semantics": "Code edges are typed; data stages and contracts are not automatically direct calls"}
