from app.config import AGREEMENT_THRESHOLD
from app.orchestrator.decision import DecisionEngine


def main():
    engine = DecisionEngine()

    print("\n--- NEXVERITY DECISION TEST ---")
    print("Threshold:", AGREEMENT_THRESHOLD)

    test_scores = [92.8, 85.0, 84.9, 72.4]

    for score in test_scores:
        decision = engine.evaluate(score)

        print(
            f"Score: {score}% "
            f"→ Decision: {decision}"
        )


if __name__ == "__main__":
    main()