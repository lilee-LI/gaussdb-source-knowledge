"""Shared structured tools, stdio MCP and loopback HTTP adapters."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import sqlite3
from pathlib import Path
import sys

from . import __version__, study
from .changes import analyze_change
from .indexer import query_graph
from .knowledge import knowledge_graph, review_context
from .planner import create_task_evidence, lease, next_tasks, read_for_task, submit, task_context, stage_research_unit, finish_research
from .releases import status
from .retrieval import explain_path, get_context, knowledge_delta, request_refresh, search
from .store import Store, canonical, require


QUERY_TOOLS = {
    "feature_candidates": "List evidence-backed feature leads and their current research or review state.",
    "navigate_code": "Look up callers and callees in the bound ECS graph or the configured repository navigation provider.",
    "study_plan": "List module boundaries, research tasks, assignments and next steps in the current project.",
    "get_context": "Return version-bound task constraints, impact, test obligations and source evidence.",
    "find_knowledge": "Find reviewed knowledge using text, symbols and optional named embeddings.",
    "query_graph": "Traverse typed code facts; candidate edges do not prove runtime behavior.",
    "read_evidence": "Read frozen source/document evidence and verify its content hash.",
    "explain_path": "Explain typed code paths and knowledge dependencies.",
    "test_obligations": "Return task test requirements, oracle origins and not_run state.",
    "impact_of_change": "Read an already registered material/knowledge change and its pending risks.",
    "knowledge_graph": "Read the responsibility/feature trees and semantic relations.",
    "status": "Read implementation, material and task state.",
    "knowledge_delta": "Compare semantic content and source bindings across frozen knowledge revisions.",
}
WORK_TOOLS = {
    "request_refresh": "Enqueue an idempotent concrete knowledge-gap task; does not execute a model or approve knowledge.",
    "plan_tasks": "Preview or apply a bounded research-task batch using the bound product adapter; never accepts knowledge.",
    "planning_feedback": "Record evidence-backed new, merged or split candidates and research gaps for subsequent task planning.",
    "focus_module": "Create a bounded module research task. ECS plans reuse indexed symbols and evidence.",
    "next_tasks": "Find research tasks whose dependencies are accepted.",
    "claim_task": "Claim a research task with a real lease.",
    "task_context": "Read the immutable research scope, methods and evidence references.",
    "read_task_evidence": "Actually read evidence for this task and record its complete/truncated receipt.",
    "create_task_evidence": "Create a bounded evidence anchor inside this task's frozen snapshot.",
    "submit_research": "Submit question coverage with actual evidence-read receipts; no automatic approval.",
    "stage_research_unit": "Save one typed unreviewed unit with source_refs read in this lease. For test_obligation use expected_from as one object {kind,ref}, e.g. kind=contract and ref=contract:example. Returns drafts_digest.",
    "finish_research": "Check staged units and submit coverage for review using the latest drafts_digest; no automatic approval.",
}
REVIEW_TOOLS = {"review_context": "Read proposal and evidence for an explicitly identified reviewer."}


def tools(role="query"):
    names = {**QUERY_TOOLS, **(WORK_TOOLS if role in {"researcher", "reviewer"} else {}),
             **(REVIEW_TOOLS if role == "reviewer" else {})}
    context_properties = {
        "task": {"type": "string", "enum": ["coding", "test_generation", "review", "operations"]},
        "source_snapshot": {"type": "string"}, "build_profile": {"type": "string"},
        "knowledge_revision": {"type": ["string", "null"]}, "index_run": {"type": "string"},
        "query": {"type": "string"}, "targets": {"type": "array", "items": {"type": "string"}},
        "token_budget": {"type": "integer", "minimum": 512, "maximum": 128000},
        "embedding_space": {"type": "string"}, "query_vector": {"type": "array", "items": {"type": "number"}},
        "diff_ref": {"type": "string"},
    }
    schemas = {
        "plan_tasks": ({"modules": {"type":"array","items":{"type":"string"}}, "max_tasks":{"type":"integer","minimum":1,"maximum":500},
                         "files_per_task":{"type":"integer","minimum":1,"maximum":40},"apply":{"type":"boolean"}}, []),
        "planning_feedback": ({"proposal":{"type":"object"}}, ["proposal"]),
        "study_plan": ({"module":{"type":"string"}}, []),
        "feature_candidates": ({"module":{"type":"string"},"state":{"type":"string"},
                                "limit":{"type":"integer","minimum":1,"maximum":200},"offset":{"type":"integer","minimum":0}}, []),
        "navigate_code": ({"symbol": {"type":"string"}, "repository":{"type":"string"},
                           "direction":{"type":"string","enum":["forward","reverse"]}, "limit":{"type":"integer"}}, ["symbol"]),
        "focus_module": ({"module": {"type": "string"}, "files": {"type": "array", "items": {"type": "string"}},
                          "question": {"type": "string"}, "extend": {"type": "string"}, "profile": {"type": "string"}, "symbol": {"type": "string"},
                          "limit": {"type": "integer", "minimum": 1, "maximum": 100},
                          "candidate_id":{"type":"string"},"jobs": {"type": "integer", "minimum": 1, "maximum": 8}}, []),
        "get_context": (context_properties, ["task", "source_snapshot"]),
        "find_knowledge": ({**context_properties, "limit": {"type": "integer"}}, ["source_snapshot"]),
        "query_graph": ({"run": {"type": "string"}, "targets": {"type": "array", "items": {"type": "string"}},
                         "direction": {"type": "string"}, "depth": {"type": "integer"}, "limit": {"type": "integer"},
                         "kinds": {"type": "array", "items": {"type": "string"}},
                         "walk": {"type": "string", "enum": ["bfs", "dfs"]}}, ["run", "targets"]),
        "read_evidence": ({"evidence_id": {"type": "string"}, "expected_hash": {"type": "string"}, "max_chars": {"type": "integer"}}, ["evidence_id"]),
        "explain_path": ({**context_properties, "depth": {"type": "integer"}, "limit": {"type": "integer"}}, ["source_snapshot", "targets"]),
        "test_obligations": (context_properties, ["source_snapshot"]),
        "impact_of_change": ({"change_id": {"type": "string"}}, ["change_id"]),
        "knowledge_graph": ({"revision": {"type": "string"}}, []),
        "status": ({"run": {"type": "string"}}, []),
        "knowledge_delta": ({"base_revision": {"type": "string"}, "target_revision": {"type": "string"}}, ["base_revision", "target_revision"]),
        "request_refresh": (context_properties, ["source_snapshot"]),
        "next_tasks": ({"run": {"type": "string"}, "limit": {"type": "integer"}}, ["run"]),
        "claim_task": ({"task": {"type": "string"}, "worker": {"type": "string"}, "seconds": {"type": "integer"}}, ["task", "worker"]),
        "task_context": ({"task": {"type": "string"}}, ["task"]),
        "read_task_evidence": ({"task": {"type": "string"}, "worker": {"type": "string"}, "token": {"type": "string"},
                               "evidence": {"type": "string"}, "max_chars": {"type": "integer"}}, ["task", "worker", "token", "evidence"]),
        "submit_research": ({"task": {"type": "string"}, "worker": {"type": "string"}, "token": {"type": "string"}, "result": {"type": "object"}},
                            ["task", "worker", "token", "result"]),
        "stage_research_unit": ({"task": {"type": "string"}, "worker": {"type": "string"}, "token": {"type": "string"},
                                 "unit": {"type":"object","properties":{
                                     "expected_from":{"type":"object","properties":{"kind":{"type":"string","enum":["contract","claim","requirement","source_prediction"]},
                                     "ref":{"type":"string"}},"required":["kind","ref"]}}}, "previous_hash": {"type": "string"}}, ["task", "worker", "token", "unit"]),
        "finish_research": ({"task": {"type": "string"}, "worker": {"type": "string"}, "token": {"type": "string"},
                             "coverage": {"type":"array","items":{"type":"object","properties":{"question":{"type":"string"},
                             "status":{"type":"string","enum":["answered","open","not_applicable"]},"explanation":{"type":"string"},
                             "evidence_refs":{"type":"array","items":{"type":"string"}}},"required":["question","status","explanation"]}}, "drafts_digest": {"type": "string"}}, ["task", "worker", "token", "coverage", "drafts_digest"]),
        "create_task_evidence": ({"task": {"type": "string"}, "worker": {"type": "string"}, "token": {"type": "string"},
                                  "asset": {"type": "string"}, "start": {"type": "integer"}, "end": {"type": "integer"}},
                                 ["task", "worker", "token", "asset", "start", "end"]),
        "review_context": ({"proposal_id": {"type": "string"}, "reviewer": {"type": "string"}, "max_chars": {"type": "integer"}},
                           ["proposal_id", "reviewer"]),
    }
    return [{"name": name, "description": description, "inputSchema": {"type": "object", "properties": schemas[name][0],
             "required": schemas[name][1], "additionalProperties": False},
             "annotations": {"readOnlyHint": name in QUERY_TOOLS and name != "request_refresh", "destructiveHint": False, "openWorldHint": False}}
            for name, description in names.items()]


def _validate(values, schema):
    require(isinstance(values, dict), "Tool arguments must be an object")
    require(set(schema.get("required", [])) <= set(values), "Required tool argument missing")
    require(not (set(values) - set(schema["properties"])), "Unknown tool argument")
    types = {"string": str, "integer": int, "number": (int, float), "array": list, "object": dict, "null": type(None), "boolean": bool}
    for key, value in values.items():
        spec = schema["properties"][key]
        choices = spec["type"] if isinstance(spec["type"], list) else [spec["type"]]
        require(any(isinstance(value, types[t]) and not (t in {"integer", "number"} and isinstance(value, bool)) for t in choices),
                "Tool argument type mismatch: " + key)
        if "enum" in spec:
            require(value in spec["enum"], "Tool argument enum mismatch: " + key)
        if "minimum" in spec:
            require(value >= spec["minimum"], "Tool argument below minimum")
        if "maximum" in spec:
            require(value <= spec["maximum"], "Tool argument above maximum")


def invoke(store, name, values, *, role="query"):
    specification = next((t for t in tools(role) if t["name"] == name), None)
    require(specification is not None, "Tool unavailable for this role")
    _validate(values, specification["inputSchema"])
    if name == "plan_tasks":
        from .task_planning import construct
        return construct(store, **values)
    if name == "planning_feedback":
        from .task_planning import propose
        return propose(store, values["proposal"])
    if name == "navigate_code":
        from .navigation import navigate
        p = study.current(store)
        if p.get("source_index") or p.get("reuse_index") or p.get("source_only"):
            return study.ecs_neighbors(store,p,values["symbol"],values.get("direction","forward"),values.get("limit",20))
        return navigate(store, p["snapshot"], **values)
    if name == "study_plan":
        return study.module_guide(store, values["module"]) if values.get("module") else study.guide(store)
    if name == "feature_candidates":
        from .catalog import listing
        return listing(store,study.current(store),**values)
    if name == "focus_module":
        return study.focus(store, **values)
    if name == "get_context":
        return get_context(store, values)
    if name == "find_knowledge":
        return search(store, {k: v for k, v in values.items() if k != "limit"}, limit=values.get("limit", 12))
    if name == "query_graph":
        return query_graph(store, **values)
    if name == "read_evidence":
        return store.read_evidence(**values)
    if name == "explain_path":
        return explain_path(store, values)
    if name == "test_obligations":
        return get_context(store, {**values, "task": "test_generation"})
    if name == "impact_of_change":
        return store.record("changes", values["change_id"])
    if name == "knowledge_graph":
        return knowledge_graph(store, **values)
    if name == "status":
        return status(store, **values)
    if name == "knowledge_delta":
        return knowledge_delta(store, **values)
    if name == "request_refresh":
        return request_refresh(store, values)
    if name == "next_tasks":
        return next_tasks(store, **values)
    if name == "claim_task":
        return lease(store, **values)
    if name == "task_context":
        return task_context(store, **values)
    if name == "read_task_evidence":
        return read_for_task(store, **values)
    if name == "create_task_evidence":
        return create_task_evidence(store, **values)
    if name == "submit_research":
        return submit(store, **values)
    if name == "stage_research_unit":
        return stage_research_unit(store, **values)
    if name == "finish_research":
        return finish_research(store, **values)
    if name == "review_context":
        return review_context(store, **values)
    raise ValueError("Unknown tool")


def stdio(home, role="query", incoming=None, outgoing=None):
    incoming, outgoing = incoming or sys.stdin, outgoing or sys.stdout
    for line in incoming:
        request = {}
        try:
            require(len(line.encode("utf-8")) <= 2_000_000, "MCP message too large")
            request = json.loads(line)
            if "id" not in request:
                continue
            method = request.get("method")
            if method == "initialize":
                version = request.get("params", {}).get("protocolVersion")
                result = {"protocolVersion": version if version in {"2025-06-18", "2025-03-26", "2024-11-05"} else "2025-06-18",
                          "capabilities": {"tools": {}}, "serverInfo": {"name": "unified-source-knowledge", "version": __version__}}
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": tools(role)}
            elif method == "tools/call":
                args = request.get("params", {})
                try:
                    with Store(home, readonly=(role == "query" and args.get("name") != "request_refresh")) as store:
                        data = invoke(store, args.get("name"), args.get("arguments", {}), role=role)
                    result = {"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False)}], "isError": False}
                except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as error:
                    result = {"content": [{"type": "text", "text": canonical({"error": str(error)})}], "isError": True}
            else:
                raise ValueError("Unsupported MCP method")
            response = {"jsonrpc": "2.0", "id": request["id"], "result": result}
        except (ValueError, KeyError, TypeError) as error:
            response = {"jsonrpc": "2.0", "id": request.get("id"), "error": {"code": -32602, "message": str(error)}}
        outgoing.write(json.dumps(response, ensure_ascii=False) + "\n")
        outgoing.flush()


def http_server(home, *, host="127.0.0.1", port=0, role="query"):
    require(host in {"127.0.0.1", "::1", "localhost"}, "HTTP adapter binds loopback; use an authenticated gateway for remote access")
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, code, data):
            raw = canonical(data).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            if self.path == "/health":
                self.reply(200, {"service": "unified-source-knowledge", "role": role, "status": "ready"})
            elif self.path == "/tools":
                self.reply(200, {"tools": tools(role)})
            else:
                self.reply(404, {"error": "not_found"})

        def do_POST(self):
            try:
                require(self.path.startswith("/tools/"), "Unknown route")
                length = int(self.headers.get("Content-Length", "0"))
                require(0 < length <= 2_000_000, "Invalid request body size")
                request = json.loads(self.rfile.read(length).decode("utf-8"))
                tool_name = self.path[len("/tools/"):]
                with Store(home, readonly=(role == "query" and tool_name != "request_refresh")) as store:
                    data = invoke(store, tool_name, request, role=role)
                self.reply(200, data)
            except (OSError, ValueError, TypeError, KeyError, sqlite3.Error) as error:
                self.reply(422, {"error": {"code": "invalid_or_unavailable_scope", "message": str(error)}})
    return ThreadingHTTPServer((host, port), Handler)
