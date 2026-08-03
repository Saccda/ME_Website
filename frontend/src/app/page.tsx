/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import ImpactStory from "@/components/ImpactStory";
import JobOpportunities from "@/components/IndustryCareers";
import QuadrupleHelix from "@/components/QuadrupleHelix";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData, getNewsEvents } from "@/lib/api";
import { selectDispatches } from "@/lib/homeDispatches";
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
  const dispatches = selectDispatches(newsEvents);

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

        {dispatches.length > 0 ? (
          <section className="section cream" id="latest">
            <div className="shell">
              <div className="section-masthead">
                <p className="eyebrow">News &amp; events</p>
                <EditorialSectionHeading text="What is happening now. Read and join in." />
              </div>

              <div className="dispatch-grid">
                {dispatches.map((entry) => (
                  <article
                    className={`dispatch-card${entry.kind === "event" ? " is-event" : ""}`}
                    key={entry.item.id}
                  >
                    {entry.item.image ? (
                      <div className="dispatch-media">
                        <img
                          src={entry.item.image}
                          alt={entry.item.title}
                          loading="lazy"
                        />
                      </div>
                    ) : null}
                    <div className="dispatch-body">
                      <p className="dispatch-kicker">
                        <strong>{entry.label}</strong>
                        {entry.date ? <span>{entry.date}</span> : null}
                      </p>
                      <h3>{entry.item.title}</h3>
                      <p>{entry.item.excerpt}</p>
                      <Link
                        className="dispatch-link"
                        href={`/news-events#${entry.item.slug}`}
                      >
                        {entry.kind === "event" ? "Event details" : "Read article"}{" "}
                        <span aria-hidden="true">→</span>
                      </Link>
                    </div>
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
