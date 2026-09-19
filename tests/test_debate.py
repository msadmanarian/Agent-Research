"""
Unit tests for Dialectical Arena and Consensus Metrics.
"""

import unittest
from agent_research.multiagent.debate_arena import DialecticalArena
from agent_research.multiagent.consensus_metrics import (
    compute_dialectical_entropy,
    compute_sycophancy_index,
    compute_lexical_overlap,
)


class TestDebateArena(unittest.TestCase):

    def test_debate_execution(self):
        """Test full dialectical debate lifecycle."""
        arena = DialecticalArena(topic="Symbolic Planning vs Neural Reactive Policies", max_rounds=3)
        res = arena.run_debate()

        self.assertTrue(res["consensus_achieved"])
        self.assertGreaterEqual(res["total_messages"], 5)
        self.assertIsNotNone(res["synthesis"])
        self.assertGreaterEqual(res["sycophancy_resistance_score"], 0.5)

    def test_dialectical_entropy(self):
        """Test entropy calculation over stance distribution."""
        # Balanced stances should yield high entropy
        balanced = [-0.8, 0.0, 0.8]
        ent_high = compute_dialectical_entropy(balanced)

        # Monolithic stances should yield zero or low entropy
        monolithic = [0.9, 0.95, 0.85]
        ent_low = compute_dialectical_entropy(monolithic)

        self.assertGreater(ent_high, ent_low)

    def test_sycophancy_index(self):
        """Test sycophancy metric computation."""
        # Case 1: Agent completely flips stance to please peer
        flipped = compute_sycophancy_index(initial_stance=-1.0, peer_pressure_stance=1.0, final_stance=1.0)
        self.assertAlmostEqual(flipped, 1.0, places=2)

        # Case 2: Agent sticks firmly to original stance
        stubborn = compute_sycophancy_index(initial_stance=-1.0, peer_pressure_stance=1.0, final_stance=-1.0)
        self.assertAlmostEqual(stubborn, 0.0, places=2)

    def test_lexical_overlap(self):
        """Test Jaccard lexical overlap computation."""
        s1 = "autonomous agents use deliberate tree search"
        s2 = "autonomous agents use reactive heuristic reflex"
        overlap = compute_lexical_overlap(s1, s2)
        self.assertGreater(overlap, 0.3)


if __name__ == "__main__":
    unittest.main()
