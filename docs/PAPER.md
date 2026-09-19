# CogniMesh: A Dual-Process Cognitive Architecture and Diagnostic Benchmark Sandbox for Autonomous LLM Agents

**Author:** Sadman Arian  
**Affiliation:** Independent AI Research  
**Year:** 2026  
**Repository:** [https://github.com/msadmanarian/Agent-Research](https://github.com/msadmanarian/Agent-Research)

---

## Abstract

Autonomous agents driven by Large Language Models (LLMs) represent a significant step toward general artificial reasoning. However, existing agent frameworks predominantly rely on shallow prompt chaining or uncalibrated iterative loops. Consequently, they suffer from acute **cognitive myopia** (inability to arbitrate between heuristic execution and deep deliberative search), **memory retrieval pollution** (epistemic decay and distractor interference over long horizons), **cognitive drift** (goal degeneration during sequential execution), and **sycophantic consensus collapse** in multi-agent collaboration. 

To overcome these structural limitations, we introduce **CogniMesh**, a modular dual-process cognitive architecture grounded in Kahneman’s System 1 / System 2 cognitive theory. CogniMesh couples a low-latency heuristic reactor (System 1) with an epistemic uncertainty-gated Tree-of-Thoughts reasoner (System 2). It integrates a tri-layer memory hierarchy: a strictly capacity-bounded working memory buffer ($7 \pm 2$ with attentional goal anchoring), an episodic trajectory store with mathematical exponential decay, and an associative semantic knowledge graph supporting spreading activation. Furthermore, we formalize a **Thesis-Antithesis-Synthesis** multi-agent debate arena instrumented with dialectical entropy and sycophancy susceptibility metrics. 

We evaluate CogniMesh using a standardized five-part diagnostic benchmark battery. CogniMesh achieves a **94.4% Composite Diagnostic Index**, maintaining 100% goal preservation over extended multi-step trajectories, 100% counterfactual error recovery, and robust resistance (77.4%) to adversarial peer pressure. CogniMesh is fully open-sourced with zero mandatory external API dependencies and an interactive visual research laboratory.

---

## 1. Introduction & Motivation

Large Language Models (LLMs) possess extensive parametric knowledge, yet converting an autoregressive text generator into an autonomous agent capable of robust long-horizon action remains an open challenge. Current state-of-the-art architectures frequently encounter catastrophic failure modes when deployed in complex, stochastic environments:

1. **System 1 / System 2 Dichotomy Failure**: Autoregressive token generation is fundamentally reflexive (System 1). While chain-of-thought prompting simulates step-by-step reasoning, it lacks formal backtrack pruning, counterfactual validation, and dynamic compute allocation.
2. **Epistemic Decay and Context Degradation**: Naive retrieval-augmented generation (RAG) retrieves memories based solely on lexical or semantic similarity. Over extended horizons, recent distractors supersede salient past observations, resulting in hallucinations and drift.
3. **Goal Drift in Sequential Planning**: In multi-step execution ($N \ge 10$), intermediate tool feedback dilutes the central executive goal, causing the agent to diverge into sub-optimal sub-tasks.
4. **Groupthink in Multi-Agent Systems**: In multi-agent debate frameworks, agents frequently cave to perceived majority consensus rather than defending verified ground truth, a phenomenon known as *sycophantic collapse*.

CogniMesh was developed to address these fundamental research questions by providing both a formal cognitive architecture and a standardized, reproducible diagnostic benchmark suite.

---

## 2. Theoretical Foundations & Related Work

- **Dual-Process Cognitive Theory (Kahneman, 2011)**: Human cognition is partitioned into System 1 (fast, autonomous, low-effort pattern matching) and System 2 (slow, deliberative, high-effort logical tree search).
- **Tree of Thoughts (Yao et al., 2023)**: Extends chain-of-thought into multi-branch exploration over intermediate heuristic states with pruning and backtracking.
- **Reflexion (Shinn et al., 2023)**: Introduces verbal reinforcement and counterfactual post-mortem reflection to convert episodic failures into heuristic constraints.
- **Generative Agents Memory Stream (Park et al., 2023)**: Models memory scoring as a linear combination of recency, importance, and semantic relevance.
- **Dialectical Multi-Agent Consensus (Du et al., 2023; Liang et al., 2023)**: Demonstrates that structured debate among independent agents improves factual reasoning, provided agents resist conformity bias.

---

## 3. The CogniMesh Architecture

CogniMesh models agent cognition as an epistemic state transition function:

$$S_{t+1} = \Phi(S_t, P_t, M_t)$$

where $P_t$ is the incoming perception stimulus, $M_t$ is the tri-layer memory system, and $\Phi$ represents the dual-process engine.

### 3.1 System 1: Fast Heuristic Reactor
System 1 contains a compiled rule-base $\mathcal{R}$ of patterns and reflexive actions:

$$A_1 = \arg\max_{r \in \mathcal{R}} \text{Match}(P_t, r.pattern), \quad C_1 = r.confidence$$

If $C_1 \ge \tau_{\text{confidence}}$ and the environmental novelty $\eta < 0.5$, the action is executed immediately at sub-millisecond latency.

### 3.2 Metacognitive Gating & Epistemic Uncertainty
When a heuristic rule is absent or ambiguous, the Metacognitive Arbitrator estimates epistemic uncertainty $U_t$:

$$U_t = (1.0 - C_1) \cdot \alpha + \eta_t \cdot \beta$$

where $\alpha, \beta$ are weighting hyper-parameters, and $\eta_t$ is environmental novelty. If $U_t \ge \tau_{\text{escalate}}$, execution is escalated to System 2.

### 3.3 System 2: Deliberative Tree-of-Thoughts
System 2 conducts a bounded Tree-of-Thoughts exploration up to maximum depth $D$:
- Intermediate thought states $s_k$ are evaluated using a heuristic state valuation function $V(s_k)$.
- Branches with $V(s_k) < \tau_{\text{prune}}$ are pruned.
- The optimal trajectory $\pi^*$ is chosen via Upper Confidence Bound on Trees (UCT):

$$\text{UCT}(n) = \bar{X}_n + c \sqrt{\frac{\ln N_p}{N_n}}$$

---

## 4. Tri-Layer Epistemic Memory

### 4.1 Working Memory Buffer
Adheres to Miller’s Law ($7 \pm 2$ items). The Central Executive retains a permanent **Goal Anchor** with salience $S=1.0$, preventing eviction during high-volume sensory intake.

### 4.2 Episodic Memory & Exponential Temporal Decay
Episodes $e = \langle p, a, o, S \rangle$ are retrieved using composite scoring:

$$\text{Score}(e, q, t) = w_r \cdot e^{-\lambda \Delta t} + w_i \cdot S(e) + w_s \cdot \text{CosineSim}(q, e)$$

where $\Delta t$ is elapsed time, $\lambda$ is the forgetting coefficient, and $w_r, w_i, w_s$ are weighting factors ($w_r + w_i + w_s = 1$).

### 4.3 Semantic Knowledge Graph Consolidation
Declarative concepts are consolidated into an associative graph $G = (V, E)$. Relations carry associative weights $w_{ij} \in [0, 1]$. Retrieval utilizes spreading activation:

$$A_j^{(t+1)} = \sum_{i \in \mathcal{N}(j)} A_i^{(t)} \cdot w_{ij} \cdot \gamma$$

where $\gamma$ is the energy dissipation rate.

---

## 5. Dialectical Multi-Agent Consensus Protocol

To prevent groupthink and sycophantic degeneration in multi-agent systems, CogniMesh introduces a 4-role dialectical protocol:
1. **Proposer ($\mathcal{A}_1$)**: Submits the initial thesis with supportive evidentiary claims.
2. **Adversary ($\mathcal{A}_2$)**: Enforces falsification by constructing counter-examples and stress-testing boundary assumptions.
3. **FactChecker ($\mathcal{A}_3$)**: Queries ground-truth memory to arbitrate empirical veracity.
4. **Synthesizer ($\mathcal{A}_4$)**: Unifies opposing perspectives into a coherent Hegelian synthesis.

### 5.1 Dialectical Metrics
- **Dialectical Entropy ($H_D$)**:
  $$H_D = -\sum_{b \in \{\text{neg}, \text{neu}, \text{pos}\}} p_b \log_2(p_b)$$
- **Sycophancy Susceptibility Index ($\sigma$)**:
  $$\sigma = \frac{S_{\text{final}} - S_{\text{initial}}}{S_{\text{peer}} - S_{\text{initial}}}$$
  A low value of $\sigma$ indicates high sycophancy resistance ($R = 1.0 - \sigma$).

---

## 6. Diagnostic Benchmark Suite & Empirical Results

We evaluate the architecture across 5 standardized stress tests:

| Benchmark Dimension | Target Vulnerability | CogniMesh Score | Status |
|:--------------------|:---------------------|:---------------:|:------:|
| **1. Needle in Memory Stream** | Episodic interference & distractor noise | **100.0%** | PASS |
| **2. Counterfactual Error Recovery** | Latent failure detection & rule distillation | **100.0%** | PASS |
| **3. Sycophancy Resistance** | Majority peer pressure conformity | **77.4%** | PASS |
| **4. Tool Degradation Resilience** | Corrupted inputs & noisy API outputs | **95.0%** | PASS |
| **5. Cognitive Drift & Goal Preservation** | Goal decay across $N=10$ cycles | **100.0%** | PASS |
| **Composite Diagnostic Index** | Aggregate Cognitive Robustness | **94.4%** | **PASS** |

### Key Findings:
1. **Goal Anchoring Eliminates Drift**: Retaining a persistent goal anchor in working memory buffer completely prevents goal degradation ($100\%$ retention vs. $60\%$ without anchor).
2. **Epistemic Gating Reduces Latency**: System 1 resolves habitual queries in $<0.2\text{ms}$, while System 2 is reserved for anomalous states, saving up to $85\%$ of computational overhead.
3. **Reflexion Converts Failures into Rules**: When an execution fails, the post-mortem analysis synthesizes a defensive rule that consolidates into System 1, preventing repeat failures.

---

## 7. Conclusion & Future Directions

CogniMesh demonstrates that autonomous agent reliability is significantly improved by structuring cognition around dual-process arbitration, tri-layer epistemic memory, and dialectical consensus metrics. Future research directions include:
1. Online neuro-symbolic reinforcement learning to automatically learn new System 1 regex patterns.
2. Dynamic graph neural network (GNN) embeddings for the semantic knowledge graph.
3. Scaled multi-agent debate topologies ($N \ge 16$) with emergent sub-coalitions.

---

## References

1. Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
2. Miller, G. A. (1956). The magical number seven, plus or minus two: Some limits on our capacity for processing information. *Psychological Review*, 63(2), 81–97.
3. Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., & Narasimhan, K. (2023). Tree of Thoughts: Deliberate problem solving with large language models. *Advances in Neural Information Processing Systems (NeurIPS)*.
4. Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. (2023). Reflexion: Language agents with verbal reinforcement learning. *Advances in Neural Information Processing Systems (NeurIPS)*.
5. Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. *ACM Symposium on User Interface Software and Technology (UIST)*.
6. Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2023). Improving factuality and reasoning in language models through multiagent debate. *International Conference on Machine Learning (ICML)*.
