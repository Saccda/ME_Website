import type { NewsEvent } from "./api";

export type NewsEntry = {
  item: NewsEvent;
  date: string;
};

export type EventEntry = {
  item: NewsEvent;
  date: string;
  isUpcoming: boolean;
};

const DATE_FORMAT: Intl.DateTimeFormatOptions = {
  day: "numeric",
  month: "long",
  year: "numeric",
};

export function formatDispatchDate(value: string | null): string {
  if (!value) return "";
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime())
    ? ""
    : parsed.toLocaleDateString("en-GB", DATE_FORMAT);
}

function time(value: string | null): number {
  if (!value) return Number.NaN;
  const parsed = new Date(value).getTime();
  return Number.isNaN(parsed) ? Number.NaN : parsed;
}

/** Newest articles first. */
export function selectLatestNews(items: NewsEvent[], limit = 3): NewsEntry[] {
  return items
    .filter((item) => item.content_type === "news")
    .filter((item) => !Number.isNaN(time(item.published_at)))
    .sort((a, b) => time(b.published_at) - time(a.published_at))
    .slice(0, limit)
    .map((item) => ({ item, date: formatDispatchDate(item.published_at) }));
}

/**
 * Events still to come, soonest first.
 *
 * A programme with nothing scheduled would otherwise show an empty band, so any
 * remaining places are filled with the most recent past events — flagged, so a
 * card never implies a date that has already gone. `now` is injected to make the
 * boundary verifiable rather than dependent on the clock.
 */
export function selectUpcomingEvents(
  items: NewsEvent[],
  now: Date = new Date(),
  limit = 3,
): EventEntry[] {
  const startOfToday = new Date(now);
  startOfToday.setHours(0, 0, 0, 0);

  const dated = (item: NewsEvent) => time(item.event_date ?? item.published_at);

  const events = items
    .filter((item) => item.content_type === "event")
    .filter((item) => !Number.isNaN(dated(item)));

  const upcoming = events
    .filter((item) => dated(item) >= startOfToday.getTime())
    .sort((a, b) => dated(a) - dated(b))
    .map((item) => ({ item, isUpcoming: true }));

  const past = events
    .filter((item) => dated(item) < startOfToday.getTime())
    .sort((a, b) => dated(b) - dated(a))
    .map((item) => ({ item, isUpcoming: false }));

  return [...upcoming, ...past].slice(0, limit).map(({ item, isUpcoming }) => ({
    item,
    isUpcoming,
    date: formatDispatchDate(item.event_date ?? item.published_at),
  }));
}
