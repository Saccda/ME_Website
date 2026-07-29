/* eslint-disable @next/next/no-img-element */
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData, getNewsEvents, type NewsEvent } from "@/lib/api";

export const dynamic = "force-dynamic";

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
        {item.image ? <img src={item.image} alt="" /> : <span>ME</span>}
        <small>{item.content_type}</small>
      </div>
      <div>
        <time dateTime={item.event_date || item.published_at}>
          {formatDate(item.event_date || item.published_at)}
        </time>
        <h3>{item.title}</h3>
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
        <section className="directory-hero">
          <div className="shell">
            <p className="eyebrow light">News & events</p>
            <h1>
              Ideas, activities and
              <em>program life.</em>
            </h1>
            <p>
              Follow laboratory open houses, seminar series, student work,
              publications, partnerships, and Mechanical Engineering news.
            </p>
          </div>
        </section>

        <section className="section white" id="latest">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Latest</p>
                <h2>News from the ME community.</h2>
              </div>
            </div>
            {stories.length > 0 ? (
              <div className="story-grid">
                {stories.slice(0, 9).map((item) => (
                  <StoryCard item={item} key={item.id} />
                ))}
              </div>
            ) : (
              <div className="content-empty-state">
                <h3>News and event posts are coming soon.</h3>
                <p>
                  Lab open houses, seminars and program news can be published
                  from the ME content management system.
                </p>
              </div>
            )}
          </div>
        </section>

        <section className="section cream" id="lab-openhouse">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Upcoming events</p>
                <h2>Open houses, seminars and program activities.</h2>
              </div>
            </div>
            {events.length > 0 ? (
              <div className="story-grid compact-stories">
                {events.slice(0, 6).map((item) => (
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
                <p className="eyebrow light">Seminars & publications</p>
                <h2>Knowledge shared beyond the classroom.</h2>
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
