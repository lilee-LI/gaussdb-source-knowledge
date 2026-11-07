"""Official MCP Streamable HTTP transport over the release-bound read-only query API."""
from contextlib import asynccontextmanager
from html import escape
import hmac
import json
import os
from pathlib import Path
import sqlite3

from . import publication, query_api, retrieval_pipeline
from .store import Store, canonical, require


def tool_specs():
    release = {"release_id":{"type":"string"}}
    query = {**release,"question":{"type":"string","minLength":1,"maxLength":8000},
             "targets":{"type":"array","items":{"type":"string"},"maxItems":20},
             "limit":{"type":"integer","minimum":1,"maximum":100}}
    paging = {**release,"limit":{"type":"integer","minimum":1,"maximum":200},"cursor":{"type":"string"},
              "max_bytes":{"type":"integer","minimum":2048,"maximum":262144},"timeout_ms":{"type":"integer","minimum":1,"maximum":10000}}
    definitions = {
        "release_info":("Read the exact source, build and knowledge release binding.",release,[]),
        "find_knowledge":("Retrieve reviewed knowledge IDs, with release and content-hash checks.",query,["question"]),
        "knowledge_context":("Return complete evidence groups including conditions, counterexamples and frozen source; incomplete groups are omitted explicitly.",
            {**query,"max_bytes":{"type":"integer","minimum":4096,"maximum":256000}},["question"]),
        "lookup_symbols":("Find an exact source symbol name or ID within this release.",{**paging,"query":{"type":"string","minLength":1,"maxLength":2000}},["query"]),
        "graph_neighbors":("Read one page of static source relations. Use returned IDs for subsequent hops; unresolved edges remain unresolved.",
            {**paging,"symbol":{"type":"string"},"direction":{"type":"string","enum":["forward","reverse","both"]},"kinds":{"type":"array","items":{"type":"string"},"maxItems":20}},["symbol"]),
        "read_evidence":("Read hash-checked frozen evidence from this release only.",
            {**release,"evidence_id":{"type":"string"},"max_chars":{"type":"integer","minimum":1,"maximum":64000}},["evidence_id"]),
    }
    return [{"name":name,"description":description,"inputSchema":{"type":"object","properties":properties,"required":required,"additionalProperties":False},
             "annotations":{"readOnlyHint":True,"destructiveHint":False,"openWorldHint":False}} for name,(description,properties,required) in definitions.items()]


def invoke(home, name, arguments, *, allowed_releases=None):
    import jsonschema
    spec = next((s for s in tool_specs() if s["name"] == name), None)
    require(spec is not None, "Tool is not exposed by the read-only gateway")
    try:
        jsonschema.validate(arguments, spec["inputSchema"])
    except jsonschema.ValidationError as exc:
        raise ValueError("Invalid tool arguments: " + exc.message) from exc
    args = dict(arguments)
    with Store(home, readonly=True) as store:
        release = publication.get(store, args.pop("release_id", None))
        require(allowed_releases is None or release["id"] in allowed_releases, "Release is outside gateway access scope")
        if name == "release_info":
            return {"release_id":release["id"],"binding":release["binding"],"knowledge_revision":release["knowledge_revision"],
                    "retrieval_provider":release["provider"]["kind"],"retrieval_config_digest":release["retrieval_config_digest"],"status":release["status"]}
        if name in {"knowledge_context", "find_knowledge"}:
            fn = retrieval_pipeline.context if name == "knowledge_context" else retrieval_pipeline.retrieve
            return fn(store, release_id=release["id"], **args)
        if name == "lookup_symbols":
            result = query_api.lookup_symbols(store, release["binding"]["index_run"], **args)
        elif name == "graph_neighbors":
            result = query_api.neighbors(store, release["binding"]["index_run"], **args)
        else:
            result = query_api.evidence(store, release["binding"]["source_snapshot"], **args)
        return {**result,"release_id":release["id"]}


def create_app(home, *, token_env=None, allowed_releases=None):
    import anyio
    from mcp.server.lowlevel import Server
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
    from mcp.types import Tool, CallToolResult, TextContent
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import JSONResponse, HTMLResponse
    from starlette.routing import Route

    home = Path(home).resolve()
    require((home / "knowledge.sqlite3").is_file(), "Knowledge workspace does not exist")
    token = os.environ.get(token_env) if token_env else None
    require(not token_env or token, "Gateway credential environment variable is missing")
    server = Server("gaussdb-source-knowledge")
    @server.list_tools()
    async def list_tools():
        return [Tool(**s) for s in tool_specs()]
    @server.call_tool()
    async def call_tool(name, arguments):
        try:
            result = await anyio.to_thread.run_sync(lambda: invoke(home, name, arguments, allowed_releases=allowed_releases))
            return CallToolResult(content=[TextContent(type="text", text=canonical(result))], structuredContent=result, isError=False)
        except (ValueError, OSError, sqlite3.Error) as exc:
            return CallToolResult(content=[TextContent(type="text",text=str(exc))], isError=True)
    manager = StreamableHTTPSessionManager(server, json_response=True, stateless=True, max_request_body_size=65536)
    @asynccontextmanager
    async def lifespan(app):
        async with manager.run():
            yield
    class Transport:
        async def __call__(self, scope, receive, send):
            await manager.handle_request(scope, receive, send)
    async def health(request):
        return JSONResponse({"status":"ok","transport":"mcp-streamable-http","read_only":True})
    async def source(request):
        try:
            values = {"evidence_id":request.path_params["evidence_id"]}
            if request.query_params.get("release_id"):
                values["release_id"] = request.query_params["release_id"]
            result = await anyio.to_thread.run_sync(lambda: invoke(home, "read_evidence", values, allowed_releases=allowed_releases))
            title = f"{result['asset']}:{result['start']}–{result['end']}"
            return HTMLResponse('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>' + escape(title) +
                '</title><h1>' + escape(title) + '</h1><p>' + escape(result["release_id"]) + '</p><pre>' + escape(result["text"]) +
                '</pre><p>' + ("范围已截断，请通过 read_evidence 调整读取范围。" if result["truncated"] else "引用范围完整；内容哈希已核对。") + '</p></html>')
        except (ValueError, OSError, sqlite3.Error) as exc:
            return JSONResponse({"error":str(exc)}, status_code=400)
    async def context_api(request):
        raw = await request.body()
        if len(raw) > 65536:
            return JSONResponse({"error":"Request exceeds byte budget"}, status_code=413)
        try:
            arguments = json.loads(raw)
            result = await anyio.to_thread.run_sync(lambda: invoke(home, "knowledge_context", arguments, allowed_releases=allowed_releases))
            return JSONResponse(result)
        except (ValueError, OSError, sqlite3.Error) as exc:
            return JSONResponse({"error":str(exc)}, status_code=400)
    app = Starlette(routes=[Route("/health",health),Route("/mcp",Transport(),methods=["GET","POST","DELETE"]),
                            Route("/evidence/{evidence_id:path}",source),Route("/api/context",context_api,methods=["POST"])], lifespan=lifespan)
    class Access:
        async def __call__(self, scope, receive, send):
            if scope["type"] == "http" and scope.get("path") != "/health":
                headers = dict(scope.get("headers", []))
                if token and not hmac.compare_digest(headers.get(b"authorization", b""), ("Bearer " + token).encode()):
                    await JSONResponse({"error":"Unauthorized"}, status_code=401)(scope, receive, send)
                    return
            await app(scope, receive, send)
    return Access()
