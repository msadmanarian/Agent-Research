"""
Semantic Knowledge Graph.
Maintains an associative concept network representing consolidated declarative knowledge,
entities, relations, and spreading activation.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
import uuid


@dataclass
class ConceptNode:
    """A semantic concept node."""
    name: str
    category: str = "concept"
    description: str = ""
    activation: float = 0.0
    confidence: float = 0.90
    node_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "activation": round(self.activation, 3),
            "confidence": round(self.confidence, 3),
        }


@dataclass
class SemanticEdge:
    """A directed relational edge between two concepts."""
    source_id: str
    target_id: str
    relation: str
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source_id,
            "target": self.target_id,
            "relation": self.relation,
            "weight": round(self.weight, 3),
        }


class SemanticKnowledgeGraph:
    """
    Associative Semantic Memory Network.
    Enables declarative reasoning, relation traversal, and associative spreading activation.
    """

    def __init__(self):
        self.nodes: Dict[str, ConceptNode] = {}  # node_id -> ConceptNode
        self.name_to_id: Dict[str, str] = {}    # normalized name -> node_id
        self.edges: List[SemanticEdge] = []
        self.adjacency: Dict[str, List[Tuple[str, str, float]]] = {}  # source_id -> [(target_id, relation, weight)]
        self._init_baseline_concepts()

    def _init_baseline_concepts(self) -> None:
        """Seed initial domain knowledge regarding agent cognitive architectures."""
        c1 = self.add_concept("Perception", "cognitive_component", "Intake of environmental signals and user inputs")
        c2 = self.add_concept("Working Memory", "memory_system", "Active bounded buffer for current cognitive task")
        c3 = self.add_concept("System 1", "reasoning_engine", "Fast heuristic pattern matching and intuitive reaction")
        c4 = self.add_concept("System 2", "reasoning_engine", "Deliberative tree-of-thoughts and forward planning")
        c5 = self.add_concept("Episodic Memory", "memory_system", "Time-indexed log of past actions and outcomes")
        c6 = self.add_concept("Metacognition", "supervisory_layer", "Self-reflective evaluation of uncertainty and failure")
        c7 = self.add_concept("Consensus Arena", "multiagent_system", "Dialectical debate protocol for truth alignment")

        self.add_relation(c1, c2, "feeds_into", 0.95)
        self.add_relation(c2, c3, "triggers_fast_path", 0.90)
        self.add_relation(c3, c6, "escalates_on_uncertainty", 0.85)
        self.add_relation(c6, c4, "activates_deliberation", 0.92)
        self.add_relation(c4, c5, "commits_episode", 0.88)
        self.add_relation(c5, c2, "retrieves_context", 0.80)
        self.add_relation(c4, c7, "submits_thesis", 0.75)

    def add_concept(
        self,
        name: str,
        category: str = "general",
        description: str = "",
        confidence: float = 0.90
    ) -> str:
        """Add or update a concept in the semantic graph. Returns node_id."""
        normalized = name.strip().lower()
        if normalized in self.name_to_id:
            node_id = self.name_to_id[normalized]
            self.nodes[node_id].activation += 0.2
            return node_id

        node = ConceptNode(name=name, category=category, description=description, confidence=confidence)
        self.nodes[node.node_id] = node
        self.name_to_id[normalized] = node.node_id
        self.adjacency[node.node_id] = []
        return node.node_id

    def add_relation(self, source_id: str, target_id: str, relation: str, weight: float = 1.0) -> None:
        """Add a directed relation between two concepts."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return

        # Check existing
        for edge in self.edges:
            if edge.source_id == source_id and edge.target_id == target_id and edge.relation == relation:
                edge.weight = min(1.0, edge.weight + 0.1)
                return

        edge = SemanticEdge(source_id=source_id, target_id=target_id, relation=relation, weight=weight)
        self.edges.append(edge)
        self.adjacency[source_id].append((target_id, relation, weight))

    def spread_activation(self, seed_concept: str, decay: float = 0.65, max_hops: int = 2) -> Dict[str, float]:
        """
        Spreading activation algorithm:
        Activates seed concept and propagates energy through adjacent edges.
        """
        normalized = seed_concept.strip().lower()
        if normalized not in self.name_to_id:
            return {}

        seed_id = self.name_to_id[normalized]
        activations: Dict[str, float] = {seed_id: 1.0}
        frontier: List[Tuple[str, float, int]] = [(seed_id, 1.0, 0)]

        while frontier:
            curr_id, current_energy, hop = frontier.pop(0)
            if hop >= max_hops:
                continue

            for target_id, _, weight in self.adjacency.get(curr_id, []):
                transferred = current_energy * weight * decay
                if transferred > 0.05:
                    new_val = activations.get(target_id, 0.0) + transferred
                    activations[target_id] = min(1.0, new_val)
                    frontier.append((target_id, transferred, hop + 1))

        # Update node activation levels
        for nid, val in activations.items():
            if nid in self.nodes:
                self.nodes[nid].activation = max(self.nodes[nid].activation, val)

        return activations

    def query_facts(self, keyword: str) -> List[str]:
        """Generate human-readable semantic facts related to a keyword."""
        normalized = keyword.strip().lower()
        facts: List[str] = []

        # Find matching nodes
        for node in self.nodes.values():
            if normalized in node.name.lower() or normalized in node.description.lower():
                facts.append(f"Concept '{node.name}' ({node.category}): {node.description}")
                # Add adjacent relations
                for target_id, relation, weight in self.adjacency.get(node.node_id, []):
                    target = self.nodes.get(target_id)
                    if target:
                        facts.append(f"Fact: '{node.name}' {relation.replace('_', ' ')} '{target.name}' (weight: {weight:.2f})")

        return facts[:5]

    def to_graph_data(self) -> Dict[str, Any]:
        """Export graph formatted for HTML5 dynamic canvas rendering."""
        return {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
        }

    def __len__(self) -> int:
        return len(self.nodes)
