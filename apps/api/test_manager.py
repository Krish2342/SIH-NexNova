import asyncio

from app.orchestrator.manager import ProviderManager


async def main():
    manager = ProviderManager()

    providers = await manager.get_available_providers()

    print("\n--- NEXVERITY PROVIDER MANAGER ---")

    if not providers:
        print("No providers available.")
        return

    for provider in providers:
        print(
            f"Provider: {provider.__class__.__name__} | "
            f"Model: {provider.model}"
        )


if __name__ == "__main__":
    asyncio.run(main())