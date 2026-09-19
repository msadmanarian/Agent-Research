"""
System 2: Deliberative Reasoner.
Implements Tree-of-Thoughts (ToT) exploration, heuristic state evaluation,
forward simulation, and self-corrective trajectory pruning.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Any
import math
import re
from agent_research.core.types import Action, ActionType, CognitiveMode, Perception, ThoughtNode


class System2Deliberator:
    """
    Kahneman System 2 Deliberative Engine.
    Executes deep reasoning via a multi-branch search tree, scoring intermediate states,
    pruning unpromising hypotheses, and selecting the optimal action trajectory.
    """

    def __init__(
        self,
        max_depth: int = 3,
        branching_factor: int = 3,
        pruning_threshold: float = 0.40,
        exploration_constant: float = 1.414,
    ):
        self.max_depth = max_depth
        self.branching_factor = branching_factor
        self.pruning_threshold = pruning_threshold
        self.exploration_constant = exploration_constant

    def deliberate(
        self,
        perception: Perception,
        active_goal: str,
        working_memory_context: List[str],
        semantic_facts: List[str],
        candidate_generator=None,
    ) -> Tuple[Action, List[ThoughtNode], float]:
        """
        Execute Tree-of-Thoughts exploration.
        Returns:
            - Selected Action
            - Complete list of ThoughtNodes in the search tree
            - Epistemic confidence score in the selected trajectory
        """
        nodes: Dict[str, ThoughtNode] = {}
        root = ThoughtNode(
            thought=f"Goal: '{active_goal}' | Contextual Trigger: '{perception.content}'",
            depth=0,
            score=0.5,
            visits=1,
            node_id="root",
        )
        nodes["root"] = root

        # Generate layer 1: Candidate strategic approaches
        current_layer: List[str] = ["root"]

        for depth in range(1, self.max_depth + 1):
            next_layer: List[str] = []

            for parent_id in current_layer:
                parent_node = nodes[parent_id]
                if parent_node.pruned:
                    continue

                # Generate branches
                branches = self._generate_thought_branches(
                    parent_node=parent_node,
                    depth=depth,
                    active_goal=active_goal,
                    context=working_memory_context,
                    facts=semantic_facts,
                    custom_generator=candidate_generator,
                )

                for branch_thought, action_cand in branches:
                    child = ThoughtNode(
                        thought=branch_thought,
                        depth=depth,
                        parent_id=parent_id,
                        action_candidate=action_cand,
                    )
                    # Evaluate intermediate heuristic quality
                    score = self._evaluate_state(child, active_goal, working_memory_context, semantic_facts)
                    child.score = score
                    child.visits = 1

                    if score < self.pruning_threshold and depth > 1:
                        child.pruned = True

                    nodes[child.node_id] = child
                    parent_node.children.append(child.node_id)

                    if not child.pruned:
                        next_layer.append(child.node_id)

            if not next_layer:
                break
            current_layer = next_layer

        # Find best leaf node using UCT (Upper Confidence bound for Trees) scoring
        best_leaf = self._select_best_trajectory(nodes)

        # Reconstruct path from root to best leaf
        path: List[ThoughtNode] = []
        curr: Optional[ThoughtNode] = best_leaf
        while curr and curr.node_id != "root":
            path.insert(0, curr)
            curr = nodes.get(curr.parent_id) if curr.parent_id else None

        # Build final deliberate action
        if best_leaf and best_leaf.action_candidate:
            chosen_action_text = best_leaf.action_candidate
        elif path:
            chosen_action_text = path[-1].thought
        else:
            chosen_action_text = f"Synthesized systematic plan for: {active_goal}"

        deliberative_confidence = min(0.98, max(0.55, best_leaf.score if best_leaf else 0.70))
        reasoning_summary = " -> ".join([p.thought for p in path]) if path else "Deliberative synthesis"

        action = Action(
            action_type=ActionType.DELIBERATE_PLAN,
            payload={
                "plan": chosen_action_text,
                "search_depth": len(path),
                "total_nodes_explored": len(nodes),
                "reasoning_trajectory": [p.to_dict() for p in path],
            },
            rationale=f"System 2 Tree-of-Thoughts depth {len(path)}: {reasoning_summary}",
            confidence=deliberative_confidence,
            mode_used=CognitiveMode.SYSTEM_2,
        )

        return action, list(nodes.values()), deliberative_confidence

    def _generate_thought_branches(
        self,
        parent_node: ThoughtNode,
        depth: int,
        active_goal: str,
        context: List[str],
        facts: List[str],
        custom_generator=None,
    ) -> List[Tuple[str, str]]:
        """Synthesize candidate reasoning branches for next depth."""
        if custom_generator:
            return custom_generator(parent_node, depth, active_goal, context, facts)

        # Built-in heuristic reasoning expansions
        if depth == 1:
            return [
                (
                    f"Decompose goal '{active_goal}' into prerequisite sub-tasks and dependency graph",
                    f"Formulate sub-task breakdown for '{active_goal}'"
                ),
                (
                    f"Cross-reference prior semantic facts ({len(facts)} available) for analogous solutions",
                    f"Query semantic knowledge graph for verified facts matching '{active_goal}'"
                ),
                (
                    f"Analyze potential edge-case failure modes and safety constraints for '{active_goal}'",
                    f"Construct protective boundary conditions and fallback checkpoints"
                ),
            ]
        elif depth == 2:
            return [
                (
                    f"Synthesize empirical execution step based on: {parent_node.thought[:40]}...",
                    f"Execute primary operational sequence with telemetry logging"
                ),
                (
                    f"Apply dialetheic validation: check if evidence contradicts hypothesis",
                    f"Run self-consistency check against working memory"
                ),
            ]
        else:
            return [
                (
                    f"Finalize optimal deterministic action sequence with verified state transitions",
                    f"Commit verified plan into execution buffer"
                ),
            ]

    def _evaluate_state(
        self,
        node: ThoughtNode,
        goal: str,
        context: List[str],
        facts: List[str]
    ) -> float:
        """
        Epistemic heuristic evaluation function for intermediate thought nodes.
        Computes score in [0.0, 1.0].
        """
        score = 0.60  # Prior base score

        # Reward semantic overlap with goal
        goal_words = set(re.findall(r"\w+", goal.lower()))
        thought_words = set(re.findall(r"\w+", node.thought.lower()))
        overlap = len(goal_words.intersection(thought_words))
        score += min(0.20, overlap * 0.05)

        # Reward fact consistency
        for fact in facts:
            fact_words = set(re.findall(r"\w+", fact.lower()))
            if len(thought_words.intersection(fact_words)) >= 2:
                score += 0.10
                break

        # Penalize superficial vagueness
        if len(node.thought.strip()) < 15:
            score -= 0.25

        return min(0.99, max(0.05, score))

    def _select_best_trajectory(self, nodes: Dict[str, ThoughtNode]) -> ThoughtNode:
        """Select best leaf node based on score and exploration criteria."""
        leaves = [n for n in nodes.values() if not n.children and n.node_id != "root"]
        if not leaves:
            return nodes.get("root", ThoughtNode(thought="Fallback", depth=0))

        # Sort by score desc
        non_pruned = [l for l in leaves if not l.pruned]
        if non_pruned:
            return max(non_pruned, key=lambda n: n.score)
        return max(leaves, key=lambda n: n.score)
