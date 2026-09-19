"""
Unit tests for Tri-Layer Epistemic Memory (Working, Episodic, Semantic).
"""

import unittest
import time
from agent_research.memory.working_memory import WorkingMemory
from agent_research.memory.episodic_memory import EpisodicMemory
from agent_research.memory.semantic_graph import SemanticKnowledgeGraph


class TestEpistemicMemory(unittest.TestCase):

    def test_working_memory_bounded_capacity(self):
        """Test that working memory strictly respects Miller's 7 capacity limit."""
        wm = WorkingMemory(capacity=7)
        for i in range(10):
            wm.add(f"Memory item {i}", salience=0.1 * (i + 1))

        self.assertEqual(len(wm), 7)
        # Verify lowest salience items were evicted
        contents = wm.get_contents()
        self.assertNotIn("Memory item 0", contents)
        self.assertIn("Memory item 9", contents)

    def test_working_memory_focus_boost(self):
        """Test attentional focus boosting items matching goal query."""
        wm = WorkingMemory(capacity=7)
        wm.add("Routine telemetry packet", salience=0.3)
        wm.add("Emergency firewall shutdown override", salience=0.4)

        focused = wm.focus("firewall override")
        self.assertGreater(focused[0].salience, 0.5)
        self.assertIn("firewall", focused[0].content)

    def test_episodic_memory_retrieval_and_decay(self):
        """Test episodic trajectory storage and retrieval scoring."""
        em = EpisodicMemory(decay_rate=0.01)
        em.record("Database connection failed", "Retried connection", "Success", salience=0.8)
        em.record("Routine heartbeat check", "Sent ping", "Received pong", salience=0.3)

        # Retrieve relevant episode
        results = em.retrieve(query="database connection", top_k=1)
        self.assertEqual(len(results), 1)
        top_ep, score = results[0]
        self.assertIn("database", top_ep.perception_summary.lower())
        self.assertGreater(score, 0.4)

    def test_semantic_graph_spreading_activation(self):
        """Test semantic graph concept addition, relation linking, and spreading activation."""
        sg = SemanticKnowledgeGraph()
        c1 = sg.add_concept("Agent", "core", "Autonomous entity")
        c2 = sg.add_concept("Goal", "core", "Target objective")
        sg.add_relation(c1, c2, "pursues", 0.9)

        activations = sg.spread_activation("Agent", decay=0.8, max_hops=1)
        self.assertIn(c1, activations)
        self.assertIn(c2, activations)
        self.assertGreater(activations[c2], 0.5)

    def test_semantic_facts_query(self):
        """Test querying facts from the semantic knowledge graph."""
        sg = SemanticKnowledgeGraph()
        facts = sg.query_facts("Perception")
        self.assertGreater(len(facts), 0)
        self.assertTrue(any("perception" in f.lower() for f in facts))


if __name__ == "__main__":
    unittest.main()
