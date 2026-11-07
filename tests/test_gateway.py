import asyncio
import json
from pathlib import Path
import socket
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from platform_fixture import workspace
from unified_knowledge import publication, gateway


class GatewayTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        store, plan, unit = workspace(self.root)
        try:
            self.release = publication.prepare(store)
            publication.sync(store, self.release["id"])
            publication.activate(store, self.release["id"])
            self.evidence = unit["source_refs"][0]
        finally:
            store.close()
        self.home = self.root / "home"

    def test_http_context_evidence_and_unauthorized_requests(self):
        from starlette.testclient import TestClient
        with patch.dict("os.environ", {"KB_TEST_GATEWAY_TOKEN":"synthetic-test-token"}):
            app = gateway.create_app(self.home, token_env="KB_TEST_GATEWAY_TOKEN")
        with TestClient(app) as client:
            self.assertEqual(client.get("/health").status_code, 200)
            self.assertEqual(client.post("/api/context", json={"question":"fixture"}).status_code, 401)
            client.headers["Authorization"] = "Bearer synthetic-test-token"
            response = client.post("/api/context", json={"question":"fixture increment"})
            self.assertEqual(response.status_code, 200)
            pack = response.json()
            self.assertEqual(pack["release_id"], self.release["id"])
            evidence = client.get(pack["groups"][0]["evidence"][0]["url"])
            self.assertEqual(evidence.status_code, 200)
            self.assertIn("value + 1", evidence.text)
            self.assertEqual(client.post("/api/context", json={"question":"fixture","run":"wrong"}).status_code, 400)
        with self.assertRaisesRegex(ValueError, "not exposed"):
            gateway.invoke(self.home, "request_refresh", {})
        with self.assertRaisesRegex(ValueError, "access scope"):
            gateway.invoke(self.home, "release_info", {}, allowed_releases=["unrelated-release"])

    def test_official_mcp_client_against_real_http_server(self):
        import uvicorn
        from mcp import ClientSession
        from mcp.client.streamable_http import streamable_http_client
        sock = socket.socket()
        sock.bind(("127.0.0.1",0))
        port = sock.getsockname()[1]
        server = uvicorn.Server(uvicorn.Config(gateway.create_app(self.home), log_level="error", lifespan="on"))
        thread = threading.Thread(target=server.run, kwargs={"sockets":[sock]}, daemon=True)
        thread.start()
        try:
            until = time.monotonic() + 15
            while not server.started and time.monotonic() < until:
                time.sleep(.05)
            self.assertTrue(server.started)
            async def run():
                async with streamable_http_client(f"http://127.0.0.1:{port}/mcp") as (read,write,_):
                    async with ClientSession(read,write) as session:
                        await session.initialize()
                        tools = await session.list_tools()
                        self.assertEqual({t.name for t in tools.tools}, {t["name"] for t in gateway.tool_specs()})
                        self.assertTrue(all(t.annotations.readOnlyHint for t in tools.tools))
                        result = await session.call_tool("knowledge_context", {"question":"fixture increment"})
                        self.assertFalse(result.isError)
                        self.assertEqual(result.structuredContent["release_id"], self.release["id"])
                        bad = await session.call_tool("request_refresh", {})
                        self.assertTrue(bad.isError)
            asyncio.run(asyncio.wait_for(run(), timeout=25))
        finally:
            server.should_exit = True
            thread.join(timeout=10)
            sock.close()
        self.assertFalse(thread.is_alive())
