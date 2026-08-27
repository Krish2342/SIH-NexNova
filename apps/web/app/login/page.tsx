"use client";

import Link from "next/link";
import { useState } from "react";

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <main className="auth-page">
      {/* Same NEXVERITY background video */}
      <video
        className="auth-background-video"
        autoPlay
        muted
        loop
        playsInline
        aria-hidden="true"
      >
        <source
          src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260809_012548_ef22562c-c0ae-4816-ad9d-f8922af4e6a7.mp4"
          type="video/mp4"
        />
      </video>

      <div className="auth-background-overlay" />

      {/* Top logo */}
      <header className="auth-header">
        <Link href="/" className="auth-brand">
          NEXVERITY
        </Link>
      </header>

      {/* Center login */}
      <section className="auth-content">
        <div className="login-panel">
          <div className="login-heading">
            <h1>Welcome back.</h1>

            <p>
              Access your secure verification dashboard.
            </p>
          </div>

          <form className="login-form">
            {/* Email */}
            <div className="auth-field">
              <label htmlFor="email">
                Email address
              </label>

              <input
                id="email"
                name="email"
                type="email"
                placeholder="Email address"
                autoComplete="email"
                required
              />
            </div>

            {/* Password */}
            <div className="auth-field">
              <div className="password-label-row">
                <label htmlFor="password">
                  Password
                </label>

                <Link href="/forgot-password">
                  Forgot password?
                </Link>
              </div>

              <div className="password-input">
                <input
                  id="password"
                  name="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Password"
                  autoComplete="current-password"
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                >
                  {showPassword ? "◉" : "◌"}
                </button>
              </div>
            </div>

            {/* Sign in */}
            <button
              type="submit"
              className="auth-submit"
            >
              <span>Sign In</span>
              <span aria-hidden="true">→</span>
            </button>

            {/* Divider */}
            <div className="auth-divider">
              <span />
              <em>or</em>
              <span />
            </div>

            {/* Google */}
            <button
              type="button"
              className="google-button"
            >
              <span className="google-icon">
                G
              </span>

              <span>
                Continue with Google
              </span>
            </button>
          </form>

          {/* Signup */}
          <p className="auth-switch">
            Don't have an account?{" "}
            <Link href="/signup">
              Create an account
            </Link>
          </p>
        </div>
      </section>

      {/* Bottom information */}
      <footer className="auth-footer">
        <span>
          SECURE ACCESS TO NEXVERITY
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