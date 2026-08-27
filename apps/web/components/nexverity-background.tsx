"use client";

import { useEffect, useRef } from "react";

const VIDEO_URL =
  "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260809_012548_ef22562c-c0ae-4816-ad9d-f8922af4e6a7.mp4";

export default function NexverityBackground() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const fadeFrameRef = useRef<number | null>(null);
  const fadingOutRef = useRef(false);

  useEffect(() => {
    const video = videoRef.current;

    if (!video) return;

    const cancelFade = () => {
      if (fadeFrameRef.current !== null) {
        cancelAnimationFrame(fadeFrameRef.current);
        fadeFrameRef.current = null;
      }
    };

    const animateOpacity = (
      target: number,
      duration: number
    ) => {
      cancelFade();

      const startOpacity =
        Number.parseFloat(video.style.opacity || "0");

      const startTime = performance.now();

      const frame = (now: number) => {
        const progress = Math.min(
          (now - startTime) / duration,
          1
        );

        const eased =
          progress < 0.5
            ? 2 * progress * progress
            : 1 -
              Math.pow(
                -2 * progress + 2,
                2
              ) / 2;

        const opacity =
          startOpacity +
          (target - startOpacity) * eased;

        video.style.opacity = String(opacity);

        if (progress < 1) {
          fadeFrameRef.current =
            requestAnimationFrame(frame);
        } else {
          fadeFrameRef.current = null;
        }
      };

      fadeFrameRef.current =
        requestAnimationFrame(frame);
    };

    const fadeIn = () => {
      video.style.opacity = "0";
      animateOpacity(1, 500);
    };

    const fadeOut = () => {
      if (fadingOutRef.current) return;

      fadingOutRef.current = true;

      animateOpacity(0, 500);
    };

    const handleLoaded = () => {
      video.style.opacity = "0";

      video
        .play()
        .catch(() => {});

      animateOpacity(1, 500);
    };

    const handleTimeUpdate = () => {
      if (!video.duration) return;

      const remaining =
        video.duration - video.currentTime;

      if (
        remaining <= 0.55 &&
        !fadingOutRef.current
      ) {
        fadeOut();
      }
    };

    const handleEnded = () => {
      cancelFade();

      video.style.opacity = "0";

      window.setTimeout(() => {
        video.currentTime = 0;

        fadingOutRef.current = false;

        video
          .play()
          .catch(() => {});

        fadeIn();
      }, 100);
    };

    video.addEventListener(
      "loadeddata",
      handleLoaded
    );

    video.addEventListener(
      "timeupdate",
      handleTimeUpdate
    );

    video.addEventListener(
      "ended",
      handleEnded
    );

    return () => {
      cancelFade();

      video.removeEventListener(
        "loadeddata",
        handleLoaded
      );

      video.removeEventListener(
        "timeupdate",
        handleTimeUpdate
      );

      video.removeEventListener(
        "ended",
        handleEnded
      );
    };
  }, []);

  return (
    <>
      <video
        ref={videoRef}
        className="nexverity-video"
        autoPlay
        muted
        playsInline
        preload="auto"
        aria-hidden="true"
      >
        <source
          src={VIDEO_URL}
          type="video/mp4"
        />
      </video>

      <div
        className="nexverity-overlay"
        aria-hidden="true"
      />
    </>
  );
}