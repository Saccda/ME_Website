/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData, getNewsEvents, type NewsEvent } from "@/lib/api";
import { formatDateRange } from "@/lib/homeDispatches";

export const dynamic = "force-dynamic";

function formatDate(value: string | null) {
  if (!value) return "Date to be announced";
  return new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(value));
}

/** Events can run over several days; news has a single publication date. */
function storyDate(item: NewsEvent) {
  if (item.content_type === "event" && item.event_date) {
    return formatDateRange(item.event_date, item.event_end_date);
  }
  return formatDate(item.event_date || item.published_at);
}

function StoryCard({ item }: { item: NewsEvent }) {
  return (
    <article className="story-card">
      <div className="story-media">
        {item.image ? <img src={item.image} alt="" /> : <span>ME</span>}
        <small>{item.content_type}</small>
      </div>
      <div>
        {/* A span in words is not a datetime, so it cannot use <time>. Work
            that ran across months reads truer as its period than as the one
            date it happened to be filed under. */}
        {item.period ? (
          <span className="story-period">{item.period}</span>
        ) : (
          <time dateTime={item.event_date || item.published_at}>
            {storyDate(item)}
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

export default async function NewsEventsPage() {
  const [home, stories] = await Promise.all([getHomeData(), getNewsEvents()]);
  const events = stories.filter((item) => item.content_type === "event");
  const publications = stories.filter(
    (item) =>
      item.content_type === "news" &&
      /publication|journal|paper|research|seminar/i.test(
        `${item.title} ${item.excerpt}`,
      ),
  );

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs trail={[{ label: "News & Events" }]} />
        <section className="directory-hero">
          <div className="shell">
            <p className="eyebrow light">News & events</p>
            <h1>News &amp; Events</h1>
            <p>
              Open houses, seminar series, student work, publications,
              partnerships, and Mechanical Engineering program news.
            </p>
          </div>
        </section>

        <section className="section white" id="latest">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Latest</p>
                <h2>News from the program</h2>
              </div>
            </div>
            {stories.length > 0 ? (
              /* Every published story, not the newest nine. The cap made
                 older articles unreachable from the site as soon as the
                 archive outgrew it, with no pagination to reach them. */
              <div className="story-grid">
                {stories.map((item) => (
                  <StoryCard item={item} key={item.id} />
                ))}
              </div>
            ) : (
              <div className="content-empty-state">
                <h3>No posts have been published yet</h3>
                <p>
                  Open houses, seminars, and program news are published from
                  the ME content management system.
                </p>
              </div>
            )}
          </div>
        </section>

        <section className="section cream" id="lab-openhouse">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Upcoming</p>
                <h2>Events and open houses</h2>
              </div>
            </div>
            {events.length > 0 ? (
              <div className="story-grid compact-stories">
                {events.map((item) => (
                  <StoryCard item={item} key={item.id} />
                ))}
              </div>
            ) : (
              <p className="section-empty-copy">
                The next event schedule will be announced here.
              </p>
            )}
          </div>
        </section>

        <section className="section navy" id="seminar-series">
          <span id="publication" aria-hidden="true" />
          <div className="shell">
            <div className="detail-section-heading inverse">
              <div>
                <p className="eyebrow light">Knowledge sharing</p>
                <h2>Seminars and publications</h2>
              </div>
            </div>
            {publications.length > 0 ? (
              <div className="publication-list">
                {publications.map((item) => (
                  <article key={item.id}>
                    <time>{formatDate(item.published_at)}</time>
                    <h3>{item.title}</h3>
                    <p>{item.excerpt}</p>
                  </article>
                ))}
              </div>
            ) : (
              <p className="section-empty-copy light-copy">
                Seminar recordings and publication highlights will be added as
                they become available.
              </p>
            )}
          </div>
        </section>
      </main>
      <SiteFooter
        focusAreas={home.focus_areas}
        settings={home.settings}
      />
    </>
  );
}
