"""
CogniMesh: Dual-Process Cognitive Architecture & Diagnostic Research Sandbox for Autonomous Agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A modular research framework for exploring System 1 / System 2 cognitive dynamics,
tri-layer epistemic memory consolidation, dialectical multi-agent consensus,
and empirical diagnostic benchmarking.
"""

__version__ = "1.0.0"
__author__ = "Sadman Arian"
__license__ = "MIT"

from agent_research.core.engine import CognitiveEngine
from agent_research.core.types import Perception, Action, CognitiveState
from agent_research.memory.working_memory import WorkingMemory
from agent_research.memory.episodic_memory import EpisodicMemory
from agent_research.memory.semantic_graph import SemanticKnowledgeGraph
from agent_research.multiagent.debate_arena import DialecticalArena
from agent_research.benchmarks.harness import BenchmarkHarness

__all__ = [
    "CognitiveEngine",
    "Perception",
    "Action",
    "CognitiveState",
    "WorkingMemory",
    "EpisodicMemory",
    "SemanticKnowledgeGraph",
    "DialecticalArena",
    "BenchmarkHarness",
]
