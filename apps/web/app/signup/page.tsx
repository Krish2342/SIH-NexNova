"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import NexverityBackground from "@/components/nexverity-background";
import { supabase } from "@/lib/supabase";

export default function SignupPage() {
  const router = useRouter();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [acceptedTerms, setAcceptedTerms] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSignup(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (!fullName.trim()) {
      setError("Please enter your full name.");
      return;
    }

    if (!email.trim()) {
      setError("Please enter your email address.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (!acceptedTerms) {
      setError(
        "Please accept the Terms of Service and Privacy Policy."
      );
      return;
    }

    setLoading(true);

    try {
      const { data, error: signupError } =
        await supabase.auth.signUp({
          email: email.trim(),
          password,
          options: {
            data: {
              full_name: fullName.trim(),
            },
          },
        });

      if (signupError) {
        setError(signupError.message);
        return;
      }

      if (data.session) {
        router.push("/analyze");
        router.refresh();
        return;
      }

      setSuccess(
        "Account created. Check your email to confirm your account, then sign in."
      );
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function handleGoogleSignup() {
    setError("");
    setSuccess("");

    if (!acceptedTerms) {
      setError(
        "Please accept the Terms of Service and Privacy Policy."
      );
      return;
    }

    setLoading(true);

    try {
      const { error: googleError } =
        await supabase.auth.signInWithOAuth({
          provider: "google",
          options: {
            redirectTo:
              `${window.location.origin}/auth/callback`,
          },
        });

      if (googleError) {
        setError(googleError.message);
        setLoading(false);
      }
    } catch (err) {
      console.error(err);
      setError("Unable to continue with Google.");
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

      <header className="auth-header">
        <Link href="/" className="auth-brand">
          NEXVERITY
        </Link>
      </header>

      <section className="auth-content">
        <div className="login-panel">
          <div className="login-heading">
            <h1>Create account.</h1>

            <p>
              Create your secure verification account.
            </p>
          </div>

          <form
            className="login-form"
            onSubmit={handleSignup}
          >
            <div className="auth-field">
              <label htmlFor="fullName">
                Full name
              </label>

              <input
                id="fullName"
                name="fullName"
                type="text"
                autoComplete="name"
                placeholder="Full name"
                value={fullName}
                onChange={(event) =>
                  setFullName(event.target.value)
                }
                disabled={loading}
              />
            </div>

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
              />
            </div>

            <div className="auth-field">
              <label htmlFor="password">
                Password
              </label>

              <div className="password-input">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  placeholder="Password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  disabled={loading}
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="confirmPassword">
                Confirm password
              </label>

              <div className="password-input">
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  autoComplete="new-password"
                  placeholder="Confirm password"
                  value={confirmPassword}
                  onChange={(event) =>
                    setConfirmPassword(event.target.value)
                  }
                  disabled={loading}
                />
              </div>
            </div>

            <label
              htmlFor="terms"
              className="flex items-start gap-2 cursor-pointer mt-1"
            >
              <input
                id="terms"
                type="checkbox"
                checked={acceptedTerms}
                onChange={(event) =>
                  setAcceptedTerms(
                    event.target.checked
                  )
                }
                disabled={loading}
                className="mt-0.5 h-3.5 w-3.5 shrink-0 accent-white"
              />

              <span className="text-[9px] leading-[1.45] text-white/45">
                I agree to the{" "}
                <Link
                  href="/terms"
                  className="text-white/75 hover:text-white transition-colors"
                >
                  Terms of Service
                </Link>{" "}
                and{" "}
                <Link
                  href="/privacy"
                  className="text-white/75 hover:text-white transition-colors"
                >
                  Privacy Policy
                </Link>
                .
              </span>
            </label>

            {error && (
              <div
                role="alert"
                className="rounded-xl border border-red-400/20 bg-red-400/10 px-3 py-2 text-center text-[10px] leading-4 text-red-200"
              >
                {error}
              </div>
            )}

            {success && (
              <div
                role="status"
                className="rounded-xl border border-white/15 bg-white/5 px-3 py-2 text-center text-[10px] leading-4 text-white/70"
              >
                {success}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="auth-submit disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading
                ? "Creating account..."
                : "Create Account"}

              {!loading && <span>→</span>}
            </button>

            <div className="auth-divider">
              <span />
              <em>or</em>
              <span />
            </div>

            <button
              type="button"
              className="google-button disabled:cursor-not-allowed disabled:opacity-60"
              onClick={handleGoogleSignup}
              disabled={loading}
            >
              <span className="google-icon">G</span>

              <span>
                Continue with Google
              </span>
            </button>
          </form>

          <p className="auth-switch">
            Already have an account?{" "}
            <Link href="/login">
              Sign in
            </Link>
          </p>
        </div>
      </section>

      <footer className="auth-footer">
        <span>SECURE AUTHENTICATION</span>

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