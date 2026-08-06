"use client";

/* eslint-disable @next/next/no-img-element */
import { useEffect, useState } from "react";

const INTERVAL_MS = 4000;

/**
 * The picture area of a news or event card.
 *
 * With more than one still it crossfades between them, so a card previews the
 * activity rather than a single frame of it. The slideshow is decorative: it
 * carries no controls, because the card is already one link and a second set of
 * targets inside it would compete with that. Anyone who stops on a card and
 * anyone who does not both reach the same story.
 *
 * It does not run at all when the reader has asked for reduced motion, and it
 * never autoplays video — three players on a homepage is a slow page on a
 * mobile connection, so a video story is marked with a badge instead.
 */
export default function CardMedia({
  slides,
  hasVideo,
}: {
  slides: string[];
  hasVideo: boolean;
}) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (slides.length < 2) return;
    if (
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ) {
      return;
    }

    const timer = window.setInterval(
      () => setIndex((current) => (current + 1) % slides.length),
      INTERVAL_MS,
    );
    return () => window.clearInterval(timer);
  }, [slides.length]);

  if (slides.length === 0) return null;

  return (
    <div className="news-card-media">
      {slides.map((slide, position) => (
        <img
          alt=""
          className={position === index ? "is-current" : undefined}
          key={slide}
          loading={position === 0 ? "lazy" : "lazy"}
          src={slide}
        />
      ))}

      {hasVideo ? (
        <span className="news-card-video" aria-hidden="true" />
      ) : null}

      {slides.length > 1 ? (
        <span className="news-card-dots" aria-hidden="true">
          {slides.map((slide, position) => (
            <i className={position === index ? "is-current" : undefined} key={slide} />
          ))}
        </span>
      ) : null}
    </div>
  );
}
