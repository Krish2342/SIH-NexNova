def build_refinement_prompt(
    original_prompt: str,
    responses: list,
    agreement_score: float,
) -> str:
    response_text = "\n\n".join(
        f"[{response.provider}]\n{response.answer}"
        for response in responses
    )

    return f"""
You are participating in a response verification process.

Original question:
{original_prompt}

The previous model responses had an agreement score of
{agreement_score}%.

Because the score was below the required threshold, reconsider
the question carefully.

Previous responses:
{response_text}

Generate a revised answer.

Requirements:
- Focus on the actual question.
- Resolve differences between the previous responses.
- Prefer precise, factual statements.
- Avoid unsupported claims.
- Do not mention this verification process.
- Return only the revised answer.
""".strip()