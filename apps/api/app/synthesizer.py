import re

from app.providers.base import LLMProvider


class AnswerSynthesizer:
    """
    Produces one final answer using multiple available
    providers with automatic fallback.
    """

    def __init__(self, providers: list[LLMProvider]):
        self.providers = providers

    @staticmethod
    def _clean_answer(answer: str) -> str:
        """
        Clean common formatting artifacts produced by LLMs
        without changing the meaning of the answer.
        """

        if not answer:
            return ""

        answer = answer.strip()

        # Normalize spaces and tabs.
        answer = re.sub(r"[ \t]+", " ", answer)

        # Preserve paragraph breaks while removing excessive blank lines.
        answer = re.sub(r"\n[ \t]+", "\n", answer)
        answer = re.sub(r"\n{3,}", "\n\n", answer)

        # Fix common missing spaces after punctuation.
        answer = re.sub(
            r"([,.!?;:])([A-Za-z])",
            r"\1 \2",
            answer,
        )

        # Fix common word-boundary artifacts.
        replacements = {
            "modelslike": "models like",
            "performingtasks": "performing tasks",
            "andadapting": "and adapting",
            "automatecognitive": "automate cognitive",
            "computational modelslike": (
                "computational models like"
            ),
            "neural networks,to": (
                "neural networks, to"
            ),
            "complexmachine": (
                "complex machine"
            ),
        }

        for old, new in replacements.items():
            answer = answer.replace(old, new)

        # Remove accidental spaces before punctuation.
        answer = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            answer,
        )

        return answer.strip()

    async def synthesize(
        self,
        question: str,
        responses: list,
    ) -> tuple[str | None, str | None, list[dict]]:

        # Only use responses that actually contain an answer.
        valid_responses = [
            response
            for response in responses
            if getattr(response, "answer", None)
            and response.answer.strip()
        ]

        if not valid_responses:
            return None, None, [
                {
                    "provider": "synthesizer",
                    "error_type": "NoResponses",
                    "message": (
                        "No valid provider responses were available "
                        "for synthesis."
                    ),
                }
            ]

        response_text = "\n\n".join(
            f"""
PROVIDER: {response.provider}

MODEL: {response.model}

ANSWER:

{response.answer}
""".strip()
            for response in valid_responses
        )

        prompt = f"""
You are the final answer synthesizer for NEXVERITY.

Original user question:

{question}

Verified independent AI responses:

{response_text}

Produce ONE final answer for the user.

Rules:

- Directly answer the original question.
- Combine useful information from the responses.
- Resolve differences carefully.
- Prefer precise and factual information.
- Do not invent unsupported information.
- Remove unnecessary repetition.
- Use correct spacing, punctuation, and grammar.
- Write naturally and clearly.
- Do not mention Gemini, Groq, OpenRouter, providers,
  models, agreement scores, verification rounds,
  or the synthesis process.
- Do not explain your reasoning.
- Return ONLY the final answer.
""".strip()

        errors = []

        for provider in self.providers:
            try:
                result = await provider.generate(prompt)

                raw_answer = getattr(result, "answer", None)

                if not raw_answer:
                    errors.append(
                        {
                            "provider": (
                                provider.__class__.__name__
                            ),
                            "error_type": "EmptyResponse",
                            "message": (
                                "Provider returned an empty "
                                "synthesis response."
                            ),
                        }
                    )
                    continue

                answer = self._clean_answer(raw_answer)

                if not answer:
                    errors.append(
                        {
                            "provider": (
                                provider.__class__.__name__
                            ),
                            "error_type": "EmptyAfterCleaning",
                            "message": (
                                "Provider returned text, but "
                                "cleaning produced an empty answer."
                            ),
                        }
                    )
                    continue

                print(
                    f"Synthesis successful: "
                    f"{provider.__class__.__name__}"
                )

                return (
                    answer,
                    result.provider,
                    errors,
                )

            except Exception as exc:
                error_type = type(exc).__name__
                error_message = str(exc)

                print(
                    f"Synthesis provider failed: "
                    f"{provider.__class__.__name__}: "
                    f"{error_type}: {error_message}"
                )

                errors.append(
                    {
                        "provider": (
                            provider.__class__.__name__
                        ),
                        "error_type": error_type,
                        "message": error_message,
                    }
                )

        return None, None, errors