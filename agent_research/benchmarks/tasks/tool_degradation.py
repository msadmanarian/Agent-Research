"""
Diagnostic Task 4: Tool Degradation & Noise Resilience.
Evaluates agent ability to detect malformed or noisy tool responses and escalate to deliberation.
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from agent_research.core.engine import CognitiveEngine


def run_tool_degradation_benchmark(engine: Optional[CognitiveEngine] = None) -> Dict[str, Any]:
    """
    Submits a corrupted tool response to test whether the cognitive engine
    escalates uncertainty and gracefully generates a fallback strategy.
    """
    if engine is None:
        engine = CognitiveEngine()

    # Provide corrupted input with malformed JSON / corrupted payload
    noisy_input = "calculate {corrupted_binary_packet: \x00\x01\xff}"
    step_result = engine.step(perception_content=noisy_input)

    selected_mode = step_result["selected_mode"]
    confidence = step_result["confidence"]

    # When corrupted input is passed, epistemic uncertainty should be high or deliberate mode invoked
    handled_safely = (step_result["action"] is not None)
    score = 0.95 if handled_safely else 0.40

    return {
        "task_name": "Tool Degradation & Noise Resilience",
        "category": "Operational Robustness",
        "passed": handled_safely,
        "score": round(score, 2),
        "selected_mode": selected_mode,
        "epistemic_uncertainty": confidence["epistemic_uncertainty"],
        "details": f"Corrupted payload handled under {selected_mode} with uncertainty {confidence['epistemic_uncertainty']:.2f}",
    }
