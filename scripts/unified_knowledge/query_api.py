"""Compact indexed source queries with keyset pagination and SQL time budgets."""
import base64
from contextlib import contextmanager
import json
import sqlite3
import time

from .store import canonical, digest, require


@contextmanager
def execution_budget(store, timeout_ms=2000):
    require(type(timeout_ms) is int and 1 <= timeout_ms <= 10000, "timeout_ms must be 1..10000")
    deadline = time.monotonic() + timeout_ms / 1000
    store.db.set_progress_handler(lambda: int(time.monotonic() > deadline), 1000)
    try:
        yield
    except sqlite3.OperationalError as exc:
        if "interrupt" in str(exc).lower():
            raise ValueError("Query execution budget exhausted; result is unknown, not empty") from exc
        raise
    finally:
        store.db.set_progress_handler(None, 0)


def _cursor(value, scope):
    if value is None:
        return ""
    require(isinstance(value, str) and len(value) <= 4096, "Invalid cursor")
    try:
        row = json.loads(base64.urlsafe_b64decode(value.encode("ascii")))
    except (ValueError, UnicodeError) as exc:
        raise ValueError("Invalid cursor") from exc
    require(isinstance(row, dict) and row.get("scope") == scope and isinstance(row.get("after"), str), "Cursor belongs to another query or version")
    return row["after"]


def _next(scope, after):
    return base64.urlsafe_b64encode(canonical({"scope": scope, "after": after}).encode()).decode("ascii")


def _page(rows, scope, limit, max_bytes, *, fields="items"):
    require(type(limit) is int and 1 <= limit <= 200, "limit must be 1..200")
    require(type(max_bytes) is int and 1024 <= max_bytes <= 262144, "Invalid internal response budget")
    result = {fields: [], "truncated": False, "next_cursor": None, "query_scope": scope}
    for row in rows[:limit]:
        result[fields].append(row)
        # Reserve room for the version-bound continuation and explicit omission report.
        if len(canonical(result).encode()) + 1024 > max_bytes:
            result[fields].pop()
            result["truncated"] = True
            result["stop_reason"] = "response_byte_budget"
            break
    result["truncated"] |= len(rows) > len(result[fields])
    if result["truncated"]:
        if result[fields]:
            result["next_cursor"] = _next(scope, result[fields][-1]["id"])
        else:
            result["stop_reason"] = "single_item_exceeds_budget"
    for _ in range(3):
        result["returned_bytes"] = len(canonical(result).encode())
    require(result["returned_bytes"] <= max_bytes, "Response envelope exceeds budget")
    return result


def _binding(store, run):
    index = store.record("runs", run)
    require(index["status"] in {"ready", "partial"}, "Index is not queryable")
    return {"run": run, "snapshot": index["snapshot"], "profile": index["profile"],
            "facts_digest": index.get("facts_digest"), "index_status": index["status"]}, index


def _sources(store, table, run):
    sources = [("main", run)]
    if store.graph_path:
        row = store.db.execute("SELECT upstream FROM main.graph_bindings WHERE study=?", (run,)).fetchone()
        if row:
            sources.append(("source_graph", row[0]))
    return sources


def _seek_index(store, schema, table, column):
    # ORDER BY id otherwise tempts SQLite to scan the whole run's primary key,
    # instead of seeking name/source first. Handoffs may use different index names.
    cache = getattr(store, "_query_seek_indexes", {})
    key = (schema, table, column)
    if key not in cache:
        indexes = store.db.execute("PRAGMA " + schema + ".index_list(" + table + ")").fetchall()
        chosen = None
        for item in indexes:
            name = item["name"]
            columns = [row["name"] for row in store.db.execute("PRAGMA " + schema + '.index_info("' + name.replace('"','""') + '")')]
            if columns[:2] == ["run", column]:
                chosen = name
                break
        require(chosen, "Source index lacks bounded lookup index for " + table + "." + column)
        cache[key] = ' INDEXED BY "' + chosen.replace('"','""') + '"'
        store._query_seek_indexes = cache
    return cache[key]


def lookup_symbols(store, run, query, *, limit=30, cursor=None, max_bytes=32768, timeout_ms=2000):
    require(type(max_bytes) is int and 2048 <= max_bytes <= 262144, "max_bytes must be 2048..262144")
    require(isinstance(query, str) and 1 <= len(query) <= 2000, "Exact symbol ID or name required")
    require(type(limit) is int and 1 <= limit <= 200, "limit must be 1..200")
    binding, _ = _binding(store, run)
    scope = digest(["symbols/v1", binding, query])
    after = _cursor(cursor, scope)
    projection = ("id,logical,substr(name,1,500) name,asset,kind,json_extract(data,'$.definition') definition,"
                  "json_extract(data,'$.start') start,json_extract(data,'$.end') end,json_extract(data,'$.evidence') evidence")
    with execution_budget(store, timeout_ms):
        found = {}
        for schema, physical_run in _sources(store, "symbols", run):
            for column in ("name", "id"):
                hint = _seek_index(store, schema, "symbols", column)
                rows = store.db.execute("SELECT " + projection + " FROM " + schema + ".symbols" + hint +
                    " WHERE run=? AND " + column + "=? AND id>? ORDER BY id LIMIT ?", (physical_run, query, after, limit + 1))
                for row in rows:
                    found.setdefault(row["id"], dict(row))
    rows = [found[key] for key in sorted(found)[:limit + 1]]
    result = _page(rows, scope, limit, max_bytes - 512)
    return {**result, **binding, "match": "exact_name_or_id", "budget": {"timeout_ms":timeout_ms,"max_bytes":max_bytes}}


