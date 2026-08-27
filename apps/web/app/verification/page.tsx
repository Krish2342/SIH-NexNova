"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

type ProviderResponse = {
  provider?: string;
  model?: string;
  answer?: string;
  latency_ms?: number;
};

type AnalysisResult = {
  status?: string;
  answer?: string;
  agreement_score?: number;
  threshold?: number;
  contradiction_detected?: boolean;
  synthesis_provider?: string;
  difficulty?: string;
  providers_requested?: number;
  providers_used?: number;
  rounds?: Array<{
    round?: number;
    agreement_score?: number;
    decision?: string;
    contradiction_detected?: boolean;
    responses?: ProviderResponse[];
  }>;
};

export default function VerificationPage() {
  const [result, setResult] =
    useState<AnalysisResult | null>(null);

  useEffect(() => {
    const stored =
      sessionStorage.getItem(
        "nexverity_analysis"
      );

    if (!stored) {
      return;
    }

    try {
      setResult(JSON.parse(stored));
    } catch (error) {
      console.error(
        "Unable to read analysis result:",
        error
      );
    }
  }, []);

  const score =
    typeof result?.agreement_score === "number"
      ? result.agreement_score
      : 0;

  const passed =
    result?.status === "PASS";

  const contradiction =
    result?.contradiction_detected === true;

  const responses =
    result?.rounds?.[0]?.responses || [];

  return (
    <main className="verification-page">
      {/* Background */}
      <div className="verification-background">
        <div className="verification-orb orb-one" />
        <div className="verification-orb orb-two" />
        <div className="verification-grid" />
      </div>

      <div className="verification-overlay" />

      {/* Header */}
      <header className="verification-header">
        <Link
          href="/"
          className="verification-logo"
        >
          NEXVERITY
        </Link>

        <div className="verification-header-actions">
          <Link href="/analyze">
            New verification
          </Link>

          <Link href="/history">
            History
          </Link>
        </div>
      </header>

      {/* Content */}
      <section className="verification-content">
        <div className="verification-container">

          {/* Status */}
          <div className="verification-status">
            <span
              className={
                passed
                  ? "status-dot status-pass"
                  : "status-dot status-review"
              }
            />

            <span>
              {passed
                ? "VERIFICATION PASSED"
                : "VERIFICATION REVIEW"}
            </span>
          </div>

          {/* Heading */}
          <h1 className="verification-title">
            Verified
            <br />
            <em>intelligence.</em>
          </h1>

          <p className="verification-subtitle">
            NEXVERITY compared independent AI
            responses and evaluated their agreement
            before producing this answer.
          </p>

          {/* Answer card */}
          <article className="verification-answer-card">

            <div className="answer-card-top">
              <span>
                VERIFIED ANSWER
              </span>

              <span className="answer-check">
                ✓
              </span>
            </div>

            <div className="answer-text">
              {result?.answer ||
                "No verification result found."}
            </div>

            <div className="answer-card-bottom">
              <span>
                SYNTHESIZED BY{" "}
                {(
                  result?.synthesis_provider ||
                  "NEXVERITY"
                ).toUpperCase()}
              </span>

              <span>
                {result?.difficulty
                  ? result.difficulty.toUpperCase()
                  : "ANALYSIS"}
              </span>
            </div>
          </article>

          {/* Metrics */}
          <div className="verification-metrics">

            <div className="metric-card">
              <span className="metric-label">
                AGREEMENT
              </span>

              <strong>
                {score.toFixed(2)}%
              </strong>

              <div className="metric-bar">
                <div
                  className="metric-bar-fill"
                  style={{
                    width: `${Math.min(
                      score,
                      100
                    )}%`,
                  }}
                />
              </div>

              <small>
                Threshold{" "}
                {result?.threshold ?? 85}%
              </small>
            </div>

            <div className="metric-card">
              <span className="metric-label">
                CONTRADICTION
              </span>

              <strong
                className={
                  contradiction
                    ? "metric-warning"
                    : "metric-good"
                }
              >
                {contradiction
                  ? "DETECTED"
                  : "NONE"}
              </strong>

              <small>
                Cross-provider consistency
              </small>
            </div>

            <div className="metric-card">
              <span className="metric-label">
                PROVIDERS
              </span>

              <strong>
                {result?.providers_used ?? 0}
              </strong>

              <small>
                of{" "}
                {result?.providers_requested ?? 0}{" "}
                requested
              </small>
            </div>
          </div>

          {/* Provider responses */}
          {responses.length > 0 && (
            <section className="provider-section">
              <div className="provider-heading">
                <span>
                  INDEPENDENT RESPONSES
                </span>

                <span>
                  {responses.length} PROVIDERS
                </span>
              </div>

              <div className="provider-list">
                {responses.map(
                  (response, index) => (
                    <article
                      className="provider-card"
                      key={`${response.provider}-${index}`}
                    >
                      <div className="provider-top">
                        <div>
                          <strong>
                            {(
                              response.provider ||
                              "Provider"
                            ).toUpperCase()}
                          </strong>

                          <small>
                            {response.model ||
                              "AI model"}
                          </small>
                        </div>

                        <span>
                          {response.latency_ms
                            ? `${Math.round(
                                response.latency_ms
                              )} ms`
                            : "—"}
                        </span>
                      </div>

                      <p>
                        {response.answer ||
                          "No response available."}
                      </p>
                    </article>
                  )
                )}
              </div>
            </section>
          )}

          {/* Actions */}
          <div className="verification-actions">
            <Link
              href="/analyze"
              className="verification-primary"
            >
              <span>
                Verify another question
              </span>

              <span>→</span>
            </Link>

            <Link
              href="/history"
              className="verification-secondary"
            >
              View history
            </Link>
          </div>

        </div>
      </section>

      {/* Footer */}
      <footer className="verification-footer">
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