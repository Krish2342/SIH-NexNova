import time

import httpx

from app.config import (
    CLOUDFLARE_API_TOKEN,
    CLOUDFLARE_ACCOUNT_ID,
)
from app.providers.base import (
    LLMProvider,
    ModelResponse,
)


class CloudflareProvider(LLMProvider):
    """
    Cloudflare Workers AI provider for NEXVERITY.

    Uses Cloudflare's OpenAI-compatible chat-completions
    endpoint.

    Workers AI models use the @cf/ model prefix.
    """

    def __init__(
        self,
        model: str,
    ):
        if not CLOUDFLARE_API_TOKEN:
            raise ValueError(
                "CLOUDFLARE_API_TOKEN "
                "is not configured."
            )

        if not CLOUDFLARE_ACCOUNT_ID:
            raise ValueError(
                "CLOUDFLARE_ACCOUNT_ID "
                "is not configured."
            )

        self.model = model

        self.base_url = (
            "https://api.cloudflare.com/client/v4/"
            f"accounts/{CLOUDFLARE_ACCOUNT_ID}"
            "/ai/v1"
        )

        self.client = httpx.AsyncClient(
            timeout=60.0,
            headers={
                "Authorization": (
                    f"Bearer {CLOUDFLARE_API_TOKEN}"
                ),
                "Content-Type": (
                    "application/json"
                ),
            },
        )

    async def generate(
        self,
        prompt: str,
    ) -> ModelResponse:
        """
        Generate an answer using Cloudflare Workers AI.
        """

        start_time = time.perf_counter()

        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            },
        )

        response.raise_for_status()

        data = response.json()

        latency_ms = (
            time.perf_counter()
            - start_time
        ) * 1000

        # -----------------------------------------------------
        # Cloudflare response validation
        # -----------------------------------------------------

        if not data.get("success", True):
            errors = data.get(
                "errors",
                [],
            )

            raise RuntimeError(
                "Cloudflare API request failed: "
                f"{errors}"
            )

        choices = data.get(
            "choices",
            [],
        )

        if not choices:
            raise RuntimeError(
                "Cloudflare returned no choices."
            )

        message = choices[0].get(
            "message",
            {},
        )

        answer = message.get(
            "content",
            "",
        )

        # -----------------------------------------------------
        # Usage
        # -----------------------------------------------------

        usage = data.get(
            "usage",
            {},
        )

        return ModelResponse(
            provider="cloudflare",
            model=self.model,
            answer=answer or "",
            latency_ms=round(
                latency_ms,
                2,
            ),
            input_tokens=usage.get(
                "prompt_tokens"
            ),
            output_tokens=usage.get(
                "completion_tokens"
            ),
        )

    async def health_check(
        self,
    ) -> bool:
        """
        Check whether Cloudflare Workers AI is responding.
        """

        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                "Respond with OK."
                            ),
                        }
                    ],
                    "max_tokens": 10,
                },
            )

            if response.status_code != 200:
                return False

            data = response.json()

            return bool(
                data.get("choices")
            )

        except Exception:
            return False

    async def close(self):
        """
        Close the underlying HTTP client.
        """

        await self.client.aclose()