import Link from "next/link";

export default function StatusPage() {
  return (
    <main className="status-page">
      <header className="status-header">
        <div className="status-header-inner">
          <Link href="/" className="status-logo">
            NEXVERITY
          </Link>

          <nav className="status-nav">
            <Link href="/analyze">Analyze</Link>
            <Link href="/history">History</Link>
            <Link href="/settings">Settings</Link>
          </nav>
        </div>
      </header>

      <section className="status-main">
        <div className="status-container">

          <div className="status-intro">
            <span className="status-eyebrow">
              SYSTEM STATUS
            </span>

            <h1>
              Everything is
              <br />
              <em>operational.</em>
            </h1>

            <p>
              Current status of the NEXVERITY
              verification engine and its core services.
            </p>
          </div>

          <div className="status-overall">
            <div className="status-indicator">
              <span className="status-live-dot" />

              <div>
                <strong>
                  All systems operational
                </strong>

                <span>
                  No known incidents
                </span>
              </div>
            </div>

            <span className="status-time">
              CURRENT STATUS
            </span>
          </div>

          <section className="status-services">

            <div className="status-section-heading">
              <span>CORE SERVICES</span>
              <span>STATUS</span>
            </div>

            <article className="status-service">
              <div>
                <strong>
                  Verification Engine
                </strong>

                <p>
                  Processes questions and evaluates
                  agreement between AI providers.
                </p>
              </div>

              <span className="service-state">
                Operational
              </span>
            </article>

            <article className="status-service">
              <div>
                <strong>
                  AI Provider Connections
                </strong>

                <p>
                  Connections used to obtain independent
                  provider responses.
                </p>
              </div>

              <span className="service-state">
                Operational
              </span>
            </article>

            <article className="status-service">
              <div>
                <strong>
                  Authentication
                </strong>

                <p>
                  Account sign-in, registration, and
                  password recovery services.
                </p>
              </div>

              <span className="service-state">
                Operational
              </span>
            </article>

            <article className="status-service">
              <div>
                <strong>
                  Verification History
                </strong>

                <p>
                  Storage and retrieval of previous
                  verification activity.
                </p>
              </div>

              <span className="service-state">
                Operational
              </span>
            </article>

            <article className="status-service">
              <div>
                <strong>
                  Web Application
                </strong>

                <p>
                  NEXVERITY dashboard and user interface.
                </p>
              </div>

              <span className="service-state">
                Operational
              </span>
            </article>

          </section>

          <section className="status-note">
            <span className="status-note-label">
              ABOUT THIS PAGE
            </span>

            <p>
              This page provides a general overview of
              NEXVERITY service availability. Individual
              verification requests may occasionally be
              affected by third-party provider availability,
              network conditions, or maintenance.
            </p>
          </section>

          <div className="status-actions">
            <Link
              href="/analyze"
              className="status-primary"
            >
              Start a verification →
            </Link>

            <Link
              href="/"
              className="status-secondary"
            >
              Back home
            </Link>
          </div>

        </div>
      </section>

      <footer className="status-footer">
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