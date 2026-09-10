"use client";

import { useCallback, useEffect, useId, useRef, useState } from "react";
import type { BrochurePage } from "@/data/brochurePages";

/**
 * A page-turning publication reader.
 *
 * The turn is physical, not a fade or a slide. Sheets stand on the spine, each
 * carrying two faces, so half as many sheets as pages. A sheet rotates about
 * `transform-origin: left center`, its back face pre-rotated 180deg and both
 * faces `backface-visibility: hidden`, which is what makes the far side appear
 * as the sheet passes vertical. That is the whole trick, and the reason this
 * cannot be swapped for a carousel: a carousel has no far side.
 *
 * `cursor` is the zero-based logical page. `leaf` is how many sheets have been
 * turned, which is what the desktop spread is actually made of -- the two are
 * not the same number, because the cover stands alone on the right before any
 * sheet has moved.
 *
 * Turning is locked for the length of the animation. Without the lock a reader
 * holding the arrow key re-enters mid-rotation, the z-index order is rebuilt
 * against a stack that has not settled, and sheets surface through one another.
 *
 * The engine knows nothing about the publication: it renders whatever pages it
 * is handed.
 */

const TURN_MS = 920; // The CSS transition is 880ms; this outlasts it.
const MOBILE = "(max-width: 760px)";

type Props = {
  pages: BrochurePage[];
  /** Shown in the bar above the viewer. */
  title: string;
  subtitle: string;
};

