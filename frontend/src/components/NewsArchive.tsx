/* eslint-disable @next/next/no-img-element */
"use client";

import Link from "next/link";
import { useState } from "react";
import type { NewsEvent } from "@/lib/api";

/**
 * The archive: every story once, filterable, revealed a page at a time.
 *
 * It replaces three overlapping bands. The old page listed all stories, then
 * listed the events again beneath them, then picked "publications" by
 * regex-matching titles for words like research and seminar -- so an event
 * appeared twice and a seminar write-up three times, and the page ran to five
 * and a half screens to say less than it appears to.
 *
 * Filtering is by type rather than by the CMS category field: seven articles
 * currently carry six categories, among them "Projects & Community" and
 * "Projects and Community Engagement", so category chips would read as noise
 * until an author has tidied them.
 */

const PAGE = 9;

type Filter = "all" | "news" | "event";

function formatDate(value: string | null) {
  if (!value) return "Date to be announced";
  return new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(value));
}

function StoryCard({ item }: { item: NewsEvent }) {
  return (
    <article className="story-card">
      <div className="story-media">
        {item.image ? <img src={item.image} alt="" loading="lazy" /> : <span>ME</span>}
        <small>{item.content_type}</small>
      </div>
      <div>
        {/* A span in words is not a datetime, so it cannot use <time>. */}
        {item.period ? (
          <span className="story-period">{item.period}</span>
        ) : (
          <time dateTime={item.event_date || item.published_at}>
            {formatDate(item.event_date || item.published_at)}
          </time>
        )}
        <h3>
          <Link href={`/news-events/${item.slug}`}>{item.title}</Link>
        </h3>
        <p>{item.excerpt}</p>
      </div>
    </article>
  );
}

export default function NewsArchive({ stories }: { stories: NewsEvent[] }) {
  const [filter, setFilter] = useState<Filter>("all");
  const [shown, setShown] = useState(PAGE);

  const counts = {
    all: stories.length,
    news: stories.filter((item) => item.content_type === "news").length,
    event: stories.filter((item) => item.content_type === "event").length,
  };

  const filtered =
    filter === "all"
      ? stories
      : stories.filter((item) => item.content_type === filter);
  const visible = filtered.slice(0, shown);
  const remaining = filtered.length - visible.length;

  // A filter with nothing behind it is a dead end, so it is not offered.
  const tabs = (["all", "news", "event"] as const).filter(
    (key) => counts[key] > 0,
  );

  if (stories.length === 0) {
    return (
      <div className="content-empty-state archive-empty">
        <h3>No posts have been published yet</h3>
        <p>
          Open houses, seminars, and program news are published from the ME
          content management system.
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="archive-head">
        <div>
          <p className="eyebrow">Archive</p>
          <h2>News from the program</h2>
        </div>
        {tabs.length > 1 ? (
          <div className="archive-filters" role="group" aria-label="Filter stories">
            {tabs.map((key) => (
              <button
                aria-pressed={filter === key}
                className="archive-filter"
                key={key}
                onClick={() => {
                  setFilter(key);
                  setShown(PAGE);
                }}
                type="button"
              >
                {key === "all" ? "All" : key === "news" ? "News" : "Events"}
                <span>{counts[key]}</span>
              </button>
            ))}
          </div>
        ) : null}
      </div>

      <div className="story-grid">
        {visible.map((item) => (
          <StoryCard item={item} key={item.id} />
        ))}
      </div>

      {remaining > 0 ? (
        <p className="archive-more">
          <button
            className="button button-navy"
            onClick={() => setShown((count) => count + PAGE)}
            type="button"
          >
            Show {Math.min(remaining, PAGE)} more
          </button>
          {/* Said plainly, so the reader knows how much archive is left rather
              than pressing a button that might go on forever. */}
          <span>
            Showing {visible.length} of {filtered.length}
          </span>
        </p>
      ) : null}
    </>
  );
}
