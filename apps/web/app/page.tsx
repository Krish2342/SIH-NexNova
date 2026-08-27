"use client";

import { ArrowRight, Menu, Share2, ShieldCheck, Network, ScanSearch } from "lucide-react";

export default function Home() {
  return (
    <main className="nexverity-landing">
      {/* Background */}
      <video
        className="nexverity-video"
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

      <div className="nexverity-overlay" />

      {/* Header */}
      <header className="nexverity-header">
        <div className="nexverity-header-inner">
          <a href="/" className="nexverity-logo">
            NEXVERITY
          </a>

          <nav className="nexverity-nav">
            <a href="#features">Features</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#why-nexverity">Why NEXVERITY</a>
          </nav>

          <div className="nexverity-actions">
            <a href="/login" className="nexverity-login">
              Log In
            </a>

            <a href="/signup" className="nexverity-primary">
              Get Started
            </a>

            <button
              type="button"
              className="nexverity-menu"
              aria-label="Open menu"
            >
              <Menu size={20} />
            </button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="nexverity-hero">
        <div className="nexverity-hero-inner">
          <h1 className="nexverity-title">
            <span>AI answers aren't enough.</span>
            <span className="nexverity-title-italic">
              Verify before you trust.
            </span>
          </h1>

          <p className="nexverity-description">
            NEXVERITY verifies answers across multiple AI models, compares
            their reasoning, detects contradictions, and delivers a
            confidence-backed answer.
          </p>

          <div className="nexverity-cta">
            <a href="/analyze" className="nexverity-primary nexverity-start">
              Start Verifying
              <ArrowRight size={16} />
            </a>

            <a href="/help" className="nexverity-secondary">
              See how it works
            </a>
          </div>

          <p className="nexverity-philosophy">
            ONE QUESTION. MULTIPLE MODELS. ONE VERIFIED ANSWER.
          </p>

          <div className="nexverity-features" id="features">
            <div className="nexverity-feature">
              <Network size={15} />
              <span>MULTI-MODEL</span>
              <small>Independent AI responses</small>
            </div>

            <div className="nexverity-feature">
              <ShieldCheck size={15} />
              <span>VERIFICATION</span>
              <small>Semantic agreement scoring</small>
            </div>

            <div className="nexverity-feature">
              <ScanSearch size={15} />
              <span>DETECTION</span>
              <small>Cross-answer conflict detection</small>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="nexverity-footer">
        <span>© 2026 NEXVERITY. All rights reserved.</span>

        <div>
          <a href="/privacy">Privacy Policy</a>
          <a href="/terms">Terms of Service</a>
          <a href="#" aria-label="Share">
            <Share2 size={15} />
          </a>
        </div>
      </footer>
    </main>
  );
}