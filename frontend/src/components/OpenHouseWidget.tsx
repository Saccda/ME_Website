"use client";

import { useCallback, useEffect, useRef, useState } from "react";

/**
 * ME Lab Open House event widget.
 *
 * Ported from the approved mock-up
 * `ME-Lab-Open-House-Robot-Arm-Always-Visible-Mockup.html`
 * (sha256 ffe362cad809494ff0aed8dc913072eb8191b6c9c656cc4dbbd7a13fd5b86c67).
 *
 * The markup, class names, element ids, inline SVG, keyframes and geometry are
 * reproduced exactly; only the supplied IIFE is expressed with React state,
 * because the framework owns the DOM. The class sequence it drives is
 * unchanged: `is-opening` for 1080ms, then `is-open`.
 *
 * The card and the industrial arm are independent siblings. The arm is
 * absolutely positioned inside `.panel-scene`, so it never contributes to the
 * card's width and never enters it.
 */

const OPEN_DELAY_MS = 1080;

export default function OpenHouseWidget() {
  const [state, setState] = useState<"closed" | "opening" | "open">("closed");
  const [toastVisible, setToastVisible] = useState(false);
  const launcherRef = useRef<HTMLButtonElement>(null);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    return () => {
      if (timerRef.current !== null) window.clearTimeout(timerRef.current);
    };
  }, []);

  const setOpen = useCallback((open: boolean) => {
    if (timerRef.current !== null) window.clearTimeout(timerRef.current);

    if (!open) {
      setState("closed");
      setToastVisible(false);
      return;
    }

    const reduceMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    if (reduceMotion) {
      setState("open");
      return;
    }

    setState("opening");
    timerRef.current = window.setTimeout(
      () => setState("open"),
      OPEN_DELAY_MS,
    );
  }, []);

  const closeAndRefocus = useCallback(() => {
    setOpen(false);
    launcherRef.current?.focus();
  }, [setOpen]);

  const layerClass = [
    "event-layer",
    state === "opening" ? "is-opening" : "",
    state === "open" ? "is-open" : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div
      id="me-open-house-widget-demo"
      onKeyDown={(event) => {
        if (event.key === "Escape" && state !== "closed") closeAndRefocus();
      }}
    >
      <div className={layerClass} id="me-event-layer">
        <div className="panel-scene">
          <div className="independent-robot-arm" aria-hidden="true">
            <svg
              viewBox="0 0 240 330"
              role="img"
              aria-label="Freestanding three dimensional robot arm presenting the Open House card"
            >
              <defs>
                <linearGradient id="armShell3d" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0" stopColor="#ffffff" />
                  <stop offset=".38" stopColor="#e3efff" />
                  <stop offset=".72" stopColor="#8eb1df" />
                  <stop offset="1" stopColor="#456faa" />
                </linearGradient>
                <linearGradient id="armBlue3d" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0" stopColor="#2373d0" />
                  <stop offset=".48" stopColor="#0b469e" />
                  <stop offset="1" stopColor="#031a46" />
                </linearGradient>
                <radialGradient id="armGold3d" cx="30%" cy="22%" r="85%">
                  <stop offset="0" stopColor="#fff9d8" />
                  <stop offset=".28" stopColor="#f3c53d" />
                  <stop offset="1" stopColor="#9a6100" />
                </radialGradient>
                <linearGradient id="armFloor3d" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0" stopColor="#154b91" stopOpacity=".42" />
                  <stop offset="1" stopColor="#021638" stopOpacity="0" />
                </linearGradient>
                <filter
                  id="armGlow3d"
                  x="-100%"
                  y="-100%"
                  width="300%"
                  height="300%"
                >
                  <feGaussianBlur stdDeviation="5" />
                </filter>
              </defs>

              <ellipse cx="119" cy="306" rx="89" ry="17" fill="#021638" opacity=".22" />
              <ellipse cx="119" cy="300" rx="66" ry="10" fill="url(#armFloor3d)" />

              <g className="arm-machine">
                <path
                  d="M66 279 Q70 253 92 244 H145 Q167 253 172 279 L164 298 H74Z"
                  fill="url(#armBlue3d)"
                  stroke="#05285f"
                  strokeWidth="4"
                />
                <path
                  d="M76 279 H162 L154 293 H84Z"
                  fill="url(#armShell3d)"
                  stroke="#6388b9"
                  strokeWidth="3"
                />
                <rect
                  x="84"
                  y="257"
                  width="69"
                  height="24"
                  rx="11"
                  fill="#071f46"
                  stroke="#2c64a8"
                  strokeWidth="3"
                />
                <text
                  x="118.5"
                  y="273"
                  textAnchor="middle"
                  fill="#f3c53d"
                  fontFamily="Inter,Arial,sans-serif"
                  fontSize="13"
                  fontWeight="900"
                >
                  ME
                </text>
                <circle
                  className="arm-status-light"
                  cx="146"
                  cy="269"
                  r="4"
                  fill="#32d21f"
                  filter="url(#armGlow3d)"
                />

                <path
                  d="M88 250 Q78 240 79 222 Q80 203 96 195 H131 Q149 202 151 221 Q151 240 137 250Z"
                  fill="url(#armShell3d)"
                  stroke="#6388b9"
                  strokeWidth="4"
                />
                <circle
                  cx="114"
                  cy="220"
                  r="24"
                  fill="url(#armGold3d)"
                  stroke="#915b00"
                  strokeWidth="4"
                />
                <circle
                  cx="114"
                  cy="220"
                  r="11"
                  fill="#092b67"
                  stroke="#4f7fba"
                  strokeWidth="3"
                />

                <path
                  d="M104 205 Q82 181 80 155 Q79 136 93 128 Q108 123 120 139 L137 191 Q138 205 125 214 Q114 219 104 205Z"
                  fill="url(#armBlue3d)"
                  stroke="#05285f"
                  strokeWidth="5"
                />
                <path
                  d="M101 196 Q89 176 87 153 Q86 143 94 139 Q102 137 108 147 L124 191Z"
                  fill="url(#armShell3d)"
                  opacity=".72"
                />
                <circle
                  cx="91"
                  cy="143"
                  r="24"
                  fill="url(#armGold3d)"
                  stroke="#915b00"
                  strokeWidth="4"
                />
                <circle
                  cx="91"
                  cy="143"
                  r="10"
                  fill="#08265b"
                  stroke="#4f7fba"
                  strokeWidth="3"
                />

                <g className="arm-forearm">
                  <path
                    d="M101 130 Q123 102 151 83 Q164 75 176 87 Q186 100 173 112 L119 151 Q105 158 95 147 Q86 138 101 130Z"
                    fill="url(#armShell3d)"
                    stroke="#6388b9"
                    strokeWidth="5"
                  />
                  <path
                    d="M113 126 Q135 104 155 93 Q164 88 170 95 Q174 102 165 108 L119 141Z"
                    fill="url(#armBlue3d)"
                    opacity=".78"
                  />
                  <circle
                    cx="170"
                    cy="96"
                    r="20"
                    fill="url(#armGold3d)"
                    stroke="#915b00"
                    strokeWidth="4"
                  />
                  <circle
                    cx="170"
                    cy="96"
                    r="8"
                    fill="#08265b"
                    stroke="#4f7fba"
                    strokeWidth="3"
                  />

                  <path
                    d="M184 88 L205 82 Q214 81 217 89 L217 104 Q216 111 208 112 L185 106Z"
                    fill="url(#armBlue3d)"
                    stroke="#05285f"
                    strokeWidth="4"
                  />
                  <path
                    d="M214 87 L229 77"
                    fill="none"
                    stroke="url(#armGold3d)"
                    strokeWidth="7"
                    strokeLinecap="round"
                  />
                  <path
                    d="M215 106 L232 115"
                    fill="none"
                    stroke="url(#armGold3d)"
                    strokeWidth="7"
                    strokeLinecap="round"
                  />
                  <path
                    d="M225 78 L235 80"
                    fill="none"
                    stroke="#fff4c8"
                    strokeWidth="3"
                    strokeLinecap="round"
                  />
                  <path
                    d="M229 114 L237 109"
                    fill="none"
                    stroke="#fff4c8"
                    strokeWidth="3"
                    strokeLinecap="round"
                  />
                </g>

                <path
                  d="M85 130 Q90 124 99 124"
                  fill="none"
                  stroke="#ffffff"
                  strokeWidth="4"
                  strokeLinecap="round"
                  opacity=".68"
                />
                <path
                  d="M88 204 Q97 195 108 196"
                  fill="none"
                  stroke="#ffffff"
                  strokeWidth="4"
                  strokeLinecap="round"
                  opacity=".55"
                />
              </g>
            </svg>
          </div>

          <section
            className="event-panel"
            id="me-event-panel"
            role="dialog"
            aria-modal="false"
            aria-labelledby="me-event-title"
          >
            <div className="fold-section fold-section-top">
              <div className="panel-top">
                <span className="live-label">
                  <span className="live-dot" aria-hidden="true"></span>
                  Registration open
                </span>
                <button
                  className="close-event"
                  id="me-event-close"
                  type="button"
                  aria-label="Close event announcement"
                  onClick={closeAndRefocus}
                >
                  ×
                </button>
              </div>

              <div className="event-hero">
                <div className="date-plate" aria-label="Saturday 15 August 2026">
                  <span>AUG</span>
                  <strong>15</strong>
                  <small>SAT 2026</small>
                </div>
                <div>
                  <p className="event-kicker">Upcoming event</p>
                  <h2 className="event-title" id="me-event-title">
                    ME Lab Open House 2026
                  </h2>
                  <p className="event-subtitle">Explore. Experience. Engineer.</p>
                </div>
              </div>
            </div>

            <div className="fold-section fold-section-middle">
              <div className="event-meta">
                <div className="meta-row">
                  <span className="meta-icon" aria-hidden="true">
                    ◷
                  </span>
                  <span>9:00 AM–12:00 PM</span>
                </div>
                <div className="meta-row">
                  <span className="meta-icon" aria-hidden="true">
                    ⌖
                  </span>
                  <span>ME CDIO Learning Workspace</span>
                </div>
              </div>

              <p className="experience-label">What you will experience</p>
              <ul className="experience-list">
                <li>Hands-on activities</li>
                <li>Live equipment demos</li>
                <li>Guided laboratory tour</li>
              </ul>
            </div>

            <div className="fold-section fold-section-bottom">
              <div className="event-actions">
                <a
                  className="register-action"
                  id="me-register-action"
                  href="#registration-form-placeholder"
                  onClick={(event) => {
                    event.preventDefault();
                    setToastVisible(true);
                  }}
                >
                  Register free <span aria-hidden="true">→</span>
                </a>
                <a
                  className="details-action"
                  id="me-details-action"
                  href="#event-details-placeholder"
                  onClick={(event) => {
                    event.preventDefault();
                    setToastVisible(true);
                  }}
                >
                  Details
                </a>
              </div>
              <p className="event-footnote">
                Free admission · Advance registration required
              </p>
              <div
                className={`event-toast${toastVisible ? " is-visible" : ""}`}
                id="me-event-toast"
                role="status"
              >
                Replace this placeholder with the official registration-form
                link.
              </div>
            </div>
          </section>
        </div>

        <button
          className="event-launcher"
          id="me-event-launcher"
          type="button"
          aria-expanded={state !== "closed"}
          aria-controls="me-event-panel"
          onClick={() => setOpen(true)}
          ref={launcherRef}
        >
          <span className="new-tag">NEW</span>
          <span className="launcher-mascot" aria-hidden="true"></span>
          <span className="launcher-copy">
            <small>Upcoming event</small>
            <strong>ME Lab Open House · 15 Aug</strong>
          </span>
        </button>
      </div>
    </div>
  );
}
