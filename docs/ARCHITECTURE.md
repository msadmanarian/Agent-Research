# CogniMesh Architecture & Developer Guide

This document provides a technical deep dive into the inner workings of CogniMesh, covering state transitions, memory mechanics, extensibility patterns, and REST API contracts.

---

## 1. High-Level System Architecture

```text
+-------------------------------------------------------------------------+
|                               Perception                                |
|                                (Sensory)                                |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                              Working Memory                             |
|                        (Bounded FIFO: Capacity = 7)                     |
|                   [ Goal Anchor (Salience = 1.0) ]                     |
+-------------------+--------------------------------+--------------------+
                    |                                |
                    v                                v
+------------------------------------+ +----------------------------------+
|           Episodic Memory          | |      Semantic Knowledge Graph    |
|   (Decay: E(t) = exp(-λΔt) * S)    | |  (Concepts, Relations & Energy)  |
+-------------------+----------------+ +-----------------+----------------+
                    |                                    |
                    +----------------+-------------------+
                                     | Context Retrieval
                                     v
+-------------------------------------------------------------------------+
|                      System 1: Fast Heuristic Reactor                   |
|                        - Regex Pattern Matcher                          |
|                        - Associative Reflex Cache                       |
+------------------------------------+------------------------------------+
                                     | Heuristic Action & Confidence (C1)
                                     v
+-------------------------------------------------------------------------+
|                      Metacognitive Arbitrator                           |
|        Computes Epistemic Uncertainty U = (1 - C1)*α + Novelty*β        |
|                  Decision: Is U < Threshold (0.75)?                     |
+--------------------+-------------------------------+--------------------+
                     | YES                           | NO (Escalate)
                     v                               v
            +-----------------+             +-----------------------------+
            | System 1 Action |             | System 2 Deliberative Engine|
            +--------+--------+             |  - Tree-of-Thoughts Search  |
                     |                      |  - Intermediate Evaluation  |
                     |                      |  - Trajectory Pruning       |
                     |                      +--------------+--------------+
                     |                                     |
                     +----------------+--------------------+
                                      | Final Action
                                      v
+-------------------------------------------------------------------------+
|                         Environmental Execution                         |
|                             & Feedback Loop                             |
+-------------------------------------+-----------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------+
|                      Metacognitive Self-Reflector                       |
|         - Detects Divergence & Epistemic Drift                          |
|         - Generates Counterfactual Recovery Strategy                    |
|         - Distills Defensive Heuristic Rule into System 1               |
+-------------------------------------------------------------------------+
```

---

## 2. Core Modules Reference

### `agent_research.core`
- **`types.py`**: Strong typing primitives (`Perception`, `Action`, `ThoughtNode`, `CognitiveState`, `ConfidenceMetric`, `ReflectionTrace`).
- **`system1.py`**: `HeuristicRule` and `System1Reactor` implementing regex pattern matching, response templating, and instant cache dispatch.
- **`system2.py`**: `System2Deliberator` implementing Tree-of-Thoughts depth-first / beam search, heuristic state scoring, and branch pruning.
- **`engine.py`**: `CognitiveEngine` coordinating the complete perceptual, deliberative, and reflective lifecycle.

### `agent_research.memory`
- **`working_memory.py`**: `WorkingMemory` with Miller capacity limit ($7$), priority eviction of low-salience items, and persistent Central Executive goal anchoring.
- **`episodic_memory.py`**: `EpisodicMemory` with time-indexed decay retrieval scoring ($S_{\text{retrieval}} = w_r \cdot \text{Recency} + w_i \cdot \text{Importance} + w_s \cdot \text{Relevance}$).
- **`semantic_graph.py`**: `SemanticKnowledgeGraph` supporting concept nodes, directed relational edges, fact synthesis, and multi-hop spreading activation.

### `agent_research.metacognition`
- **`uncertainty_evaluator.py`**: Evaluates epistemic uncertainty and dynamically chooses between `SYSTEM_1_HEURISTIC` and `SYSTEM_2_DELIBERATIVE`.
- **`self_reflection.py`**: `SelfReflector` analyzing environment failure feedback, computing counterfactual alternatives, and consolidating learned rules.

### `agent_research.multiagent`
- **`debate_arena.py`**: `DialecticalArena` executing multi-round Thesis-Antithesis-Synthesis debates across four specialized roles.
- **`consensus_metrics.py`**: Computes dialectical entropy, Jaccard lexical overlap, and sycophancy susceptibility indices.

---

## 3. Extensibility Guide

### Adding a Custom Heuristic Rule to System 1
```python
from agent_research.core.engine import CognitiveEngine
from agent_research.core.types import ActionType

engine = CognitiveEngine()
engine.system1.add_rule(
    pattern=r"\b(deploy|release)\s+([a-zA-Z0-9_\-]+)",
    action_type=ActionType.TOOL_EXECUTE,
    response_template="Initiate deployment pipeline for service: {match_1}",
    confidence=0.90,
    category="devops"
)
```

### Adding a Custom Real LLM Backend
```python
from agent_research.llm.base import BaseLLMProvider

class CustomLLMProvider(BaseLLMProvider):
    def generate(self, prompt: str, system_prompt: str = None, temperature: float = 0.7) -> str:
        # Call your private model or custom endpoint
        return "Model completion"

    def generate_deliberation(self, goal: str, context: list, depth: int) -> list:
        # Return 3 strategic reasoning steps
        return [f"Branch 1 for {goal}", f"Branch 2 for {goal}", f"Branch 3 for {goal}"]
```

### Creating a New Diagnostic Benchmark Task
```python
def run_custom_stress_test(engine=None):
    if engine is None:
        engine = CognitiveEngine()
    
    # 1. Setup initial conditions
    # 2. Run cognitive cycle: result = engine.step(...)
    # 3. Evaluate criteria
    passed = True
    score = 1.0
    
    return {
        "task_name": "Custom Constraint Test",
        "category": "Safety",
        "passed": passed,
        "score": score,
        "details": "All safety boundaries preserved"
    }
```
