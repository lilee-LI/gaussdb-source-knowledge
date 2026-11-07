"""Deterministic retrieval evaluation; semantic answer ratings require separate actual review."""
from collections import defaultdict
import time

from . import publication
from .retrieval_pipeline import context, retrieve
from .store import digest, require


def validate_cases(value):
    require(value.get("schema") == "knowledge-evaluation/v1", "Unsupported evaluation schema")
    cases = value.get("cases")
    require(isinstance(cases, list) and cases, "Evaluation cases required")
    ids, groups = set(), {}
    for case in cases:
        require(case.get("id") and case["id"] not in ids, "Duplicate evaluation case")
        ids.add(case["id"])
        require(case.get("split") in {"development","acceptance"} and case.get("group"), "Explicit split and mechanism group required")
        require(groups.get(case["group"], case["split"]) == case["split"], "Mechanism group leaks across development/acceptance split")
        groups[case["group"]] = case["split"]
        require(isinstance(case.get("question"), str) and case["question"], "Question required")
        require(isinstance(case.get("answerable"), bool), "answerable must be explicit")
        alternatives = case.get("necessary_unit_sets", [])
        require(isinstance(alternatives, list) and all(isinstance(g,list) and g and all(isinstance(v,str) for v in g) for g in alternatives), "Invalid necessary unit sets")
        require(bool(alternatives) == case["answerable"], "Answerable cases require complete acceptable evidence sets")
        require(case.get("topics") and isinstance(case["topics"], list), "Case topic labels required")
    return cases


def evaluate(store, dataset, *, release_id=None, split="acceptance", limit=20, max_bytes=60000, provider_client=None):
    cases = validate_cases(dataset)
    release = publication.get(store, release_id)
    require(dataset.get("release_id") == release["id"], "Evaluation dataset belongs to another release")
    require(split in {"development","acceptance"}, "Unknown evaluation split")
    selected = [c for c in cases if c["split"] == split]
    require(selected, "No cases in selected evaluation split")
    rows = []
    for case in selected:
        for group in case.get("necessary_unit_sets", []):
            require(set(group) <= set(release["documents"]), "Gold unit does not exist in this release")
        began = time.monotonic()
        ranked = retrieve(store, case["question"], release_id=release["id"], targets=case.get("targets"), limit=limit, provider_client=provider_client)
        pack = context(store, case["question"], release_id=release["id"], targets=case.get("targets"), limit=limit, max_bytes=max_bytes, provider_client=provider_client, _retrieved=ranked)
        hits = {h["id"] for h in ranked["hits"]}
        supported = {u["id"] for g in pack["groups"] if g["complete"] for u in g["units"]}
        groups = [set(g) for g in case.get("necessary_unit_sets", [])]
        rows.append({"id":case["id"],"topics":case["topics"],"answerable":case["answerable"],
            "recall":max((len(g & hits)/len(g) for g in groups), default=None),
            "complete_evidence_recalled":any(g <= hits for g in groups) if groups else None,
            "complete_context":any(g <= supported for g in groups) if groups else None,
            "no_answer":pack["status"] == "no_answer", "answer_semantic_correctness":"not_evaluated",
            "seconds":round(time.monotonic()-began,4),"retrieved_ids":sorted(hits),"context_ids":sorted(supported)})
    topics = defaultdict(list)
    for row in rows:
        for topic in row["topics"]:
            topics[topic].append(row)
    def summary(batch):
        known = [r for r in batch if r["answerable"]]
        unknown = [r for r in batch if not r["answerable"]]
        return {"count":len(batch),"answerable_count":len(known),"unanswerable_count":len(unknown),
                "recall_at_k":sum(r["recall"] for r in known)/len(known) if known else None,
                "complete_context_rate":sum(r["complete_context"] for r in known)/len(known) if known else None,
                "unanswerable_no_context_rate":sum(r["no_answer"] for r in unknown)/len(unknown) if unknown else None}
    return {"schema":"knowledge-evaluation-report/v1","release_id":release["id"],"dataset_digest":digest(dataset),"split":split,
            "k":limit,"max_bytes":max_bytes,"provider":release["provider"],"summary":summary(rows),
            "by_topic":{k:summary(v) for k,v in topics.items()},"cases":rows,
            "semantic_answer_accuracy":"requires_separate_review", "database_execution":"not_run"}
