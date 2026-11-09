"""Read-only, bounded source-reading plans inside module/feature tasks.

The graph helps order reading; it neither creates one task per function nor
proves that a file or feature has been understood. No receipt is written here.
"""
from collections import defaultdict
import json

import networkx as nx

from .knowledge import UnitMap, freshness
from .planner import task_status
from .query_api import _sources, _seek_index, execution_budget
from .store import canonical, digest, require
from .study import current


def _selected_files(store, task, plan):
    bundle = task["bundle"]
    module = bundle.get("module")
    available = plan.get("modules", {}).get(module, {}).get("files", [])
    selected = bundle.get("selected_files")
    if selected is None:
        selected = bundle.get("file_assets") or available
    selected = list(selected or [])
    explicit_selection = set(selected)
    selected += [bundle["asset"]] if bundle.get("asset") else []
    # Original symbol tasks and document tasks still work without a module.
    for ref in bundle.get("source_anchor_refs", []):
        anchor = store.record("anchors", ref)
        if store.evidence_in_scope(anchor, task["snapshot"]):
            selected.append(anchor["asset"])
    for symbol in bundle.get("symbol_refs", [])[:200]:
        row = store.db.execute("SELECT asset FROM symbols WHERE run=? AND id=?", (task["run"], symbol)).fetchone()
        if row:
            selected.append(row[0])
    normalized = []
    for key in sorted(set(selected)):
        row = store.db.execute("SELECT key FROM assets WHERE snapshot=? AND (key=? OR path=?) AND status<>'excluded' ORDER BY key LIMIT 2",
                               (task["snapshot"], key, key)).fetchall()
        require(len(row) <= 1, "Ambiguous task file: " + key)
        if row:
            if available and bundle.get("selected_files") is not None and key in explicit_selection:
                require(row[0][0] in available, "Selected file is outside its task module")
            normalized.append(row[0][0])
    return sorted(set(normalized))


def _graph(store, run, files, *, node_limit=120, edge_limit=200):
    """Build only the induced graph of a bounded file/symbol page.

    Every returned SCC has all its members and internal/cross edges in this
    induced graph. If the edge page is incomplete, no SCC order is asserted.
    Boundary edges remain typed and are never converted into confirmed calls.
    """
    nodes, edges = {}, {}
    nodes_truncated = edges_truncated = False
    projection = ("id,logical,name,asset,kind,json_extract(data,'$.start') start,"
                  "json_extract(data,'$.end') end,json_extract(data,'$.evidence') evidence,"
                  "json_extract(data,'$.definition') definition")
    with execution_budget(store, 2000):
        for schema, physical_run in _sources(store, "symbols", run):
            hint = _seek_index(store, schema, "symbols", "asset")
            for asset in files:
                rows = store.db.execute("SELECT " + projection + " FROM " + schema + ".symbols" + hint +
                    " WHERE run=? AND asset=? ORDER BY id LIMIT ?", (physical_run, asset, node_limit + 1)).fetchall()
                for row in rows:
                    if len(nodes) >= node_limit and row["id"] not in nodes:
                        nodes_truncated = True
                    else:
                        nodes.setdefault(row["id"], dict(row))
        fields = ("id,source,target,kind,resolution,json_extract(data,'$.evidence') evidence,"
                  "json_extract(data,'$.target_binding') target_binding")
        for schema, physical_run in _sources(store, "relations", run):
            for column in ("source", "target"):
                hint = _seek_index(store, schema, "relations", column)
                for uid in sorted(nodes):
                    rows = store.db.execute("SELECT " + fields + " FROM " + schema + ".relations" + hint +
                        " WHERE run=? AND " + column + "=? ORDER BY id LIMIT ?", (physical_run, uid, edge_limit + 1)).fetchall()
                    for row in rows:
                        if len(edges) >= edge_limit and row["id"] not in edges:
                            edges_truncated = True
                        else:
                            edges.setdefault(row["id"], dict(row))
    index = store.record("runs", run)
    legacy = index.get("graph_storage") == "reference" and "call_binding" not in index.get("coverage", {})
    if legacy:
        for edge in edges.values():
            if edge["kind"] == "CALLS":
                edge["stored_resolution"] = edge["resolution"]
                if edge["resolution"] == "resolved":
                    edge["resolution"] = "candidate"
                edge["target_binding"] = "legacy_requires_binding_review"
    internal = [edge for edge in edges.values() if edge["source"] in nodes and edge["target"] in nodes]
    boundary = [edge for edge in edges.values() if edge["source"] not in nodes or edge["target"] not in nodes]
    chunks = []
    if not edges_truncated:
        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from((e["source"], e["target"]) for e in internal if e["kind"] == "CALLS" and e["resolution"] == "resolved")
        condensed = nx.condensation(graph, [set(group) for group in sorted((sorted(g) for g in nx.strongly_connected_components(graph)))])
        for component in reversed(list(nx.lexicographical_topological_sort(condensed))):
            members = sorted(condensed.nodes[component]["members"])
            member_set = set(members)
            chunks.append({"id": "read-chunk:" + digest([run, members])[:24], "members": members,
                           "internal_edges": [e["id"] for e in internal if e["source"] in member_set and e["target"] in member_set],
                           "cross_edges": [e["id"] for e in edges.values() if (e["source"] in member_set) != (e["target"] in member_set)],
                           "learning_task": False})
    connected = {e[endpoint] for e in edges.values() for endpoint in ("source", "target")}
    return {"scope": "induced_graph_of_returned_symbols_in_file_page", "nodes": [nodes[k] for k in sorted(nodes)],
            "relations": [edges[k] for k in sorted(edges)], "boundary_edges": [e["id"] for e in boundary],
            "chunks": chunks, "read_order": "callee_first_scc_postorder" if not edges_truncated else "unknown_edge_page_incomplete",
            "orphan_symbols": sorted(set(nodes) - connected), "nodes_truncated": nodes_truncated,
            "edges_truncated": edges_truncated, "global_scc_completeness": "not_claimed",
            "static_only": True, "binding_notice": "legacy_binding_requires_review" if legacy else "analyzer_static_result"}


