from app.database.supabase import SupabaseService


def main():
    service = SupabaseService()

    print("Supabase client initialized successfully.")

    result = (
        service.client
        .table("analysis_runs")
        .select("id")
        .limit(1)
        .execute()
    )

    print("Supabase connection successful.")
    print("Rows:", result.data)


if __name__ == "__main__":
    main()