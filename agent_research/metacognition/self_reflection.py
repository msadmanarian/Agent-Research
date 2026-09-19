"""
Self-Reflection & Counterfactual Reasoner.
Implements the Reflexion loop: analyzes action feedback, detects failure and cognitive drift,
synthesizes counterfactual alternative decisions, and generates consolidated heuristic rules.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any, Tuple
from agent_research.core.types import Action, ActionType, ReflectionTrace


class SelfReflector:
    """
    Metacognitive Self-Critic and Rule Distiller.
    Reflects on environmental outcomes and converts episodic failures into defensive rules.
    """

    def __init__(self):
        self.reflection_history: List[ReflectionTrace] = []

    def reflect(
        self,
        action: Action,
        environment_feedback: str,
        expected_outcome: str,
    ) -> ReflectionTrace:
        """
        Evaluate execution feedback against expected outcome.
        Returns a ReflectionTrace with critique and counterfactual recommendations.
        """
        fb_lower = environment_feedback.lower()
        exp_lower = expected_outcome.lower()

        # Check for failure signals
        failure_keywords = ["error", "fail", "unexpected", "rejected", "timeout", "exception", "mismatch", "violation"]
        is_failure = any(k in fb_lower for k in failure_keywords)

        if not is_failure and ("success" in fb_lower or "completed" in fb_lower or "nominal" in fb_lower):
            critique = f"Action '{action.action_type.value}' executed successfully. Feedback aligned with expectations."
            counterfactual = "Maintain current heuristic strategy."
            new_rule = None
            drift = False
            successful = True
        else:
            successful = False
            drift = True
            critique = (
                f"Execution failed or diverged. Expected '{expected_outcome}', but received '{environment_feedback}'. "
                f"Action was driven by {action.mode_used.value} with confidence {action.confidence:.2f}."
            )
            counterfactual = (
                f"Instead of {action.action_type.value}, agent should verify precondition boundaries "
                f"and fallback to safe checkpoint before retrying."
            )

            # Synthesize defensive heuristic rule
            action_snippet = str(action.payload.get("output", action.payload.get("plan", "action")))[:20]
            new_rule = f"WHEN encountering '{action_snippet}' FAILURE: fallback to diagnostic verification before re-executing."

        trace = ReflectionTrace(
            successful=successful,
            critique=critique,
            counterfactual_alternative=counterfactual,
            heuristic_rule_learned=new_rule,
            epistemic_drift_detected=drift,
        )

        self.reflection_history.append(trace)
        return trace

    def get_summary(self) -> Dict[str, Any]:
        """Aggregate statistical metrics on reflections."""
        total = len(self.reflection_history)
        if total == 0:
            return {"total_reflections": 0, "success_rate": 1.0, "rules_learned": 0}

        successes = sum(1 for r in self.reflection_history if r.successful)
        rules = sum(1 for r in self.reflection_history if r.heuristic_rule_learned is not None)

        return {
            "total_reflections": total,
            "success_rate": round(successes / total, 3),
            "rules_learned": rules,
        }
