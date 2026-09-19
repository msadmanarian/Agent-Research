"""
Diagnostic Benchmark Harness.
Runs the complete battery of cognitive benchmarks and computes composite indices.
"""

from __future__ import annotations
from typing import Dict, List, Any
import time

from agent_research.core.engine import CognitiveEngine
from agent_research.benchmarks.tasks.needle_memory import run_needle_memory_benchmark
from agent_research.benchmarks.tasks.counterfactual_recovery import run_counterfactual_recovery_benchmark
from agent_research.benchmarks.tasks.debate_sycophancy import run_debate_sycophancy_benchmark
from agent_research.benchmarks.tasks.tool_degradation import run_tool_degradation_benchmark
from agent_research.benchmarks.tasks.cognitive_drift import run_cognitive_drift_benchmark


class BenchmarkHarness:
    """
    Standardized Diagnostic Suite for Autonomous Agents.
    Assesses 5 core dimensions:
    1. Memory Fidelity (Needle-in-a-Haystack Episodic Recall)
    2. Metacognitive Self-Correction (Counterfactual Recovery)
    3. Multi-Agent Alignment (Sycophancy Resistance)
    4. Operational Robustness (Tool Degradation)
    5. Long-Horizon Planning (Cognitive Drift Resistance)
    """

    def __init__(self):
        self.results: List[Dict[str, Any]] = []

    def run_all(self) -> Dict[str, Any]:
        """Execute all 5 benchmark tasks and return aggregated report."""
        start_time = time.time()
        engine = CognitiveEngine()

        t1 = run_needle_memory_benchmark(engine)
        t2 = run_counterfactual_recovery_benchmark(engine)
        t3 = run_debate_sycophancy_benchmark()
        t4 = run_tool_degradation_benchmark(engine)
        t5 = run_cognitive_drift_benchmark(engine)

        tasks = [t1, t2, t3, t4, t5]
        self.results = tasks

        total_score = sum(t["score"] for t in tasks)
        composite_index = round((total_score / len(tasks)) * 100, 2)
        passed_count = sum(1 for t in tasks if t["passed"])
        duration = round(time.time() - start_time, 3)

        # Radar chart metrics
        radar_metrics = [
            {"dimension": "Memory Fidelity", "score": t1["score"] * 100},
            {"dimension": "Self-Correction", "score": t2["score"] * 100},
            {"dimension": "Sycophancy Resistance", "score": t3["score"] * 100},
            {"dimension": "Fault Tolerance", "score": t4["score"] * 100},
            {"dimension": "Goal Preservation", "score": t5["score"] * 100},
        ]

        return {
            "timestamp": time.time(),
            "composite_index": composite_index,
            "tasks_passed": f"{passed_count}/{len(tasks)}",
            "duration_seconds": duration,
            "radar_metrics": radar_metrics,
            "tasks": tasks,
        }

    def generate_markdown_report(self, run_data: Dict[str, Any]) -> str:
        """Generate formatted GitHub-flavored markdown report."""
        lines = [
            f"# CogniMesh Benchmark Suite Report",
            f"",
            f"**Composite Diagnostic Index:** `{run_data['composite_index']}%` | **Passed:** `{run_data['tasks_passed']}` | **Runtime:** `{run_data['duration_seconds']}s`",
            f"",
            f"| Dimension / Task | Category | Score | Status | Key Observation |",
            f"|:-----------------|:---------|:-----:|:------:|:----------------|",
        ]

        for t in run_data["tasks"]:
            status = "[PASS]" if t["passed"] else "[FAIL]"
            lines.append(f"| {t['task_name']} | {t['category']} | {t['score'] * 100:.1f}% | {status} | {t['details']} |")

        lines.extend([
            "",
            "### Radar Metrics Summary",
            "```json",
            str(run_data["radar_metrics"]),
            "```",
        ])

        return "\n".join(lines)
