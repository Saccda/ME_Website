import type { NewsEvent } from "./api";

export type Dispatch = {
  item: NewsEvent;
  kind: "article" | "event";
  label: string;
  date: string | null;
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

/**
 * Picks the newest article and the next event still to come.
 *
 * When nothing is upcoming the most recent past event is used instead, relabelled
 * so the page never implies a date that has already passed. `now` is injected so
 * the boundary behaviour is verifiable rather than dependent on the clock.
 */
export function selectDispatches(
  items: NewsEvent[],
  now: Date = new Date(),
): Dispatch[] {
  const startOfToday = new Date(now);
  startOfToday.setHours(0, 0, 0, 0);

  const time = (value: string | null) => {
    if (!value) return Number.NaN;
    const parsed = new Date(value).getTime();
    return Number.isNaN(parsed) ? Number.NaN : parsed;
  };

  const latestArticle = items
    .filter((item) => item.content_type === "news")
    .filter((item) => !Number.isNaN(time(item.published_at)))
    .sort((a, b) => time(b.published_at) - time(a.published_at))[0];

  const events = items.filter((item) => item.content_type === "event");
  const upcoming = events
    .filter((item) => time(item.event_date) >= startOfToday.getTime())
    .sort((a, b) => time(a.event_date) - time(b.event_date))[0];
  const fallback = [...events].sort(
    (a, b) =>
      (time(b.event_date) || time(b.published_at)) -
      (time(a.event_date) || time(a.published_at)),
  )[0];
  const event = upcoming ?? fallback;

  const dispatches: Dispatch[] = [];

  if (latestArticle) {
    dispatches.push({
      item: latestArticle,
      kind: "article",
      label: "Latest article",
      date: formatDispatchDate(latestArticle.published_at),
    });
  }

  if (event) {
    dispatches.push({
      item: event,
      kind: "event",
      label: upcoming ? "Upcoming event" : "Most recent event",
      date: formatDispatchDate(event.event_date ?? event.published_at),
    });
  }

  return dispatches;
}
