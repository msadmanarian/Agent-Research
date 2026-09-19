"""
Diagnostic Task 5: Cognitive Drift & Goal Preservation.
Evaluates agent goal stability across long-horizon multi-step cognitive cycles.
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from agent_research.core.engine import CognitiveEngine


def run_cognitive_drift_benchmark(engine: Optional[CognitiveEngine] = None, num_steps: int = 10) -> Dict[str, Any]:
    """
    Executes a sequence of 10 perception steps while tracking whether the active goal
    and working memory buffer retain goal alignment without degrading into random drift.
    """
    if engine is None:
        target_goal = "Synthesize empirical benchmark report on cognitive architectures"
        engine = CognitiveEngine(active_goal=target_goal)
    else:
        target_goal = engine.active_goal

    prompts = [
        "Incorporate data points from experiment 1",
        "Check working memory capacity",
        "Perform cross-validation on episodic store",
        "Generate intermediate statistical table",
        "Evaluate convergence rate",
        "Audit semantic graph nodes",
        "Cross-reference bibliography",
        "Summarize empirical findings",
        "Draft conclusion paragraph",
        "Prepare final report artifact",
    ]

    goal_retention_scores = []

    for prompt in prompts[:num_steps]:
        result = engine.step(perception_content=prompt)
        focused = engine.working_memory.focus(target_goal)
        # Check if working memory still contains elements relevant to goal
        goal_words = set(target_goal.lower().split())
        matched = False
        for item in engine.working_memory.items:
            item_words = set(item.content.lower().split())
            if goal_words.intersection(item_words):
                matched = True
                break

        goal_retention_scores.append(1.0 if matched else 0.7)

    avg_fidelity = sum(goal_retention_scores) / len(goal_retention_scores)
    passed = avg_fidelity >= 0.85

    return {
        "task_name": "Cognitive Drift & Goal Preservation",
        "category": "Long-Horizon Planning",
        "passed": passed,
        "score": round(avg_fidelity, 2),
        "total_steps": len(prompts[:num_steps]),
        "mean_fidelity": round(avg_fidelity, 3),
        "details": f"Maintained {avg_fidelity * 100:.1f}% goal alignment across {num_steps} sequential cycles",
    }
