import asyncio

from app.orchestrator.collector import collect_responses
from app.orchestrator.manager import ProviderManager


async def main():
    manager = ProviderManager()

    providers = await manager.get_available_providers()

    print("\n--- NEXVERITY PARALLEL TEST ---")
    print("Available providers:", len(providers))

    responses = await collect_responses(
        providers,
        "In one short paragraph, explain what artificial intelligence is.",
    )

    print("\n--- RESPONSES ---")

    for response in responses:
        print("\nProvider:", response.provider)
        print("Model:", response.model)
        print("Answer:", response.answer)
        print("Latency:", response.latency_ms, "ms")
        print("Input tokens:", response.input_tokens)
        print("Output tokens:", response.output_tokens)


if __name__ == "__main__":
    asyncio.run(main())