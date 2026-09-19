"""
Fundamental types and dataclasses for the CogniMesh architecture.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time
import uuid


class CognitiveMode(str, Enum):
    """Execution mode of the cognitive loop."""
    SYSTEM_1 = "system_1_heuristic"
    SYSTEM_2 = "system_2_deliberative"
    HYBRID = "hybrid_arbitrated"


class ActionType(str, Enum):
    """Categorization of agent actions."""
    HEURISTIC_REPLY = "heuristic_reply"
    TOOL_EXECUTE = "tool_execute"
    DELIBERATE_PLAN = "deliberate_plan"
    REFLECT = "reflect"
    ABORT = "abort"


class MemorySalience(float, Enum):
    """Epistemic salience assigned to memory nodes."""
    LOW = 0.25
    MEDIUM = 0.50
    HIGH = 0.80
    CRITICAL = 1.00


@dataclass
class Perception:
    """Incoming sensory or environmental stimuli."""
    content: str
    source: str = "environment"
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    perception_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.perception_id,
            "content": self.content,
            "source": self.source,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class ThoughtNode:
    """A single node within the System 2 Tree-of-Thoughts / MCTS graph."""
    thought: str
    depth: int
    score: float = 0.0
    visits: int = 0
    parent_id: Optional[str] = None
    node_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    children: List[str] = field(default_factory=list)
    pruned: bool = False
    action_candidate: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "parent_id": self.parent_id,
            "thought": self.thought,
            "depth": self.depth,
            "score": round(self.score, 4),
            "visits": self.visits,
            "pruned": self.pruned,
            "action_candidate": self.action_candidate,
            "children": self.children,
        }


@dataclass
class Action:
    """An action determined by the cognitive engine."""
    action_type: ActionType
    payload: Dict[str, Any]
    rationale: str
    confidence: float
    mode_used: CognitiveMode
    timestamp: float = field(default_factory=time.time)
    action_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type.value,
            "payload": self.payload,
            "rationale": self.rationale,
            "confidence": round(self.confidence, 4),
            "mode_used": self.mode_used.value,
            "timestamp": self.timestamp,
        }


@dataclass
class ConfidenceMetric:
    """Detailed breakdown of epistemic confidence."""
    heuristic_score: float
    deliberative_score: float
    epistemic_uncertainty: float
    selected_mode: CognitiveMode
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "heuristic_score": round(self.heuristic_score, 4),
            "deliberative_score": round(self.deliberative_score, 4),
            "epistemic_uncertainty": round(self.epistemic_uncertainty, 4),
            "selected_mode": self.selected_mode.value,
            "reason": self.reason,
        }


@dataclass
class ReflectionTrace:
    """Metacognitive post-mortem inspection trace."""
    successful: bool
    critique: str
    counterfactual_alternative: str
    heuristic_rule_learned: Optional[str] = None
    epistemic_drift_detected: bool = False
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "successful": self.successful,
            "critique": self.critique,
            "counterfactual_alternative": self.counterfactual_alternative,
            "heuristic_rule_learned": self.heuristic_rule_learned,
            "epistemic_drift_detected": self.epistemic_drift_detected,
            "timestamp": self.timestamp,
        }


@dataclass
class CognitiveState:
    """Snapshot of agent internal state across cycles."""
    cycle_index: int
    active_goal: str
    working_memory_count: int
    episodic_memory_count: int
    semantic_concepts_count: int
    last_action: Optional[Action] = None
    last_reflection: Optional[ReflectionTrace] = None
    current_mode: CognitiveMode = CognitiveMode.SYSTEM_1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cycle_index": self.cycle_index,
            "active_goal": self.active_goal,
            "working_memory_count": self.working_memory_count,
            "episodic_memory_count": self.episodic_memory_count,
            "semantic_concepts_count": self.semantic_concepts_count,
            "last_action": self.last_action.to_dict() if self.last_action else None,
            "last_reflection": self.last_reflection.to_dict() if self.last_reflection else None,
            "current_mode": self.current_mode.value,
        }
