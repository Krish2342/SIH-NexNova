from supabase import Client, create_client

from app.config import (
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_URL,
)


class SupabaseService:
    """
    Server-side Supabase database service for NEXVERITY.
    """

    def __init__(self):
        url = (SUPABASE_URL or "").strip()
        key = (SUPABASE_SERVICE_ROLE_KEY or "").strip()

        if not url:
            raise ValueError(
                "SUPABASE_URL is not configured."
            )

        if not key:
            raise ValueError(
                "SUPABASE_SERVICE_ROLE_KEY "
                "is not configured."
            )

        # -------------------------------------------------
        # Validate project URL.
        # -------------------------------------------------

        if not url.startswith(
            "https://"
        ):
            raise ValueError(
                "SUPABASE_URL must start with https://"
            )

        if "/rest/v1" in url:
            raise ValueError(
                "SUPABASE_URL must be the Supabase "
                "project URL only. Remove /rest/v1."
            )

        # Remove accidental trailing slash.
        url = url.rstrip("/")

        self.client: Client = create_client(
            url,
            key,
        )

    # =====================================================
    # ANALYSIS RUN
    # =====================================================

    def create_analysis_run(
        self,
        data: dict,
    ) -> dict:

        response = (
            self.client
            .table("analysis_runs")
            .insert(data)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                "Failed to create analysis run."
            )

        return response.data[0]

    # =====================================================
    # PROVIDER RESPONSE
    # =====================================================

    def create_provider_response(
        self,
        data: dict,
    ) -> dict:

        response = (
            self.client
            .table("provider_responses")
            .insert(data)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                "Failed to save provider response."
            )

        return response.data[0]

    # =====================================================
    # VERIFICATION ROUND
    # =====================================================

    def create_verification_round(
        self,
        data: dict,
    ) -> dict:

        response = (
            self.client
            .table("verification_rounds")
            .insert(data)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                "Failed to save verification round."
            )

        return response.data[0]

    # =====================================================
    # COMPARISON
    # =====================================================

    def create_comparison(
        self,
        data: dict,
    ) -> dict:

        response = (
            self.client
            .table("comparisons")
            .insert(data)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                "Failed to save comparison."
            )

        return response.data[0]

    # =====================================================
    # CONTRADICTION
    # =====================================================

    def create_contradiction(
        self,
        data: dict,
    ) -> dict:

        response = (
            self.client
            .table("contradictions")
            .insert(data)
            .execute()
        )

        if not response.data:
            raise RuntimeError(
                "Failed to save contradiction."
            )

        return response.data[0]