"""Reproduce the local knowledge lifecycle without an external model or database server.

This is a synthetic software-protocol acceptance run, not product-semantic validation.
"""
import argparse
import json
from pathlib import Path
import time

from verify_ecs_workflow import exercise
from unified_knowledge import publication, retrieval_pipeline, evaluation, query_api, study
from unified_knowledge.store import Store, atomic_write, canonical


def verify(output):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    began = time.monotonic()
    legacy = exercise(output / "workflow")
    home = output / "workflow" / "hub"
    with Store(home) as store:
        source = query_api.source_manifest(store, study.current(store))
        release = publication.prepare(store)
        synced = publication.sync(store, release["id"])
        assert synced["status"] == "ready"
        publication.activate(store, release["id"])
        assert publication.prepare(store)["id"] == release["id"]
        pack = retrieval_pipeline.context(store, "cg_consume fixture", targets=["cg_consume"])
        assert pack["groups"] and all(g["complete"] for g in pack["groups"])
        assert all(store.evidence_in_scope(e, source["source_snapshot"]) for g in pack["groups"] for e in g["evidence"])
        dataset = {"schema":"knowledge-evaluation/v1","release_id":release["id"],"cases":[
            {"id":"fixture-contract","group":"fixture-forwarding","split":"acceptance","question":"cg_consume fixture",
             "targets":["cg_consume"],"answerable":True,"topics":["contract"],"necessary_unit_sets":[["ecs-fixture-executor"]]},
            {"id":"fixture-unknown","group":"fixture-unknown","split":"acceptance","question":"zzz_unrelated_unimplemented_zzy",
             "answerable":False,"topics":["unknown"],"necessary_unit_sets":[]}]}
        evaluated = evaluation.evaluate(store, dataset)
        assert evaluated["summary"]["complete_context_rate"] == 1
        assert evaluated["summary"]["unanswerable_no_context_rate"] == 1
        atomic_write(output / "source-binding.json", canonical(source) + "\n")
        atomic_write(output / "context.json", canonical(pack) + "\n")
        atomic_write(output / "evaluation-cases.json", canonical(dataset) + "\n")
        atomic_write(output / "evaluation-report.json", canonical(evaluated) + "\n")
    report = {"result":"passed","validation":"synthetic local lifecycle; not product-semantic or model accuracy acceptance",
              "legacy_workflow":legacy,"release_id":release["id"],"workspace":str(home),"provider":"local",
              "external_model_calls":0,"database_execution":"not_run","seconds":round(time.monotonic()-began,3)}
    atomic_write(output / "report.json", canonical(report) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    print(json.dumps(verify(parser.parse_args().output), ensure_ascii=False, indent=2))
