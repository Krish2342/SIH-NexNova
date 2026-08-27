from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ModelResponse:
    provider: str
    model: str
    answer: str
    latency_ms: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None


class LLMProvider(ABC):
    """Base interface that every NEXVERITY AI provider must implement."""

    @abstractmethod
    async def generate(self, prompt: str) -> ModelResponse:
        """Generate an answer from the AI provider."""
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """Check whether the provider is available."""
        raise NotImplementedError