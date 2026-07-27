"use client";

/* eslint-disable @next/next/no-img-element */
import { useEffect, useState, type CSSProperties } from "react";
import type { ImpactProject } from "@/lib/impactProjects";

type ImpactStoryProps = {
  projects: ImpactProject[];
};

export default function ImpactStory({ projects }: ImpactStoryProps) {
  const slides = projects;
  const [activeIndex, setActiveIndex] = useState(0);
  const [paused, setPaused] = useState(false);
  const [interacting, setInteracting] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const updatePreference = () => setReducedMotion(mediaQuery.matches);
    updatePreference();
    mediaQuery.addEventListener("change", updatePreference);
    return () => mediaQuery.removeEventListener("change", updatePreference);
  }, []);

  useEffect(() => {
    if (slides.length < 2 || paused || interacting || reducedMotion) return;
    const timer = window.setInterval(() => {
      setActiveIndex((current) => (current + 1) % slides.length);
    }, 7000);
    return () => window.clearInterval(timer);
  }, [interacting, paused, reducedMotion, slides.length]);

  if (slides.length === 0) return null;
  const activeProject = slides[activeIndex];
  const accentStyle = {
    "--impact-accent": activeProject.accent,
    "--impact-accent-text":
      activeProject.accentText === "dark" ? "var(--navy)" : "var(--white)",
  } as CSSProperties;

  return (
    <div
      className="impact-story"
      onMouseEnter={() => setInteracting(true)}
      onMouseLeave={() => setInteracting(false)}
      onFocusCapture={() => setInteracting(true)}
      onBlurCapture={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget)) {
          setInteracting(false);
        }
      }}
    >
      <div className="impact-stage">
        <div className="impact-images">
          {slides.map((slide, index) => (
            <img
              className={index === activeIndex ? "active" : ""}
              src={slide.image}
              alt={index === activeIndex ? slide.alt : ""}
              loading={index === 0 ? "eager" : "lazy"}
              key={slide.id}
            />
          ))}
        </div>

        <div
          className="impact-feature"
          style={accentStyle}
          key={activeProject.id}
        >
          <div className="impact-feature-title">
            <span>{activeProject.field}</span>
            <h3>{activeProject.title}</h3>
          </div>

          <div className="impact-feature-panel">
            <p>{activeProject.description}</p>
            <a
              className="impact-action"
              href={activeProject.actionUrl}
              target="_blank"
              rel="noreferrer"
            >
              <span className="impact-action-icon" aria-hidden="true">
                {activeProject.actionKind === "video" ? "▶" : "≡"}
              </span>
              <span>{activeProject.actionLabel}</span>
            </a>
          </div>
        </div>

        <div className="impact-controls">
          <div
            className="impact-dots"
            role="tablist"
            aria-label="Design and manufacturing stories"
          >
            {slides.map((slide, index) => (
              <button
                className={index === activeIndex ? "active" : ""}
                type="button"
                role="tab"
                aria-label={`Show ${slide.title}`}
                aria-selected={index === activeIndex}
                onClick={() => setActiveIndex(index)}
                key={slide.id}
              />
            ))}
          </div>

          {!reducedMotion ? (
            <button
              className="impact-playback"
              type="button"
              aria-label={paused ? "Play image story" : "Pause image story"}
              aria-pressed={paused}
              onClick={() => setPaused((current) => !current)}
            >
              <span aria-hidden="true">{paused ? "▶" : "Ⅱ"}</span>
            </button>
          ) : null}
        </div>

        <a
          className="impact-credit"
          href={activeProject.sourceUrl}
          target="_blank"
          rel="noreferrer"
        >
          Image: {activeProject.sourceLabel} <span aria-hidden="true">↗</span>
        </a>
      </div>
    </div>
  );
}