def _prerequisites(store, task, revision, maximum=20):
    requested, task_states = set(), []
    for value in task["bundle"].get("requires_knowledge", []):
        uid = value.get("id", value.get("ref")) if isinstance(value, dict) else value
        if isinstance(uid, str):
            requested.add(uid)
    for dep, status in sorted(task["dependency_states"].items()):
        task_states.append({"task": dep, "status": status})
        if status == "accepted":
            result = task_status(store, dep).get("result", {})
            requested.update(row if isinstance(row, str) else row.get("id") for row in result.get("claims", [])
                             if isinstance(row, (str, dict)))
    requested.discard(None)
    units = UnitMap(store, revision, store.units(revision, ids=sorted(requested)[:maximum]) if revision else {})
    reviewed, missing = [], []
    for uid in sorted(requested)[:maximum]:
        unit = units.get(uid) if revision else None
        reasons = freshness(store, unit, task["snapshot"], task["run"], units) if unit else [{"code": "not_published_in_revision"}]
        if reasons:
            missing.append({"id": uid, "reasons": reasons})
        else:
            reviewed.append({k: unit.get(k) for k in ("id", "kind", "title", "conditions", "source_refs", "review")})
    return reviewed, missing, task_states, len(requested) > maximum


def build(store, task, *, max_chars=32768, offset=0, limit=20):
    """Return a paged reading plan without source reads, receipts or mutations."""
    require(type(max_chars) is int and 2048 <= max_chars <= 262144, "max_chars must be 2048..262144")
    require(type(offset) is int and offset >= 0 and type(limit) is int and 1 <= limit <= 100, "Invalid source-file page")
    value = task_status(store, task) if isinstance(task, str) else task_status(store, task["id"])
    bundle = value["bundle"]
    plan = current(store, bundle.get("plan_id"))
    require(plan["snapshot"] == value["snapshot"] and plan["run"] == value["run"], "Task plan/source graph binding mismatch")
    files = _selected_files(store, value, plan)
    selected = files[offset:offset + limit]
    index = store.record("runs", value["run"])
    revision = store.get_meta("knowledge_head")
    reviewed, missing, dependencies, prereq_truncated = _prerequisites(store, value, revision)
    profile = store.profile(value["snapshot"], value["profile"])
    compiled = {profile.get("repository", "") + "/" + command["file"] for command in profile.get("commands", [])}
    # Source reading instructions and reviewed prerequisites need room too.
    # Use a small induced graph by default; callers can request a larger budget
    # or one file per page without rescanning the full repository graph.
    try:
        graph = _graph(store, value["run"], selected, node_limit=min(160, max(8, max_chars // 1800)), edge_limit=min(300, max(12, max_chars // 1100)))
    except ValueError as exc:
        if "Query execution budget exhausted" not in str(exc):
            raise
        graph = {"scope": "file_page", "nodes": [], "relations": [], "chunks": [], "nodes_truncated": True,
                 "edges_truncated": True, "read_order": "unknown_query_budget_exhausted", "static_only": True,
                 "stop_reason": "query_budget_exhausted", "expansion": "Continue source reads or request one file per graph page"}
    file_nodes = defaultdict(list)
    for node in graph["nodes"]:
        file_nodes[node["asset"]].append(node["id"])
    reads = []
    for key in selected:
        asset = store.asset(value["snapshot"], key)
        reads.append({"asset": key, "sha256": asset.get("sha"), "kind": asset["kind"], "status": asset["status"],
                      "compiled": key in compiled if profile.get("commands") else "unknown",
                      "symbol_refs": file_nodes[key], "residual_review_required": True,
                      "residual_scope": "Entire file, including globals, macros, registrations and code outside indexed symbols",
                      "read": {"action": "read_source", "task": value["id"], "asset": key, "start": 1, "lines": 200},
                      "continue": "Follow next_line until EOF; only actual reads create receipts"})
    result = {"schema": "task-read-plan/v1", "task": value["id"], "task_kind": value["kind"],
              "module": bundle.get("module"), "question": bundle.get("question"),
              "selectors": {k: bundle[k] for k in ("module", "feature_id", "mainline_id", "feature_ids", "mainline_ids") if bundle.get(k)},
              "scope": {"source_snapshot": value["snapshot"], "build_profile": value["profile"], "index_run": value["run"],
                        "index_facts_digest": index.get("facts_digest"), "index_status": index["status"],
                        "knowledge_revision": revision, "study_plan": plan["id"]},
              "reviewed_prerequisites": reviewed, "missing_prerequisites": missing,
              "task_dependencies": dependencies, "prerequisites_truncated": prereq_truncated,
              "source_reads": reads, "graph": graph,
              "read_strategy": ["Read applicable reviewed prerequisites and their citations first",
                                "Follow graph.chunks in order; map each member to graph.nodes and read its frozen source range with read_source",
                                "Then follow every source_reads instruction through EOF, including residual code, macros and uncompiled files",
                                "Record behavior, conditions, state, consumers, counterexamples and unknowns; submit to actual review"],
              "page": {"offset": offset, "limit": limit, "total_files": len(files),
                       "next_offset": offset + len(selected) if offset + len(selected) < len(files) else None},
              "source_only_limits": ["Graph absence does not exclude behavior", "Uncompiled files and inactive macro branches still require source reading"],
              "read_only": True, "receipts_created": 0, "automatic_semantic_approval": False,
              "runtime_validation": "not_run", "truncated": bool(prereq_truncated or graph["nodes_truncated"] or graph["edges_truncated"])}
    # Drop complete graph/read groups only. Never return half of a cycle while
    # labelling it a complete SCC. The source continuation remains explicit.
    while len(canonical(result).encode("utf8")) > max_chars - 180:
        result["truncated"] = True
        if result["graph"]["nodes"] or result["graph"]["relations"]:
            result["graph"] = {"scope": "file_page", "nodes": [], "relations": [], "chunks": [],
                               "read_order": "deferred_for_response_budget", "truncated": True,
                               "expand_with": {"action": "build_context", "task": value["id"], "offset": offset, "limit": 1, "max_chars": min(262144, max_chars * 2)}}
            for read in reads:
                read["symbol_refs"] = []
        elif len(result["source_reads"]) > 1:
            result["source_reads"].pop()
            result["page"]["next_offset"] = offset + len(result["source_reads"])
        elif result["reviewed_prerequisites"]:
            result["reviewed_prerequisites"].pop()
            result["prerequisites_truncated"] = True
        elif result["missing_prerequisites"]:
            result["missing_prerequisites"].pop()
            result["prerequisites_truncated"] = True
        elif result["task_dependencies"]:
            result["task_dependencies"].pop()
            result["prerequisites_truncated"] = True
        else:
            # Narrow envelopes still explain how to continue, without a false
            # claim that zero omitted files means complete coverage.
            result = {"schema": "task-read-plan/v1", "task": value["id"], "scope": result["scope"],
                      "page": {"offset": offset, "limit": limit, "total_files": len(files), "next_offset": offset},
                      "source_reads": [], "graph": {"chunks": []}, "truncated": True,
                      "stop_reason": "response_budget", "read_only": True, "receipts_created": 0,
                      "automatic_semantic_approval": False, "runtime_validation": "not_run"}
            break
    for _ in range(3):
        result["returned_utf8_bytes"] = len(canonical(result).encode("utf8"))
    require(result["returned_utf8_bytes"] <= max_chars, "Task context exceeds response budget")
    return result
