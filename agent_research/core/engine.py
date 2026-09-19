"""
CogniMesh Central Cognitive Engine.
Orchestrates the complete dual-process perception-deliberation-action-reflection cycle.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any, Tuple
import time

from agent_research.core.types import (
    Action,
    ActionType,
    CognitiveMode,
    CognitiveState,
    ConfidenceMetric,
    Perception,
    ReflectionTrace,
    ThoughtNode,
)
from agent_research.core.system1 import System1Reactor
from agent_research.core.system2 import System2Deliberator
from agent_research.memory.working_memory import WorkingMemory
from agent_research.memory.episodic_memory import EpisodicMemory
from agent_research.memory.semantic_graph import SemanticKnowledgeGraph
from agent_research.metacognition.uncertainty_evaluator import UncertaintyEvaluator
from agent_research.metacognition.self_reflection import SelfReflector


class CognitiveEngine:
    """
    Master CogniMesh Engine.
    Coordinates dual-process reasoning, memory consolidation, and metacognitive arbitration.
    """

    def __init__(
        self,
        active_goal: str = "Accomplish autonomous task objectives with high reliability",
        working_memory_capacity: int = 7,
        confidence_threshold: float = 0.75,
    ):
        self.active_goal = active_goal
        self.cycle_index = 0

        # Subsystems
        self.system1 = System1Reactor(confidence_threshold=confidence_threshold)
        self.system2 = System2Deliberator(max_depth=3, branching_factor=3)
        self.working_memory = WorkingMemory(capacity=working_memory_capacity)
        self.episodic_memory = EpisodicMemory()
        self.semantic_graph = SemanticKnowledgeGraph()
        self.uncertainty_evaluator = UncertaintyEvaluator(escalation_threshold=confidence_threshold)
        self.self_reflector = SelfReflector()

        # Telemetry
        self.last_action: Optional[Action] = None
        self.last_confidence: Optional[ConfidenceMetric] = None
        self.last_thought_tree: List[ThoughtNode] = []
        self.last_reflection: Optional[ReflectionTrace] = None

    def step(
        self,
        perception_content: str,
        source: str = "environment",
        metadata: Optional[Dict[str, Any]] = None,
        simulate_feedback: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute one full cognitive cycle:
        1. Sensory Intake & Perception Formation
        2. Working Memory Ingestion & Attentional Focus
        3. Memory Context Retrieval (Episodic + Semantic Graph)
        4. System 1 Reflex Evaluation
        5. Metacognitive Uncertainty Evaluation & Mode Arbitration
        6. System 2 Deliberation (if escalated)
        7. Action Finalization & Execution
        8. Reflection, Memory Consolidation & Rule Distillation
        """
        self.cycle_index += 1
        cycle_start = time.time()

        # 1. Perception
        perception = Perception(content=perception_content, source=source, metadata=metadata or {})

        # Ensure active goal anchor is retained in working memory
        if not any(it.tag == "goal_anchor" for it in self.working_memory.items):
            self.working_memory.add(content=f"Active Goal: {self.active_goal}", salience=1.0, tag="goal_anchor")

        # 2. Working Memory Focus
        self.working_memory.add(content=perception.content, salience=0.6, tag="input")
        focused_items = self.working_memory.focus(self.active_goal)
        working_context = [it.content for it in focused_items]

        # 3. Memory Retrieval
        past_episodes = self.episodic_memory.retrieve(query=perception.content, top_k=2)
        semantic_facts = self.semantic_graph.query_facts(keyword=perception.content)
        # Also spread activation in semantic graph
        self.semantic_graph.spread_activation(seed_concept="Perception", decay=0.6)

        # 4. System 1 Reflex Check
        s1_action, s1_confidence = self.system1.evaluate(perception=perception, active_goal=self.active_goal)

        # 5. Metacognitive Arbitration
        novelty_score = 0.1 if s1_action else 0.65
        arbitration = self.uncertainty_evaluator.evaluate(
            perception=perception,
            heuristic_action_available=(s1_action is not None),
            heuristic_confidence=s1_confidence,
            working_memory_size=len(self.working_memory),
            novelty_score=novelty_score,
        )
        self.last_confidence = arbitration

        # 6. Execution or Escalation
        if arbitration.selected_mode == CognitiveMode.SYSTEM_1 and s1_action:
            action = s1_action
            thought_tree = []
        else:
            # Escalate to System 2 Deliberation
            action, thought_tree, s2_conf = self.system2.deliberate(
                perception=perception,
                active_goal=self.active_goal,
                working_memory_context=working_context,
                semantic_facts=semantic_facts,
            )
            # Update working memory with chosen plan
            plan_str = str(action.payload.get("plan", "deliberate plan"))
            self.working_memory.add(content=f"Plan: {plan_str}", salience=0.9, tag="plan")

        self.last_action = action
        self.last_thought_tree = thought_tree

        # 7. Simulated or Provided Environmental Feedback & Reflection
        feedback = simulate_feedback or f"Execution nominal: {action.action_type.value} applied."
        reflection = self.self_reflector.reflect(
            action=action,
            environment_feedback=feedback,
            expected_outcome="Nominal task progression",
        )
        self.last_reflection = reflection

        # 8. Memory Consolidation: Record Episode
        self.episodic_memory.record(
            perception_summary=perception.content[:100],
            action_taken=str(action.payload),
            outcome=feedback,
            salience=0.8 if reflection.epistemic_drift_detected else 0.5,
            metadata={"mode": action.mode_used.value, "cycle": self.cycle_index},
        )

        # Distill newly learned heuristic rule if reflection yielded one
        if reflection.heuristic_rule_learned:
            self.system1.add_rule(
                pattern=rf"\b({perception.content[:15].strip()})\b",
                action_type=ActionType.REFLECT,
                response_template=f"Reflexive mitigation: {reflection.heuristic_rule_learned}",
                confidence=0.82,
                category="distilled_reflex",
            )

        cycle_duration = round((time.time() - cycle_start) * 1000, 2)

        return {
            "cycle_index": self.cycle_index,
            "perception": perception.to_dict(),
            "selected_mode": action.mode_used.value,
            "confidence": arbitration.to_dict(),
            "action": action.to_dict(),
            "thought_nodes_count": len(thought_tree),
            "reflection": reflection.to_dict(),
            "duration_ms": cycle_duration,
            "working_memory": self.working_memory.to_dict(),
            "episodic_count": len(self.episodic_memory),
            "semantic_nodes_count": len(self.semantic_graph),
        }

    def get_state(self) -> CognitiveState:
        """Capture current cognitive state snapshot."""
        return CognitiveState(
            cycle_index=self.cycle_index,
            active_goal=self.active_goal,
            working_memory_count=len(self.working_memory),
            episodic_memory_count=len(self.episodic_memory),
            semantic_concepts_count=len(self.semantic_graph),
            last_action=self.last_action,
            last_reflection=self.last_reflection,
            current_mode=self.last_action.mode_used if self.last_action else CognitiveMode.SYSTEM_1,
        )
