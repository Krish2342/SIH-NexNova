"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

type AnalysisRun = {
  id: string;
  question: string;
  status: string;
  final_answer: string | null;
  agreement_score: number | null;
  threshold: number | null;
  contradiction_detected: boolean | null;
  synthesis_provider: string | null;
  difficulty: string | null;
  providers_requested: number | null;
  providers_used: number | null;
  message: string | null;
  created_at: string;
};

export default function HistoryPage() {
  const [runs, setRuns] = useState<AnalysisRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    setLoading(true);
    setError("");

    const { data, error } = await supabase
      .from("analysis_runs")
      .select(`
        id,
        question,
        status,
        final_answer,
        agreement_score,
        threshold,
        contradiction_detected,
        synthesis_provider,
        difficulty,
        providers_requested,
        providers_used,
        message,
        created_at
      `)
      .order("created_at", {
        ascending: false,
      });

    if (error) {
      console.error("History error:", error);
      setError(error.message);
      setLoading(false);
      return;
    }

    setRuns(data ?? []);
    setLoading(false);
  }

  function formatDate(value: string) {
    return new Date(value).toLocaleString(
      undefined,
      {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }
    );
  }

  function getScore(run: AnalysisRun) {
    if (
      typeof run.agreement_score !==
      "number"
    ) {
      return "—";
    }

    return `${run.agreement_score.toFixed(2)}%`;
  }

  return (
    <main className="history-page">
      <div className="history-background">
        <div className="history-glow history-glow-one" />
        <div className="history-glow history-glow-two" />
        <div className="history-grid" />
      </div>

      <div className="history-overlay" />

      {/* Header */}
      <header className="history-header">
        <Link
          href="/"
          className="history-logo"
        >
          NEXVERITY
        </Link>

        <nav className="history-nav">
          <Link href="/analyze">
            New verification
          </Link>

          <Link
            href="/history"
            className="history-nav-active"
          >
            History
          </Link>
        </nav>
      </header>

      {/* Main */}
      <section className="history-content">
        <div className="history-container">

          <div className="history-intro">
            <div className="history-eyebrow">
              VERIFICATION HISTORY
            </div>

            <h1>
              Your verified
              <br />
              <em>intelligence.</em>
            </h1>

            <p>
              Review previous questions,
              verification scores, provider
              agreement, and final answers.
            </p>
          </div>

          {/* Loading */}
          {loading && (
            <div className="history-state">
              <div className="history-spinner" />
              <p>
                Loading verification history...
              </p>
            </div>
          )}

          {/* Error */}
          {!loading && error && (
            <div className="history-error">
              <strong>
                Unable to load history
              </strong>

              <p>{error}</p>

              <button
                onClick={loadHistory}
              >
                Try again
              </button>
            </div>
          )}

          {/* Empty */}
          {!loading &&
            !error &&
            runs.length === 0 && (
              <div className="history-empty">
                <div className="history-empty-icon">
                  N
                </div>

                <h2>
                  No verification history yet.
                </h2>

                <p>
                  Run your first verification
                  to see it appear here.
                </p>

                <Link
                  href="/analyze"
                  className="history-primary"
                >
                  Start verifying →
                </Link>
              </div>
            )}

          {/* History list */}
          {!loading &&
            !error &&
            runs.length > 0 && (
              <div className="history-list">

                <div className="history-list-header">
                  <span>
                    {runs.length} VERIFICATION
                    {runs.length === 1
                      ? ""
                      : "S"}
                  </span>

                  <button
                    onClick={loadHistory}
                    className="history-refresh"
                  >
                    Refresh
                  </button>
                </div>

                {runs.map((run) => {
                  const passed =
                    run.status === "PASS";

                  return (
                    <article
                      key={run.id}
                      className="history-card"
                    >
                      <div className="history-card-top">

                        <div className="history-status">
                          <span
                            className={
                              passed
                                ? "history-status-dot passed"
                                : "history-status-dot review"
                            }
                          />

                          <span>
                            {passed
                              ? "VERIFIED"
                              : run.status}
                          </span>
                        </div>

                        <time>
                          {formatDate(
                            run.created_at
                          )}
                        </time>
                      </div>

                      <h2>
                        {run.question}
                      </h2>

                      {run.final_answer && (
                        <p className="history-answer">
                          {run.final_answer}
                        </p>
                      )}

                      <div className="history-card-footer">

                        <div className="history-meta">

                          <div>
                            <span>
                              AGREEMENT
                            </span>

                            <strong>
                              {getScore(run)}
                            </strong>
                          </div>

                          <div>
                            <span>
                              CONTRADICTION
                            </span>

                            <strong>
                              {run.contradiction_detected
                                ? "DETECTED"
                                : "NONE"}
                            </strong>
                          </div>

                          <div>
                            <span>
                              PROVIDERS
                            </span>

                            <strong>
                              {run.providers_used ??
                                "—"}
                            </strong>
                          </div>

                          <div>
                            <span>
                              SYNTHESIS
                            </span>

                            <strong>
                              {run.synthesis_provider
                                ? run.synthesis_provider.toUpperCase()
                                : "—"}
                            </strong>
                          </div>

                        </div>

                        <Link
                          href={`/verification?id=${run.id}`}
                          className="history-view"
                        >
                          View →
                        </Link>

                      </div>
                    </article>
                  );
                })}
              </div>
            )}

        </div>
      </section>

      {/* Footer */}
      <footer className="history-footer">
        <span>
          NEXVERITY VERIFICATION ENGINE
        </span>

        <div>
          <Link href="/privacy">
            Privacy
          </Link>

          <Link href="/terms">
            Terms
          </Link>
        </div>
      </footer>
    </main>
  );
}