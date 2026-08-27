import time

from openai import AsyncOpenAI

from app.config import OPENAI_API_KEY
from app.providers.base import LLMProvider, ModelResponse


class OpenAIProvider(LLMProvider):
    def __init__(self, model: str):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")

        self.model = model
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate(self, prompt: str) -> ModelResponse:
        start_time = time.perf_counter()

        response = await self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        latency_ms = (time.perf_counter() - start_time) * 1000

        usage = response.usage

        return ModelResponse(
            provider="openai",
            model=self.model,
            answer=response.output_text,
            latency_ms=round(latency_ms, 2),
            input_tokens=getattr(usage, "input_tokens", None),
            output_tokens=getattr(usage, "output_tokens", None),
        )

    async def health_check(self) -> bool:
        try:
            response = await self.client.responses.create(
                model=self.model,
                input="Respond with OK.",
            )

            return bool(response.output_text)

        except Exception:
            return False