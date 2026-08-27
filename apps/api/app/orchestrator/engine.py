from app.config import MAX_REGENERATION_ROUNDS

from app.orchestrator.collector import collect_responses
from app.orchestrator.comparison import ComparisonEngine
from app.orchestrator.contradiction import ContradictionEngine
from app.orchestrator.decision import DecisionEngine
from app.orchestrator.difficulty import (
    Difficulty,
    DifficultyEngine,
)
from app.orchestrator.manager import ProviderManager
from app.orchestrator.refinement import (
    build_refinement_prompt,
)

from app.synthesizer import AnswerSynthesizer


class NexverityEngine:
    """
    Main NEXVERITY orchestration engine.

    Pipeline:

        Question
            ↓
        Difficulty classification
            ↓
        Provider selection
            ↓
        Independent responses
            ↓
        Semantic comparison
            ↓
        Contradiction detection
            ↓
        Decision
            ↓
        Regeneration if required
            ↓
        Final synthesis
            ↓
        Final answer

    Provider routing:

        EASY:
            2 successful providers

        MODERATE:
            up to 4 successful providers

        HARD:
            all available providers

    Provider failures are handled through automatic
    failover whenever another provider is available.
    """

    def __init__(self):
        self.provider_manager = ProviderManager()

        self.comparison_engine = (
            ComparisonEngine()
        )

        self.contradiction_engine = (
            ContradictionEngine()
        )

        self.decision_engine = (
            DecisionEngine()
        )

        self.difficulty_engine = (
            DifficultyEngine()
        )

    # =========================================================
    # PROVIDER HELPERS
    # =========================================================

    @staticmethod
    def _provider_name(provider) -> str:
        """
        Convert provider class name into the provider name
        used by ModelResponse.
        """

        return (
            provider.__class__.__name__
            .replace("Provider", "")
            .lower()
        )

    @staticmethod
    def _get_successful_providers(
        providers,
        responses,
    ):
        """
        Return provider objects that successfully generated
        a response.
        """

        successful_names = {
            response.provider
            for response in responses
        }

        successful_providers = []

        for provider in providers:

            if (
                NexverityEngine._provider_name(
                    provider
                )
                in successful_names
            ):
                successful_providers.append(
                    provider
                )

        return successful_providers

    # =========================================================
    # PROVIDER SELECTION
    # =========================================================

    def _select_providers(
        self,
        question: str,
        available_providers,
    ):
        """
        Select providers according to question difficulty.

        EASY:
            2 providers

        MODERATE:
            up to 4 providers

        HARD:
            all available providers
        """

        available_count = len(
            available_providers
        )

        if available_count == 0:
            return [], Difficulty.EASY

        difficulty = (
            self.difficulty_engine.classify(
                question
            )
        )

        provider_count = (
            self._requested_provider_count(
                difficulty,
                available_count,
            )
        )

        selected_providers = (
            available_providers[
                :provider_count
            ]
        )

        print(
            "NEXVERITY routing:",
            f"difficulty={difficulty.value}",
            f"available={available_count}",
            f"selected={len(selected_providers)}",
            "providers=",
            [
                self._provider_name(provider)
                for provider in selected_providers
            ],
        )

        return (
            selected_providers,
            difficulty,
        )

    @staticmethod
    def _requested_provider_count(
        difficulty: Difficulty,
        available_count: int,
    ) -> int:
        """
        Determine target number of providers.
        """

        if difficulty == Difficulty.EASY:
            return min(
                2,
                available_count,
            )

        if difficulty == Difficulty.MODERATE:
            return min(
                4,
                available_count,
            )

        # HARD:
        # Use every available provider.
        return available_count

    # =========================================================
    # PROVIDER FAILOVER
    # =========================================================

    async def _fill_failed_providers(
        self,
        selected_providers,
        responses,
        required_count,
    ):
        """
        Add only as many backup providers as are actually
        required.

        Example:

            Required = 2

            Gemini      ❌
            Groq        ✅

            Need = 1

            Add only one backup:

            OpenRouter  → backup

            Result:
                Groq + OpenRouter

        This prevents Easy questions from unnecessarily
        using 3+ successful providers.
        """

        # -----------------------------------------------------
        # How many successful responses do we already have?
        # -----------------------------------------------------

        needed = max(
            0,
            required_count
            - len(responses),
        )

        if needed == 0:
            return selected_providers

        # -----------------------------------------------------
        # Providers that already responded successfully.
        # -----------------------------------------------------

        successful_names = {
            response.provider
            for response in responses
        }

        # -----------------------------------------------------
        # Providers already attempted.
        # -----------------------------------------------------

        attempted_names = {
            self._provider_name(
                provider
            )
            for provider in selected_providers
        }

        # -----------------------------------------------------
        # Get providers that are not currently in cooldown.
        # -----------------------------------------------------

        available_providers = (
            await self.provider_manager
            .get_available_providers()
        )

        added = 0

        for provider in available_providers:

            if added >= needed:
                break

            provider_name = (
                self._provider_name(
                    provider
                )
            )

            # Already successful.
            if provider_name in successful_names:
                continue

            # Already attempted.
            if provider_name in attempted_names:
                continue

            selected_providers.append(
                provider
            )

            attempted_names.add(
                provider_name
            )

            added += 1

            print(
                "NEXVERITY failover:",
                f"adding={provider_name}",
                f"needed={needed}",
                f"added={added}",
            )

        return selected_providers

    # =========================================================
    # FALLBACK ANSWER
    # =========================================================

    @staticmethod
    def _fallback_answer(
        responses,
    ):
        """
        Return the first valid provider answer.

        Used only when final synthesis fails.
        """

        if not responses:
            return None, None

        for response in responses:

            answer = getattr(
                response,
                "answer",
                None,
            )

            if (
                isinstance(
                    answer,
                    str,
                )
                and answer.strip()
            ):
                return (
                    answer.strip(),
                    getattr(
                        response,
                        "provider",
                        None,
                    ),
                )

        return None, None

    # =========================================================
    # SAFE ANSWER
    # =========================================================

    @staticmethod
    def _safe_answer(
        final_answer,
        responses,
    ):
        """
        Guarantee a non-empty final answer whenever
        a provider returned usable content.
        """

        if (
            isinstance(
                final_answer,
                str,
            )
            and final_answer.strip()
        ):
            return final_answer.strip()

        fallback_answer, _ = (
            NexverityEngine._fallback_answer(
                responses
            )
        )

        if fallback_answer:
            return fallback_answer

        return (
            "The providers returned responses, "
            "but a final answer could not be generated."
        )

    # =========================================================
    # SYNTHESIS
    # =========================================================

    async def _synthesize(
        self,
        question,
        responses,
        providers,
    ):
        """
        Synthesize the final answer using providers that
        actually returned successful responses.
        """

        synthesis_providers = (
            self._get_successful_providers(
                providers,
                responses,
            )
        )

        if not synthesis_providers:
            return (
                None,
                None,
                [],
            )

        synthesizer = AnswerSynthesizer(
            synthesis_providers
        )

        return await synthesizer.synthesize(
            question=question,
            responses=responses,
        )

    # =========================================================
    # ROUND RESULT
    # =========================================================

    @staticmethod
    def _build_round_result(
        round_number,
        average_score,
        decision,
        contradiction_detected,
        comparisons,
        contradictions,
        contradiction_evidence,
        responses,
        current_prompt,
        provider_errors,
        difficulty,
        requested_provider_count,
    ):
        """
        Create a consistent round result.
        """

        return {
            "round": round_number,

            "agreement_score": average_score,

            "decision": decision,

            "contradiction_detected": (
                contradiction_detected
            ),

            "comparisons": comparisons,

            "contradictions": contradictions,

            "contradiction_evidence": (
                contradiction_evidence
            ),

            "responses": responses,

            "prompt": current_prompt,

            "provider_errors": provider_errors,

            "difficulty": difficulty.value,

            "providers_requested": (
                requested_provider_count
            ),

            "providers_used": len(
                responses
            ),
        }

    # =========================================================
    # MAIN PROCESS
    # =========================================================

    async def process(
        self,
        prompt: str,
    ) -> dict:
        """
        Execute the complete NEXVERITY pipeline.
        """

        prompt = prompt.strip()

        # =====================================================
        # EMPTY QUESTION
        # =====================================================

        if not prompt:
            return {
                "status": "INVALID_REQUEST",
                "message": (
                    "Question cannot be empty."
                ),
                "rounds": [],
                "final_answer": None,
                "final_responses": [],
                "difficulty": None,
                "providers_requested": 0,
                "providers_used": 0,
            }

        # =====================================================
        # AVAILABLE PROVIDERS
        # =====================================================

        available_providers = (
            await self.provider_manager
            .get_available_providers()
        )

        if len(available_providers) < 2:
            return {
                "status": "INSUFFICIENT_PROVIDERS",
                "message": (
                    "At least two providers "
                    "are required."
                ),
                "rounds": [],
                "final_answer": None,
                "final_responses": [],
                "difficulty": None,
                "providers_requested": 2,
                "providers_used": len(
                    available_providers
                ),
            }

        # =====================================================
        # DIFFICULTY + INITIAL PROVIDERS
        # =====================================================

        (
            selected_providers,
            difficulty,
        ) = self._select_providers(
            prompt,
            available_providers,
        )

        requested_provider_count = (
            self._requested_provider_count(
                difficulty,
                len(available_providers),
            )
        )

        if len(selected_providers) < 2:
            return {
                "status": "INSUFFICIENT_PROVIDERS",
                "message": (
                    "Fewer than two providers "
                    "are available."
                ),
                "rounds": [],
                "final_answer": None,
                "final_responses": [],
                "difficulty": difficulty.value,
                "providers_requested": 2,
                "providers_used": len(
                    selected_providers
                ),
            }

        # =====================================================
        # ROUND STATE
        # =====================================================

        rounds = []

        current_prompt = prompt

        current_providers = list(
            selected_providers
        )

        best_round = None

        total_rounds = (
            MAX_REGENERATION_ROUNDS + 1
        )

        # =====================================================
        # VERIFICATION ROUNDS
        # =====================================================

        for round_number in range(
            1,
            total_rounds + 1,
        ):

            print(
                f"NEXVERITY verification round "
                f"{round_number}/{total_rounds}"
            )

            print(
                "NEXVERITY providers:",
                [
                    self._provider_name(
                        provider
                    )
                    for provider in current_providers
                ],
            )

            # =================================================
            # COLLECT INITIAL RESPONSES
            # =================================================

            (
                responses,
                provider_errors,
            ) = await collect_responses(
                current_providers,
                current_prompt,
                provider_manager=(
                    self.provider_manager
                ),
            )

            # =================================================
            # FAILOVER
            # =================================================

            if len(responses) < requested_provider_count:

                previous_count = len(
                    responses
                )

                original_provider_names = {
                    self._provider_name(
                        provider
                    )
                    for provider in current_providers
                }

                current_providers = (
                    await self._fill_failed_providers(
                        current_providers,
                        responses,
                        requested_provider_count,
                    )
                )

                # -------------------------------------------------
                # Find only newly-added providers.
                # -------------------------------------------------

                new_providers = [
                    provider
                    for provider in current_providers
                    if self._provider_name(
                        provider
                    )
                    not in original_provider_names
                ]

                if new_providers:

                    print(
                        "NEXVERITY failover candidates:",
                        [
                            self._provider_name(
                                provider
                            )
                            for provider in new_providers
                        ],
                    )

                    (
                        extra_responses,
                        extra_errors,
                    ) = await collect_responses(
                        new_providers,
                        current_prompt,
                        provider_manager=(
                            self.provider_manager
                        ),
                    )

                    responses.extend(
                        extra_responses
                    )

                    provider_errors.extend(
                        extra_errors
                    )

                    print(
                        "NEXVERITY failover result:",
                        f"before={previous_count}",
                        f"after={len(responses)}",
                    )

            # =================================================
            # STILL NOT ENOUGH RESPONSES
            # =================================================

            if len(responses) < 2:

                # If we have a previous good round,
                # keep it rather than destroying the result.
                if best_round is not None:
                    print(
                        "NEXVERITY: regeneration could "
                        "not obtain two responses; "
                        "keeping best previous round."
                    )
                    break

                (
                    fallback_answer,
                    fallback_provider,
                ) = self._fallback_answer(
                    responses
                )

                return {
                    "status": (
                        "INSUFFICIENT_RESPONSES"
                    ),
                    "message": (
                        "At least two successful "
                        "provider responses are "
                        "required."
                    ),
                    "provider_errors": (
                        provider_errors
                    ),
                    "rounds": rounds,
                    "final_responses": responses,
                    "final_answer": (
                        fallback_answer
                    ),
                    "synthesis_provider": (
                        fallback_provider
                    ),
                    "difficulty": (
                        difficulty.value
                    ),
                    "providers_requested": (
                        requested_provider_count
                    ),
                    "providers_used": len(
                        responses
                    ),
                }

            # =================================================
            # COMPARE ALL SUCCESSFUL RESPONSES
            # =================================================

            comparisons = []

            contradictions = []

            for i in range(
                len(responses)
            ):

                for j in range(
                    i + 1,
                    len(responses),
                ):

                    response_a = (
                        responses[i]
                    )

                    response_b = (
                        responses[j]
                    )

                    # -----------------------------------------
                    # Semantic agreement
                    # -----------------------------------------

                    score = (
                        self.comparison_engine.compare(
                            response_a.answer,
                            response_b.answer,
                        )
                    )

                    # -----------------------------------------
                    # Contradiction detection
                    # -----------------------------------------

                    contradiction = (
                        self.contradiction_engine.compare(
                            response_a.answer,
                            response_b.answer,
                        )
                    )

                    comparisons.append(
                        {
                            "provider_a": (
                                response_a.provider
                            ),
                            "provider_b": (
                                response_b.provider
                            ),
                            "score": score,
                        }
                    )

                    contradictions.append(
                        {
                            "provider_a": (
                                response_a.provider
                            ),
                            "provider_b": (
                                response_b.provider
                            ),
                            **contradiction,
                        }
                    )

            # =================================================
            # SAFETY CHECK
            # =================================================

            if not comparisons:

                (
                    fallback_answer,
                    fallback_provider,
                ) = self._fallback_answer(
                    responses
                )

                return {
                    "status": (
                        "INSUFFICIENT_COMPARISONS"
                    ),
                    "message": (
                        "Unable to compare "
                        "provider responses."
                    ),
                    "provider_errors": (
                        provider_errors
                    ),
                    "rounds": rounds,
                    "final_responses": responses,
                    "final_answer": (
                        fallback_answer
                    ),
                    "synthesis_provider": (
                        fallback_provider
                    ),
                    "difficulty": (
                        difficulty.value
                    ),
                    "providers_requested": (
                        requested_provider_count
                    ),
                    "providers_used": len(
                        responses
                    ),
                }

            # =================================================
            # AGREEMENT SCORE
            # =================================================

            scores = [
                item["score"]
                for item in comparisons
            ]

            average_score = round(
                sum(scores)
                / len(scores),
                2,
            )

            average_score = max(
                0.0,
                min(
                    100.0,
                    average_score,
                ),
            )

            # =================================================
            # CONTRADICTION RESULT
            # =================================================

            contradiction_detected = any(
                item["contradiction"]
                for item in contradictions
            )

            contradiction_evidence = [
                item
                for item in contradictions
                if item["contradiction"]
            ]

            # =================================================
            # DECISION
            # =================================================

            decision = (
                self.decision_engine.evaluate(
                    average_score
                )
            )

            # A contradiction overrides PASS.
            if (
                decision == "PASS"
                and contradiction_detected
            ):
                decision = "REGENERATE"

            # =================================================
            # SAVE ROUND
            # =================================================

            round_result = (
                self._build_round_result(
                    round_number=round_number,
                    average_score=average_score,
                    decision=decision,
                    contradiction_detected=(
                        contradiction_detected
                    ),
                    comparisons=comparisons,
                    contradictions=contradictions,
                    contradiction_evidence=(
                        contradiction_evidence
                    ),
                    responses=responses,
                    current_prompt=current_prompt,
                    provider_errors=provider_errors,
                    difficulty=difficulty,
                    requested_provider_count=(
                        requested_provider_count
                    ),
                )
            )

            rounds.append(
                round_result
            )

            # =================================================
            # BEST ROUND
            # =================================================

            if not contradiction_detected:

                if (
                    best_round is None
                    or average_score
                    > best_round[
                        "agreement_score"
                    ]
                ):
                    best_round = (
                        round_result
                    )

            # =================================================
            # PASS
            # =================================================

            if decision == "PASS":

                (
                    final_answer,
                    synthesis_provider,
                    synthesis_errors,
                ) = await self._synthesize(
                    question=prompt,
                    responses=responses,
                    providers=current_providers,
                )

                safe_answer = (
                    self._safe_answer(
                        final_answer,
                        responses,
                    )
                )

                # -------------------------------------------------
                # Successful synthesis.
                # -------------------------------------------------

                if (
                    isinstance(
                        final_answer,
                        str,
                    )
                    and final_answer.strip()
                ):

                    return {
                        "status": "PASS",
                        "agreement_score": (
                            average_score
                        ),
                        "threshold": (
                            self.decision_engine.threshold
                        ),
                        "contradiction_detected": (
                            contradiction_detected
                        ),
                        "final_answer": (
                            safe_answer
                        ),
                        "synthesis_provider": (
                            synthesis_provider
                        ),
                        "rounds": rounds,
                        "final_responses": (
                            responses
                        ),
                        "difficulty": (
                            difficulty.value
                        ),
                        "providers_requested": (
                            requested_provider_count
                        ),
                        "providers_used": len(
                            responses
                        ),
                    }

                # -------------------------------------------------
                # Synthesis failed but provider answers exist.
                # -------------------------------------------------

                (
                    _,
                    fallback_provider,
                ) = self._fallback_answer(
                    responses
                )

                return {
                    "status": "PASS",
                    "agreement_score": (
                        average_score
                    ),
                    "threshold": (
                        self.decision_engine.threshold
                    ),
                    "contradiction_detected": (
                        contradiction_detected
                    ),
                    "final_answer": (
                        safe_answer
                    ),
                    "synthesis_provider": (
                        synthesis_provider
                        or fallback_provider
                    ),
                    "rounds": rounds,
                    "final_responses": (
                        responses
                    ),
                    "synthesis_errors": (
                        synthesis_errors
                    ),
                    "difficulty": (
                        difficulty.value
                    ),
                    "providers_requested": (
                        requested_provider_count
                    ),
                    "providers_used": len(
                        responses
                    ),
                    "message": (
                        "Verification passed. "
                        "The answer shown is the "
                        "best available provider response."
                    ),
                }

            # =================================================
            # REGENERATION
            # =================================================

            if (
                decision == "REGENERATE"
                and round_number < total_rounds
            ):

                current_prompt = (
                    build_refinement_prompt(
                        original_prompt=prompt,
                        responses=responses,
                        agreement_score=(
                            average_score
                        ),
                    )
                )

                # -------------------------------------------------
                # Refresh providers after cooldowns/failures.
                # -------------------------------------------------

                refreshed_available = (
                    await self.provider_manager
                    .get_available_providers()
                )

                if len(
                    refreshed_available
                ) >= 2:

                    (
                        refreshed_providers,
                        refreshed_difficulty,
                    ) = self._select_providers(
                        prompt,
                        refreshed_available,
                    )

                    if len(
                        refreshed_providers
                    ) >= 2:

                        current_providers = list(
                            refreshed_providers
                        )

                        difficulty = (
                            refreshed_difficulty
                        )

                        requested_provider_count = (
                            self._requested_provider_count(
                                difficulty,
                                len(
                                    refreshed_available
                                ),
                            )
                        )

            # =================================================
            # MAX ROUNDS
            # =================================================

        # =====================================================
        # NO VALID ROUND
        # =====================================================

        if best_round is None:

            (
                fallback_answer,
                fallback_provider,
            ) = self._fallback_answer(
                rounds[-1]["responses"]
                if rounds
                else []
            )

            return {
                "status": (
                    "VERIFICATION_FAILED"
                ),
                "agreement_score": (
                    rounds[-1][
                        "agreement_score"
                    ]
                    if rounds
                    else 0.0
                ),
                "threshold": (
                    self.decision_engine.threshold
                ),
                "contradiction_detected": (
                    rounds[-1][
                        "contradiction_detected"
                    ]
                    if rounds
                    else False
                ),
                "final_answer": (
                    fallback_answer
                ),
                "synthesis_provider": (
                    fallback_provider
                ),
                "rounds": rounds,
                "final_responses": (
                    rounds[-1]["responses"]
                    if rounds
                    else []
                ),
                "difficulty": (
                    difficulty.value
                ),
                "providers_requested": (
                    requested_provider_count
                ),
                "providers_used": (
                    len(
                        rounds[-1]["responses"]
                    )
                    if rounds
                    else 0
                ),
                "message": (
                    "No non-contradictory "
                    "verification round was available."
                ),
            }

        # =====================================================
        # SYNTHESIZE BEST ROUND
        # =====================================================

        (
            final_answer,
            synthesis_provider,
            synthesis_errors,
        ) = await self._synthesize(
            question=prompt,
            responses=best_round[
                "responses"
            ],
            providers=current_providers,
        )

        safe_answer = (
            self._safe_answer(
                final_answer,
                best_round[
                    "responses"
                ],
            )
        )

        if (
            not isinstance(
                final_answer,
                str,
            )
            or not final_answer.strip()
        ):

            (
                _,
                fallback_provider,
            ) = self._fallback_answer(
                best_round[
                    "responses"
                ]
            )

            synthesis_provider = (
                synthesis_provider
                or fallback_provider
            )

        # =====================================================
        # FINAL MAX-ROUNDS RESULT
        # =====================================================

        return {
            "status": (
                "MAX_ROUNDS_REACHED"
            ),
            "agreement_score": (
                best_round[
                    "agreement_score"
                ]
            ),
            "threshold": (
                self.decision_engine.threshold
            ),
            "contradiction_detected": (
                best_round[
                    "contradiction_detected"
                ]
            ),
            "final_answer": (
                safe_answer
            ),
            "synthesis_provider": (
                synthesis_provider
            ),
            "rounds": rounds,
            "final_responses": (
                best_round[
                    "responses"
                ]
            ),
            "synthesis_errors": (
                synthesis_errors
            ),
            "difficulty": (
                difficulty.value
            ),
            "providers_requested": (
                requested_provider_count
            ),
            "providers_used": len(
                best_round[
                    "responses"
                ]
            ),
            "message": (
                "Agreement threshold was not reached "
                "within the allowed regeneration rounds. "
                "The answer shown is the best available "
                "synthesis and should be verified."
            ),
        }