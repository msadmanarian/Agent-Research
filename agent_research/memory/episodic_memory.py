"""
Episodic Trajectory Store.
Implements time-indexed experiential episodes with mathematical decay scoring,
retrieval arbitration, and episodic-to-semantic consolidation triggers.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import math
import time
import re
import uuid


@dataclass
class Episode:
    """An episodic experiential trace."""
    episode_id: str
    perception_summary: str
    action_taken: str
    outcome: str
    salience: float = 0.5
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    retrieval_count: int = 0

    def compute_retrieval_score(
        self,
        query: str,
        current_time: float,
        decay_rate: float = 0.005,
        w_recency: float = 0.30,
        w_importance: float = 0.35,
        w_relevance: float = 0.35,
    ) -> float:
        """
        Calculates composite retrieval score:
        Score = w_recency * Recency + w_importance * Importance + w_relevance * Relevance
        Where Recency = exp(-decay_rate * delta_t).
        """
        delta_t = max(0.0, current_time - self.timestamp)
        recency = math.exp(-decay_rate * delta_t)

        importance = self.salience

        # Semantic/lexical relevance
        query_words = set(re.findall(r"\w+", query.lower()))
        content_text = f"{self.perception_summary} {self.action_taken} {self.outcome}".lower()
        content_words = set(re.findall(r"\w+", content_text))

        if not query_words:
            relevance = 0.1
        else:
            intersection = query_words.intersection(content_words)
            relevance = len(intersection) / len(query_words)

        score = (w_recency * recency) + (w_importance * importance) + (w_relevance * relevance)
        return min(1.0, max(0.0, score))


class EpisodicMemory:
    """
    Episodic Memory Bank.
    Maintains a chronological log of agent interactions, calculating dynamic
    temporal decay and prioritizing relevant memories during retrieval.
    """

    def __init__(self, decay_rate: float = 0.001, max_episodes: int = 2000):
        self.decay_rate = decay_rate
        self.max_episodes = max_episodes
        self.episodes: List[Episode] = []

    def record(
        self,
        perception_summary: str,
        action_taken: str,
        outcome: str,
        salience: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Episode:
        """Record a new experiential episode."""
        ep = Episode(
            episode_id=str(uuid.uuid4())[:8],
            perception_summary=perception_summary,
            action_taken=action_taken,
            outcome=outcome,
            salience=min(1.0, max(0.1, salience)),
            timestamp=time.time(),
            metadata=metadata or {},
        )

        if len(self.episodes) >= self.max_episodes:
            # Drop lowest salience episode
            min_idx = 0
            min_sal = self.episodes[0].salience
            for i, e in enumerate(self.episodes):
                if e.salience < min_sal:
                    min_sal = e.salience
                    min_idx = i
            self.episodes.pop(min_idx)

        self.episodes.append(ep)
        return ep

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Episode, float]]:
        """Retrieve the top_k most relevant and salient episodes for a given query."""
        now = time.time()
        scored: List[Tuple[Episode, float]] = []

        for ep in self.episodes:
            score = ep.compute_retrieval_score(query=query, current_time=now, decay_rate=self.decay_rate)
            scored.append((ep, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        results = scored[:top_k]
        for ep, _ in results:
            ep.retrieval_count += 1

        return results

    def find_analogous_failures(self, query: str, top_k: int = 2) -> List[Episode]:
        """Query episodes specifically tagged with negative or failure outcomes for counterfactual learning."""
        candidates = [e for e in self.episodes if "fail" in e.outcome.lower() or "error" in e.outcome.lower()]
        now = time.time()
        scored = [(e, e.compute_retrieval_score(query, now, self.decay_rate)) for e in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [e for e, _ in scored[:top_k]]

    def __len__(self) -> int:
        return len(self.episodes)

    def to_dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": e.episode_id,
                "perception": e.perception_summary,
                "action": e.action_taken,
                "outcome": e.outcome,
                "salience": round(e.salience, 3),
                "timestamp": e.timestamp,
                "retrieval_count": e.retrieval_count,
            }
            for e in self.episodes[-25:]  # Return most recent 25 for inspection
        ]
