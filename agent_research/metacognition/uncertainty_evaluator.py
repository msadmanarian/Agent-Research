"""
Metacognitive Uncertainty Evaluator.
Arbitrates execution between System 1 (fast heuristic) and System 2 (deliberative planning)
based on epistemic confidence, task ambiguity, and environmental novelty.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from agent_research.core.types import CognitiveMode, ConfidenceMetric, Perception


class UncertaintyEvaluator:
    """
    Epistemic Supervisory Monitor.
    Decides whether the agent can safely rely on fast reflexive System 1 intuition
    or must escalate to costly System 2 deliberative planning.
    """

    def __init__(self, escalation_threshold: float = 0.70):
        self.escalation_threshold = escalation_threshold

    def evaluate(
        self,
        perception: Perception,
        heuristic_action_available: bool,
        heuristic_confidence: float,
        working_memory_size: int,
        novelty_score: float = 0.0,
    ) -> ConfidenceMetric:
        """
        Compute epistemic uncertainty and select execution mode.
        """
        # Calculate epistemic uncertainty
        # If novelty is high or heuristic confidence is low, uncertainty climbs
        base_uncertainty = 1.0 - heuristic_confidence
        epistemic_uncertainty = min(1.0, max(0.0, (base_uncertainty * 0.7) + (novelty_score * 0.3)))

        # Deliberative expected score if escalated
        deliberative_score = min(0.95, max(0.60, 0.85 - (novelty_score * 0.15)))

        if heuristic_action_available and heuristic_confidence >= self.escalation_threshold and novelty_score < 0.5:
            mode = CognitiveMode.SYSTEM_1
            reason = (
                f"Sufficient heuristic confidence ({heuristic_confidence:.2f} >= {self.escalation_threshold:.2f}) "
                f"with low environmental novelty ({novelty_score:.2f})."
            )
        else:
            mode = CognitiveMode.SYSTEM_2
            if not heuristic_action_available:
                reason = "No matching heuristic rule found in System 1 reflex base. Escalating to deliberative tree search."
            elif heuristic_confidence < self.escalation_threshold:
                reason = (
                    f"Heuristic confidence ({heuristic_confidence:.2f}) fell below safety threshold ({self.escalation_threshold:.2f}). "
                    "Engaging System 2 deliberation."
                )
            else:
                reason = f"High environmental novelty ({novelty_score:.2f}) detected. Overriding reflex to ensure safety."

        return ConfidenceMetric(
            heuristic_score=heuristic_confidence,
            deliberative_score=deliberative_score,
            epistemic_uncertainty=epistemic_uncertainty,
            selected_mode=mode,
            reason=reason,
        )
