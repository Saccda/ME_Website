/* eslint-disable @next/next/no-img-element */
"use client";

import { useState } from "react";
import type { Facility } from "@/lib/api";

/**
 * The equipment catalogue, filterable and revealed a page at a time.
 *
 * Thirty machines in one flat list ran to six screens, and a reader looking
 * for a lathe had no way to ask for one. Two filters answer the two questions
 * actually asked of a catalogue: which area does this belong to, and can I use
 * it yet.
 *
 * The focus-area link has been on the model all along; it simply was not being
 * sent to the browser, so it could not be filtered on.
 */

const PAGE = 12;

type Availability = Facility["availability_status"];

export default function FacilityCatalog({ facilities }: { facilities: Facility[] }) {
  const [area, setArea] = useState<string>("all");
  const [status, setStatus] = useState<Availability | "all">("all");
  const [shown, setShown] = useState(PAGE);

  // Built from the data, so an area with no equipment is never offered and a
  // newly added one needs no code change.
  const areas = [...
    new Map(
      facilities
        .flatMap((item) => item.focus_areas)
        .map((focus) => [focus.code, focus]),
    ).values(),
  ].sort((a, b) => a.code.localeCompare(b.code));

  const statuses = [...new Set(facilities.map((item) => item.availability_status))];
  const statusLabel = (value: Availability) =>
    facilities.find((item) => item.availability_status === value)
      ?.availability_label ?? value;

  const filtered = facilities.filter(
    (item) =>
      (area === "all" || item.focus_areas.some((focus) => focus.code === area)) &&
      (status === "all" || item.availability_status === status),
  );
  const visible = filtered.slice(0, shown);
  const remaining = filtered.length - visible.length;

  const reset = () => setShown(PAGE);

  return (
    <>
      <div className="catalog-filters">
        {areas.length > 1 ? (
          <div className="catalog-filter-group" role="group" aria-label="Filter by area of focus">
            <span className="catalog-filter-label">Area</span>
            <button
              aria-pressed={area === "all"}
              className="archive-filter"
              onClick={() => {
                setArea("all");
                reset();
              }}
              type="button"
            >
              All<span>{facilities.length}</span>
            </button>
            {areas.map((focus) => {
              const count = facilities.filter((item) =>
                item.focus_areas.some((f) => f.code === focus.code),
              ).length;
              return (
                <button
                  aria-pressed={area === focus.code}
                  className="archive-filter"
                  key={focus.code}
                  onClick={() => {
                    setArea(focus.code);
                    reset();
                  }}
                  style={
                    area === focus.code
                      ? { background: focus.accent_color, borderColor: focus.accent_color }
                      : undefined
                  }
                  title={focus.title}
                  type="button"
                >
                  {focus.code}
                  <span>{count}</span>
                </button>
              );
            })}
          </div>
        ) : null}

        {statuses.length > 1 ? (
          <div className="catalog-filter-group" role="group" aria-label="Filter by availability">
            <span className="catalog-filter-label">Status</span>
            <button
              aria-pressed={status === "all"}
              className="archive-filter"
              onClick={() => {
                setStatus("all");
                reset();
              }}
              type="button"
            >
              Any
            </button>
            {statuses.map((value) => (
              <button
                aria-pressed={status === value}
                className="archive-filter"
                key={value}
                onClick={() => {
                  setStatus(value);
                  reset();
                }}
                type="button"
              >
                {statusLabel(value)}
                <span>
                  {facilities.filter((i) => i.availability_status === value).length}
                </span>
              </button>
            ))}
          </div>
        ) : null}
      </div>

      {/* A filter combination can legitimately match nothing; saying so beats
          an empty grid that looks broken. */}
      {filtered.length === 0 ? (
        <p className="section-empty-copy">
          No equipment matches that combination.{" "}
          <button
            className="catalog-clear"
            onClick={() => {
              setArea("all");
              setStatus("all");
              reset();
            }}
            type="button"
          >
            Clear the filters
          </button>
        </p>
      ) : (
        <div className="focus-equipment-grid">
          {visible.map((facility, index) => (
            <article
              className={`equipment-card status-${facility.availability_status}`}
              key={facility.id ?? `${facility.name}-${index}`}
            >
              <div className="equipment-media">
                {facility.image ? (
                  <img src={facility.image} alt={facility.name} loading="lazy" />
                ) : (
                  <div className="equipment-image-placeholder" aria-hidden="true">
                    <svg viewBox="0 0 64 64" focusable="false">
                      <path d="M13 51h38M17 47V14h30v33M22 20h20v16H22zM27 24h10v8H27zM23 42h18" />
                      <circle cx="42" cy="42" r="2" />
                    </svg>
                    <span>ME</span>
                  </div>
                )}
                <span className="equipment-index">
                  {String(index + 1).padStart(2, "0")}
                </span>
                {facility.availability_status !== "available" ? (
                  <small className="equipment-status">
                    {facility.availability_label}
                  </small>
                ) : null}
              </div>
              <div className="equipment-card-body">
                <h3>{facility.name}</h3>
                <p>{facility.description}</p>
                {facility.focus_areas.length > 0 ? (
                  <ul className="equipment-areas">
                    {facility.focus_areas.map((focus) => (
                      <li
                        key={focus.code}
                        style={{ "--chip": focus.accent_color } as React.CSSProperties}
                        title={focus.title}
                      >
                        {focus.code}
                      </li>
                    ))}
                  </ul>
                ) : null}
              </div>
            </article>
          ))}
        </div>
      )}

      {remaining > 0 ? (
        <p className="archive-more">
          <button
            className="button button-navy"
            onClick={() => setShown((count) => count + PAGE)}
            type="button"
          >
            Show {Math.min(remaining, PAGE)} more
          </button>
          <span>
            Showing {visible.length} of {filtered.length}
          </span>
        </p>
      ) : null}
    </>
  );
}
