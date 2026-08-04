/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import ImpactStory from "@/components/ImpactStory";
import JobOpportunities from "@/components/IndustryCareers";
import QuadrupleHelix from "@/components/QuadrupleHelix";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData, getNewsEvents } from "@/lib/api";
import {
  selectLatestNews,
  selectUpcomingEvents,
} from "@/lib/homeDispatches";
import { impactProjects } from "@/lib/impactProjects";

export const dynamic = "force-dynamic";

function EditorialSectionHeading({ text }: { text: string }) {
  const sentenceBreak = text.match(/^(.+?[.!?])\s+(.+)$/);

  if (!sentenceBreak) {
    return <h2>{text}</h2>;
  }

  return (
    <h2>
      <span>{sentenceBreak[1]}</span>{" "}
      <em>{sentenceBreak[2]}</em>
    </h2>
  );
}

export default async function Home() {
  const [data, newsEvents] = await Promise.all([getHomeData(), getNewsEvents()]);
  const program = data.settings;
  const partners = [...data.partners, ...data.partners];
  const latestNews = selectLatestNews(newsEvents);
  const upcomingEvents = selectUpcomingEvents(newsEvents);

  return (
    <>
      <SiteHeader settings={program} />

      <main id="main-content">
        <section className="hero" id="top">
          <img
            className="hero-image"
            src={program.hero_image || "/assets/hero-lab.png"}
            alt="Mechanical engineering students working in a robotics laboratory"
          />
          <div className="hero-overlay" />
          <div className="hero-grid" aria-hidden="true" />
          <div className="shell hero-content">
            <h1>
              <span>{program.hero_title}</span>
              <em>{program.hero_emphasis}</em>
            </h1>
            <p>{program.hero_description}</p>
            <div className="hero-actions">
              <a className="button button-gold" href="#what-is-me">
                Explore the program <span>↗</span>
              </a>
              <a className="text-link light" href="#partners">
                Partner with us <span>→</span>
              </a>
            </div>
          </div>
          <div className="hero-stats">
            <div className="shell stat-grid">
              <div className="stat-card">
                <strong>{program.program_years}</strong>
                <span>Year program</span>
              </div>
              <div className="stat-card">
                <strong>{data.focus_areas.length}</strong>
                <span>Areas of focus</span>
              </div>
              <div className="stat-card stat-card-phrase">
                <strong>Theory + Practice</strong>
                <span>Balanced learning</span>
              </div>
              <div className="stat-card">
                <strong>{program.credit_hours}+</strong>
                <span>Credit hours</span>
              </div>
            </div>
          </div>
        </section>

        <section className="section cream discipline-section" id="what-is-me">
          <div className="shell">
            <div className="section-masthead">
              <p className="eyebrow">{program.what_is_me_eyebrow}</p>
              <EditorialSectionHeading text={program.what_is_me_heading} />
              <p>{program.what_is_me_intro}</p>
            </div>
            <ImpactStory projects={impactProjects} />
          </div>
        </section>

        <section className="section white" id="focus">
          <div className="shell">
            <div className="section-masthead">
              <p className="eyebrow">{program.focus_section_eyebrow}</p>
              <EditorialSectionHeading text={program.focus_section_heading} />
              <p>{program.focus_section_intro}</p>
            </div>
            <div className="focus-grid">
              {data.focus_areas.map((area, index) => (
                <Link
                  className="focus-card"
                  href={`/focus/${area.slug}`}
                  key={area.code}
                  style={{ "--accent": area.accent_color } as React.CSSProperties}
                >
                  <div className="focus-meta">
                    <span>{area.code}</span>
                    <b>0{index + 1}</b>
                  </div>
                  <div className="focus-media">
                    <img src={area.image || ""} alt="" loading="lazy" />
                  </div>
                  <h3>{area.title}</h3>
                  <p>{area.description}</p>
                  <span className="focus-link">
                    Explore {area.code} <span>↗</span>
                  </span>
                </Link>
              ))}
            </div>
          </div>
        </section>

        <section className="section cream" id="why-me">
          <div className="shell">
            <div className="section-masthead">
              <p className="eyebrow">{program.why_section_eyebrow}</p>
              <EditorialSectionHeading text={program.why_section_heading} />
              <p>{program.why_section_intro}</p>
            </div>
            <div className="proof-grid">
              {data.why_choose.map((item, index) => (
                <article className="proof-card" key={item.id || item.title}>
                  <header>
                    <span>{String(index + 1).padStart(2, "0")}</span>
                    <h3>{item.title}</h3>
                  </header>
                  <div
                    className={`proof-media ${item.media_kind === "logo" ? "logo-media" : ""}`}
                  >
                    <img src={item.image || ""} alt="" loading="lazy" />
                  </div>
                  <p>{item.description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section gold partners" id="partners">
          <QuadrupleHelix />
          <div className="shell partner-lead">
            <div className="partner-lead-copy">
              <p className="eyebrow">{program.partners_section_eyebrow}</p>
              <EditorialSectionHeading text={program.partners_section_heading} />
              <p>{program.partners_section_intro}</p>
            </div>
            <div className="partner-lead-action">
              <Link className="button button-navy" href="/partnership">
                Learn more about partnering with ME <span>↗</span>
              </Link>
            </div>
          </div>
          <div className="marquee" aria-label="ME Program partners">
            <div className="marquee-track">
              {partners.map((partner, index) => {
                const logo = (
                  <>
                    <img
                      src={partner.logo || ""}
                      alt={partner.name}
                      loading="lazy"
                    />
                    <small>{partner.partner_type}</small>
                  </>
                );

                return partner.website ? (
                  <a
                    className="partner-logo"
                    href={partner.website}
                    key={`${partner.name}-${index}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`Visit ${partner.name} website`}
                  >
                    {logo}
                  </a>
                ) : (
                  <div
                    className="partner-logo"
                    key={`${partner.name}-${index}`}
                  >
                    {logo}
                  </div>
                );
              })}
            </div>
          </div>
          <div className="partner-jobs-band">
            <div className="shell">
              <JobOpportunities
                email={program.email}
                facebookUrl={program.facebook_url}
                opportunities={data.opportunities}
                telegramUrl={program.telegram_url}
              />
            </div>
          </div>
        </section>

        {latestNews.length > 0 ? (
          <section className="section cream home-feed" id="latest-news">
            <div className="shell">
              {/* Centred masthead: the section carries projects, community
                  work and partnerships as well as news, so it is introduced
                  as a whole rather than labelled with a single content type. */}
              <header className="home-feed-head centred">
                <p className="eyebrow">{program.news_section_eyebrow}</p>
                <h2>{program.news_section_heading}</h2>
                <p className="home-feed-intro">{program.news_section_intro}</p>
              </header>

              <div className="home-feed-grid">
                {latestNews.map((entry) => (
                  <article className="news-card" key={entry.item.id}>
                    {entry.item.image ? (
                      <div className="news-card-media">
                        <img src={entry.item.image} alt="" loading="lazy" />
                      </div>
                    ) : null}
                    <div className="news-card-body">
                      <p className="news-card-kicker">
                        {entry.item.category || "News"}
                      </p>
                      {/* Only the title is a link; it stretches over the card so
                          the row exposes one target per article. */}
                      <h3>
                        <Link href={`/news-events/${entry.item.slug}`}>
                          {entry.item.title}
                        </Link>
                      </h3>
                      <p className="news-card-excerpt">{entry.item.excerpt}</p>
                      <span className="news-card-cue" aria-hidden="true">
                        Read story <span>→</span>
                      </span>
                    </div>
                  </article>
                ))}
              </div>

              <p className="home-feed-action">
                <Link className="button button-navy" href="/news-events">
                  {program.news_section_cta_label}{" "}
                  <span aria-hidden="true">→</span>
                </Link>
              </p>
            </div>
          </section>
        ) : null}

        {upcomingEvents.length > 0 ? (
          <section className="section white home-feed" id="upcoming-events">
            <div className="shell">
              <header className="home-feed-head">
                <h2>Upcoming events</h2>
                <Link className="home-feed-all" href="/news-events">
                  View all events
                </Link>
              </header>

              <div className="home-feed-grid">
                {upcomingEvents.map((entry) => (
                  <article className="event-card" key={entry.item.id}>
                    {entry.item.image ? (
                      <div className="event-card-media">
                        <img src={entry.item.image} alt="" loading="lazy" />
                      </div>
                    ) : null}
                    <p className="event-card-badge">
                      {entry.item.category ||
                        (entry.isUpcoming ? "Upcoming event" : "Recent event")}
                    </p>
                    <h3>{entry.item.title}</h3>
                    {entry.date ? (
                      <p className="event-card-date">{entry.date}</p>
                    ) : null}
                    <p className="event-card-excerpt">{entry.item.excerpt}</p>
                    <Link
                      className="event-card-action"
                      href={`/news-events/${entry.item.slug}`}
                      aria-label={`Event details: ${entry.item.title}`}
                    >
                      Event details
                    </Link>
                  </article>
                ))}
              </div>
            </div>
          </section>
        ) : null}

      </main>

      <SiteFooter focusAreas={data.focus_areas} settings={program} />
    </>
  );
}
