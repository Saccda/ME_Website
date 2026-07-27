/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import ImpactStory from "@/components/ImpactStory";
import JobOpportunities from "@/components/IndustryCareers";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData } from "@/lib/api";
import { getResearchImage } from "@/lib/editorialImages";
import { impactProjects } from "@/lib/impactProjects";

export const dynamic = "force-dynamic";

export default async function Home() {
  const data = await getHomeData();
  const program = data.settings;
  const partners = [...data.partners, ...data.partners];

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
              <div>
                <strong>{program.program_years}</strong>
                <span>Year program</span>
              </div>
              <div>
                <strong>{data.focus_areas.length}</strong>
                <span>Areas of focus</span>
              </div>
              <div>
                <strong>{program.credit_hours}+</strong>
                <span>Credit hours</span>
              </div>
              <div>
                <strong>Theory + Practice</strong>
                <span>Balanced learning</span>
              </div>
            </div>
          </div>
        </section>

        <section className="section cream discipline-section" id="what-is-me">
          <div className="shell">
            <div className="impact-heading">
              <div>
                <p className="eyebrow">What is mechanical engineering?</p>
                <h2>
                  Designed by engineers.
                  <em>Built for the world.</em>
                </h2>
              </div>
              <p>
                From drones and vehicles to satellites, robots, and the cooling
                systems behind AI, mechanical engineers shape how modern
                products move, work, and endure.
              </p>
            </div>
            <ImpactStory projects={impactProjects} />
          </div>
        </section>

        <section className="section white" id="focus">
          <div className="shell">
            <div className="section-intro">
              <div>
                <p className="eyebrow">Areas of focus</p>
                <h2>
                  Four paths.
                  <em>One purpose.</em>
                </h2>
              </div>
              <p>
                Move fluently between theory, simulation, fabrication, testing,
                and responsible engineering practice.
              </p>
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
            <div className="section-intro">
              <div>
                <p className="eyebrow">Why choose ME at RUPP?</p>
                <h2>
                  Nine reasons.
                  <em>One future-ready program.</em>
                </h2>
              </div>
              <p>
                Our learning model brings technology, social responsibility,
                and active practice together—so graduates leave ready to
                contribute from day one.
              </p>
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

        <section className="section navy" id="research">
          <div className="shell">
            <div className="section-intro inverse">
              <div>
                <p className="eyebrow light">Applied research</p>
                <h2>
                  Ideas made
                  <em>useful.</em>
                </h2>
              </div>
              <p>
                Student and faculty teams investigate practical problems with
                measurable relevance to Cambodian communities and industry.
              </p>
            </div>
            <div className="research-grid">
              {data.research.map((project) => (
                <article className="research-card" key={project.slug}>
                  <div className="research-media">
                    <img
                      src={getResearchImage(project.title, project.image || "")}
                      alt=""
                      loading="lazy"
                    />
                    <span>{project.focus_area?.code || "ME"}</span>
                  </div>
                  <div>
                    <small>Student & faculty research</small>
                    <h3>{project.title}</h3>
                    <p>{project.summary}</p>
                    <a
                      href={`mailto:${program.email}?subject=${encodeURIComponent(
                        `ME research enquiry: ${project.title}`,
                      )}`}
                    >
                      Discuss the project <span>↗</span>
                    </a>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section gold partners" id="partners">
          <div className="shell partner-lead">
            <div className="partner-lead-copy">
              <p className="eyebrow">Partners & industry</p>
              <h2>Education and industry, connected.</h2>
            </div>
            <div className="partner-lead-action">
              <p>
                Our partnerships connect learning with applied research,
                industry experience, and career opportunities for ME students.
              </p>
              <a
                className="button button-navy"
                href={`mailto:${program.email}?subject=ME partnership enquiry`}
              >
                Start a partnership <span>↗</span>
              </a>
            </div>
          </div>
          <div className="marquee" aria-label="ME Program partners">
            <div className="marquee-track">
              {partners.map((partner, index) => (
                <div className="partner-logo" key={`${partner.name}-${index}`}>
                  <img src={partner.logo || ""} alt={partner.name} loading="lazy" />
                  <small>{partner.partner_type}</small>
                </div>
              ))}
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

      </main>

      <SiteFooter focusAreas={data.focus_areas} settings={program} />
    </>
  );
}
