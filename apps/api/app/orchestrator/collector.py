import asyncio

from app.providers.base import LLMProvider, ModelResponse


async def collect_responses(
    providers: list[LLMProvider],
    prompt: str,
    provider_manager=None,
) -> tuple[list[ModelResponse], list[dict]]:
    tasks = [
        provider.generate(prompt)
        for provider in providers
    ]

    results = await asyncio.gather(
        *tasks,
        return_exceptions=True,
    )

    responses: list[ModelResponse] = []
    errors: list[dict] = []

    for provider, result in zip(providers, results):
        if isinstance(result, Exception):
            error_type = type(result).__name__
            error_message = str(result)

            print(
                f"Provider request failed: "
                f"{provider.__class__.__name__}: "
                f"{error_type}: {error_message}"
            )

            if provider_manager is not None:
                provider_manager.mark_provider_failed(
                    provider,
                    result,
                )

            errors.append(
                {
                    "provider": provider.__class__.__name__,
                    "error_type": error_type,
                    "message": error_message,
                }
            )

            continue

        responses.append(result)

    return responses, errors