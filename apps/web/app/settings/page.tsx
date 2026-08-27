"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

export default function SettingsPage() {
  const router = useRouter();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");

  const [threshold, setThreshold] = useState(85);
  const [providers, setProviders] = useState(2);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadAccount() {
      try {
        const {
          data: { user },
        } = await supabase.auth.getUser();

        if (!user) {
          router.replace("/login");
          return;
        }

        setEmail(user.email || "");

        setFullName(
          user.user_metadata?.full_name || ""
        );

        const savedThreshold =
          user.user_metadata?.verification_threshold;

        const savedProviders =
          user.user_metadata?.providers_count;

        if (
          typeof savedThreshold === "number"
        ) {
          setThreshold(savedThreshold);
        }

        if (
          typeof savedProviders === "number"
        ) {
          setProviders(savedProviders);
        }
      } catch (err) {
        console.error(err);
        setError(
          "Unable to load account information."
        );
      } finally {
        setLoading(false);
      }
    }

    loadAccount();
  }, [router]);

  async function saveSettings() {
    setError("");
    setMessage("");
    setSaving(true);

    try {
      const { error: updateError } =
        await supabase.auth.updateUser({
          data: {
            full_name: fullName.trim(),
            verification_threshold: threshold,
            providers_count: providers,
          },
        });

      if (updateError) {
        throw updateError;
      }

      setMessage("Settings saved successfully.");
    } catch (err) {
      console.error(err);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to save settings."
      );
    } finally {
      setSaving(false);
    }
  }

  async function changePassword() {
    setError("");
    setMessage("");

    if (!email) {
      setError("No email address found.");
      return;
    }

    setSaving(true);

    try {
      const { error: resetError } =
        await supabase.auth.resetPasswordForEmail(
          email,
          {
            redirectTo:
              `${window.location.origin}/reset-password`,
          }
        );

      if (resetError) {
        throw resetError;
      }

      setMessage(
        "Password reset instructions have been sent to your email."
      );
    } catch (err) {
      console.error(err);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to send password reset email."
      );
    } finally {
      setSaving(false);
    }
  }

  async function signOut() {
    setError("");

    const { error: signOutError } =
      await supabase.auth.signOut();

    if (signOutError) {
      setError(signOutError.message);
      return;
    }

    router.replace("/login");
    router.refresh();
  }

  async function deleteAccount() {
    const confirmed = window.confirm(
      "Are you sure you want to delete your account? This action cannot be undone."
    );

    if (!confirmed) {
      return;
    }

    setError(
      "Account deletion must be completed through the account administration flow."
    );
  }

  if (loading) {
    return (
      <main className="settings-page">
        <div className="settings-loading">
          Loading settings...
        </div>
      </main>
    );
  }

  return (
    <main className="settings-page">
      {/* HEADER */}

      <header className="settings-header">
        <div className="settings-header-inner">
          <Link
            href="/"
            className="settings-logo"
          >
            NEXVERITY
          </Link>

          <nav className="settings-nav">
            <Link href="/analyze">
              Analyze
            </Link>

            <Link href="/history">
              History
            </Link>

            <Link
              href="/settings"
              className="active"
            >
              Settings
            </Link>
          </nav>
        </div>
      </header>

      {/* CONTENT */}

      <section className="settings-main">
        <div className="settings-container">

          <div className="settings-heading">
            <span className="settings-eyebrow">
              ACCOUNT SETTINGS
            </span>

            <h1>
              Your settings.
            </h1>

            <p>
              Manage your account and verification
              preferences.
            </p>
          </div>

          {/* ACCOUNT */}

          <section className="settings-card">
            <div className="settings-card-heading">
              <div>
                <span className="settings-card-label">
                  ACCOUNT
                </span>

                <h2>
                  Account information
                </h2>
              </div>
            </div>

            <div className="settings-fields">

              <div className="settings-field">
                <label htmlFor="fullName">
                  Full name
                </label>

                <input
                  id="fullName"
                  type="text"
                  value={fullName}
                  onChange={(event) =>
                    setFullName(
                      event.target.value
                    )
                  }
                  placeholder="Your full name"
                />
              </div>

              <div className="settings-field">
                <label htmlFor="email">
                  Email address
                </label>

                <input
                  id="email"
                  type="email"
                  value={email}
                  disabled
                />

                <small>
                  Your email address is managed by
                  your authentication provider.
                </small>
              </div>

            </div>
          </section>

          {/* VERIFICATION */}

          <section className="settings-card">
            <div className="settings-card-heading">
              <div>
                <span className="settings-card-label">
                  VERIFICATION
                </span>

                <h2>
                  Verification preferences
                </h2>
              </div>
            </div>

            <div className="settings-fields">

              <div className="settings-field">
                <label htmlFor="threshold">
                  Agreement threshold
                </label>

                <div className="settings-range-row">
                  <input
                    id="threshold"
                    type="range"
                    min="50"
                    max="100"
                    step="1"
                    value={threshold}
                    onChange={(event) =>
                      setThreshold(
                        Number(
                          event.target.value
                        )
                      )
                    }
                  />

                  <strong>
                    {threshold}%
                  </strong>
                </div>

                <small>
                  Answers must reach this agreement
                  score to pass verification.
                </small>
              </div>

              <div className="settings-field">
                <label htmlFor="providers">
                  AI providers
                </label>

                <select
                  id="providers"
                  value={providers}
                  onChange={(event) =>
                    setProviders(
                      Number(
                        event.target.value
                      )
                    )
                  }
                >
                  <option value={2}>
                    2 providers
                  </option>

                  <option value={3}>
                    3 providers
                  </option>

                  <option value={4}>
                    4 providers
                  </option>
                </select>

                <small>
                  Number of independent AI providers
                  used during verification.
                </small>
              </div>

            </div>

            <button
              type="button"
              className="settings-save"
              onClick={saveSettings}
              disabled={saving}
            >
              {saving
                ? "Saving..."
                : "Save settings"}
            </button>
          </section>

          {/* SECURITY */}

          <section className="settings-card">
            <div className="settings-card-heading">
              <div>
                <span className="settings-card-label">
                  SECURITY
                </span>

                <h2>
                  Security
                </h2>
              </div>
            </div>

            <div className="settings-action-row">
              <div>
                <strong>
                  Change password
                </strong>

                <p>
                  Receive an email with instructions
                  to create a new password.
                </p>
              </div>

              <button
                type="button"
                className="settings-secondary"
                onClick={changePassword}
                disabled={saving}
              >
                Send reset email
              </button>
            </div>

            <div className="settings-action-row">
              <div>
                <strong>
                  Sign out
                </strong>

                <p>
                  Sign out of your NEXVERITY account
                  on this device.
                </p>
              </div>

              <button
                type="button"
                className="settings-secondary"
                onClick={signOut}
              >
                Sign out
              </button>
            </div>
          </section>

          {/* STATUS */}

          {(message || error) && (
            <div
              className={
                error
                  ? "settings-message settings-error"
                  : "settings-message"
              }
              role={
                error
                  ? "alert"
                  : "status"
              }
            >
              {error || message}
            </div>
          )}

          {/* DANGER */}

          <section className="settings-card settings-danger">
            <div className="settings-card-heading">
              <div>
                <span className="settings-card-label">
                  DANGER ZONE
                </span>

                <h2>
                  Delete account
                </h2>
              </div>
            </div>

            <p>
              Permanently delete your NEXVERITY
              account and associated account data.
            </p>

            <button
              type="button"
              className="settings-delete"
              onClick={deleteAccount}
            >
              Delete account
            </button>
          </section>

          {/* BACK */}

          <div className="settings-back">
            <Link href="/analyze">
              ← Back to verification
            </Link>
          </div>

        </div>
      </section>

      {/* FOOTER */}

      <footer className="settings-footer">
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