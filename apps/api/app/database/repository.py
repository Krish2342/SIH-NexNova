from app.database.supabase import SupabaseService


class AnalysisRepository:
    """
    Persists NEXVERITY analysis results in Supabase.
    """

    def __init__(self):
        self.db = SupabaseService()

    def save_analysis(
        self,
        question: str,
        result: dict,
    ) -> str:
        """
        Save a complete NEXVERITY analysis.

        Returns:
            str: analysis_run UUID
        """

        # -----------------------------------------------------
        # Analysis run
        # -----------------------------------------------------

        analysis_run = self.db.create_analysis_run(
            {
                "question": question,
                "status": result.get("status"),
                "final_answer": result.get(
                    "final_answer"
                ),
                "agreement_score": result.get(
                    "agreement_score"
                ),
                "threshold": result.get(
                    "threshold"
                ),
                "contradiction_detected": bool(
                    result.get(
                        "contradiction_detected",
                        False,
                    )
                ),
                "synthesis_provider": result.get(
                    "synthesis_provider"
                ),
                "difficulty": result.get(
                    "difficulty"
                ),
                "providers_requested": result.get(
                    "providers_requested"
                ),
                "providers_used": result.get(
                    "providers_used"
                ),
                "message": result.get(
                    "message"
                ),
            }
        )

        analysis_run_id = analysis_run["id"]

        # -----------------------------------------------------
        # Verification rounds
        # -----------------------------------------------------

        rounds = result.get(
            "rounds",
            [],
        )

        if not isinstance(
            rounds,
            list,
        ):
            rounds = []

        for round_data in rounds:

            if not isinstance(
                round_data,
                dict,
            ):
                continue

            round_number = round_data.get(
                "round",
                1,
            )

            # -------------------------------------------------
            # Verification round
            # -------------------------------------------------

            verification_round = (
                self.db.create_verification_round(
                    {
                        "analysis_run_id": (
                            analysis_run_id
                        ),
                        "round_number": (
                            round_number
                        ),
                        "agreement_score": (
                            round_data.get(
                                "agreement_score"
                            )
                        ),
                        "decision": (
                            round_data.get(
                                "decision"
                            )
                        ),
                        "contradiction_detected": bool(
                            round_data.get(
                                "contradiction_detected",
                                False,
                            )
                        ),
                        "prompt": (
                            round_data.get(
                                "prompt"
                            )
                        ),
                        "providers_requested": (
                            round_data.get(
                                "providers_requested"
                            )
                        ),
                        "providers_used": (
                            round_data.get(
                                "providers_used"
                            )
                        ),
                    }
                )
            )

            verification_round_id = (
                verification_round["id"]
            )

            # -------------------------------------------------
            # Provider responses
            # -------------------------------------------------

            responses = round_data.get(
                "responses",
                [],
            )

            if isinstance(
                responses,
                list,
            ):
                for response in responses:

                    if not isinstance(
                        response,
                        dict,
                    ):
                        continue

                    self.db.create_provider_response(
                        {
                            "analysis_run_id": (
                                analysis_run_id
                            ),
                            "round_number": (
                                round_number
                            ),
                            "provider": (
                                response.get(
                                    "provider"
                                )
                            ),
                            "model": (
                                response.get(
                                    "model"
                                )
                            ),
                            "answer": (
                                response.get(
                                    "answer"
                                )
                            ),
                            "latency_ms": (
                                response.get(
                                    "latency_ms"
                                )
                            ),
                            "input_tokens": (
                                response.get(
                                    "input_tokens"
                                )
                            ),
                            "output_tokens": (
                                response.get(
                                    "output_tokens"
                                )
                            ),
                        }
                    )

            # -------------------------------------------------
            # Comparisons
            # -------------------------------------------------

            comparisons = round_data.get(
                "comparisons",
                [],
            )

            if isinstance(
                comparisons,
                list,
            ):
                for comparison in comparisons:

                    if not isinstance(
                        comparison,
                        dict,
                    ):
                        continue

                    self.db.create_comparison(
                        {
                            "verification_round_id": (
                                verification_round_id
                            ),
                            "provider_a": (
                                comparison.get(
                                    "provider_a"
                                )
                            ),
                            "provider_b": (
                                comparison.get(
                                    "provider_b"
                                )
                            ),
                            "score": (
                                comparison.get(
                                    "score"
                                )
                            ),
                        }
                    )

            # -------------------------------------------------
            # Contradictions
            # -------------------------------------------------

            contradictions = round_data.get(
                "contradictions",
                [],
            )

            if isinstance(
                contradictions,
                list,
            ):
                for contradiction in contradictions:

                    if not isinstance(
                        contradiction,
                        dict,
                    ):
                        continue

                    self.db.create_contradiction(
                        {
                            "verification_round_id": (
                                verification_round_id
                            ),
                            "provider_a": (
                                contradiction.get(
                                    "provider_a"
                                )
                            ),
                            "provider_b": (
                                contradiction.get(
                                    "provider_b"
                                )
                            ),
                            "contradiction": bool(
                                contradiction.get(
                                    "contradiction",
                                    False,
                                )
                            ),
                            "checked_pairs": (
                                contradiction.get(
                                    "checked_pairs"
                                )
                            ),
                            "strongest_score": (
                                contradiction.get(
                                    "strongest_score"
                                )
                            ),
                            "evidence": (
                                contradiction.get(
                                    "evidence"
                                )
                            ),
                        }
                    )

        return analysis_run_id