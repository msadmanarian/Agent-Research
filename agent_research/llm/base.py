"""
Base interface for LLM providers in CogniMesh.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class BaseLLMProvider(ABC):
    """Abstract interface for language model backends."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        """Generate textual completion for a given prompt."""
        pass

    @abstractmethod
    def generate_deliberation(self, goal: str, context: List[str], depth: int) -> List[str]:
        """Generate multi-branch candidate hypotheses for System 2."""
        pass
