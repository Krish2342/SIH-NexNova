import time

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    REQUESTY_API_KEY,
    REQUESTY_MODEL,
    MISTRAL_API_KEY,
    MISTRAL_MODEL,
    CLOUDFLARE_API_TOKEN,
    CLOUDFLARE_ACCOUNT_ID,
    CLOUDFLARE_MODEL,
)

from app.providers.base import LLMProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.groq_provider import GroqProvider
from app.providers.openrouter_provider import OpenRouterProvider
from app.providers.requesty_provider import RequestyProvider
from app.providers.mistral import MistralProvider
from app.providers.cloudflare_provider import CloudflareProvider


class ProviderManager:
    """
    Manages all configured NEXVERITY AI providers.

    Responsibilities:
    - Initialize configured providers.
    - Track provider cooldowns.
    - Temporarily disable rate-limited providers.
    - Return currently available providers.
    """

    COOLDOWN_SECONDS = 60

    def __init__(self):
        self.providers: list[LLMProvider] = []

        self.cooldowns: dict[
            LLMProvider,
            float,
        ] = {}

        # -----------------------------------------------------
        # Gemini
        # -----------------------------------------------------

        if GEMINI_API_KEY:
            self.providers.append(
                GeminiProvider(
                    model=GEMINI_MODEL
                )
            )

        # -----------------------------------------------------
        # Groq
        # -----------------------------------------------------

        if GROQ_API_KEY:
            self.providers.append(
                GroqProvider(
                    model=GROQ_MODEL
                )
            )

        # -----------------------------------------------------
        # OpenRouter
        # -----------------------------------------------------

        if OPENROUTER_API_KEY:
            self.providers.append(
                OpenRouterProvider(
                    model=OPENROUTER_MODEL
                )
            )

        # -----------------------------------------------------
        # Requesty
        # -----------------------------------------------------

        if REQUESTY_API_KEY:
            self.providers.append(
                RequestyProvider(
                    model=REQUESTY_MODEL
                )
            )

        # -----------------------------------------------------
        # Mistral
        # -----------------------------------------------------

        if MISTRAL_API_KEY:
            self.providers.append(
                MistralProvider(
                    model=MISTRAL_MODEL
                )
            )

        # -----------------------------------------------------
        # Cloudflare Workers AI
        # -----------------------------------------------------

        if (
            CLOUDFLARE_API_TOKEN
            and CLOUDFLARE_ACCOUNT_ID
        ):
            self.providers.append(
                CloudflareProvider(
                    model=CLOUDFLARE_MODEL
                )
            )

        # -----------------------------------------------------
        # Startup information
        # -----------------------------------------------------

        print(
            "NEXVERITY providers initialized:",
            [
                provider.__class__.__name__
                for provider in self.providers
            ],
        )

    # =========================================================
    # COOLDOWN
    # =========================================================

    def _is_in_cooldown(
        self,
        provider: LLMProvider,
    ) -> bool:
        """
        Check whether a provider is currently in cooldown.

        If the cooldown has expired, remove it and make the
        provider available again.
        """

        cooldown_until = self.cooldowns.get(
            provider
        )

        if cooldown_until is None:
            return False

        if time.monotonic() >= cooldown_until:
            del self.cooldowns[provider]

            print(
                f"Provider cooldown expired: "
                f"{provider.__class__.__name__}"
            )

            return False

        return True

    # =========================================================
    # MARK PROVIDER FAILED
    # =========================================================

    def mark_provider_failed(
        self,
        provider: LLMProvider,
        error: Exception,
    ) -> None:
        """
        Temporarily disable a provider after a rate-limit
        or quota-related failure.
        """

        error_text = str(error).upper()

        is_rate_limited = (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "RATE LIMIT" in error_text
            or "RATE_LIMIT" in error_text
            or "QUOTA" in error_text
            or "TOO MANY REQUESTS" in error_text
        )

        if not is_rate_limited:
            return

        self.cooldowns[provider] = (
            time.monotonic()
            + self.COOLDOWN_SECONDS
        )

        print(
            f"Provider cooldown activated: "
            f"{provider.__class__.__name__} "
            f"for {self.COOLDOWN_SECONDS}s"
        )

    # =========================================================
    # AVAILABLE PROVIDERS
    # =========================================================

    async def get_available_providers(
        self,
    ) -> list[LLMProvider]:
        """
        Return all providers that are currently available.
        """

        available: list[LLMProvider] = []

        for provider in self.providers:
            if not self._is_in_cooldown(
                provider
            ):
                available.append(provider)

        return available

    # =========================================================
    # AVAILABLE PROVIDER COUNT
    # =========================================================

    async def get_available_provider_count(
        self,
    ) -> int:
        """
        Return the number of currently available providers.
        """

        providers = (
            await self.get_available_providers()
        )

        return len(providers)

    # =========================================================
    # PROVIDER STATUS
    # =========================================================

    async def get_provider_status(
        self,
    ) -> list[dict]:
        """
        Return the current status of every configured provider.
        """

        status: list[dict] = []

        for provider in self.providers:

            in_cooldown = (
                self._is_in_cooldown(
                    provider
                )
            )

            cooldown_until = (
                self.cooldowns.get(
                    provider
                )
            )

            remaining_seconds = 0

            if cooldown_until is not None:
                remaining_seconds = max(
                    0,
                    round(
                        cooldown_until
                        - time.monotonic()
                    ),
                )

            status.append(
                {
                    "provider": (
                        provider.__class__.__name__
                    ),
                    "available": (
                        not in_cooldown
                    ),
                    "cooldown_seconds": (
                        remaining_seconds
                    ),
                }
            )

        return status