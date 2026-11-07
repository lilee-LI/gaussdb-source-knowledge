"""Release-bound retrieval and atomic evidence groups shared by HTTP, MCP and CLI."""
from collections import defaultdict
from urllib.parse import quote

from . import publication, query_api
from .knowledge import content_hash, freshness
from .ragflow_provider import Ragflow
from .retrieval import search as local_search
from .store import canonical, require


def retrieve(store, question, *, release_id=None, targets=None, limit=20, provider_client=None):
    require(isinstance(question, str) and 0 < len(question.strip()) <= 8000, "Question must contain 1..8000 characters")
    require(type(limit) is int and 1 <= limit <= 100, "Retrieval limit must be 1..100")
    release = publication.get(store, release_id)
    bound = release["binding"]
    request = {"query":question,"targets":targets or [],"source_snapshot":bound["source_snapshot"],
               "build_profile":bound["build_profile"],"index_run":bound["index_run"],"knowledge_revision":release["knowledge_revision"]}
    with query_api.execution_budget(store, 10000):
        lexical = local_search(store, request, limit=limit)
    ranked = [lexical["hits"]]
    mode = release["provider"]["kind"]
    rejected = []
    if mode == "ragflow":
        client = Ragflow(release["provider"], client=provider_client)
        try:
            chunks = client.retrieve(release["dataset_id"], release["id"], question, limit)
        finally:
            client.close()
        by_document = {v["document_id"]:uid for uid,v in release["sync"].items() if v.get("document_id")}
        external, seen = [], set()
        for item in chunks:
            uid = by_document.get(item.get("document_id"))
            if item.get("dataset_id") != release["dataset_id"] or uid is None:
                rejected.append({"reason":"foreign_dataset_or_document", "chunk_id":str(item.get("id", ""))[:200]})
                continue
            if uid not in seen:
                external.append({"id":uid})
                seen.add(uid)
        ranked.append(external)
    scores = defaultdict(float)
    for hits in ranked:
        for rank, hit in enumerate(hits, 1):
            scores[hit["id"]] += 1 / (60 + rank)
    rows = store.units(release["knowledge_revision"], ids=list(scores))
    # Resolve dependencies against the same revision, not the mutable current head.
    from .knowledge import UnitMap
    units = UnitMap(store, release["knowledge_revision"], rows)
    hits = []
    for uid in sorted(scores, key=lambda k:(-scores[k], k)):
        unit = units.get(uid)
        spec = release["documents"].get(uid)
        if not unit or not spec or content_hash(unit) != spec["content_hash"]:
            rejected.append({"id":uid,"reason":"unit_content_hash_mismatch"})
            continue
        reasons = freshness(store, unit, bound["source_snapshot"], bound["index_run"], units)
        if reasons:
            rejected.append({"id":uid,"reason":"stale_knowledge","details":reasons})
            continue
        hits.append({"id":uid,"title":unit["title"],"kind":unit["kind"],"content_hash":spec["content_hash"],"score":round(scores[uid],8)})
    return {"release_id":release["id"],"binding":bound,"knowledge_revision":release["knowledge_revision"],"provider":mode,
            "retrieval_config_digest":release["retrieval_config_digest"],"hits":hits[:limit],"rejected":rejected,
            "seed_symbols":lexical["seed_symbols"],"unresolved_targets":lexical["unresolved_targets"],
            "truncated":lexical["truncated"] or len(hits) > limit,
            "semantic_embedding":release["provider"].get("embedding_model")}


