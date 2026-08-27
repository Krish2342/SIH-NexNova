from app.config import AGREEMENT_THRESHOLD


class DecisionEngine:
    def __init__(self, threshold: float = AGREEMENT_THRESHOLD):
        self.threshold = threshold

    def evaluate(self, similarity_score: float) -> str:
        if similarity_score >= self.threshold:
            return "PASS"

        return "REGENERATE"