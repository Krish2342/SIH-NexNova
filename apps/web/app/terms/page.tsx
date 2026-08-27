import Link from "next/link";

export default function TermsPage() {
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
              Terms of
              <br />
              <em>Service.</em>
            </h1>

            <p>
              These terms explain the rules for using
              NEXVERITY and the verification services
              provided through the platform.
            </p>

            <span className="legal-updated">
              Last updated: August 27, 2026
            </span>
          </div>

          <article className="legal-document">

            <section className="legal-section">
              <span>01</span>

              <div>
                <h2>Acceptance of terms</h2>

                <p>
                  By creating an account or using
                  NEXVERITY, you agree to these Terms of
                  Service and our Privacy Policy.
                </p>

                <p>
                  If you do not agree with these terms,
                  please do not use the service.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>02</span>

              <div>
                <h2>The NEXVERITY service</h2>

                <p>
                  NEXVERITY is a verification platform
                  that compares responses from multiple
                  AI providers and evaluates their
                  consistency.
                </p>

                <p>
                  The service may generate agreement
                  scores, identify potential contradictions,
                  and produce a synthesized answer.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>03</span>

              <div>
                <h2>AI-generated information</h2>

                <p>
                  NEXVERITY uses third-party AI systems to
                  generate and compare responses.
                </p>

                <p>
                  Verification results are intended to
                  provide additional confidence and
                  consistency analysis. They should not be
                  treated as an absolute guarantee that
                  information is correct.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>04</span>

              <div>
                <h2>User accounts</h2>

                <p>
                  You are responsible for providing
                  accurate account information and keeping
                  your authentication credentials secure.
                </p>

                <p>
                  You are responsible for activity that
                  occurs through your account unless the
                  activity resulted from unauthorized access
                  that you could not reasonably prevent.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>05</span>

              <div>
                <h2>Acceptable use</h2>

                <p>
                  You agree to use NEXVERITY lawfully and
                  responsibly.
                </p>

                <p>
                  You must not attempt to disrupt the
                  service, bypass security controls,
                  interfere with other users, abuse
                  third-party AI services, or use the
                  platform for unlawful purposes.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>06</span>

              <div>
                <h2>Submitted content</h2>

                <p>
                  You retain responsibility for questions,
                  prompts, and other content that you submit
                  to NEXVERITY.
                </p>

                <p>
                  You should not submit confidential,
                  sensitive, or personally identifying
                  information unless you have a legitimate
                  reason and are comfortable with the
                  processing required to provide the service.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>07</span>

              <div>
                <h2>Third-party providers</h2>

                <p>
                  NEXVERITY may depend on external services
                  for authentication, AI processing,
                  hosting, infrastructure, and other
                  functionality.
                </p>

                <p>
                  Availability and performance of those
                  services may affect the availability of
                  NEXVERITY.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>08</span>

              <div>
                <h2>Service availability</h2>

                <p>
                  We may modify, suspend, or discontinue
                  parts of the service when necessary for
                  maintenance, security, improvements, or
                  other operational reasons.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>09</span>

              <div>
                <h2>Intellectual property</h2>

                <p>
                  NEXVERITY branding, interface design,
                  software, visual elements, and other
                  platform materials are protected by
                  applicable intellectual property laws.
                </p>

                <p>
                  You may not copy, reproduce, modify,
                  distribute, or commercially exploit
                  platform materials without appropriate
                  authorization.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>10</span>

              <div>
                <h2>Account termination</h2>

                <p>
                  You may stop using NEXVERITY at any time.
                </p>

                <p>
                  Access may be restricted or terminated
                  when necessary to protect the service,
                  users, infrastructure, or to address
                  violations of these terms.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>11</span>

              <div>
                <h2>Disclaimer</h2>

                <p>
                  NEXVERITY is provided on an
                  availability basis. AI-generated
                  information can contain errors,
                  omissions, or outdated information.
                </p>

                <p>
                  You should independently verify important
                  information before relying on it for
                  decisions involving significant financial,
                  legal, medical, safety, or other
                  consequences.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>12</span>

              <div>
                <h2>Limitation of responsibility</h2>

                <p>
                  To the extent permitted by applicable law,
                  NEXVERITY is not responsible for decisions
                  made solely on the basis of AI-generated
                  answers or verification scores.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>13</span>

              <div>
                <h2>Changes to these terms</h2>

                <p>
                  These Terms of Service may be updated
                  from time to time. Updated terms will be
                  made available through the NEXVERITY
                  application.
                </p>
              </div>
            </section>

            <section className="legal-section">
              <span>14</span>

              <div>
                <h2>Contact</h2>

                <p>
                  If you have questions about these terms
                  or the NEXVERITY service, please contact
                  the NEXVERITY team through the support
                  channel provided by the application.
                </p>
              </div>
            </section>

          </article>

          <div className="legal-actions">
            <Link href="/privacy">
              ← Privacy Policy
            </Link>

            <Link href="/analyze">
              Back to verification →
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