def context(store, question, *, release_id=None, targets=None, limit=20, max_bytes=60000, provider_client=None, _retrieved=None):
    require(type(max_bytes) is int and 4096 <= max_bytes <= 256000, "Context byte budget must be 4096..256000")
    found = _retrieved or retrieve(store, question, release_id=release_id, targets=targets, limit=limit, provider_client=provider_client)
    require(not release_id or found["release_id"] == release_id, "Context retrieval belongs to another release")
    release = publication.get(store, found["release_id"])
    from .knowledge import UnitMap
    units = UnitMap(store, release["knowledge_revision"], {})
    pack = {"schema":"knowledge-evidence-context/v1", "release_id":release["id"],
            "scope":{k:release["binding"][k] for k in ("product","source_snapshot","build_profile","index_run")},
            "knowledge_revision":release["knowledge_revision"],"groups":[],"omitted":[],"unknowns":[],
            "retrieval":{"provider":found["provider"],"config_digest":found["retrieval_config_digest"],"candidate_ids":[h["id"] for h in found["hits"]]},
            "status":"no_answer","runtime_validation":"not_run","truncated":found["truncated"]}
    if found["rejected"]:
        pack["unknowns"].append({"code":"rejected_retrieval_candidates","count":len(found["rejected"])})
    if found["unresolved_targets"]:
        pack["unknowns"].append({"code":"unresolved_symbol_targets","targets":found["unresolved_targets"]})
    if release["binding"]["index_status"] != "ready" or release["binding"]["build_profile"] == "unknown":
        pack["unknowns"].append({"code":"index_or_build_coverage_incomplete"})
    included = set()
    for hit in found["hits"]:
        if hit["id"] in included:
            continue
        queue, needed, error = [hit["id"]], {}, None
        while queue:
            uid = queue.pop(0)
            if uid in needed:
                continue
            if len(needed) >= 30:
                error = "knowledge_dependency_budget"
                break
            unit = units.get(uid)
            if not unit or uid not in release["documents"] or content_hash(unit) != release["documents"][uid]["content_hash"]:
                error = "missing_or_changed_knowledge_dependency"
                break
            if freshness(store, unit, found["binding"]["source_snapshot"], found["binding"]["index_run"], units):
                error = "stale_knowledge_dependency"
                break
            needed[uid] = unit
            queue.extend(d["ref"] for d in unit.get("_binding", {}).get("knowledge_dependencies", []))
            expected = unit.get("expected_from", {})
            if expected.get("kind") in {"claim","contract","requirement"}:
                queue.append(expected["ref"])
        group = {"root":hit["id"],"units":[],"evidence":[],"complete":False}
        if not error:
            refs = sorted({ref for unit in needed.values() for ref in unit.get("source_refs", [])})
            if len(refs) > 60:
                error = "evidence_count_budget"
            else:
                for ref in refs:
                    try:
                        evidence = query_api.evidence(store, found["binding"]["source_snapshot"], ref, max_chars=64000)
                        if evidence["truncated"]:
                            error = "evidence_range_exceeds_budget"
                            break
                        evidence["url"] = "/evidence/" + quote(ref, safe="") + "?release_id=" + quote(release["id"], safe="")
                        group["evidence"].append(evidence)
                    except (ValueError, OSError):
                        error = "evidence_unavailable_or_wrong_version"
                        break
        if error:
            pack["omitted"].append({"id":hit["id"],"reason":error})
            continue
        group["units"] = [{k:v for k,v in unit.items() if k != "_binding"} for unit in needed.values()]
        group["complete"] = True
        pack["groups"].append(group)
        if len(canonical(pack).encode()) + 3000 > max_bytes:
            pack["groups"].pop()
            pack["omitted"].append({"id":hit["id"],"reason":"whole_evidence_group_exceeds_remaining_budget"})
        else:
            included.update(needed)
    pack["truncated"] |= bool(pack["omitted"])
    pack["status"] = "context_ready" if pack["groups"] and not pack["truncated"] else "partial" if pack["groups"] else "no_answer"
    if not pack["groups"]:
        pack["unknowns"].append({"code":"no_complete_supported_evidence_group"})
    pack["budget"] = {"max_bytes":max_bytes,"counting":"utf8_bytes","atomic_evidence_groups":True}
    # An exceptionally long list of omitted IDs is itself bounded, with a count kept.
    pack["omitted_count"] = len(pack["omitted"])
    pack["omitted"] = pack["omitted"][:10]
    if len(canonical(pack).encode()) > max_bytes:
        pack["retrieval"].pop("candidate_ids", None)
        pack["omitted"] = []
    require(len(canonical(pack).encode()) <= max_bytes, "Context envelope exceeds budget")
    return pack
