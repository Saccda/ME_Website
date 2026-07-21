/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import CurriculumTabs from "@/components/CurriculumTabs";
import InquiryForm from "@/components/InquiryForm";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData } from "@/lib/api";
import {
  getHomeFacilityImage,
  getResearchImage,
} from "@/lib/editorialImages";

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
              <a className="button button-gold" href="#why-me">
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

        <section className="section navy vision" id="vision">
          <div className="shell vision-layout">
            <div>
              <p className="eyebrow light">Our vision</p>
              <span className="orbit" aria-hidden="true" />
            </div>
            <blockquote>“{program.vision}.”</blockquote>
          </div>
        </section>

        <section className="section cream">
          <div className="shell">
            <div className="section-intro compact">
              <div>
                <p className="eyebrow">Our mission</p>
                <h2>
                  Education with
                  <em>purpose and momentum.</em>
                </h2>
              </div>
            </div>
            <div className="mission-grid">
              {[program.mission_one, program.mission_two].map((mission, index) => (
                <article key={mission}>
                  <span>0{index + 1}</span>
                  <div className="mission-icon" aria-hidden="true">
                    {index === 0 ? "⌁" : "◎"}
                  </div>
                  <p>{mission}</p>
                </article>
              ))}
            </div>
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

        <section className="section cream" id="curriculum">
          <div className="shell">
            <div className="section-intro">
              <div>
                <p className="eyebrow">Curriculum journey</p>
                <h2>
                  Foundations to
                  <em>professional practice.</em>
                </h2>
              </div>
              <p>
                A four-year progression from core scientific thinking to
                integrated design, industry experience, and capstone work.
              </p>
            </div>
            <CurriculumTabs years={data.curriculum} />
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
                    <a href="#contact">
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
            <div>
              <p className="eyebrow">Our partners</p>
              <h2>Education, industry & innovation—working together.</h2>
            </div>
            <p>
              We welcome universities, industry, government, and community
              organizations to collaborate on teaching, research, and applied
              innovation.
            </p>
            <a className="button button-navy" href="#contact">
              Start a conversation <span>↗</span>
            </a>
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
        </section>

        <section className="section white facilities">
          <div className="shell">
            <div className="section-intro">
              <div>
                <p className="eyebrow">Learning environment</p>
                <h2>
                  Tools for turning theory
                  <em>into ability.</em>
                </h2>
              </div>
              <p>
                Students combine seminars and lectures with laboratories,
                workshops, site visits, and community practice.
              </p>
            </div>
            <div className="facility-grid">
              {data.facilities.map((facility, index) => (
                <article key={facility.name}>
                  <span>0{index + 1}</span>
                  <img
                    src={getHomeFacilityImage(
                      facility.name,
                      facility.image || "",
                    )}
                    alt=""
                    loading="lazy"
                  />
                  <h3>{facility.name}</h3>
                  <p>{facility.description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section navy contact-section" id="contact">
          <div className="shell contact-layout">
            <div>
              <p className="eyebrow light">Contact the program</p>
              <h2>
                Ready to engineer
                <em>your future?</em>
              </h2>
              <p>
                Ask about admission, curriculum, research, facilities, or a new
                collaboration.
              </p>
              <dl>
                <div>
                  <dt>Email</dt>
                  <dd>
                    <a href={`mailto:${program.email}`}>{program.email}</a>
                  </dd>
                </div>
                <div>
                  <dt>Phone</dt>
                  <dd>{program.phone}</dd>
                </div>
                <div>
                  <dt>Address</dt>
                  <dd>{program.address}</dd>
                </div>
              </dl>
            </div>
            <InquiryForm />
          </div>
        </section>
      </main>

      <footer>
        <div className="shell footer-grid">
          <div className="footer-brand">
            <img src="/assets/me-logo.png" alt="ME Program logo" />
            <p>
              Mechanical Engineering Program
              <br />
              Faculty of Engineering · RUPP
            </p>
          </div>
          <div>
            <h3>Program</h3>
            <a href="#why-me">Why ME</a>
            <a href="#vision">Vision & mission</a>
            <a href="#curriculum">Curriculum</a>
          </div>
          <div>
            <h3>Focus areas</h3>
            {data.focus_areas.map((area) => (
              <a href="#focus" key={area.code}>
                {area.code}
              </a>
            ))}
          </div>
          <div>
            <h3>Connect</h3>
            <a href="#research">Research</a>
            <a href="#partners">Partnership</a>
            <a href={`mailto:${program.email}`}>Email ME</a>
          </div>
        </div>
        <div className="shell footer-bottom">
          <span>© {new Date().getFullYear()} Mechanical Engineering · RUPP</span>
          <span>Nature · Nurture · Nourish</span>
        </div>
      </footer>
    </>
  );
}
