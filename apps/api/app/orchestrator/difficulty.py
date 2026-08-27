from enum import Enum


class Difficulty(str, Enum):
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"


class DifficultyEngine:
    """
    Classifies a question into an approximate difficulty level
    and determines how many providers should be used.
    """

    EASY_PROVIDER_COUNT = 2
    MODERATE_PROVIDER_COUNT = 4

    def classify(self, question: str) -> Difficulty:
        question = question.strip()

        score = 0

        # -----------------------------------------------------
        # Length / structural complexity
        # -----------------------------------------------------

        words = question.split()
        word_count = len(words)

        if word_count <= 12:
            score += 0

        elif word_count <= 30:
            score += 1

        else:
            score += 2

        # -----------------------------------------------------
        # Multi-part questions
        # -----------------------------------------------------

        if "?" in question[:-1]:
            score += 1

        conjunctions = [
            " and ",
            " versus ",
            " vs ",
            " compared to ",
            "compare ",
            "difference between ",
        ]

        for term in conjunctions:
            if term in question.lower():
                score += 1
                break

        # -----------------------------------------------------
        # Reasoning / analysis indicators
        # -----------------------------------------------------

        reasoning_terms = [
            "why",
            "how",
            "explain",
            "analyze",
            "analysis",
            "evaluate",
            "assess",
            "reason",
            "reasoning",
            "justify",
            "implications",
            "consequences",
            "trade-off",
            "tradeoff",
            "pros and cons",
            "advantages",
            "disadvantages",
        ]

        lower_question = question.lower()

        reasoning_matches = sum(
            1
            for term in reasoning_terms
            if term in lower_question
        )

        score += min(reasoning_matches, 3)

        # -----------------------------------------------------
        # Complex / technical indicators
        # -----------------------------------------------------

        complex_terms = [
            "algorithm",
            "architecture",
            "distributed",
            "statistical",
            "probability",
            "optimization",
            "mathematical",
            "mathematics",
            "physics",
            "quantum",
            "machine learning",
            "neural network",
            "economics",
            "economic",
            "legal",
            "law",
            "medical",
            "scientific",
            "research",
            "experiment",
            "proof",
            "derive",
            "calculate",
        ]

        complex_matches = sum(
            1
            for term in complex_terms
            if term in lower_question
        )

        score += min(complex_matches, 3)

        # -----------------------------------------------------
        # Explicit multi-step requests
        # -----------------------------------------------------

        multi_step_terms = [
            "step by step",
            "step-by-step",
            "in detail",
            "detailed explanation",
            "deep dive",
            "comprehensive",
            "thoroughly",
            "multiple factors",
            "from first principles",
        ]

        if any(
            term in lower_question
            for term in multi_step_terms
        ):
            score += 2

        # -----------------------------------------------------
        # Final classification
        # -----------------------------------------------------

        if score <= 1:
            return Difficulty.EASY

        if score <= 4:
            return Difficulty.MODERATE

        return Difficulty.HARD

    def provider_count(
        self,
        difficulty: Difficulty,
        available_count: int,
    ) -> int:
        """
        Determine how many providers should be used.

        The requested number is always capped by the number
        of providers currently available.
        """

        if available_count <= 0:
            return 0

        if difficulty == Difficulty.EASY:
            requested = self.EASY_PROVIDER_COUNT

        elif difficulty == Difficulty.MODERATE:
            requested = self.MODERATE_PROVIDER_COUNT

        else:
            requested = available_count

        return min(
            requested,
            available_count,
        )