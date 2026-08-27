import Link from "next/link";

export default function PrivacyPage() {
  return (
    <main className="legal-page">
      <header className="legal-header">
        <div className="legal-header-inner">
          <Link href="/" className="legal-logo">
            NEXVERITY
          </Link>

          <nav className="legal-nav">
            <Link href="/analyze">Analyze</Link>
            <Link href="/history">History</Link>
            <Link href="/settings">Settings</Link>
          </nav>
        </div>
      </header>

      <section className="legal-main">
        <div className="legal-container">

          <div className="legal-intro">
            <span className="legal-eyebrow">
              NEXVERITY
            </span>

            <h1>
              Privacy
              <br />
              <em>Policy.</em>
            </h1>

            <p>
              Your privacy matters. This policy explains
              what information NEXVERITY collects, how it
              is used, and how it is protected.
            </p>

            <span className="legal-updated">
              Last updated: August 27, 2026
            </span>
          </div>

          <article className="legal-document">

            <section className="legal-section">
              <span>01</span>

              <div>
                <h2>Information we collect</h2>

                <p>
                  When you create a NEXVERITY account,
                  we may collect information such as your
                  name and email address.
                </p>

                <p>
                  When you use the verification engine,
                  we may store the questions you submit,
                  verification results, provider responses,
                  agreement scores, and related analysis
                  information.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>02</span>

              <div>
                <h2>How we use your information</h2>

                <p>
                  We use account information to provide,
                  maintain, and secure your NEXVERITY
                  account.
                </p>

                <p>
                  Verification data is used to process
                  questions, compare independent AI
                  responses, calculate agreement, detect
                  contradictions, and provide verification
                  results.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>03</span>

              <div>
                <h2>AI providers</h2>

                <p>
                  NEXVERITY may send submitted questions
                  to third-party AI providers in order to
                  perform independent analysis.
                </p>

                <p>
                  The responses returned by those providers
                  may be processed by the NEXVERITY
                  verification engine to evaluate
                  consistency and produce a final result.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>04</span>

              <div>
                <h2>Verification history</h2>

                <p>
                  Your verification history may include
                  submitted questions, final answers,
                  agreement scores, provider information,
                  timestamps, and other information required
                  to display previous verification activity.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>05</span>

              <div>
                <h2>Cookies and local storage</h2>

                <p>
                  NEXVERITY may use browser storage,
                  cookies, or similar technologies to
                  maintain authentication sessions and
                  provide application functionality.
                </p>

                <p>
                  Temporary browser storage may also be
                  used to transfer verification results
                  between pages of the application.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>06</span>

              <div>
                <h2>Account security</h2>

                <p>
                  We take reasonable measures to protect
                  account information and application data.
                  Authentication is handled through the
                  configured authentication provider.
                </p>

                <p>
                  You are responsible for keeping your
                  account credentials confidential and for
                  notifying us if you believe your account
                  has been accessed without authorization.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>07</span>

              <div>
                <h2>Data retention</h2>

                <p>
                  Account and verification information may
                  be retained for as long as necessary to
                  provide the service, maintain verification
                  history, comply with applicable obligations,
                  and protect the security of the platform.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>08</span>

              <div>
                <h2>Your choices</h2>

                <p>
                  You may access and update certain account
                  information through your account settings.
                </p>

                <p>
                  You may also sign out of your account or
                  request assistance with account-related
                  information where applicable.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>09</span>

              <div>
                <h2>Third-party services</h2>

                <p>
                  NEXVERITY may rely on third-party services
                  for authentication, AI processing,
                  infrastructure, analytics, or other
                  functionality.
                </p>

                <p>
                  Those services may process information
                  according to their own privacy policies
                  and terms.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>10</span>

              <div>
                <h2>Changes to this policy</h2>

                <p>
                  We may update this Privacy Policy from
                  time to time. When changes are made, the
                  updated version will be made available
                  through NEXVERITY.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>11</span>

              <div>
                <h2>Contact</h2>

                <p>
                  If you have questions about this Privacy
                  Policy or the handling of your information,
                  please contact the NEXVERITY team through
                  the support channel provided by the
                  application.
                </p>
              </div>
            </section>

          </article>

          <div className="legal-actions">
            <Link href="/terms">
              Read Terms of Service →
            </Link>

            <Link href="/analyze">
              ← Back to NEXVERITY
            </Link>
          </div>

        </div>
      </section>

      <footer className="legal-footer">
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