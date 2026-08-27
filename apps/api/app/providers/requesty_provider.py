import time

from openai import AsyncOpenAI

from app.config import (
    REQUESTY_API_KEY,
    REQUESTY_MODEL,
)
from app.providers.base import (
    LLMProvider,
    ModelResponse,
)


class RequestyProvider(LLMProvider):
    """
    Requesty AI Gateway provider.

    Requesty exposes an OpenAI-compatible API, so we can
    use the official OpenAI Python SDK with Requesty's
    base URL.
    """

    BASE_URL = "https://router.requesty.ai/v1"

    def __init__(self, model: str):
        if not REQUESTY_API_KEY:
            raise ValueError(
                "REQUESTY_API_KEY is not configured."
            )

        self.model = model

        self.client = AsyncOpenAI(
            api_key=REQUESTY_API_KEY,
            base_url=self.BASE_URL,
        )

    async def generate(
        self,
        prompt: str,
    ) -> ModelResponse:

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

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        usage = response.usage

        answer = (
            response.choices[0].message.content
            or ""
        )

        return ModelResponse(
            provider="requesty",
            model=self.model,
            answer=answer,
            latency_ms=round(
                latency_ms,
                2,
            ),
            input_tokens=getattr(
                usage,
                "prompt_tokens",
                None,
            ),
            output_tokens=getattr(
                usage,
                "completion_tokens",
                None,
            ),
        )

    async def health_check(self) -> bool:
        try:
            response = (
                await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": "Respond with OK.",
                        }
                    ],
                )
            )

            return bool(
                response.choices[0].message.content
            )

        except Exception:
            return False