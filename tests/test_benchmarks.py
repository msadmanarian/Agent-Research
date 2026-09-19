"""
Unit tests for Diagnostic Benchmark Suite.
"""

import unittest
from agent_research.benchmarks.harness import BenchmarkHarness
from agent_research.benchmarks.tasks.needle_memory import run_needle_memory_benchmark
from agent_research.benchmarks.tasks.counterfactual_recovery import run_counterfactual_recovery_benchmark
from agent_research.benchmarks.tasks.debate_sycophancy import run_debate_sycophancy_benchmark
from agent_research.benchmarks.tasks.tool_degradation import run_tool_degradation_benchmark
from agent_research.benchmarks.tasks.cognitive_drift import run_cognitive_drift_benchmark


class TestBenchmarkSuite(unittest.TestCase):

    def test_needle_memory_task(self):
        res = run_needle_memory_benchmark()
        self.assertTrue(res["passed"])
        self.assertEqual(res["score"], 1.0)

    def test_counterfactual_recovery_task(self):
        res = run_counterfactual_recovery_benchmark()
        self.assertTrue(res["passed"])
        self.assertTrue(res["drift_detected"])

    def test_debate_sycophancy_task(self):
        res = run_debate_sycophancy_benchmark()
        self.assertTrue(res["passed"])
        self.assertGreaterEqual(res["score"], 0.70)

    def test_tool_degradation_task(self):
        res = run_tool_degradation_benchmark()
        self.assertTrue(res["passed"])
        self.assertGreater(res["score"], 0.8)

    def test_cognitive_drift_task(self):
        res = run_cognitive_drift_benchmark(num_steps=5)
        self.assertTrue(res["passed"])
        self.assertGreaterEqual(res["score"], 0.8)

    def test_full_benchmark_harness(self):
        harness = BenchmarkHarness()
        report = harness.run_all()
        self.assertEqual(len(report["tasks"]), 5)
        self.assertGreaterEqual(report["composite_index"], 85.0)
        self.assertEqual(len(report["radar_metrics"]), 5)

        md = harness.generate_markdown_report(report)
        self.assertIn("CogniMesh Benchmark Suite Report", md)
        self.assertIn("[PASS]", md)


if __name__ == "__main__":
    unittest.main()
