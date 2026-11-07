"""Read-only bounded source query replay against an existing real index workspace."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import math
from pathlib import Path
import statistics
import time

from unified_knowledge import query_api, study
from unified_knowledge.store import Store, atomic_write, canonical, require


def benchmark(home, *, symbol="ExecSort", concurrency=8, requests=80):
    require(1 <= concurrency <= 32 and concurrency <= requests <= 1000, "Invalid benchmark workload")
    with Store(home, readonly=True) as store:
        plan = study.current(store)
        manifest = query_api.source_manifest(store, plan)
        initial = query_api.lookup_symbols(store, plan["run"], symbol)
        selected = next((row for row in initial["items"] if row["definition"]), None)
        require(selected, "No matching defined symbol in the bound source index")
        symbol_id = selected["id"]
        source = query_api.evidence(store, plan["snapshot"], selected["evidence"])
        assert not source["truncated"] or source["returned_chars"] > 0
        graph_bytes = store.graph_path.stat().st_size if store.graph_path else (store.home / "knowledge.sqlite3").stat().st_size
        local_counts = {name:store.db.execute("SELECT count(*) FROM main." + name).fetchone()[0] for name in ("symbols","relations")}
    def one(_):
        started = time.perf_counter()
        with Store(home, readonly=True) as store:
            opened = time.perf_counter()
            result = query_api.neighbors(store, plan["run"], symbol_id, limit=60)
            completed = time.perf_counter()
        return {"query_ms":(completed-opened)*1000,"including_open_ms":(completed-started)*1000,
                "response_bytes":len(canonical(result).encode()),"relations":len(result["relations"]),"truncated":result["truncated"]}
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        samples = list(pool.map(one, range(requests)))
    def stats(key):
        values = sorted(r[key] for r in samples)
        return {"p50":round(statistics.median(values),3),"p95":round(values[math.ceil(.95*len(values))-1],3),"max":round(max(values),3)}
    return {"schema":"source-gateway-benchmark/v1","binding":manifest,"symbol":symbol,"symbol_id":symbol_id,
            "graph_bytes":graph_bytes,"local_fact_counts":local_counts,"concurrency":concurrency,"requests":requests,
            "cache_condition":"OS cache not cleared; lookup and evidence read performed before measurement",
            "query_ms":stats("query_ms"),"including_workspace_open_ms":stats("including_open_ms"),
            "max_response_bytes":max(r["response_bytes"] for r in samples),"relation_counts":sorted({r["relations"] for r in samples}),
            "truncated_responses":sum(r["truncated"] for r in samples),"frontend_invocations":0,"database_execution":"not_run",
            "limitations":"One symbol and one hop; not whole-repository semantic coverage, cold-cache or end-to-end model latency"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--symbol", default="ExecSort")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--requests", type=int, default=80)
    args = parser.parse_args()
    report = benchmark(args.home, symbol=args.symbol, concurrency=args.concurrency, requests=args.requests)
    atomic_write(args.output, canonical(report) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
