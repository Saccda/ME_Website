"use client";

/* eslint-disable @next/next/no-img-element */
import { useEffect, useRef, useState } from "react";
import type { GalleryItem } from "@/lib/api";
import { videoEmbedUrl, videoThumbnail } from "@/lib/video";

/**
 * Photo story gallery.
 *
 * Built to `PHOTO-STORY-DESIGN-SPEC.md` and `photo-story-gallery.html`: one
 * fixed-height stage with a thumbnail rail, rather than a grid that grows with
 * the set. Forty photographs then cost the article the same vertical space as
 * four, and the reader browses instead of scrolling past.
 *
 * Videos keep their existing behaviour -- a still with a play badge in the rail,
 * and a player created only for the item actually being viewed, so a long set
 * never loads a player per item.
 */

const FADE_MS = 120;

function itemTitle(item: GalleryItem, index: number) {
  return item.caption || item.alt_text || `Photograph ${index + 1}`;
}

function thumbSrc(item: GalleryItem) {
  return item.thumb || videoThumbnail(item.url) || item.url;
}

/** The stage and the dialog show the same thing; CSS decides cover vs contain. */
function Media({ item }: { item: GalleryItem }) {
  if (item.kind === "video" && item.file_url) {
    return <video controls poster={item.thumb ?? undefined} src={item.file_url} />;
  }
  if (item.kind === "video") {
    return (
      <iframe
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        src={videoEmbedUrl(item.url) ?? item.url}
        title={item.caption || "Video"}
      />
    );
  }
  return <img alt={item.alt_text} src={item.url} />;
}

