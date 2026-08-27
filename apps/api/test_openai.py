import asyncio

from app.config import OPENAI_MODEL
from app.providers.openai_provider import OpenAIProvider


async def main():
    provider = OpenAIProvider(model=OPENAI_MODEL)

    response = await provider.generate(
        "In one short sentence, explain what artificial intelligence is."
    )

    print("\n--- NEXVERITY OPENAI TEST ---")
    print("Provider:", response.provider)
    print("Model:", response.model)
    print("Answer:", response.answer)
    print("Latency:", response.latency_ms, "ms")
    print("Input tokens:", response.input_tokens)
    print("Output tokens:", response.output_tokens)


if __name__ == "__main__":
    asyncio.run(main())