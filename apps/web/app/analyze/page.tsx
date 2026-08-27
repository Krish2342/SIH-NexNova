"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import NexverityBackground from "@/components/nexverity-background";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export default function AnalyzePage() {
  const router = useRouter();

  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      setError("Please enter a question.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/v1/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: trimmedQuestion,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            data?.message ||
            "Analysis failed."
        );
      }

      sessionStorage.setItem(
        "nexverity_analysis",
        JSON.stringify(data)
      );

      router.push("/verification");
    } catch (err) {
      console.error(err);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to analyze the question."
      );
    } finally {
      setLoading(false);
    }
  }

  function useExample(example: string) {
    setQuestion(example);
    setError("");
  }

  return (
    <main className="auth-page">
      <NexverityBackground />

      <div
        className="auth-background-overlay"
        aria-hidden="true"
      />

      {/* Header */}
      <header className="nexverity-header">
        <div className="nexverity-header-inner">
          <Link
            href="/"
            className="nexverity-logo"
          >
            NEXVERITY
          </Link>

          <nav className="nexverity-nav">
            <Link href="/analyze">
              Analyze
            </Link>

            <Link href="/history">
              History
            </Link>
          </nav>

          <div className="nexverity-actions">
            <Link
              href="/settings"
              className="nexverity-login"
            >
              Settings
            </Link>
          </div>
        </div>
      </header>

      {/* Main */}
      <section className="auth-content">
        <div
          style={{
            width: "min(760px, 94vw)",
            textAlign: "center",
          }}
        >
          <div
            style={{
              marginBottom: "12px",
              color: "rgba(255,255,255,0.45)",
              fontSize: "10px",
              fontWeight: 600,
              letterSpacing: "0.18em",
              textTransform: "uppercase",
            }}
          >
            NEXVERITY ENGINE
          </div>

          <h1
            style={{
              margin: 0,
              color: "#fff",
              fontFamily:
                'Georgia, "Times New Roman", serif',
              fontSize:
                "clamp(46px, 7vw, 76px)",
              fontWeight: 400,
              lineHeight: 1,
              letterSpacing: "-0.045em",
            }}
          >
            Ask anything.
          </h1>

          <p
            style={{
              margin:
                "18px auto 0",
              maxWidth: "500px",
              color:
                "rgba(255,255,255,0.62)",
              fontSize: "14px",
              lineHeight: 1.5,
            }}
          >
            Multiple models. One verified answer.
          </p>

          {/* Question box */}
          <form
            onSubmit={handleAnalyze}
            style={{
              width: "100%",
              marginTop: "42px",
              overflow: "hidden",
              border:
                "1px solid rgba(255,255,255,0.15)",
              borderRadius: "18px",
              background:
                "rgba(0,0,0,0.48)",
              backdropFilter: "blur(18px)",
              WebkitBackdropFilter:
                "blur(18px)",
              boxShadow:
                "0 25px 80px rgba(0,0,0,0.45)",
              textAlign: "left",
            }}
          >
            <textarea
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              placeholder="Ask a question you want NEXVERITY to verify..."
              disabled={loading}
              rows={5}
              style={{
                width: "100%",
                resize: "none",
                border: 0,
                outline: "none",
                padding: "24px",
                background:
                  "transparent",
                color: "#fff",
                fontSize: "14px",
                lineHeight: 1.6,
              }}
            />

            <div
              style={{
                minHeight: "58px",
                padding:
                  "10px 14px 10px 20px",
                display: "flex",
                alignItems: "center",
                justifyContent:
                  "space-between",
                gap: "16px",
                borderTop:
                  "1px solid rgba(255,255,255,0.08)",
              }}
            >
              <span
                style={{
                  color:
                    "rgba(255,255,255,0.4)",
                  fontSize: "9px",
                  letterSpacing:
                    "0.03em",
                }}
              >
                NEXVERITY WILL CROSS-CHECK
                YOUR QUESTION ACROSS
                AVAILABLE AI PROVIDERS.
              </span>

              <button
                type="submit"
                disabled={loading}
                style={{
                  width: "42px",
                  height: "42px",
                  flexShrink: 0,
                  border: 0,
                  borderRadius: "50%",
                  background: "#fff",
                  color: "#000",
                  fontSize: "18px",
                  cursor: loading
                    ? "not-allowed"
                    : "pointer",
                  opacity: loading
                    ? 0.55
                    : 1,
                }}
              >
                {loading ? "…" : "→"}
              </button>
            </div>
          </form>

          {/* Error */}
          {error && (
            <div
              role="alert"
              style={{
                marginTop: "14px",
                padding:
                  "10px 14px",
                border:
                  "1px solid rgba(255,100,100,0.2)",
                borderRadius: "12px",
                background:
                  "rgba(255,70,70,0.08)",
                color:
                  "rgba(255,190,190,0.9)",
                fontSize: "11px",
              }}
            >
              {error}
            </div>
          )}

          {/* Examples */}
          <div
            style={{
              marginTop: "30px",
            }}
          >
            <div
              style={{
                marginBottom: "12px",
                color:
                  "rgba(255,255,255,0.38)",
                fontSize: "9px",
                fontWeight: 600,
                letterSpacing:
                  "0.16em",
                textTransform:
                  "uppercase",
              }}
            >
              Try an example
            </div>

            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                justifyContent:
                  "center",
                gap: "8px",
              }}
            >
              <button
                type="button"
                onClick={() =>
                  useExample(
                    "What is the capital of Japan?"
                  )
                }
                style={{
                  padding:
                    "9px 14px",
                  border:
                    "1px solid rgba(255,255,255,0.12)",
                  borderRadius: "999px",
                  background:
                    "rgba(0,0,0,0.25)",
                  color:
                    "rgba(255,255,255,0.7)",
                  fontSize: "10px",
                  cursor: "pointer",
                }}
              >
                What is the capital of Japan?
              </button>

              <button
                type="button"
                onClick={() =>
                  useExample(
                    "Explain quantum computing simply."
                  )
                }
                style={{
                  padding:
                    "9px 14px",
                  border:
                    "1px solid rgba(255,255,255,0.12)",
                  borderRadius: "999px",
                  background:
                    "rgba(0,0,0,0.25)",
                  color:
                    "rgba(255,255,255,0.7)",
                  fontSize: "10px",
                  cursor: "pointer",
                }}
              >
                Explain quantum computing simply.
              </button>

              <button
                type="button"
                onClick={() =>
                  useExample(
                    "Compare two competing technologies."
                  )
                }
                style={{
                  padding:
                    "9px 14px",
                  border:
                    "1px solid rgba(255,255,255,0.12)",
                  borderRadius: "999px",
                  background:
                    "rgba(0,0,0,0.25)",
                  color:
                    "rgba(255,255,255,0.7)",
                  fontSize: "10px",
                  cursor: "pointer",
                }}
              >
                Compare two competing technologies.
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="auth-footer">
        <span>
          NEXVERITY ENGINE | SYSTEM STATE: OPTIMAL
        </span>

        <div>
          <Link href="/status">
            Status
          </Link>

          <Link href="/documentation">
            Documentation
          </Link>

          <Link href="/privacy">
            Privacy
          </Link>
        </div>
      </footer>
    </main>
  );
}