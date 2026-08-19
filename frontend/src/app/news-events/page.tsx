import Link from "next/link";
import Breadcrumbs from "@/components/Breadcrumbs";
import NewsArchive from "@/components/NewsArchive";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData, getNewsEvents, type NewsEvent } from "@/lib/api";
import { formatDateRange } from "@/lib/homeDispatches";

export const dynamic = "force-dynamic";

/**
 * An event is upcoming until the day it finishes. A multi-day event is still
 * upcoming while it is running, so the end date decides.
 */
function isUpcoming(item: NewsEvent, now: Date) {
  if (item.content_type !== "event") return false;
  const start = Date.parse(item.event_date ?? item.published_at);
  if (Number.isNaN(start)) return false;
  const finish = Date.parse(item.event_end_date ?? "") || start;

  const startOfToday = new Date(now);
  startOfToday.setHours(0, 0, 0, 0);
  return finish >= startOfToday.getTime();
}

function UpcomingCard({ item }: { item: NewsEvent }) {
  return (
    <article className="upcoming-card">
      <p className="upcoming-when">
        {formatDateRange(
          item.event_date ?? item.published_at,
          item.event_end_date,
        )}
      </p>
      <h3>
        <Link href={`/news-events/${item.slug}`}>{item.title}</Link>
      </h3>
      <p className="upcoming-excerpt">{item.excerpt}</p>
      <span className="upcoming-cue" aria-hidden="true">
        Event details <span>&rarr;</span>
      </span>
    </article>
  );
}

export default async function NewsEventsPage() {
  const [home, stories] = await Promise.all([getHomeData(), getNewsEvents()]);

  const now = new Date();
  const upcoming = stories
    .filter((item) => isUpcoming(item, now))
    .sort(
      (a, b) =>
        Date.parse(a.event_date ?? a.published_at) -
        Date.parse(b.event_date ?? b.published_at),
    );

  // Whatever is in the upcoming strip is left out of the archive, so no story
  // is listed twice. An event drops into the archive once it has happened.
  const upcomingIds = new Set(upcoming.map((item) => item.id));
  const archive = stories.filter((item) => !upcomingIds.has(item.id));

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs trail={[{ label: "News & Events" }]} />

        {/* Compact: the full-height version spent 60% of the first screen on a
            title and one sentence, and pushed the first article 820px down. */}
        <section className="directory-hero is-compact">
          <div className="shell">
            <h1>News &amp; Events</h1>
            <p>
              Open houses, seminar series, student work, publications,
              partnerships, and Mechanical Engineering program news.
            </p>
          </div>
        </section>

        {upcoming.length > 0 ? (
          <section className="section cream" id="upcoming">
            <div className="shell">
              <div className="detail-section-heading">
                <div>
                  <p className="eyebrow">Upcoming</p>
                  <h2>
                    {upcoming.length === 1
                      ? "One event coming up"
                      : `${upcoming.length} events coming up`}
                  </h2>
                </div>
              </div>
              <div className="upcoming-grid">
                {upcoming.map((item) => (
                  <UpcomingCard item={item} key={item.id} />
                ))}
              </div>
            </div>
          </section>
        ) : null}

        <section className="section white archive-section" id="latest">
          <div className="shell">
            {/* The filters sit on the heading row rather than under it: a row
                of their own cost 68px and pushed the first card off screen. */}
            <NewsArchive stories={archive} />
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
