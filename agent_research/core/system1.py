"""
System 1: Fast Heuristic Reactor.
Implements low-latency pattern-matching reflexes, action caching, and rule-based intuition.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Any
import re
from agent_research.core.types import Action, ActionType, CognitiveMode, Perception


class HeuristicRule:
    """A learned or hardwired pattern-action reflex."""
    def __init__(
        self,
        pattern: str,
        action_type: ActionType,
        response_template: str,
        confidence: float = 0.85,
        category: str = "general"
    ):
        self.pattern = pattern
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.action_type = action_type
        self.response_template = response_template
        self.confidence = confidence
        self.category = category
        self.activation_count = 0

    def match(self, text: str) -> Optional[re.Match]:
        m = self.regex.search(text)
        if m:
            self.activation_count += 1
        return m


class System1Reactor:
    """
    Kahneman System 1 Fast Reactor.
    Provides immediate instinctive responses and matches against a rule base or reflex cache.
    """

    def __init__(self, confidence_threshold: float = 0.75):
        self.confidence_threshold = confidence_threshold
        self.rules: List[HeuristicRule] = []
        self.reflex_cache: Dict[str, Tuple[Action, float]] = {}
        self._init_default_rules()

    def _init_default_rules(self) -> None:
        """Seed initial foundational heuristic rules."""
        self.add_rule(
            pattern=r"\b(ping|status|health|alive)\b",
            action_type=ActionType.HEURISTIC_REPLY,
            response_template="CogniMesh Agent operational. All telemetry subsystems nominal.",
            confidence=0.95,
            category="diagnostic"
        )
        self.add_rule(
            pattern=r"\b(who are you|identify yourself|name)\b",
            action_type=ActionType.HEURISTIC_REPLY,
            response_template="I am CogniMesh, a dual-process autonomous agent cognitive architecture.",
            confidence=0.92,
            category="identity"
        )
        self.add_rule(
            pattern=r"\b(calculate|eval|compute)\s+([0-9\+\-\*\/\^\(\)\.\s]+)$",
            action_type=ActionType.TOOL_EXECUTE,
            response_template="Execute math tool on expression: {match_1}",
            confidence=0.88,
            category="tool"
        )
        self.add_rule(
            pattern=r"\b(recall|remember|lookup concept)\s+([a-zA-Z0-9_\-\s]+)$",
            action_type=ActionType.TOOL_EXECUTE,
            response_template="Query episodic and semantic memory for: {match_1}",
            confidence=0.82,
            category="memory"
        )

    def add_rule(
        self,
        pattern: str,
        action_type: ActionType,
        response_template: str,
        confidence: float = 0.85,
        category: str = "custom"
    ) -> None:
        """Dynamically add or consolidate a learned rule (e.g., from reflection)."""
        rule = HeuristicRule(pattern, action_type, response_template, confidence, category)
        self.rules.append(rule)

    def evaluate(self, perception: Perception, active_goal: str) -> Tuple[Optional[Action], float]:
        """
        Evaluate perception using rapid heuristic reflex.
        Returns (Action, confidence).
        """
        text = perception.content.strip()

        # Check reflex cache first (normalized exact matches)
        cache_key = f"{text.lower()}||{active_goal.lower()}"
        if cache_key in self.reflex_cache:
            cached_action, cached_conf = self.reflex_cache[cache_key]
            return cached_action, cached_conf

        # Pattern match rules
        best_rule: Optional[HeuristicRule] = None
        best_match: Optional[re.Match] = None
        best_confidence: float = 0.0

        for rule in self.rules:
            m = rule.match(text)
            if m and rule.confidence > best_confidence:
                best_rule = rule
                best_match = m
                best_confidence = rule.confidence

        if best_rule and best_confidence >= self.confidence_threshold:
            match_1 = best_match.group(2) if best_match.lastindex and best_match.lastindex >= 2 else (
                best_match.group(1) if best_match.lastindex else ""
            )
            rationale = f"System 1 pattern match on rule [{best_rule.category}] with confidence {best_rule.confidence:.2f}"
            payload_msg = best_rule.response_template.format(match_1=match_1)

            action = Action(
                action_type=best_rule.action_type,
                payload={"output": payload_msg, "category": best_rule.category, "pattern": best_rule.pattern},
                rationale=rationale,
                confidence=best_confidence,
                mode_used=CognitiveMode.SYSTEM_1
            )
            # Store in cache
            self.reflex_cache[cache_key] = (action, best_confidence)
            return action, best_confidence

        # Weak or no match
        weak_confidence = max(0.1, best_confidence if best_rule else 0.2)
        return None, weak_confidence
