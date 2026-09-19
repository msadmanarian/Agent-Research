"""
Diagnostic Task 2: Counterfactual Error Recovery.
Evaluates agent ability to detect execution failure, trigger reflection,
and synthesize a defensive recovery rule.
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from agent_research.core.engine import CognitiveEngine
from agent_research.core.types import ActionType


def run_counterfactual_recovery_benchmark(engine: Optional[CognitiveEngine] = None) -> Dict[str, Any]:
    """
    Simulates an unexpected environment rejection, then evaluates whether
    the metacognitive self-reflector catches the drift and consolidates a corrective rule.
    """
    if engine is None:
        engine = CognitiveEngine()

    initial_rules_count = len(engine.system1.rules)

    # Step 1: Execute action that triggers simulated environment failure
    step_result = engine.step(
        perception_content="Execute database transaction write block 402",
        simulate_feedback="ERROR: Database transaction write block 402 rejected due to lock contention.",
    )

    reflection = step_result["reflection"]
    drift_detected = reflection["epistemic_drift_detected"]
    rule_learned = reflection["heuristic_rule_learned"] is not None
    rules_after = len(engine.system1.rules)

    passed = drift_detected and rule_learned and (rules_after > initial_rules_count)
    score = 1.0 if passed else (0.5 if drift_detected else 0.0)

    return {
        "task_name": "Counterfactual Error Recovery",
        "category": "Metacognitive Self-Correction",
        "passed": passed,
        "score": round(score, 2),
        "drift_detected": drift_detected,
        "rule_consolidated": rule_learned,
        "learned_rule": reflection["heuristic_rule_learned"],
        "details": f"Reflector synthesized defensive rule: {reflection['counterfactual_alternative'][:60]}...",
    }
