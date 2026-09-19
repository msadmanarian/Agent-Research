"""
Integration tests for CogniMesh Web Server and REST endpoints.
"""

import unittest
import threading
import time
import urllib.request
import json
import socketserver

from agent_research.web.server import LabRequestHandler


class TestWebServer(unittest.TestCase):
    server = None
    server_thread = None
    port = 8999

    @classmethod
    def setUpClass(cls):
        socketserver.TCPServer.allow_reuse_address = True
        cls.server = socketserver.TCPServer(("", cls.port), LabRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        if cls.server:
            cls.server.shutdown()
            cls.server.server_close()

    def _get(self, path):
        url = f"http://localhost:{self.port}{path}"
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.status, resp.read()

    def _post(self, path, payload):
        url = f"http://localhost:{self.port}{path}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read()

    def test_static_index_html(self):
        status, content = self._get("/")
        self.assertEqual(status, 200)
        self.assertIn(b"COGNIMESH", content)

    def test_static_css(self):
        status, content = self._get("/app.css")
        self.assertEqual(status, 200)
        self.assertIn(b":root", content)

    def test_static_js(self):
        status, content = self._get("/app.js")
        self.assertEqual(status, 200)
        self.assertIn(b"DOMContentLoaded", content)

    def test_api_status(self):
        status, content = self._get("/api/status")
        self.assertEqual(status, 200)
        data = json.loads(content.decode("utf-8"))
        self.assertEqual(data["status"], "online")

    def test_api_graph(self):
        status, content = self._get("/api/graph")
        self.assertEqual(status, 200)
        data = json.loads(content.decode("utf-8"))
        self.assertIn("nodes", data)
        self.assertIn("edges", data)

    def test_api_run_cycle(self):
        payload = {"perception": "Check health", "feedback": "Nominal"}
        status, content = self._post("/api/run-cycle", payload)
        self.assertEqual(status, 200)
        data = json.loads(content.decode("utf-8"))
        self.assertIn("action", data)
        self.assertIn("confidence", data)

    def test_api_run_debate(self):
        payload = {"topic": "Symbolic vs Subsymbolic", "rounds": 3}
        status, content = self._post("/api/run-debate", payload)
        self.assertEqual(status, 200)
        data = json.loads(content.decode("utf-8"))
        self.assertTrue(data["consensus_achieved"])

    def test_api_run_benchmark(self):
        status, content = self._post("/api/run-benchmark", {})
        self.assertEqual(status, 200)
        data = json.loads(content.decode("utf-8"))
        self.assertEqual(len(data["tasks"]), 5)


if __name__ == "__main__":
    unittest.main()
