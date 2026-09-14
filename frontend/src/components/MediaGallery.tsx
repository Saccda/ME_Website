"use client";

/* eslint-disable @next/next/no-img-element */
import { useEffect, useId, useRef, useState } from "react";
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

/**
 * The name a screen reader announces for an item. Never printed on the page:
 * without a caption it is only the file's name, or one made from the story.
 */
function itemTitle(item: GalleryItem, index: number) {
  const noun = item.kind === "video" ? "Video" : "Photograph";
  return item.caption || item.alt_text || `${noun} ${index + 1}`;
}

/** What the set holds, by kind: "3 photographs and 2 videos". */
function describeSet(items: GalleryItem[]) {
  const videos = items.filter((item) => item.kind === "video").length;
  const photographs = items.length - videos;
  return [
    photographs > 0
      ? `${photographs} ${photographs === 1 ? "photograph" : "photographs"}`
      : "",
    videos > 0 ? `${videos} ${videos === 1 ? "video" : "videos"}` : "",
  ]
    .filter(Boolean)
    .join(" and ");
}

/** The word for one item of the set, for the prompts addressed to a reader. */
function itemNoun(items: GalleryItem[]) {
  const kinds = new Set(items.map((item) => item.kind));
  if (kinds.size > 1) return "item";
  return kinds.has("video") ? "video" : "photograph";
}

/**
 * A picture to stand for the item, or null when there is none.
 *
 * A video's own address is not a picture: handed to an <img> it draws as a
 * broken image. So a video gets its poster, or its host's still, or nothing,
 * and the caller decides what to show instead.
 */
function thumbSrc(item: GalleryItem) {
  if (item.kind === "image") return item.thumb || item.url;
  return item.thumb || videoThumbnail(item.url);
}

/** A preview tile's picture. */
function TileStill({ item }: { item: GalleryItem }) {
  const src = thumbSrc(item);
  if (src) return <img alt="" src={src} />;

  // An uploaded clip nobody chose a poster for: the browser draws a frame of
  // the clip itself. #t=0.1 asks for one just past the start, which some
  // browsers need before they paint anything. A browser that cannot load the
  // file leaves the tile's own ground and play badge, not a broken image.
  if (item.file_url) {
    return (
      <video
        aria-hidden="true"
        preload="metadata"
        src={`${item.file_url}#t=0.1`}
      />
    );
  }
  return null;
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
  action,
  layout = "mosaic",
}: {
  heading: string;
  caption: string;
  items: GalleryItem[];
  /** The activity or event the set belongs to, shown as a chip. */
  galleryTitle?: string;
  /**
   * "mosaic" stands three tiles in for the whole set, which keeps a forty-photo
   * story short. "row" shows every picture abreast -- the shape a body gallery
   * block already had before it could be opened, kept so that making the
   * pictures clickable did not also rearrange them.
   */
  layout?: "mosaic" | "row";
  /**
   * An external destination the set is a preview of -- a live platform, say.
   * Sits where the chip sits, so a reader finds it before browsing rather
   * than after five screenshots.
   */
  action?: { href: string; label: string };
}) {
  const [index, setIndex] = useState(0);
  const [dialogOpen, setDialogOpen] = useState(false);

  const dialogRef = useRef<HTMLDialogElement>(null);
  const railRef = useRef<HTMLDivElement>(null);

  const total = items.length;
  // Unique per instance: an article may carry more than one gallery, and a
  // fixed id would repeat, leaving aria-labelledby pointing at whichever
  // heading came first.
  const headingId = `article-gallery-title-${useId()}`;

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

  const isRow = layout === "row";
  const preview = isRow ? items : items.slice(0, PREVIEW);
  const remaining = total - preview.length;
  const current = items[index];
  // A body gallery block carries a caption but no heading, and a section with
  // no heading cannot be labelled by one.
  const labelled = Boolean(heading);
  const noun = itemNoun(items);

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
    <section
      aria-label={labelled ? undefined : caption || "Gallery"}
      aria-labelledby={labelled ? headingId : undefined}
      className={`article-gallery${isRow ? " article-gallery--row" : ""}`}
    >
      {/* Rendered only with a heading. `hidden` would not do it: the UA's
          `[hidden] { display: none }` loses to this element's own `display`. */}
      {labelled ? (
        <header className="article-gallery__head">
          <div>
            <h2 id={headingId}>{heading}</h2>
            {caption ? <p>{caption}</p> : null}
          </div>
          {action ? (
            <a
              className="article-gallery__action"
              href={action.href}
              rel="noopener noreferrer"
              target="_blank"
            >
              {action.label} <span aria-hidden="true">↗</span>
            </a>
          ) : null}
          {galleryTitle ? (
            <span className="article-gallery__badge" title={galleryTitle}>
              {galleryTitle}
            </span>
          ) : null}
        </header>
      ) : null}

      <div
        className={isRow ? "article-gallery__row" : "article-gallery__mosaic"}
        data-count={preview.length}
      >
        {preview.map((item, position) => (
          <button
            aria-label={`Open ${itemTitle(item, position)} in the gallery viewer`}
            className="article-gallery__tile"
            key={`${item.kind}-${position}`}
            onClick={() => openAt(position)}
            type="button"
          >
            <TileStill item={item} />
            {item.kind === "video" ? (
              <span aria-hidden="true" className="article-gallery__play" />
            ) : null}
            {/* Only a written caption earns a plate. Without one there is only
                the title -- the file's name, or one made from the story -- and
                repeating that over every picture is noise. */}
            {item.caption ? (
              <span className="article-gallery__label">{item.caption}</span>
            ) : null}
            {position === preview.length - 1 && remaining > 0 ? (
              <span className="article-gallery__more">+{remaining} more</span>
            ) : null}
          </button>
        ))}
      </div>

      {/* A row stands for the whole set, so there is no remainder to count.
          Its caption sits below the pictures, where the block had it. */}
      {isRow ? (
        caption ? (
          <p className="article-gallery__row-caption">{caption}</p>
        ) : null
      ) : (
        <footer className="article-gallery__foot">
          <p>
            {remaining > 0
              ? `${preview.length} of ${total} shown. Open any ${noun} to browse the full set.`
              : `${describeSet(items)}.`}
          </p>
          <span className="article-gallery__count">
            {total} {total === 1 ? "item" : "items"}
          </span>
        </footer>
      )}

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
              {/* A caption, or nothing: the counter above already says which
                  picture this is. */}
              <p>{current.caption}</p>
              <div
                aria-label={`Choose ${noun === "item" ? "an item" : `a ${noun}`}`}
                className="article-gallery-dialog__thumbs"
                ref={railRef}
              >
                {items.map((item, position) => {
                  const still = thumbSrc(item);
                  return (
                    <button
                      aria-label={`${position + 1}: ${itemTitle(item, position)}`}
                      className={`article-gallery-dialog__thumb${position === index ? " is-active" : ""}`}
                      key={`d-${item.kind}-${position}`}
                      onClick={() => select(position)}
                      type="button"
                    >
                      {/* The rail holds every item in the set, so drawing a
                          frame from each clip would download them all at
                          once. A video with no still gets a play mark. */}
                      {still ? (
                        <img alt="" loading="lazy" src={still} />
                      ) : (
                        <span
                          aria-hidden="true"
                          className="article-gallery-dialog__thumb-video"
                        />
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        ) : null}
      </dialog>
    </section>
  );
}
