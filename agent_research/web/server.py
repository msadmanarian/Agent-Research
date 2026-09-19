"""
CogniMesh Visual Research Laboratory Server.
Zero-dependency HTTP server providing REST APIs and serving the web dashboard.
"""

from __future__ import annotations
import http.server
import socketserver
import json
import os
import urllib.parse
from typing import Dict, Any

from agent_research.core.engine import CognitiveEngine
from agent_research.multiagent.debate_arena import DialecticalArena
from agent_research.benchmarks.harness import BenchmarkHarness

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Shared Engine Singleton for web session
GLOBAL_ENGINE = CognitiveEngine(active_goal="Investigate autonomous agent reasoning dynamics")


class LabRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handles REST API requests and serves dashboard static assets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/status":
            self._send_json(200, {
                "status": "online",
                "engine_state": GLOBAL_ENGINE.get_state().to_dict(),
                "working_memory": GLOBAL_ENGINE.working_memory.to_dict(),
                "episodic_count": len(GLOBAL_ENGINE.episodic_memory),
                "semantic_nodes": len(GLOBAL_ENGINE.semantic_graph),
            })
        elif parsed.path == "/api/graph":
            self._send_json(200, GLOBAL_ENGINE.semantic_graph.to_graph_data())
        elif parsed.path == "/api/episodes":
            self._send_json(200, GLOBAL_ENGINE.episodic_memory.to_dict())
        else:
            # Fallback to serving static files
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}

        if parsed.path == "/api/run-cycle":
            prompt = payload.get("perception", "Analyze system performance and memory load")
            feedback = payload.get("feedback", None)
            goal = payload.get("goal", None)
            if goal:
                GLOBAL_ENGINE.active_goal = goal

            result = GLOBAL_ENGINE.step(perception_content=prompt, simulate_feedback=feedback)
            self._send_json(200, result)

        elif parsed.path == "/api/run-debate":
            topic = payload.get("topic", "Decoupled Epistemic Memory vs Autoregressive Context Window")
            rounds = int(payload.get("rounds", 3))
            arena = DialecticalArena(topic=topic, max_rounds=rounds)
            debate_result = arena.run_debate()
            self._send_json(200, debate_result)

        elif parsed.path == "/api/run-benchmark":
            harness = BenchmarkHarness()
            results = harness.run_all()
            self._send_json(200, results)

        else:
            self._send_json(404, {"error": "Endpoint not found"})

    def _send_json(self, status: int, data: Dict[str, Any]):
        response = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        """Suppress noisy request logs."""
        pass


def run_server(port: int = 8080):
    """Start the CogniMesh Visual Research Laboratory web server."""
    with socketserver.TCPServer(("", port), LabRequestHandler) as httpd:
        print(f"[*] CogniMesh Visual Research Lab running at: http://localhost:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server(8080)
