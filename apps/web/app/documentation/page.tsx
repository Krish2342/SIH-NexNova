import Link from "next/link";
import NexverityBackground from "@/components/nexverity-background";

export default function DocumentationPage() {
  return (
    <main className="documentation-page">
      <NexverityBackground />

      <div
        className="documentation-overlay"
        aria-hidden="true"
      />

      {/* Header */}
      <header className="documentation-header">
        <div className="documentation-header-inner">
          <Link
            href="/"
            className="documentation-logo"
          >
            NEXVERITY
          </Link>

          <nav className="documentation-nav">
            <Link href="/analyze">
              Analyze
            </Link>

            <Link href="/history">
              History
            </Link>

            <Link href="/settings">
              Settings
            </Link>
          </nav>
        </div>
      </header>

      {/* Main */}
      <section className="documentation-main">
        <div className="documentation-container">

          {/* Intro */}
          <div className="documentation-intro">
            <span className="documentation-eyebrow">
              NEXVERITY ENGINE
            </span>

            <h1>
              Verified
              <br />
              <em>intelligence.</em>
            </h1>

            <p>
              Learn how NEXVERITY compares independent
              AI responses and turns them into a
              confidence-aware verification result.
            </p>
          </div>

          {/* Quick navigation */}
          <div className="documentation-links">
            <a href="#how-it-works">
              How it works
            </a>

            <a href="#agreement">
              Agreement score
            </a>

            <a href="#contradictions">
              Contradictions
            </a>

            <a href="#providers">
              AI providers
            </a>
          </div>

          {/* How it works */}
          <section
            id="how-it-works"
            className="documentation-section"
          >
            <div className="documentation-number">
              01
            </div>

            <div>
              <span className="documentation-label">
                VERIFICATION PROCESS
              </span>

              <h2>
                How NEXVERITY works
              </h2>

              <p>
                NEXVERITY takes a question and sends it
                through independent AI providers. Their
                responses are compared before the system
                produces a final synthesized answer.
              </p>

              <div className="documentation-steps">

                <article className="documentation-step">
                  <span>01</span>

                  <div>
                    <strong>
                      Submit a question
                    </strong>

                    <p>
                      Enter the question you want
                      NEXVERITY to verify.
                    </p>
                  </div>
                </article>

                <article className="documentation-step">
                  <span>02</span>

                  <div>
                    <strong>
                      Independent responses
                    </strong>

                    <p>
                      Multiple AI providers generate
                      their own answers independently.
                    </p>
                  </div>
                </article>

                <article className="documentation-step">
                  <span>03</span>

                  <div>
                    <strong>
                      Compare responses
                    </strong>

                    <p>
                      NEXVERITY evaluates agreement
                      and checks for contradictions.
                    </p>
                  </div>
                </article>

                <article className="documentation-step">
                  <span>04</span>

                  <div>
                    <strong>
                      Synthesize the result
                    </strong>

                    <p>
                      A final answer is produced from
                      the verification process.
                    </p>
                  </div>
                </article>

              </div>
            </div>
          </section>

          {/* Agreement */}
          <section
            id="agreement"
            className="documentation-section"
          >
            <div className="documentation-number">
              02
            </div>

            <div>
              <span className="documentation-label">
                AGREEMENT
              </span>

              <h2>
                Agreement score
              </h2>

              <p>
                The agreement score represents how
                closely the independent AI responses
                align with one another.
              </p>

              <div className="documentation-info-card">
                <div>
                  <strong>
                    85%
                  </strong>

                  <span>
                    Example verification threshold
                  </span>
                </div>

                <p>
                  A result reaching or exceeding the
                  configured threshold can be considered
                  a passing verification.
                </p>
              </div>

              <p>
                The score is a consistency signal, not
                a guarantee that every statement in an
                answer is factually correct.
              </p>
            </div>
          </section>

          {/* Contradictions */}
          <section
            id="contradictions"
            className="documentation-section"
          >
            <div className="documentation-number">
              03
            </div>

            <div>
              <span className="documentation-label">
                CONSISTENCY CHECK
              </span>

              <h2>
                Contradiction detection
              </h2>

              <p>
                NEXVERITY evaluates provider responses
                for meaningful disagreements. When
                conflicting information is detected,
                the verification result can be flagged
                for review.
              </p>

              <div className="documentation-status-grid">

                <div className="documentation-status-card">
                  <span className="documentation-status-dot good" />

                  <strong>
                    No contradiction
                  </strong>

                  <p>
                    Provider responses remain
                    consistent.
                  </p>
                </div>

                <div className="documentation-status-card">
                  <span className="documentation-status-dot warning" />

                  <strong>
                    Contradiction detected
                  </strong>

                  <p>
                    Providers contain potentially
                    conflicting information.
                  </p>
                </div>

              </div>
            </div>
          </section>

          {/* Providers */}
          <section
            id="providers"
            className="documentation-section"
          >
            <div className="documentation-number">
              04
            </div>

            <div>
              <span className="documentation-label">
                AI PROVIDERS
              </span>

              <h2>
                Independent AI responses
              </h2>

              <p>
                NEXVERITY is designed to reduce reliance
                on a single AI response by comparing
                outputs from multiple independent
                providers.
              </p>

              <p>
                Each provider response can include its
                model name, response time, and generated
                answer. These details are displayed in
                the verification result when available.
              </p>
            </div>
          </section>

          {/* Results */}
          <section className="documentation-section">
            <div className="documentation-number">
              05
            </div>

            <div>
              <span className="documentation-label">
                READING RESULTS
              </span>

              <h2>
                Understanding a verification
              </h2>

              <p>
                A verification result contains several
                signals that help you understand how
                confidently the system reached its
                answer.
              </p>

              <div className="documentation-result-list">

                <div>
                  <strong>
                    Verification status
                  </strong>

                  <span>
                    Indicates whether the result passed
                    the configured verification criteria.
                  </span>
                </div>

                <div>
                  <strong>
                    Agreement
                  </strong>

                  <span>
                    Shows how closely the provider
                    responses agree.
                  </span>
                </div>

                <div>
                  <strong>
                    Contradiction
                  </strong>

                  <span>
                    Indicates whether potentially
                    conflicting responses were detected.
                  </span>
                </div>

                <div>
                  <strong>
                    Providers
                  </strong>

                  <span>
                    Shows how many independent providers
                    participated in the analysis.
                  </span>
                </div>

              </div>
            </div>
          </section>

          {/* Important note */}
          <section className="documentation-note">
            <span>
              IMPORTANT
            </span>

            <h2>
              Verification is a confidence signal,
              not absolute truth.
            </h2>

            <p>
              AI systems can make mistakes. NEXVERITY
              is designed to provide an additional layer
              of consistency checking, but important
              information should still be independently
              verified before making consequential
              decisions.
            </p>
          </section>

          {/* Actions */}
          <div className="documentation-actions">
            <Link
              href="/analyze"
              className="documentation-primary"
            >
              Start a verification →
            </Link>

            <Link
              href="/status"
              className="documentation-secondary"
            >
              View system status
            </Link>
          </div>

        </div>
      </section>

      {/* Footer */}
      <footer className="documentation-footer">
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