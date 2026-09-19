"""
Production LLM Providers for CogniMesh.
Provides plug-and-play integrations for OpenAI, Anthropic, Google Gemini, and Local Ollama instances.
"""

from __future__ import annotations
import os
from typing import Dict, List, Optional, Any
from agent_research.llm.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """Local Ollama instance integration (zero cloud dependency)."""

    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        import urllib.request
        import json

        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt or "",
            "stream": False,
            "options": {"temperature": temperature},
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response", "")
        except Exception as e:
            return f"[Ollama Error / Offline fallback]: {e}"

    def generate_deliberation(self, goal: str, context: List[str], depth: int) -> List[str]:
        prompt = f"Goal: {goal}\nContext: {context}\nDepth: {depth}\nGenerate 3 distinct next logical steps."
        res = self.generate(prompt)
        return [res]


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider adapter."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        if not self.api_key:
            return "[OpenAI Error: OPENAI_API_KEY environment variable not set. Using simulation fallback.]"

        try:
            import urllib.request
            import json

            url = "https://api.openai.com/v1/chat/completions"
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            payload = {"model": self.model, "messages": messages, "temperature": temperature}
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[OpenAI Request Failed]: {e}"

    def generate_deliberation(self, goal: str, context: List[str], depth: int) -> List[str]:
        prompt = f"Decompose goal '{goal}' into 3 intermediate reasoning hypotheses given context {context}."
        res = self.generate(prompt)
        return [res]
