"""
Diagnostic Task 1: Needle in a Memory Stream.
Evaluates agent episodic recall and noise resistance across distracting memory episodes.
"""

from __future__ import annotations
from typing import Dict, Any
from agent_research.core.engine import CognitiveEngine


def run_needle_memory_benchmark(engine: Optional[CognitiveEngine] = None) -> Dict[str, Any]:
    """
    Inserts a critical needle fact into episodic memory amidst distracting synthetic noise,
    then evaluates whether the agent retrieves and utilizes the needle fact accurately.
    """
    if engine is None:
        engine = CognitiveEngine()

    needle_fact = "The secret security override token is DELTA-992-SIGMA."
    noise_facts = [
        "Network latency on node 12 spiked to 142ms.",
        "User updated theme preferences to dark obsidian mode.",
        "Routine cache garbage collection completed in 12ms.",
        "Diagnostic telemetry sent 40 packets to analytics cluster.",
        "Ambient temperature sensor reads 22.4 degrees Celsius.",
        "System log rotation performed for cluster beta.",
        "Query index recomputed on working dataset.",
    ]

    # Ingest noise
    for noise in noise_facts[:3]:
        engine.episodic_memory.record(
            perception_summary=noise,
            action_taken="Logged telemetry",
            outcome="Success",
            salience=0.3,
        )

    # Ingest needle with high salience
    engine.episodic_memory.record(
        perception_summary=needle_fact,
        action_taken="Stored secure credential in episodic buffer",
        outcome="Persisted",
        salience=0.95,
    )

    # Ingest remaining noise
    for noise in noise_facts[3:]:
        engine.episodic_memory.record(
            perception_summary=noise,
            action_taken="Routine checkpointing",
            outcome="Success",
            salience=0.3,
        )

    # Retrieval probe
    results = engine.episodic_memory.retrieve(query="What is the secret security override token?", top_k=1)

    if results and "DELTA-992-SIGMA" in results[0][0].perception_summary:
        retrieval_success = True
        score = 1.0
        retrieval_score = results[0][1]
    else:
        retrieval_success = False
        score = 0.0
        retrieval_score = 0.0

    return {
        "task_name": "Needle in a Memory Stream",
        "category": "Memory Fidelity",
        "passed": retrieval_success,
        "score": round(score, 2),
        "retrieval_salience_score": round(retrieval_score, 4),
        "total_distractors": len(noise_facts),
        "details": f"Found needle token with retrieval confidence {retrieval_score:.3f}",
    }
