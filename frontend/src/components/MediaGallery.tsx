"use client";

/* eslint-disable @next/next/no-img-element */
import { useEffect, useRef, useState } from "react";
import type { GalleryItem } from "@/lib/api";
import { videoEmbedUrl, videoThumbnail } from "@/lib/video";

/**
 * Article gallery.
 *
 * Built to `ME-Modern-Article-Gallery-Mockup.html`: a mosaic of three tiles --
 * one tall frame beside two stacked ones -- standing in for the whole set,
 * with the remainder counted on the last tile. A forty-photograph story then
 * costs the article the same vertical space as a three-photograph one.
 *
 * The mockup's dialog is a single image with previous/next. This one keeps the
 * thumbnail rail we already had, because picking the eleventh of twenty
 * photographs by pressing "next" ten times is not browsing. Video is likewise
 * ours, not the mockup's: a still with a play badge, and a player built only
 * for the item on the stage, so a long set never loads a player per item.
 */

const PREVIEW = 3;

function itemTitle(item: GalleryItem, index: number) {
  return item.caption || item.alt_text || `Photograph ${index + 1}`;
}

function thumbSrc(item: GalleryItem) {
  return item.thumb || videoThumbnail(item.url) || item.url;
}

/** Only ever built for the item on the stage. */
function Media({ item }: { item: GalleryItem }) {
  if (item.kind === "video" && item.file_url) {
    return (
      <video controls poster={item.thumb ?? undefined} src={item.file_url} />
    );
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
  galleryTitle,
}: {
  heading: string;
  caption: string;
  items: GalleryItem[];
  /** The activity or event the set belongs to, shown as a chip. */
  galleryTitle?: string;
}) {
  const [index, setIndex] = useState(0);
  const [dialogOpen, setDialogOpen] = useState(false);

  const dialogRef = useRef<HTMLDialogElement>(null);
  const railRef = useRef<HTMLDivElement>(null);

  const total = items.length;
  const headingId = "article-gallery-title";

  // Native showModal gives focus trapping for free.
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

  // Keep the selected thumbnail in view as the reader moves through the set.
  useEffect(() => {
    railRef.current?.children[index]?.scrollIntoView({
      block: "nearest",
      inline: "center",
    });
  }, [index, dialogOpen]);

  if (total === 0) return null;

  const preview = items.slice(0, PREVIEW);
  const remaining = total - preview.length;
  const current = items[index];

  /** Wraps continuously, so the set has no dead ends. */
  function select(next: number) {
    setIndex((next + total) % total);
  }

  function openAt(position: number) {
    setIndex(position);
    setDialogOpen(true);
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
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      select(index - 1);
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      select(index + 1);
    }
  }

  return (
    <section aria-labelledby={headingId} className="article-gallery">
      <header className="article-gallery__head">
        <div>
          <h2 id={headingId}>{heading || "Gallery"}</h2>
          {caption ? <p>{caption}</p> : null}
        </div>
        {galleryTitle ? (
          <span className="article-gallery__badge" title={galleryTitle}>
            {galleryTitle}
          </span>
        ) : null}
      </header>

      <div className="article-gallery__mosaic" data-count={preview.length}>
        {preview.map((item, position) => (
          <button
            aria-label={`Open ${itemTitle(item, position)} in the gallery viewer`}
            className="article-gallery__tile"
            key={`${item.kind}-${position}`}
            onClick={() => openAt(position)}
            type="button"
          >
            <img alt="" src={thumbSrc(item)} />
            {item.kind === "video" ? (
              <span aria-hidden="true" className="article-gallery__play" />
            ) : null}
            <span className="article-gallery__label">
              {itemTitle(item, position)}
            </span>
            {position === preview.length - 1 && remaining > 0 ? (
              <span className="article-gallery__more">+{remaining} more</span>
            ) : null}
          </button>
        ))}
      </div>

      <footer className="article-gallery__foot">
        <p>
          {remaining > 0
            ? `${preview.length} of ${total} shown. Open any photograph to browse the full set.`
            : `${total} ${total === 1 ? "photograph" : "photographs"}.`}
        </p>
        <span className="article-gallery__count">
          {total} {total === 1 ? "item" : "items"}
        </span>
      </footer>

      <dialog
        aria-label={`${heading || "Gallery"} viewer`}
        className="article-gallery-dialog"
        onClick={(event) => {
          if (event.target === dialogRef.current) setDialogOpen(false);
        }}
        onClose={() => setDialogOpen(false)}
        onKeyDown={onDialogKeyDown}
        ref={dialogRef}
      >
        {dialogOpen ? (
          <div className="article-gallery-dialog__viewer">
            <div className="article-gallery-dialog__topbar">
              <span aria-live="polite">
                {index + 1} of {total}
              </span>
              <button
                className="article-gallery-dialog__close"
                onClick={() => setDialogOpen(false)}
                type="button"
              >
                Close <span aria-hidden="true">×</span>
              </button>
            </div>

            <div className="article-gallery-dialog__stage">
              {total > 1 ? (
                <button
                  aria-label="Previous"
                  className="article-gallery-dialog__arrow article-gallery-dialog__prev"
                  onClick={() => select(index - 1)}
                  type="button"
                >
                  <span aria-hidden="true">←</span>
                </button>
              ) : null}

              <Media item={current} />

              {total > 1 ? (
                <button
                  aria-label="Next"
                  className="article-gallery-dialog__arrow article-gallery-dialog__next"
                  onClick={() => select(index + 1)}
                  type="button"
                >
                  <span aria-hidden="true">→</span>
                </button>
              ) : null}
            </div>

            <div className="article-gallery-dialog__foot">
              <p>{itemTitle(current, index)}</p>
              <div
                aria-label="Choose a photograph"
                className="article-gallery-dialog__thumbs"
                ref={railRef}
              >
                {items.map((item, position) => (
                  <button
                    aria-label={`${position + 1}: ${itemTitle(item, position)}`}
                    className={`article-gallery-dialog__thumb${position === index ? " is-active" : ""}`}
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
