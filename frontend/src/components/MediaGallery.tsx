"use client";

/* eslint-disable @next/next/no-img-element */
import { useCallback, useEffect, useState } from "react";
import type { GalleryItem } from "@/lib/api";
import { videoEmbedUrl, videoThumbnail } from "@/lib/video";

/**
 * A whole set of media from one activity: a grid of thumbnails that opens each
 * item full size.
 *
 * Videos are represented by a still with a play badge rather than an embedded
 * player, so a gallery of twenty items does not load twenty iframes; the player
 * is created only when an item is opened.
 */
export default function MediaGallery({
  heading,
  caption,
  items,
}: {
  heading: string;
  caption: string;
  items: GalleryItem[];
}) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  const isOpen = openIndex !== null;

  const close = useCallback(() => setOpenIndex(null), []);
  const step = useCallback(
    (delta: number) =>
      setOpenIndex((current) =>
        current === null
          ? current
          : (current + delta + items.length) % items.length,
      ),
    [items.length],
  );

  useEffect(() => {
    if (!isOpen) return;

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") close();
      if (event.key === "ArrowRight") step(1);
      if (event.key === "ArrowLeft") step(-1);
    };

    // The page behind must not scroll while the viewer is over it.
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    document.addEventListener("keydown", onKeyDown);

    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [isOpen, close, step]);

  const active = openIndex === null ? null : items[openIndex];

  return (
    <section className="story-media-gallery">
      {heading ? <h3>{heading}</h3> : null}

      <ul className="story-media-grid">
        {items.map((item, index) => {
          const thumb = item.thumb || videoThumbnail(item.url) || "";
          return (
            <li key={`${item.kind}-${index}`}>
              <button
                aria-label={
                  item.kind === "video"
                    ? `Play video ${index + 1} of ${items.length}`
                    : `View image ${index + 1} of ${items.length}`
                }
                onClick={() => setOpenIndex(index)}
                type="button"
              >
                {thumb ? (
                  <img alt={item.alt_text} loading="lazy" src={thumb} />
                ) : (
                  <span className="story-media-placeholder" aria-hidden="true" />
                )}
                {item.kind === "video" ? (
                  <span className="story-media-play" aria-hidden="true" />
                ) : null}
              </button>
            </li>
          );
        })}
      </ul>

      {caption ? <p className="story-media-caption">{caption}</p> : null}

      {active ? (
        <div
          aria-label={active.caption || "Media viewer"}
          aria-modal="true"
          className="story-lightbox"
          role="dialog"
        >
          <button
            aria-label="Close"
            className="story-lightbox-close"
            onClick={close}
            type="button"
          >
            <span aria-hidden="true">✕</span>
          </button>

          {items.length > 1 ? (
            <button
              aria-label="Previous"
              className="story-lightbox-prev"
              onClick={() => step(-1)}
              type="button"
            >
              <span aria-hidden="true">←</span>
            </button>
          ) : null}

          <figure>
            {active.kind === "video" && active.file_url ? (
              <video autoPlay controls src={active.file_url} />
            ) : active.kind === "video" ? (
              <div className="story-video">
                <iframe
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  src={videoEmbedUrl(active.url) ?? active.url}
                  title={active.caption || "Video"}
                />
              </div>
            ) : (
              <img alt={active.alt_text} src={active.url} />
            )}
            {active.caption ? <figcaption>{active.caption}</figcaption> : null}
          </figure>

          {items.length > 1 ? (
            <button
              aria-label="Next"
              className="story-lightbox-next"
              onClick={() => step(1)}
              type="button"
            >
              <span aria-hidden="true">→</span>
            </button>
          ) : null}

          <p className="story-lightbox-count">
            {(openIndex ?? 0) + 1} / {items.length}
          </p>
        </div>
      ) : null}
    </section>
  );
}
