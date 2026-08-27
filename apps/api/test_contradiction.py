from app.orchestrator.contradiction import ContradictionEngine


def run_test(
    engine: ContradictionEngine,
    answer_a: str,
    answer_b: str,
) -> None:

    print()
    print("A:", answer_a)
    print("B:", answer_b)

    result = engine.compare(
        answer_a,
        answer_b,
    )

    print(
        "Contradiction:",
        result["contradiction"],
    )

    print(
        "Checked pairs:",
        result["checked_pairs"],
    )

    print(
        "Strongest contradiction score:",
        result["strongest_score"],
    )

    if result["evidence"]:
        evidence = result["evidence"]

        print()
        print("Contradiction evidence:")

        print(
            "Sentence A:",
            evidence["sentence_a"],
        )

        print(
            "Sentence B:",
            evidence["sentence_b"],
        )

        print(
            "Forward label:",
            evidence["forward_label"],
        )

        print(
            "Reverse label:",
            evidence["reverse_label"],
        )

        print(
            "Forward scores:",
            evidence["forward_scores"],
        )

        print(
            "Reverse scores:",
            evidence["reverse_scores"],
        )

        print(
            "Contradiction score:",
            evidence["contradiction_score"],
        )


def main():
    print()
    print("--- NEXVERITY CONTRADICTION TEST ---")

    engine = ContradictionEngine()

    # -------------------------------------------------
    # TEST 1: IDENTICAL STATEMENTS
    # -------------------------------------------------

    run_test(
        engine,
        "The Earth has one natural moon.",
        "The Earth has one natural moon.",
    )

    # -------------------------------------------------
    # TEST 2: DIRECT CONTRADICTION
    # -------------------------------------------------

    run_test(
        engine,
        "The Earth has one natural moon.",
        "The Earth has two natural moons.",
    )

    # -------------------------------------------------
    # TEST 3: RELATED BUT NOT CONTRADICTORY
    # -------------------------------------------------

    run_test(
        engine,
        "Artificial intelligence can learn from data.",
        "Machine learning systems can learn patterns from data.",
    )


if __name__ == "__main__":
    main()