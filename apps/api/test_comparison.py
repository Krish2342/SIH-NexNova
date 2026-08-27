import asyncio

from app.orchestrator.collector import collect_responses
from app.orchestrator.comparison import ComparisonEngine
from app.orchestrator.manager import ProviderManager


async def main():
    manager = ProviderManager()

    providers = await manager.get_available_providers()

    responses = await collect_responses(
        providers,
        "In one short paragraph, explain what artificial intelligence is.",
    )

    print("\n--- NEXVERITY COMPARISON TEST ---")

    if len(responses) < 2:
        print("Need at least two successful responses.")
        return

    answer_a = responses[0]
    answer_b = responses[1]

    comparison = ComparisonEngine()

    similarity = comparison.compare(
        answer_a.answer,
        answer_b.answer,
    )

    print("\nProvider A:", answer_a.provider)
    print("Provider B:", answer_b.provider)

    print("\nAnswer A:")
    print(answer_a.answer)

    print("\nAnswer B:")
    print(answer_b.answer)

    print("\nSemantic Similarity:", similarity, "%")


if __name__ == "__main__":
    asyncio.run(main())