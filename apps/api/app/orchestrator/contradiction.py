import re

import numpy as np

from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
from sentence_transformers.util import cos_sim


class ContradictionEngine:
    """
    Conservative contradiction detector for NEXVERITY.

    Pipeline:

        Answer A / Answer B
                ↓
        Clean Markdown
                ↓
        Split into meaningful sentences
                ↓
        Semantic relevance filtering
                ↓
        Bidirectional NLI
                ↓
        Conservative contradiction decision

    NLI labels:

        0 = contradiction
        1 = entailment
        2 = neutral

    Important:
        NLI is NOT run against arbitrary sentence pairs.

        Two sentences must first be semantically related.
        This prevents unrelated statements from being
        incorrectly classified as contradictions.
    """

    def __init__(
        self,
        model_name: str = (
            "cross-encoder/nli-MiniLM2-L6-H768"
        ),
        embedding_model_name: str = (
            "all-MiniLM-L6-v2"
        ),
        contradiction_threshold: float = 0.88,
        similarity_threshold: float = 0.58,
        margin_threshold: float = 0.30,
    ):
        self.model = CrossEncoder(
            model_name
        )

        self.embedding_model = (
            SentenceTransformer(
                embedding_model_name
            )
        )

        self.contradiction_threshold = (
            contradiction_threshold
        )

        self.similarity_threshold = (
            similarity_threshold
        )

        self.margin_threshold = (
            margin_threshold
        )

    # =========================================================
    # MARKDOWN CLEANING
    # =========================================================

    @staticmethod
    def _clean_markdown(
        text: str,
    ) -> str:
        """
        Remove Markdown formatting while preserving useful
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

            stripped = line.strip()

            if not stripped:
                continue

            # -------------------------------------------------
            # Remove Markdown table separator rows.
            # -------------------------------------------------

            if re.fullmatch(
                r"\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?",
                stripped,
            ):
                continue

            # -------------------------------------------------
            # Convert table rows into normal text.
            #
            # We don't feed raw "|" formatting into NLI.
            # -------------------------------------------------

            if (
                stripped.startswith("|")
                and stripped.endswith("|")
            ):
                cells = [
                    cell.strip()
                    for cell in stripped.strip(
                        "|"
                    ).split("|")
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

            # Remove Markdown headings.
            stripped = re.sub(
                r"^#{1,6}\s+",
                "",
                stripped,
            )

            # Remove bullet markers.
            stripped = re.sub(
                r"^[-*+]\s+",
                "",
                stripped,
            )

            # Remove numbered-list markers.
            stripped = re.sub(
                r"^\d+[.)]\s+",
                "",
                stripped,
            )

            # Remove blockquotes.
            stripped = re.sub(
                r"^>\s*",
                "",
                stripped,
            )

            # Remove emphasis.
            stripped = re.sub(
                r"[*_~`]+",
                "",
                stripped,
            )

            if stripped:
                cleaned_lines.append(
                    stripped
                )

        text = " ".join(
            cleaned_lines
        )

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
        Extract meaningful natural-language sentences.
        """

        if not text:
            return []

        text = cls._clean_markdown(
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

            # Ignore tiny fragments.
            if len(sentence) < 25:
                continue

            # Avoid giant blocks.
            if len(sentence) > 600:
                continue

            # Require a meaningful number of words.
            if len(sentence.split()) < 5:
                continue

            # Ignore obvious labels.
            if sentence.endswith(":"):
                continue

            # Ignore mostly-symbolic strings.
            alphanumeric = sum(
                char.isalnum()
                for char in sentence
            )

            if alphanumeric < 15:
                continue

            result.append(
                sentence
            )

        return result

    # =========================================================
    # NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize_sentence(
        sentence: str,
    ) -> str:
        """
        Normalize sentence for duplicate detection.
        """

        sentence = sentence.lower()

        sentence = re.sub(
            r"[^a-z0-9\s]",
            " ",
            sentence,
        )

        sentence = re.sub(
            r"\s+",
            " ",
            sentence,
        )

        return sentence.strip()

    # =========================================================
    # NLI PROBABILITIES
    # =========================================================

    @staticmethod
    def _probabilities(
        scores,
    ) -> np.ndarray:
        """
        Convert model output to probabilities.

        CrossEncoder models may return either logits or
        probability-like values.
        """

        values = np.asarray(
            scores,
            dtype=np.float32,
        )

        # Already probability-like.
        if (
            np.all(values >= 0)
            and np.all(values <= 1)
            and abs(
                float(values.sum()) - 1.0
            ) < 0.01
        ):
            return values

        # Stable softmax.
        values = (
            values
            - np.max(values)
        )

        probabilities = np.exp(
            values
        )

        total = probabilities.sum()

        if total <= 0:
            return np.array(
                [
                    1 / 3,
                    1 / 3,
                    1 / 3,
                ],
                dtype=np.float32,
            )

        probabilities /= total

        return probabilities

    # =========================================================
    # NLI LABEL
    # =========================================================

    @staticmethod
    def _label(
        probabilities: np.ndarray,
    ) -> int:
        """
        Return strongest NLI class.
        """

        return int(
            np.argmax(
                probabilities
            )
        )

    # =========================================================
    # PREDICT PAIR
    # =========================================================

    def _predict_pair(
        self,
        sentence_a: str,
        sentence_b: str,
    ) -> dict:
        """
        Run NLI in both directions.

        Contradiction must be strongly supported in BOTH
        directions.
        """

        forward_raw = (
            self.model.predict(
                [
                    (
                        sentence_a,
                        sentence_b,
                    )
                ],
                apply_softmax=True,
            )[0]
        )

        reverse_raw = (
            self.model.predict(
                [
                    (
                        sentence_b,
                        sentence_a,
                    )
                ],
                apply_softmax=True,
            )[0]
        )

        forward = self._probabilities(
            forward_raw
        )

        reverse = self._probabilities(
            reverse_raw
        )

        forward_label = self._label(
            forward
        )

        reverse_label = self._label(
            reverse
        )

        forward_contradiction = float(
            forward[0]
        )

        reverse_contradiction = float(
            reverse[0]
        )

        # -----------------------------------------------------
        # Compare contradiction probability against the
        # strongest alternative class.
        # -----------------------------------------------------

        forward_alternative = max(
            float(forward[1]),
            float(forward[2]),
        )

        reverse_alternative = max(
            float(reverse[1]),
            float(reverse[2]),
        )

        forward_margin = (
            forward_contradiction
            - forward_alternative
        )

        reverse_margin = (
            reverse_contradiction
            - reverse_alternative
        )

        # -----------------------------------------------------
        # Conservative contradiction rule.
        #
        # All conditions must be satisfied:
        #
        # 1. Both directions strongly predict contradiction.
        # 2. Contradiction probability is dominant.
        # 3. Contradiction margin is sufficiently large.
        # 4. Both NLI predictions select label 0.
        # -----------------------------------------------------

        strong_probability = (
            forward_contradiction
            >= self.contradiction_threshold
            and
            reverse_contradiction
            >= self.contradiction_threshold
        )

        strong_margin = (
            forward_margin
            >= self.margin_threshold
            and
            reverse_margin
            >= self.margin_threshold
        )

        labels_confirm = (
            forward_label == 0
            and
            reverse_label == 0
        )

        contradiction = bool(
            strong_probability
            and strong_margin
            and labels_confirm
        )

        average_score = (
            forward_contradiction
            + reverse_contradiction
        ) / 2.0

        return {
            "contradiction": contradiction,
            "forward_label": forward_label,
            "reverse_label": reverse_label,
            "forward_scores": [
                round(
                    float(value),
                    4,
                )
                for value in forward
            ],
            "reverse_scores": [
                round(
                    float(value),
                    4,
                )
                for value in reverse
            ],
            "contradiction_score": round(
                average_score,
                4,
            ),
            "forward_margin": round(
                forward_margin,
                4,
            ),
            "reverse_margin": round(
                reverse_margin,
                4,
            ),
        }

    # =========================================================
    # BUILD SEMANTIC CANDIDATES
    # =========================================================

    def _build_candidate_pairs(
        self,
        sentences_a: list[str],
        sentences_b: list[str],
    ) -> list[
        tuple[str, str, float]
    ]:
        """
        Find only semantically related sentence pairs.

        This is the critical false-positive protection.

        Example:

            Sentence A:
                "Decentralized systems can use heartbeat
                 based client sampling."

            Sentence B:
                "Decentralized systems keep data on local
                 devices."

        These sentences discuss the same broad topic but
        don't make opposing claims.

        The semantic filter prevents arbitrary NLI comparisons
        from treating them as contradictions.
        """

        if (
            not sentences_a
            or not sentences_b
        ):
            return []

        all_sentences = (
            sentences_a
            + sentences_b
        )

        embeddings = (
            self.embedding_model.encode(
                all_sentences,
                convert_to_tensor=True,
                normalize_embeddings=True,
            )
        )

        embeddings_a = embeddings[
            :len(sentences_a)
        ]

        embeddings_b = embeddings[
            len(sentences_a):
        ]

        matrix = cos_sim(
            embeddings_a,
            embeddings_b,
        )

        candidates = []

        for i, sentence_a in enumerate(
            sentences_a
        ):

            normalized_a = (
                self._normalize_sentence(
                    sentence_a
                )
            )

            for j, sentence_b in enumerate(
                sentences_b
            ):

                normalized_b = (
                    self._normalize_sentence(
                        sentence_b
                    )
                )

                # Exact same sentence.
                if (
                    normalized_a
                    == normalized_b
                ):
                    continue

                similarity = float(
                    matrix[
                        i,
                        j,
                    ].item()
                )

                # -------------------------------------------------
                # CRITICAL:
                #
                # Do not send weakly related sentences to NLI.
                # -------------------------------------------------

                if (
                    similarity
                    < self.similarity_threshold
                ):
                    continue

                candidates.append(
                    (
                        sentence_a,
                        sentence_b,
                        similarity,
                    )
                )

        # Highest semantic relevance first.
        candidates.sort(
            key=lambda item: item[2],
            reverse=True,
        )

        # Safety limit.
        return candidates[:50]

    # =========================================================
    # MAIN COMPARISON
    # =========================================================

    def compare(
        self,
        answer_a: str,
        answer_b: str,
    ) -> dict:
        """
        Compare two answers for contradictions.
        """

        sentences_a = (
            self._split_sentences(
                answer_a
            )
        )

        sentences_b = (
            self._split_sentences(
                answer_b
            )
        )

        # -----------------------------------------------------
        # Nothing meaningful to compare.
        # -----------------------------------------------------

        if (
            not sentences_a
            or not sentences_b
        ):
            return {
                "contradiction": False,
                "checked_pairs": 0,
                "strongest_score": 0.0,
                "evidence": None,
            }

        # -----------------------------------------------------
        # Candidate pairs.
        # -----------------------------------------------------

        candidate_pairs = (
            self._build_candidate_pairs(
                sentences_a,
                sentences_b,
            )
        )

        if not candidate_pairs:
            return {
                "contradiction": False,
                "checked_pairs": 0,
                "strongest_score": 0.0,
                "evidence": None,
            }

        strongest_result = None

        strongest_score = 0.0

        checked_pairs = 0

        # -----------------------------------------------------
        # NLI evaluation.
        # -----------------------------------------------------

        for (
            sentence_a,
            sentence_b,
            semantic_similarity,
        ) in candidate_pairs:

            result = self._predict_pair(
                sentence_a,
                sentence_b,
            )

            checked_pairs += 1

            score = result[
                "contradiction_score"
            ]

            if (
                score
                > strongest_score
            ):
                strongest_score = score

                strongest_result = {
                    "sentence_a": sentence_a,
                    "sentence_b": sentence_b,
                    "semantic_similarity": round(
                        semantic_similarity,
                        4,
                    ),
                    "forward_label": result[
                        "forward_label"
                    ],
                    "reverse_label": result[
                        "reverse_label"
                    ],
                    "forward_scores": result[
                        "forward_scores"
                    ],
                    "reverse_scores": result[
                        "reverse_scores"
                    ],
                    "contradiction_score": round(
                        score,
                        4,
                    ),
                    "forward_margin": result[
                        "forward_margin"
                    ],
                    "reverse_margin": result[
                        "reverse_margin"
                    ],
                    "contradiction": result[
                        "contradiction"
                    ],
                }

        # -----------------------------------------------------
        # Final contradiction decision.
        # -----------------------------------------------------

        contradiction_detected = bool(
            strongest_result
            and
            strongest_result[
                "contradiction"
            ]
        )

        return {
            "contradiction": (
                contradiction_detected
            ),
            "checked_pairs": (
                checked_pairs
            ),
            "strongest_score": round(
                strongest_score,
                4,
            ),
            "evidence": (
                strongest_result
                if contradiction_detected
                else None
            ),
        }