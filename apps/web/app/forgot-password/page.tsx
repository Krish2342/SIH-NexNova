"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import NexverityBackground from "@/components/nexverity-background";
import { supabase } from "@/lib/supabase";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleForgotPassword(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");
    setSuccess("");

    const trimmedEmail = email.trim();

    if (!trimmedEmail) {
      setError("Please enter your email address.");
      return;
    }

    setLoading(true);

    try {
      const { error: resetError } =
        await supabase.auth.resetPasswordForEmail(
          trimmedEmail,
          {
            redirectTo: `${window.location.origin}/reset-password`,
          }
        );

      if (resetError) {
        setError(resetError.message);
        return;
      }

      setSuccess(
        "Check your email for a password reset link."
      );
    } catch (err) {
      console.error(err);

      setError(
        "Unable to send the reset email. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <NexverityBackground />

      <div
        className="auth-background-overlay"
        aria-hidden="true"
      />

      {/* Header */}
      <header className="auth-header">
        <Link href="/" className="auth-brand">
          NEXVERITY
        </Link>
      </header>

      {/* Main */}
      <section className="auth-content">
        <div className="login-panel">
          <div className="login-heading">
            <h1>Forgot password.</h1>

            <p>
              Enter your email and we'll send you
              instructions to reset your password.
            </p>
          </div>

          <form
            className="login-form"
            onSubmit={handleForgotPassword}
          >
            <div className="auth-field">
              <label htmlFor="email">
                Email address
              </label>

              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                placeholder="Email address"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                disabled={loading}
                required
              />
            </div>

            {/* Error */}
            {error && (
              <div
                role="alert"
                className="auth-message auth-message-error"
              >
                {error}
              </div>
            )}

            {/* Success */}
            {success && (
              <div
                role="status"
                className="auth-message auth-message-success"
              >
                {success}
              </div>
            )}

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              <span>
                {loading
                  ? "Sending..."
                  : "Send Reset Link"}
              </span>

              {!loading && (
                <span aria-hidden="true">
                  →
                </span>
              )}
            </button>
          </form>

          <p className="auth-switch">
            Remember your password?{" "}
            <Link href="/login">
              Sign in
            </Link>
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="auth-footer">
        <span>
          SECURE PASSWORD RECOVERY
        </span>

        <div>
          <Link href="/privacy">
            Privacy Policy
          </Link>

          <Link href="/terms">
            Terms of Service
          </Link>
        </div>
      </footer>
    </main>
  );
}