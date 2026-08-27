"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import NexverityBackground from "@/components/nexverity-background";
import { supabase } from "@/lib/supabase";

export default function ResetPasswordPage() {
  const router = useRouter();

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [checkingSession, setCheckingSession] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    let mounted = true;

    async function checkSession() {
      const { data } = await supabase.auth.getSession();

      if (!mounted) return;

      if (!data.session) {
        setError(
          "Your password reset link is invalid or has expired. Please request a new reset link."
        );
      }

      setCheckingSession(false);
    }

    checkSession();

    return () => {
      mounted = false;
    };
  }, []);

  async function handleResetPassword(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const { error: updateError } =
        await supabase.auth.updateUser({
          password,
        });

      if (updateError) {
        setError(updateError.message);
        return;
      }

      setSuccess(
        "Your password has been updated successfully."
      );

      setPassword("");
      setConfirmPassword("");

      setTimeout(() => {
        router.push("/login");
        router.refresh();
      }, 1500);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to update your password. Please try again."
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
            <h1>Reset password.</h1>

            <p>
              Create a new secure password for your
              NEXVERITY account.
            </p>
          </div>

          {checkingSession ? (
            <div className="reset-loading">
              Checking reset session...
            </div>
          ) : (
            <form
              className="login-form"
              onSubmit={handleResetPassword}
            >
              {/* New password */}
              <div className="auth-field">
                <label htmlFor="password">
                  New password
                </label>

                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  placeholder="New password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  disabled={loading}
                  required
                />
              </div>

              {/* Confirm password */}
              <div className="auth-field">
                <label htmlFor="confirmPassword">
                  Confirm password
                </label>

                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  autoComplete="new-password"
                  placeholder="Confirm password"
                  value={confirmPassword}
                  onChange={(event) =>
                    setConfirmPassword(
                      event.target.value
                    )
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

              {/* Submit */}
              <button
                type="submit"
                className="auth-submit"
                disabled={
                  loading ||
                  checkingSession ||
                  Boolean(error)
                }
              >
                <span>
                  {loading
                    ? "Updating password..."
                    : "Update Password"}
                </span>

                {!loading && (
                  <span aria-hidden="true">
                    →
                  </span>
                )}
              </button>
            </form>
          )}

          {/* Back to login */}
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