def neighbors(store, run, symbol, *, direction="forward", kinds=None, limit=60, cursor=None, max_bytes=32768, timeout_ms=2000):
    require(type(max_bytes) is int and 2048 <= max_bytes <= 262144, "max_bytes must be 2048..262144")
    require(direction in {"forward", "reverse", "both"}, "Invalid graph direction")
    require(isinstance(symbol, str) and 1 <= len(symbol) <= 2000, "Exact symbol ID required")
    require(type(limit) is int and 1 <= limit <= 200, "limit must be 1..200")
    kinds = sorted(set(kinds or ["CALLS"]))
    require(1 <= len(kinds) <= 20 and all(isinstance(k, str) and len(k) < 80 for k in kinds), "Invalid relation kinds")
    binding, index = _binding(store, run)
    scope = digest(["neighbors/v1", binding, symbol, direction, kinds])
    after = _cursor(cursor, scope)
    columns = ["source", "target"] if direction == "both" else ["source" if direction == "forward" else "target"]
    fields = ("id,source,target,kind,resolution,json_extract(data,'$.evidence') evidence,"
              "json_extract(data,'$.target_binding') target_binding,json_extract(data,'$.call_form') call_form")
    with execution_budget(store, timeout_ms):
        found = store.db.execute("SELECT 1 FROM symbols WHERE run=? AND id=? LIMIT 1", (run, symbol)).fetchone()
        require(found, "Symbol ID not found in bound index")
        selected = {}
        for schema, physical_run in _sources(store, "relations", run):
            for column in columns:
                hint = _seek_index(store, schema, "relations", column)
                rows = store.db.execute("SELECT " + fields + " FROM " + schema + ".relations" + hint +
                    " WHERE run=? AND " + column + "=? AND id>? AND kind IN (" + ",".join("?" for _ in kinds) + ") ORDER BY id LIMIT ?",
                    [physical_run, symbol, after, *kinds, limit + 1])
                for row in rows:
                    selected.setdefault(row["id"], dict(row))
        rows = [selected[key] for key in sorted(selected)[:limit + 1]]
    legacy = index.get("graph_storage") == "reference" and "call_binding" not in index.get("coverage", {})
    for row in rows:
        if legacy and row["kind"] == "CALLS":
            row["stored_resolution"] = row["resolution"]
            row["resolution"] = "candidate" if row["resolution"] == "resolved" else row["resolution"]
            row["target_binding"] = "legacy_requires_binding_review"
    result = _page(rows, scope, limit, max_bytes - 768, fields="relations")
    return {**result, **binding, "direction":direction, "depth":1, "runtime_trace":False,
            "binding_notice":"Legacy edges require binding review" if legacy else "Resolution is the analyzer's static result",
            "budget":{"timeout_ms":timeout_ms,"max_bytes":max_bytes}}


def evidence(store, snapshot, evidence_id, *, max_chars=12000):
    anchor = store.record("anchors", evidence_id)
    require(store.evidence_in_scope(anchor, snapshot), "Evidence belongs to another source snapshot")
    require(type(max_chars) is int and 1 <= max_chars <= 64000, "Evidence max_chars must be 1..64000")
    return store.read_evidence(evidence_id, max_chars=max_chars)


def source_manifest(store, plan):
    index = store.record("runs", plan["run"])
    snapshot = store.record("snapshots", plan["snapshot"])
    profile = store.profile(plan["snapshot"], plan["profile"])
    return {"schema":"source-binding/v1", "product":snapshot.get("product"), "source_snapshot":plan["snapshot"],
            "build_profile":plan["profile"], "build_profile_digest":profile["digest"], "index_run":plan["run"],
            "index_facts_digest":index.get("facts_digest"), "source_index":plan.get("source_index"),
            "index_status":index["status"], "index_coverage":index.get("coverage", {}),
            "adapter_digest":plan.get("product_adapter", {}).get("digest"), "method_pack_digest":snapshot.get("methods_digest"),
            "capability_limits":["Static relations are not runtime traces", "Unobserved macro branches require another real profile or source review",
                                 "A calls-only index does not establish complete macro expansion or field-flow coverage"],
            "database_execution":"not_run"}