export default function MediaGallery({
  heading,
  caption,
  items,
  eyebrow = "Photo story",
  galleryTitle,
}: {
  heading: string;
  caption: string;
  items: GalleryItem[];
  eyebrow?: string;
  /** The activity or event the set belongs to, shown over the image. */
  galleryTitle?: string;
}) {
  const [index, setIndex] = useState(0);
  const [fading, setFading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);

  const dialogRef = useRef<HTMLDialogElement>(null);
  const railRef = useRef<HTMLDivElement>(null);
  const dialogRailRef = useRef<HTMLDivElement>(null);
  const fadeTimer = useRef<number | null>(null);

  const total = items.length;
  const current = items[index];
  const headingId = "photo-story-title";

  useEffect(() => {
    return () => {
      if (fadeTimer.current !== null) window.clearTimeout(fadeTimer.current);
    };
  }, []);

  // Native showModal gives focus trapping and Escape for free.
  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (dialogOpen && !dialog.open) dialog.showModal();
    if (!dialogOpen && dialog.open) dialog.close();
  }, [dialogOpen]);

  // showModal does not reliably stop the page behind from scrolling.
  useEffect(() => {
    if (!dialogOpen) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, [dialogOpen]);

  // Keep the selected thumbnail centred in its rail.
  useEffect(() => {
    for (const rail of [railRef.current, dialogRailRef.current]) {
      const thumb = rail?.children[index];
      thumb?.scrollIntoView({ block: "nearest", inline: "center" });
    }
  }, [index, dialogOpen]);

  if (total === 0) return null;

  /** Wraps continuously, and cross-fades rather than cutting. */
  function select(next: number) {
    const target = (next + total) % total;
    if (target === index) return;
    if (fadeTimer.current !== null) window.clearTimeout(fadeTimer.current);
    setFading(true);
    fadeTimer.current = window.setTimeout(() => {
      setIndex(target);
      setFading(false);
    }, FADE_MS);
  }

  /** Arrow keys drive the gallery only while focus is inside it. */
  function onKeyDown(event: React.KeyboardEvent) {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      select(index - 1);
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      select(index + 1);
    }
  }

  /**
   * Escape is closed explicitly rather than left to the dialog's own close
   * request: not every engine fires `close`, and a dialog the reader cannot
   * dismiss also leaves the page behind it locked.
   */
  function onDialogKeyDown(event: React.KeyboardEvent) {
    if (event.key === "Escape") {
      event.preventDefault();
      setDialogOpen(false);
      return;
    }
    onKeyDown(event);
  }

  return (
    <section
      aria-labelledby={headingId}
      className="photo-story"
      onKeyDown={onKeyDown}
    >
      <header className="photo-story__heading">
        <div>
          <p className="photo-story__eyebrow">{eyebrow}</p>
          <h2 id={headingId}>{heading || "Gallery"}</h2>
        </div>
        <span className="photo-story__total">
          {total} {total === 1 ? "photograph" : "photographs"}
        </span>
      </header>

      <div className="photo-story__stage">
        <div
          className="photo-story__image"
          style={{ opacity: fading ? 0.35 : 1 }}
        >
          <Media item={current} />
        </div>

        <div className="photo-story__topline">
          {galleryTitle ? (
            <div className="photo-story__current">
              <span>Gallery:</span> {galleryTitle}
            </div>
          ) : (
            <span />
          )}
          <button
            aria-label="Open full-screen gallery"
            className="photo-story__expand"
            onClick={() => setDialogOpen(true)}
            type="button"
          >
            <svg
              aria-hidden="true"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
            >
              <path d="M8 3H3v5M16 3h5v5M8 21H3v-5M16 21h5v-5" />
            </svg>
          </button>
        </div>

        {total > 1 ? (
          <>
            <button
              aria-label="Previous photograph"
              className="photo-story__arrow photo-story__arrow--prev"
              onClick={() => select(index - 1)}
              type="button"
            >
              <span aria-hidden="true">←</span>
            </button>
            <button
              aria-label="Next photograph"
              className="photo-story__arrow photo-story__arrow--next"
              onClick={() => select(index + 1)}
              type="button"
            >
              <span aria-hidden="true">→</span>
            </button>
          </>
        ) : null}

        <div className="photo-story__bottom">
          <div className="photo-story__copy">
            <strong>{itemTitle(current, index)}</strong>
            <span>
              Photograph {index + 1} of {total}
            </span>
          </div>
          <div
            aria-label="Choose a photograph"
            className="photo-story__thumbs"
            ref={railRef}
          >
            {items.map((item, position) => (
              <button
                aria-label={`${position + 1}: ${itemTitle(item, position)}`}
                className={`photo-story__thumb${position === index ? " is-active" : ""}`}
                key={`${item.kind}-${position}`}
                onClick={() => select(position)}
                type="button"
              >
                <img alt="" loading="lazy" src={thumbSrc(item)} />
                {item.kind === "video" ? (
                  <span className="photo-story__thumb-play" aria-hidden="true" />
                ) : null}
              </button>
            ))}
          </div>
        </div>
      </div>

      {caption ? (
        <footer className="photo-story__footer">
          <p className="photo-story__caption">{caption}</p>
          <span className="photo-story__hint">Use arrow keys to browse</span>
        </footer>
      ) : null}

      <dialog
        aria-label={`${heading || "Gallery"} photographs`}
        className="photo-story-dialog"
        onClick={(event) => {
          if (event.target === dialogRef.current) setDialogOpen(false);
        }}
        onClose={() => setDialogOpen(false)}
        onKeyDown={onDialogKeyDown}
        ref={dialogRef}
      >
        {dialogOpen ? (
          <div className="photo-story-dialog__viewer">
            <div className="photo-story-dialog__main">
              <button
                aria-label="Close"
                className="photo-story-dialog__close"
                onClick={() => setDialogOpen(false)}
                type="button"
              >
                <span aria-hidden="true">×</span>
              </button>

              {total > 1 ? (
                <button
                  aria-label="Previous image"
                  className="photo-story-dialog__arrow photo-story-dialog__prev"
                  onClick={() => select(index - 1)}
                  type="button"
                >
                  <span aria-hidden="true">←</span>
                </button>
              ) : null}

              <Media item={current} />

              {total > 1 ? (
                <button
                  aria-label="Next image"
                  className="photo-story-dialog__arrow photo-story-dialog__next"
                  onClick={() => select(index + 1)}
                  type="button"
                >
                  <span aria-hidden="true">→</span>
                </button>
              ) : null}
            </div>

            <div className="photo-story-dialog__bar">
              <div className="photo-story-dialog__copy">
                <strong>{itemTitle(current, index)}</strong>
                <span>
                  {index + 1} of {total}
                </span>
              </div>
              <div className="photo-story-dialog__thumbs" ref={dialogRailRef}>
                {items.map((item, position) => (
                  <button
                    aria-label={`Open image ${position + 1}: ${itemTitle(item, position)}`}
                    className={`photo-story-dialog__thumb${position === index ? " is-active" : ""}`}
                    key={`d-${item.kind}-${position}`}
                    onClick={() => select(position)}
                    type="button"
                  >
                    <img alt="" loading="lazy" src={thumbSrc(item)} />
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : null}
      </dialog>
    </section>
  );
}
