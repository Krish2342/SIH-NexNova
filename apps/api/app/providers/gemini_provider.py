import time

from google import genai

from app.config import GEMINI_API_KEY
from app.providers.base import LLMProvider, ModelResponse


class GeminiProvider(LLMProvider):
    def __init__(self, model: str):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    async def generate(self, prompt: str) -> ModelResponse:
        start_time = time.perf_counter()

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        latency_ms = (time.perf_counter() - start_time) * 1000

        usage = getattr(response, "usage_metadata", None)

        input_tokens = getattr(
            usage,
            "prompt_token_count",
            None,
        )

        output_tokens = getattr(
            usage,
            "candidates_token_count",
            None,
        )

        return ModelResponse(
            provider="gemini",
            model=self.model,
            answer=response.text or "",
            latency_ms=round(latency_ms, 2),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

    async def health_check(self) -> bool:
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents="Respond with OK.",
            )

            return bool(response.text)

        except Exception:
            return False