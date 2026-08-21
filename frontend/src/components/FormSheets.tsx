/* eslint-disable @next/next/no-img-element */
"use client";

import { useEffect, useRef, useState } from "react";

/**
 * The application sheets, openable full size.
 *
 * A form is unreadable at card width -- the whole point is the handwriting in
 * each field -- so every sheet opens into a dialog at the size of the screen,
 * with the next and previous sheets reachable without closing it.
 *
 * The dialog mechanics follow MediaGallery: native `showModal` for focus
 * trapping, the page behind locked while it is open, and Escape handled
 * explicitly because not every engine fires `close` and a dialog a reader
 * cannot dismiss leaves the page behind it stuck.
 */

export type FormSheet = {
  image: string;
  title: string;
  khmer: string;
  note: string;
};

export default function FormSheets({ sheets }: { sheets: FormSheet[] }) {
  const [openAt, setOpenAt] = useState<number | null>(null);
  const dialogRef = useRef<HTMLDialogElement>(null);
  const total = sheets.length;

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (openAt !== null && !dialog.open) dialog.showModal();
    if (openAt === null && dialog.open) dialog.close();
  }, [openAt]);

  useEffect(() => {
    if (openAt === null) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, [openAt]);

  if (total === 0) return null;

  /** Wraps, so the set has no dead ends. */
  const select = (next: number) => setOpenAt(((next % total) + total) % total);

  function onKeyDown(event: React.KeyboardEvent) {
    if (openAt === null) return;
    if (event.key === "Escape") {
      event.preventDefault();
      setOpenAt(null);
      return;
    }
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      select(openAt - 1);
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      select(openAt + 1);
    }
  }

  const current = openAt === null ? null : sheets[openAt];

  return (
    <>
      <div className="admissions-form-sheets">
        {sheets.map((sheet, index) => (
          <figure className="admissions-sheet" key={sheet.image}>
            {/* A button rather than a link: this opens the sheet in place
                rather than navigating away from the instructions around it. */}
            <button
              aria-label={`Open ${sheet.title} full size`}
              className="admissions-sheet-open"
              onClick={() => setOpenAt(index)}
              type="button"
            >
              <img
                src={sheet.image}
                alt={`${sheet.title} sheet, completed`}
                loading={index === 0 ? undefined : "lazy"}
              />
              <span aria-hidden="true">Zoom</span>
            </button>
            <figcaption>
              <strong>
                <span aria-hidden="true">
                  {String(index + 1).padStart(2, "0")}
                </span>{" "}
                {sheet.title}
              </strong>
              <span lang="km">{sheet.khmer}</span>
              <small>{sheet.note}</small>
            </figcaption>
          </figure>
        ))}
      </div>

      <dialog
        aria-label="Application sheet"
        className="sheet-dialog"
        onCancel={(event) => {
          event.preventDefault();
          setOpenAt(null);
        }}
        onClick={(event) => {
          // The backdrop is the dialog itself; a click on the sheet must not
          // close it.
          if (event.target === dialogRef.current) setOpenAt(null);
        }}
        onKeyDown={onKeyDown}
        ref={dialogRef}
      >
        {current ? (
          <div className="sheet-dialog-inner">
            <header>
              <p>
                <strong>{current.title}</strong>
                <span lang="km">{current.khmer}</span>
              </p>
              <button
                aria-label="Close"
                onClick={() => setOpenAt(null)}
                type="button"
              >
                <span aria-hidden="true">×</span>
              </button>
            </header>

            <img src={current.image} alt={`${current.title} sheet, completed`} />

            <footer>
              <button
                aria-label="Previous sheet"
                onClick={() => select((openAt ?? 0) - 1)}
                type="button"
              >
                <span aria-hidden="true">←</span> Previous
              </button>
              <span>
                Sheet {(openAt ?? 0) + 1} of {total}
              </span>
              <button
                aria-label="Next sheet"
                onClick={() => select((openAt ?? 0) + 1)}
                type="button"
              >
                Next <span aria-hidden="true">→</span>
              </button>
            </footer>
          </div>
        ) : null}
      </dialog>
    </>
  );
}
