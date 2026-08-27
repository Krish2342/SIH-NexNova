import time

from openai import AsyncOpenAI

from app.config import GROQ_API_KEY
from app.providers.base import LLMProvider, ModelResponse


class GroqProvider(LLMProvider):
    def __init__(self, model: str):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.model = model

        self.client = AsyncOpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

    async def generate(self, prompt: str) -> ModelResponse:
        start_time = time.perf_counter()

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        latency_ms = (time.perf_counter() - start_time) * 1000

        usage = response.usage

        return ModelResponse(
            provider="groq",
            model=self.model,
            answer=response.choices[0].message.content or "",
            latency_ms=round(latency_ms, 2),
            input_tokens=getattr(usage, "prompt_tokens", None),
            output_tokens=getattr(usage, "completion_tokens", None),
        )

    async def health_check(self) -> bool:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Respond with OK.",
                    }
                ],
            )

            return bool(response.choices[0].message.content)

        except Exception:
            return False