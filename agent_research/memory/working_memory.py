"""
Working Memory Buffer.
Maintains a bounded cognitive workspace with attention-weighted priority eviction
and goal-directed attentional focus.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import time


@dataclass
class WorkingMemoryItem:
    """An item residing in working memory."""
    content: str
    salience: float = 0.5
    tag: str = "general"
    timestamp: float = field(default_factory=time.time)
    access_count: int = 0

    def boost(self, amount: float = 0.15) -> None:
        self.salience = min(1.0, self.salience + amount)
        self.access_count += 1


class WorkingMemory:
    """
    Capacity-bounded Working Memory (Miller's Law 7±2 principle).
    Prioritizes items based on attentional salience and relevance to current goal.
    """

    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.items: List[WorkingMemoryItem] = []

    def add(self, content: str, salience: float = 0.5, tag: str = "general") -> WorkingMemoryItem:
        """Add an item to working memory, evicting the lowest-salience item if capacity is exceeded."""
        item = WorkingMemoryItem(content=content, salience=salience, tag=tag)

        if len(self.items) >= self.capacity:
            # Evict item with lowest salience
            min_idx = 0
            min_val = self.items[0].salience
            for i, it in enumerate(self.items):
                if it.salience < min_val:
                    min_val = it.salience
                    min_idx = i
            self.items.pop(min_idx)

        self.items.append(item)
        return item

    def get_contents(self) -> List[str]:
        """Return list of text contents currently in working memory."""
        return [item.content for item in self.items]

    def focus(self, goal_query: str) -> List[WorkingMemoryItem]:
        """
        Attentional focus filter: boost items relevant to query and return sorted by salience.
        """
        query_words = set(goal_query.lower().split())
        for item in self.items:
            item_words = set(item.content.lower().split())
            if query_words.intersection(item_words):
                item.boost(0.2)

        sorted_items = sorted(self.items, key=lambda x: x.salience, reverse=True)
        return sorted_items

    def clear(self) -> None:
        self.items.clear()

    def __len__(self) -> int:
        return len(self.items)

    def to_dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "content": it.content,
                "salience": round(it.salience, 3),
                "tag": it.tag,
                "access_count": it.access_count,
            }
            for it in self.items
        ]
