import re

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


class ComparisonEngine:
    """
    NEXVERITY semantic agreement engine.

    Returns an agreement score from 0 to 100.

    The comparison is designed for short and long answers.
    It does not require both models to use the same wording,
    sentence structure, examples, or answer length.

    Strategy:

        1. Whole-answer semantic similarity
        2. Sentence-level semantic coverage
        3. Strong sentence-match coverage

    The whole-answer score is intentionally important because
    two long answers can discuss the same concepts using
    different sentence structures.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        sentence_match_threshold: float = 0.40,
        strong_match_threshold: float = 0.65,
    ):
        self.model = SentenceTransformer(
            model_name
        )

        self.sentence_match_threshold = (
            sentence_match_threshold
        )

        self.strong_match_threshold = (
            strong_match_threshold
        )

    # =========================================================
    # TEXT CLEANING
    # =========================================================

    @staticmethod
    def _clean_text(
        text: str,
    ) -> str:
        """
        Remove formatting noise without removing the actual
        natural-language content.
        """

        if not text:
            return ""

        # Remove fenced code blocks.
        text = re.sub(
            r"```.*?```",
            " ",
            text,
            flags=re.DOTALL,
        )

        lines = text.splitlines()

        cleaned_lines = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Markdown table separator.
            if re.fullmatch(
                r"\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?",
                line,
            ):
                continue

            # Remove table formatting but KEEP the content.
            if (
                line.startswith("|")
                and line.endswith("|")
            ):
                cells = [
                    cell.strip()
                    for cell in line.strip("|").split("|")
                ]

                cells = [
                    cell
                    for cell in cells
                    if cell
                ]

                if cells:
                    cleaned_lines.append(
                        ". ".join(cells)
                    )

                continue

            # Remove headings.
            line = re.sub(
                r"^#{1,6}\s+",
                "",
                line,
            )

            # Remove bullet markers.
            line = re.sub(
                r"^[-*+]\s+",
                "",
                line,
            )

            # Remove numbered list markers.
            line = re.sub(
                r"^\d+[.)]\s+",
                "",
                line,
            )

            # Remove blockquote markers.
            line = re.sub(
                r"^>\s*",
                "",
                line,
            )

            # Remove Markdown emphasis.
            line = re.sub(
                r"[*_~`]+",
                "",
                line,
            )

            if line:
                cleaned_lines.append(
                    line
                )

        text = " ".join(
            cleaned_lines
        )

        # Normalize whitespace.
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # =========================================================
    # SENTENCE SPLITTING
    # =========================================================

    @classmethod
    def _split_sentences(
        cls,
        text: str,
    ) -> list[str]:
        """
        Split text into meaningful sentences.
        """

        text = cls._clean_text(
            text
        )

        if not text:
            return []

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        result = []

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            if len(sentence) < 20:
                continue

            if len(sentence) > 600:
                continue

            if len(sentence.split()) < 4:
                continue

            result.append(
                sentence
            )

        return result

    # =========================================================
    # NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize(
        text: str,
    ) -> str:
        """
        Normalize text for duplicate detection.
        """

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # =========================================================
    # UNIQUE SENTENCES
    # =========================================================

    @classmethod
    def _unique_sentences(
        cls,
        sentences: list[str],
    ) -> list[str]:
        """
        Remove duplicate sentences.
        """

        result = []

        seen = set()

        for sentence in sentences:

            normalized = cls._normalize(
                sentence
            )

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(
                normalized
            )

            result.append(
                sentence
            )

        return result

    # =========================================================
    # WHOLE ANSWER SCORE
    # =========================================================

    def _whole_answer_similarity(
        self,
        answer_a: str,
        answer_b: str,
    ) -> float:
        """
        Calculate overall semantic similarity.

        This is especially useful for long technical answers
        where the models discuss the same concepts but use
        different sentence structures.
        """

        embeddings = self.model.encode(
            [
                answer_a,
                answer_b,
            ],
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        similarity = float(
            cos_sim(
                embeddings[0],
                embeddings[1],
            ).item()
        )

        return max(
            0.0,
            min(
                1.0,
                similarity,
            ),
        )

    # =========================================================
    # BEST MATCH
    # =========================================================

    @staticmethod
    def _best_matches(
        matrix,
    ) -> list[float]:
        """
        Find the best semantic match for each sentence.
        """

        if matrix.numel() == 0:
            return []

        values = matrix.max(
            dim=1
        ).values

        return [
            float(value.item())
            for value in values
        ]

    # =========================================================
    # SENTENCE COVERAGE
    # =========================================================

    def _sentence_coverage(
        self,
        similarities: list[float],
    ) -> float:
        """
        Calculate sentence-level semantic coverage.

        A sentence that has a strong semantic counterpart
        receives high credit.

        An additional sentence in one answer does not
        automatically mean disagreement.
        """

        if not similarities:
            return 0.0

        scores = []

        for similarity in similarities:

            if (
                similarity
                >= self.strong_match_threshold
            ):
                # Strong match.
                score = similarity

            elif (
                similarity
                >= self.sentence_match_threshold
            ):
                # Partial semantic match.
                ratio = (
                    similarity
                    - self.sentence_match_threshold
                ) / (
                    self.strong_match_threshold
                    - self.sentence_match_threshold
                )

                score = (
                    0.55
                    + (ratio * 0.45)
                )

            else:
                # Weakly related / unmatched sentence.
                #
                # Give a small amount of credit instead
                # of treating it as direct disagreement.
                score = 0.15

            scores.append(
                max(
                    0.0,
                    min(
                        1.0,
                        score,
                    ),
                )
            )

        return (
            sum(scores)
            / len(scores)
        )

    # =========================================================
    # STRONG MATCH COVERAGE
    # =========================================================

    def _strong_match_coverage(
        self,
        similarities: list[float],
    ) -> float:
        """
        Percentage of sentences that have a strong
        semantic counterpart.
        """

        if not similarities:
            return 0.0

        strong = sum(
            1
            for similarity in similarities
            if similarity
            >= self.strong_match_threshold
        )

        return (
            strong
            / len(similarities)
        )

    # =========================================================
    # MAIN COMPARISON
    # =========================================================

    def compare(
        self,
        answer_a: str,
        answer_b: str,
    ) -> float:
        """
        Compare two model answers.

        Returns:
            float:
                Agreement percentage from 0 to 100.
        """

        # -----------------------------------------------------
        # Empty-answer protection.
        # -----------------------------------------------------

        if not answer_a or not answer_b:
            return 0.0

        answer_a = self._clean_text(
            answer_a
        )

        answer_b = self._clean_text(
            answer_b
        )

        if not answer_a or not answer_b:
            return 0.0

        # -----------------------------------------------------
        # Whole-answer semantic similarity.
        # -----------------------------------------------------

        whole_score = (
            self._whole_answer_similarity(
                answer_a,
                answer_b,
            )
        )

        # -----------------------------------------------------
        # Sentence extraction.
        # -----------------------------------------------------

        sentences_a = (
            self._unique_sentences(
                self._split_sentences(
                    answer_a
                )
            )
        )

        sentences_b = (
            self._unique_sentences(
                self._split_sentences(
                    answer_b
                )
            )
        )

        # -----------------------------------------------------
        # If either answer cannot be split reliably,
        # use whole-answer similarity.
        # -----------------------------------------------------

        if (
            not sentences_a
            or not sentences_b
        ):
            return round(
                whole_score * 100.0,
                2,
            )

        # -----------------------------------------------------
        # Sentence embeddings.
        # -----------------------------------------------------

        embeddings_a = self.model.encode(
            sentences_a,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        embeddings_b = self.model.encode(
            sentences_b,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        # -----------------------------------------------------
        # Similarity matrix.
        # -----------------------------------------------------

        matrix = cos_sim(
            embeddings_a,
            embeddings_b,
        )

        # -----------------------------------------------------
        # A → B.
        # -----------------------------------------------------

        best_a = self._best_matches(
            matrix
        )

        # -----------------------------------------------------
        # B → A.
        # -----------------------------------------------------

        best_b = self._best_matches(
            matrix.transpose(
                0,
                1,
            )
        )

        # -----------------------------------------------------
        # Sentence-level semantic coverage.
        # -----------------------------------------------------

        coverage_a = (
            self._sentence_coverage(
                best_a
            )
        )

        coverage_b = (
            self._sentence_coverage(
                best_b
            )
        )

        sentence_coverage = (
            coverage_a
            + coverage_b
        ) / 2.0

        # -----------------------------------------------------
        # Strong semantic coverage.
        # -----------------------------------------------------

        strong_a = (
            self._strong_match_coverage(
                best_a
            )
        )

        strong_b = (
            self._strong_match_coverage(
                best_b
            )
        )

        strong_coverage = (
            strong_a
            + strong_b
        ) / 2.0

        # -----------------------------------------------------
        # Final agreement.
        #
        # Whole answer:
        #     50%
        #
        # Sentence coverage:
        #     35%
        #
        # Strong matches:
        #     15%
        #
        # This prevents long answers from receiving a
        # terrible score simply because their individual
        # sentences are phrased differently.
        # -----------------------------------------------------

        final_score = (
            whole_score * 0.50
            + sentence_coverage * 0.35
            + strong_coverage * 0.15
        )

        # -----------------------------------------------------
        # Numerical safety.
        # -----------------------------------------------------

        final_score = max(
            0.0,
            min(
                1.0,
                final_score,
            ),
        )

        # -----------------------------------------------------
        # IMPORTANT:
        #
        # NEXVERITY uses a 0–100 agreement scale.
        # -----------------------------------------------------

        return round(
            final_score * 100.0,
            2,
        )