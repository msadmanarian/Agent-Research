"""
CogniMesh Unified Command Line Interface.
"""

from __future__ import annotations
import argparse
import sys
import os
import json

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from agent_research.core.engine import CognitiveEngine
from agent_research.benchmarks.harness import BenchmarkHarness
from agent_research.multiagent.debate_arena import DialecticalArena
from agent_research.web.server import run_server


def main():
    parser = argparse.ArgumentParser(
        description="CogniMesh: Dual-Process Cognitive Architecture & Diagnostic Research Sandbox"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run an end-to-end interactive cognitive cycle demonstration."
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run the complete 5-task diagnostic benchmark suite."
    )
    parser.add_argument(
        "--debate",
        action="store_true",
        help="Convene a multi-agent dialectical debate arena."
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Decoupled Epistemic Memory vs Autoregressive Context Window in LLM Agents",
        help="Debate topic when running --debate."
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Launch the interactive Visual Research Laboratory web dashboard."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to bind the visual lab server to (default: 8080)."
    )

    args = parser.parse_args()

    if args.demo:
        run_demo()
    elif args.benchmark:
        run_benchmarks_cli()
    elif args.debate:
        run_debate_cli(args.topic)
    elif args.serve:
        print(f"[*] Starting CogniMesh Visual Laboratory on port {args.port}...")
        run_server(port=args.port)
    else:
        parser.print_help()


def run_demo():
    print("=" * 70)
    print("[COGNIMESH] Dual-Process Cognitive Architecture Demonstration")
    print("=" * 70)

    engine = CognitiveEngine(active_goal="Maintain system stability and mitigate operational failures")

    # Step 1: Routine task (System 1 should fire)
    print("\n--- [Cycle 1: Routine Health Check] ---")
    p1 = "ping cluster health status"
    print(f"Stimulus: '{p1}'")
    res1 = engine.step(perception_content=p1)
    print(f"Selected Mode: {res1['selected_mode'].upper()}")
    print(f"Confidence: {res1['confidence']['heuristic_score'] * 100:.0f}%")
    print(f"Action: {res1['action']['payload']}")
    print(f"Latency: {res1['duration_ms']}ms")

    # Step 2: Complex high-uncertainty query (System 2 deliberation invoked)
    print("\n--- [Cycle 2: Complex High-Uncertainty Dilemma] ---")
    p2 = "Analyze anomalous cross-datacenter deadlock with conflicting schema versioning"
    print(f"Stimulus: '{p2}'")
    res2 = engine.step(
        perception_content=p2,
        simulate_feedback="ERROR: Database transaction lock contention detected."
    )
    print(f"Selected Mode: {res2['selected_mode'].upper()}")
    print(f"Deliberative Nodes Explored: {res2['thought_nodes_count']}")
    print(f"Epistemic Uncertainty: {res2['confidence']['epistemic_uncertainty'] * 100:.0f}%")
    print(f"Deliberate Plan: {res2['action']['payload'].get('plan')}")
    print(f"Reflection Critique: {res2['reflection']['critique']}")
    if res2['reflection']['heuristic_rule_learned']:
        print(f"New Rule Consolidated into System 1: {res2['reflection']['heuristic_rule_learned']}")
    print(f"Working Memory Size: {len(res2['working_memory'])} / 7 items")
    print("=" * 70)


def run_benchmarks_cli():
    print("=" * 70)
    print("[BENCHMARKS] CogniMesh Diagnostic Benchmark Suite")
    print("=" * 70)
    harness = BenchmarkHarness()
    results = harness.run_all()
    md = harness.generate_markdown_report(results)
    print(md)
    print("=" * 70)


def run_debate_cli(topic: str):
    print("=" * 70)
    print(f"[DEBATE] Dialectical Arena: '{topic}'")
    print("=" * 70)
    arena = DialecticalArena(topic=topic, max_rounds=3)
    results = arena.run_debate()

    for msg in results["messages"]:
        print(f"\n[{msg['role']} - {msg['speaker']}] (Stance: {msg['stance']})")
        print(f"  {msg['content']}")

    print("\n" + "-" * 70)
    print("HEGELIAN SYNTHESIS:")
    print(results["synthesis"])
    print(f"\nSycophancy Resistance Score: {results['sycophancy_resistance_score'] * 100:.1f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
