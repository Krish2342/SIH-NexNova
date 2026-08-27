from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.database.repository import AnalysisRepository
from app.orchestrator.engine import NexverityEngine


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(
    title="NEXVERITY API",
    description=(
        "Multi-model AI verification and "
        "answer synthesis API."
    ),
    version="0.4.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REQUEST SCHEMA
# =========================================================

class AnalyzeRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Question to verify.",
    )


# =========================================================
# RESPONSE SCHEMAS
# =========================================================

class ModelResponse(BaseModel):
    provider: Optional[str] = None
    model: Optional[str] = None
    answer: Optional[str] = None
    latency_ms: Optional[float] = None


class Comparison(BaseModel):
    provider_a: Optional[str] = None
    provider_b: Optional[str] = None
    score: Optional[float] = None


class VerificationRound(BaseModel):
    round: Optional[int] = None
    agreement_score: Optional[float] = None
    decision: Optional[str] = None
    contradiction_detected: bool = False

    comparisons: list[Comparison] = Field(
        default_factory=list
    )


class AnalyzeResponse(BaseModel):
    status: Optional[str] = None

    answer: Optional[str] = None

    agreement_score: Optional[float] = None

    threshold: Optional[float] = None

    contradiction_detected: bool = False

    synthesis_provider: Optional[str] = None

    message: Optional[str] = None

    rounds: list[dict[str, Any]] = Field(
        default_factory=list
    )

    difficulty: Optional[str] = None

    providers_requested: Optional[int] = None

    providers_used: Optional[int] = None


# =========================================================
# ENGINE
# =========================================================

engine = NexverityEngine()


# =========================================================
# DATABASE
# =========================================================

analysis_repository = AnalysisRepository()


# =========================================================
# ROOT
# =========================================================

@app.get("/")
async def root():
    return {
        "name": "NEXVERITY",
        "status": "online",
        "version": "0.4.0",
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():
    """
    Basic API health check.

    This endpoint does not call any AI provider
    or database operation.
    """

    return {
        "status": "healthy",
        "service": "nexverity-api",
        "version": "0.4.0",
    }


# =========================================================
# PROVIDER STATUS
# =========================================================

@app.get("/api/v1/providers")
async def providers():
    """
    Return the current status of all configured providers.
    """

    try:
        provider_status = (
            await engine.provider_manager
            .get_provider_status()
        )

        available_count = sum(
            1
            for provider in provider_status
            if provider.get("available")
        )

        return {
            "status": "ok",
            "total": len(provider_status),
            "available": available_count,
            "providers": provider_status,
        }

    except Exception as exc:
        print(
            "NEXVERITY provider status error:",
            type(exc).__name__,
            str(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to retrieve "
                "provider status."
            ),
        ) from exc


# =========================================================
# ANALYZE
# =========================================================

@app.post(
    "/api/v1/analyze",
    response_model=AnalyzeResponse,
)
async def analyze(
    request: AnalyzeRequest,
):
    """
    Analyze and verify a user question.

    The analysis result is returned to the client and,
    when possible, persisted to Supabase.
    """

    # -----------------------------------------------------
    # Validate question
    # -----------------------------------------------------

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    # -----------------------------------------------------
    # Run NEXVERITY engine
    # -----------------------------------------------------

    try:
        result = await engine.process(
            question
        )

    except Exception as exc:
        print(
            "NEXVERITY engine error:",
            type(exc).__name__,
            str(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "NEXVERITY engine failed "
                "to process the question."
            ),
        ) from exc

    # -----------------------------------------------------
    # Save analysis to Supabase
    #
    # Database failure does NOT fail the AI request.
    # -----------------------------------------------------

    try:
        analysis_id = (
            analysis_repository.save_analysis(
                question=question,
                result=result,
            )
        )

        print(
            "NEXVERITY analysis saved:",
            analysis_id,
        )

    except Exception as exc:
        print(
            "NEXVERITY database error:",
            type(exc).__name__,
            str(exc),
        )

    # =====================================================
    # FINAL ANSWER
    # =====================================================

    final_answer = result.get(
        "final_answer"
    )

    if not final_answer:
        final_answer = result.get(
            "answer"
        )

    # =====================================================
    # AGREEMENT SCORE
    # =====================================================

    agreement_score = result.get(
        "agreement_score"
    )

    if agreement_score is not None:
        try:
            agreement_score = float(
                agreement_score
            )
        except (
            TypeError,
            ValueError,
        ):
            agreement_score = None

    # =====================================================
    # THRESHOLD
    # =====================================================

    threshold = result.get(
        "threshold"
    )

    if threshold is not None:
        try:
            threshold = float(
                threshold
            )
        except (
            TypeError,
            ValueError,
        ):
            threshold = None

    # =====================================================
    # ROUNDS
    # =====================================================

    rounds = result.get(
        "rounds",
        [],
    )

    if not isinstance(
        rounds,
        list,
    ):
        rounds = []

    # =====================================================
    # DIFFICULTY
    # =====================================================

    difficulty = result.get(
        "difficulty"
    )

    if difficulty is not None:
        difficulty = str(
            difficulty
        )

    # =====================================================
    # PROVIDER COUNTS
    # =====================================================

    providers_requested = result.get(
        "providers_requested"
    )

    providers_used = result.get(
        "providers_used"
    )

    # =====================================================
    # PUBLIC API RESPONSE
    # =====================================================

    return {
        "status": result.get(
            "status"
        ),

        "answer": final_answer,

        "agreement_score": (
            agreement_score
        ),

        "threshold": threshold,

        "contradiction_detected": bool(
            result.get(
                "contradiction_detected",
                False,
            )
        ),

        "synthesis_provider": (
            result.get(
                "synthesis_provider"
            )
        ),

        "message": result.get(
            "message"
        ),

        "rounds": rounds,

        "difficulty": difficulty,

        "providers_requested": (
            providers_requested
        ),

        "providers_used": (
            providers_used
        ),
    }