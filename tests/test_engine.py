"""
Unit tests for CogniMesh Central Engine, System 1, and System 2.
"""

import unittest
from agent_research.core.engine import CognitiveEngine
from agent_research.core.types import CognitiveMode, ActionType


class TestCognitiveEngine(unittest.TestCase):

    def setUp(self):
        self.engine = CognitiveEngine(active_goal="Maintain system integrity")

    def test_system1_heuristic_match(self):
        """Test that a recognized keyword directly matches a System 1 heuristic rule."""
        result = self.engine.step(perception_content="ping status")
        self.assertEqual(result["selected_mode"], CognitiveMode.SYSTEM_1.value)
        self.assertGreaterEqual(result["confidence"]["heuristic_score"], 0.75)
        self.assertIn("nominal", result["action"]["payload"]["output"].lower())

    def test_system2_deliberative_escalation(self):
        """Test that an unfamiliar, novel stimulus escalates to System 2 Tree-of-Thoughts."""
        novel_stimulus = "Deconstruct quantum entanglement distribution anomaly in sub-cluster 9"
        result = self.engine.step(perception_content=novel_stimulus)
        self.assertEqual(result["selected_mode"], CognitiveMode.SYSTEM_2.value)
        self.assertGreater(result["thought_nodes_count"], 1)
        self.assertIn("plan", result["action"]["payload"])

    def test_reflection_and_rule_learning(self):
        """Test that environmental failure triggers reflection and consolidates a defensive rule."""
        initial_rules = len(self.engine.system1.rules)
        result = self.engine.step(
            perception_content="Execute direct database patch",
            simulate_feedback="ERROR: Deadlock and permission violation during patch application."
        )
        self.assertTrue(result["reflection"]["epistemic_drift_detected"])
        self.assertIsNotNone(result["reflection"]["heuristic_rule_learned"])
        self.assertGreater(len(self.engine.system1.rules), initial_rules)

    def test_state_snapshot(self):
        """Test that get_state accurately reflects internal state."""
        self.engine.step(perception_content="ping")
        state = self.engine.get_state()
        self.assertEqual(state.cycle_index, 1)
        self.assertGreaterEqual(state.working_memory_count, 1)
        self.assertGreaterEqual(state.episodic_memory_count, 1)


if __name__ == "__main__":
    unittest.main()