export default function Flipbook({ pages, title, subtitle }: Props) {
  const total = pages.length;
  // Two faces to a sheet. Derived rather than fixed, so a publication can be
  // ten pages or fourteen without the engine being edited; an odd count simply
  // leaves the last sheet's back face blank.
  const sheets = Math.ceil(total / 2);

  const [cursor, setCursor] = useState(0);
  const [turning, setTurning] = useState<number | null>(null);
  const [zoom, setZoom] = useState(1);
  const [mobile, setMobile] = useState(false);
  const [panelOpen, setPanelOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [copied, setCopied] = useState(false);

  const busy = useRef(false);
  const stageRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<HTMLDivElement>(null);
  const touchX = useRef<number | null>(null);
  const panelId = useId();

  // Matches the CSS breakpoint that swaps the spread for a single page, so the
  // label and the step size agree with what is on screen.
  useEffect(() => {
    const mq = window.matchMedia(MOBILE);
    const sync = () => setMobile(mq.matches);
    sync();
    mq.addEventListener("change", sync);
    return () => mq.removeEventListener("change", sync);
  }, []);

  const leaf = cursor === 0 ? 0 : Math.ceil((cursor + 1) / 2);

  /** Desktop spreads open on odd cursors; page 0 is the cover, alone. */
  const toSpread = (page: number) =>
    page === 0 ? 0 : page % 2 === 0 ? page - 1 : page;

  const go = useCallback(
    (dir: number, jump: number | null = null) => {
      if (busy.current) return;

      let target: number;
      if (jump !== null) {
        target = mobile ? jump : toSpread(jump);
      } else if (mobile) {
        target = cursor + dir;
      } else {
        const next = Math.max(0, Math.min(sheets, leaf + dir));
        target = next === 0 ? 0 : next * 2 - 1;
      }
      target = Math.max(0, Math.min(total - 1, target));
      if (target === cursor) return;

      busy.current = true;
      // The sheet that actually rotates: going forward it is the one about to
      // turn, going back it is the one returning.
      const active = mobile ? null : dir > 0 ? leaf : leaf - 1;
      if (active !== null && active >= 0 && active < sheets) setTurning(active);

      setCursor(target);
      window.setTimeout(() => {
        setTurning(null);
        busy.current = false;
      }, TURN_MS);
    },
    [cursor, leaf, mobile, sheets, total],
  );

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "ArrowRight") go(1);
      if (event.key === "ArrowLeft") go(-1);
      if (event.key === "Escape") setPanelOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [go]);

  useEffect(() => {
    const stage = stageRef.current;
    if (!stage) return;
    const start = (e: TouchEvent) => {
      touchX.current = e.touches[0].clientX;
    };
    const end = (e: TouchEvent) => {
      if (touchX.current === null) return;
      const dx = e.changedTouches[0].clientX - touchX.current;
      touchX.current = null;
      if (Math.abs(dx) > 45) go(dx < 0 ? 1 : -1);
    };
    stage.addEventListener("touchstart", start, { passive: true });
    stage.addEventListener("touchend", end, { passive: true });
    return () => {
      stage.removeEventListener("touchstart", start);
      stage.removeEventListener("touchend", end);
    };
  }, [go]);

  const atStart = cursor === 0;
  const atEnd = mobile ? cursor === total - 1 : leaf === sheets;

  const label = mobile
    ? `${cursor + 1} / ${total}`
    : leaf === 0
      ? `1 / ${total}`
      : leaf === sheets
        ? `${total} / ${total}`
        : `${leaf * 2}–${leaf * 2 + 1} / ${total}`;

  const current = pages[cursor];
  const needle = query.trim().toLowerCase();
  const contents = pages
    .map((page, index) => ({ page, index }))
    .filter(
      ({ page }) =>
        !needle ||
        `${page.title} ${page.subtitle} ${page.chapter}`
          .toLowerCase()
          .includes(needle),
    );

  async function share() {
    const url = window.location.href;
    try {
      if (navigator.share) {
        await navigator.share({ title, url });
        return;
      }
      await navigator.clipboard.writeText(url);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      // A cancelled share sheet is not an error worth surfacing.
    }
  }

  function toggleFullscreen() {
    if (document.fullscreenElement) {
      void document.exitFullscreen();
    } else {
      void viewerRef.current?.requestFullscreen();
    }
  }

  return (
    <div className="flipbook">
      <div className="fb-bar">
        <div className="fb-bar-title">
          <span aria-hidden="true">ME</span>
          <div>
            <b>{title}</b>
            <small>{subtitle}</small>
          </div>
        </div>
        <div className="fb-bar-actions">
          <button onClick={() => window.print()} type="button">
            Print
          </button>
        </div>
      </div>

      <div className="fb-viewer" ref={viewerRef}>
        <div className="fb-topline">
          <span>
            {current.chapter} · {current.title}
          </span>
          <b>{label}</b>
        </div>

        <div className="fb-stage" ref={stageRef}>
          <button
            aria-label="Previous page"
            className="fb-turn fb-turn-left"
            disabled={atStart}
            onClick={() => go(-1)}
            type="button"
          >
            <span aria-hidden="true">‹</span>
          </button>

          {/* Desktop: the physical book. */}
          <div
            className={`fb-book${leaf === 0 ? " is-front-closed" : ""}${
              leaf === sheets ? " is-back-closed" : ""
            }`}
            style={{ ["--fb-zoom" as string]: zoom }}
          >
            <span className="fb-book-shadow" aria-hidden="true" />
            {Array.from({ length: sheets }, (_, i) => {
              const flipped = i < leaf;
              return (
                <div
                  className={`fb-sheet${flipped ? " is-flipped" : ""}${
                    turning === i ? " is-turning" : ""
                  }`}
                  key={i}
                  style={{
                    // The turning sheet rides above the whole stack for the
                    // length of its rotation, or it clips through the pages it
                    // is passing.
                    zIndex: turning === i ? 100 : flipped ? i + 1 : sheets - i,
                  }}
                >
                  <div className="fb-face fb-face-front">
                    <Page page={pages[i * 2]} number={i * 2 + 1} total={total} />
                    <span className="fb-gloss" aria-hidden="true" />
                  </div>
                  <div className="fb-face fb-face-back">
                    {/* An odd page count leaves this face with nothing on it,
                        the way the last leaf of a real booklet is blank. */}
                    {pages[i * 2 + 1] ? (
                      <Page
                        page={pages[i * 2 + 1]}
                        number={i * 2 + 2}
                        total={total}
                      />
                    ) : (
                      <div className="fb-page fb-tone-paper" />
                    )}
                    <span className="fb-gloss" aria-hidden="true" />
                  </div>
                </div>
              );
            })}
          </div>

          {/* Mobile: one page, never a squeezed spread. */}
          <div
            className="fb-single"
            style={{ ["--fb-zoom" as string]: zoom }}
          >
            <Page page={current} number={cursor + 1} total={total} />
          </div>

          <button
            aria-label="Next page"
            className="fb-turn fb-turn-right"
            disabled={atEnd}
            onClick={() => go(1)}
            type="button"
          >
            <span aria-hidden="true">›</span>
          </button>
        </div>

        <div className="fb-controls">
          <button
            aria-expanded={panelOpen}
            aria-controls={panelId}
            className={panelOpen ? "is-active" : ""}
            onClick={() => setPanelOpen((open) => !open)}
            type="button"
          >
            <span aria-hidden="true">☰</span>
            <em className="fb-sr">Contents</em>
          </button>
          <strong>{label}</strong>
          <button
            aria-label="Previous page"
            disabled={atStart}
            onClick={() => go(-1)}
            type="button"
          >
            <span aria-hidden="true">←</span>
          </button>
          <input
            aria-label="Go to page"
            max={total - 1}
            min={0}
            onChange={(e) => go(+e.target.value < cursor ? -1 : 1, +e.target.value)}
            type="range"
            value={cursor}
          />
          <button
            aria-label="Next page"
            disabled={atEnd}
            onClick={() => go(1)}
            type="button"
          >
            <span aria-hidden="true">→</span>
          </button>

          <div className="fb-zoom">
            <button
              aria-label="Zoom out"
              disabled={zoom <= 0.7}
              onClick={() => setZoom((z) => Math.max(0.7, +(z - 0.1).toFixed(2)))}
              type="button"
            >
              <span aria-hidden="true">−</span>
            </button>
            <span>{Math.round(zoom * 100)}%</span>
            <button
              aria-label="Zoom in"
              disabled={zoom >= 1.3}
              onClick={() => setZoom((z) => Math.min(1.3, +(z + 0.1).toFixed(2)))}
              type="button"
            >
              <span aria-hidden="true">+</span>
            </button>
          </div>

          <button aria-label="Fullscreen" onClick={toggleFullscreen} type="button">
            <span aria-hidden="true">⛶</span>
          </button>
          <button
            aria-label={copied ? "Link copied" : "Share this publication"}
            onClick={share}
            type="button"
          >
            <span aria-hidden="true">{copied ? "✓" : "⇗"}</span>
          </button>
        </div>

        <div className={`fb-panel${panelOpen ? " is-open" : ""}`} id={panelId}>
          <div className="fb-panel-head">
            <b>Contents</b>
            <button
              aria-label="Close contents"
              onClick={() => setPanelOpen(false)}
              type="button"
            >
              <span aria-hidden="true">×</span>
            </button>
          </div>
          <input
            aria-label="Search the contents"
            className="fb-search"
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search pages"
            type="search"
            value={query}
          />
          <div className="fb-contents">
            {contents.length === 0 ? (
              <p className="fb-contents-empty">No page matches “{query}”.</p>
            ) : (
              contents.map(({ page, index }) => (
                <button
                  className={index === cursor ? "is-active" : ""}
                  key={page.title}
                  onClick={() => {
                    go(index < cursor ? -1 : 1, index);
                    setPanelOpen(false);
                  }}
                  type="button"
                >
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <b>
                    {page.title}
                    <small>{page.subtitle}</small>
                  </b>
                </button>
              ))
            )}
          </div>
        </div>
      </div>

      <p className="fb-help">
        Use the arrows, the arrow keys, or swipe. Ten pages.
      </p>

      {/* One A4 page per sheet when printed; hidden on screen. */}
      <div className="fb-print">
        {pages.map((page, i) => (
          <Page key={page.title} number={i + 1} page={page} total={total} />
        ))}
      </div>
    </div>
  );
}

function Page({
  page,
  number,
  total,
}: {
  page: BrochurePage;
  number: number;
  total: number;
}) {
  const plain = page.tone === "cover" || page.tone === "back";
  return (
    <article className={`fb-page fb-tone-${page.tone}`}>
      {plain ? null : (
        <header className="fb-page-head">
          <span>{page.chapter}</span>
          <b>{String(number).padStart(2, "0")}</b>
        </header>
      )}
      <div className={plain ? "fb-page-plain" : "fb-page-pad"}>{page.body}</div>
      {plain ? null : (
        <footer className="fb-page-foot">
          <span>MECHANICAL ENGINEERING · RUPP</span>
          <b>
            {number} / {total}
          </b>
        </footer>
      )}
    </article>
  );
}
