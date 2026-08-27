import asyncio

from app.orchestrator.engine import NexverityEngine


async def main():
    engine = NexverityEngine()

    result = await engine.process(
        "In one short paragraph, explain what artificial intelligence is."
    )

    print("\n--- NEXVERITY ENGINE TEST ---")

    # Final status
    print("Final Status:", result["status"])

    # Final synthesized answer
    if "final_answer" in result:
        print("\n--- FINAL ANSWER ---")
        print(result["final_answer"])

    # Final agreement score
    if "agreement_score" in result:
        print(
            "\nFinal Agreement Score:",
            result["agreement_score"],
            "%",
        )

    # Verification threshold
    if "threshold" in result:
        print(
            "Threshold:",
            result["threshold"],
            "%",
        )

    # Verification rounds
    print("\n--- ROUNDS ---")

    for round_result in result.get("rounds", []):
        print(
            f"\nRound {round_result['round']}"
        )

        print(
            "Agreement:",
            round_result["agreement_score"],
            "%",
        )

        print(
            "Decision:",
            round_result["decision"],
        )

        # Provider comparisons
        for comparison in round_result.get(
            "comparisons",
            []
        ):
            print(
                f"{comparison['provider_a']} ↔ "
                f"{comparison['provider_b']}: "
                f"{comparison['score']}%"
            )

    # Optional message from the engine
    if "message" in result:
        print("\nMessage:")
        print(result["message"])


if __name__ == "__main__":
    asyncio.run(main())