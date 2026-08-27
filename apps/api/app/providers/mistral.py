import time

from mistralai.client import Mistral

from app.config import MISTRAL_API_KEY
from app.providers.base import LLMProvider, ModelResponse


class MistralProvider(LLMProvider):
    """
    Mistral AI provider for NEXVERITY.
    """

    def __init__(self, model: str):
        if not MISTRAL_API_KEY:
            raise ValueError(
                "MISTRAL_API_KEY is not configured."
            )

        self.model = model

        self.client = Mistral(
            api_key=MISTRAL_API_KEY,
        )

    async def generate(
        self,
        prompt: str,
    ) -> ModelResponse:
        start_time = time.perf_counter()

        response = await self.client.chat.complete_async(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        latency_ms = (
            time.perf_counter()
            - start_time
        ) * 1000

        message = (
            response.choices[0].message
        )

        answer = message.content or ""

        usage = getattr(
            response,
            "usage",
            None,
        )

        return ModelResponse(
            provider="mistral",
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

    async def health_check(
        self,
    ) -> bool:
        try:
            response = (
                await self.client.chat.complete_async(
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
                response.choices
                and response.choices[0].message.content
            )

        except Exception:
            return False