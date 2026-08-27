from pydantic import BaseModel
from typing import Optional


class AnalyzeRequest(BaseModel):
    question: str


class ModelResponse(BaseModel):
    provider: str
    model: str
    answer: str
    latency_ms: Optional[float] = None


class Comparison(BaseModel):
    provider_a: str
    provider_b: str
    score: float


class VerificationRound(BaseModel):
    round: int
    agreement_score: float
    decision: str
    contradiction_detected: bool
    comparisons: list[Comparison]


class AnalyzeResponse(BaseModel):
    status: str
    final_answer: Optional[str]
    agreement_score: Optional[float]
    threshold: Optional[float]
    contradiction_detected: bool
    synthesis_provider: Optional[str]
    rounds: list[VerificationRound]
    final_responses: list[ModelResponse]
    message: Optional[str]