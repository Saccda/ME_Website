/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Breadcrumbs from "@/components/Breadcrumbs";
import QuadrupleHelix from "@/components/QuadrupleHelix";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData } from "@/lib/api";
import { quadrupleHelix } from "@/lib/quadrupleHelix";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Partnership | Mechanical Engineering RUPP",
  description:
    "Academic, industry, government, and society partnerships with the Mechanical Engineering programme at the Royal University of Phnom Penh.",
};

export default async function PartnershipPage() {
  const home = await getHomeData();
  const program = home.settings;

  return (
    <>
      <SiteHeader settings={program} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs
          trail={[
            { label: "Research & Collaboration" },
            { label: "Partnership" },
          ]}
        />
        <section className="directory-hero">
          <div className="shell">
            <p className="eyebrow light">Partnership</p>
            <h1>
              Partnering with
              <em>Mechanical Engineering.</em>
            </h1>
            <p>
              We work with academic institutions, industry, government, and the
              communities around us so that teaching, research, and graduates
              answer real national needs.
            </p>
          </div>
        </section>

        <section className="section white">
          <div className="shell">
            <div className="section-masthead">
              <p className="eyebrow">Quadruple helix</p>
              <h2>Four partners. One engineering ecosystem.</h2>
              <p>
                No single institution improves engineering practice on its own.
                The quadruple helix model puts academia, industry, government,
                and society in the same system, each shaping what engineering is
                for and each accountable to the others.
              </p>
            </div>

            <ol className="partner-type-index">
              {quadrupleHelix.map((strand, index) => (
                <li
                  key={strand.id}
                  style={{ ["--strand" as string]: strand.accent }}
                >
                  <a href={`#${strand.id}`}>
                    <span className="partner-type-index-number" aria-hidden="true">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <strong>{strand.title}</strong>
                    <span className="partner-type-index-role">
                      {strand.role}
                    </span>
                  </a>
                </li>
              ))}
            </ol>
          </div>
        </section>

        {quadrupleHelix.map((strand, index) => (
          <section
            className={`section ${index % 2 === 0 ? "cream" : "white"} partner-type`}
            id={strand.id}
            key={strand.id}
            style={{ ["--strand" as string]: strand.accent }}
          >
            <div className="shell partner-type-layout">
              <div className="partner-type-media">
                <img src={strand.image} alt={strand.alt} loading="lazy" />
              </div>
              <div className="partner-type-copy">
                <p className="eyebrow">{strand.role}</p>
                <h2>{strand.title} partners</h2>
                <p className="partner-type-lead">{strand.summary}</p>
                <h3>How we work together</h3>
                <ul className="partner-type-offers">
                  {strand.offers.map((offer) => (
                    <li key={offer}>{offer}</li>
                  ))}
                </ul>
                <p className="partner-type-note">
                  A dedicated page for {strand.title.toLowerCase()} partners is
                  in preparation. Until then, contact the programme directly to
                  discuss a collaboration.
                </p>
              </div>
            </div>
          </section>
        ))}

        <section className="section gold partnership-partners">
          <QuadrupleHelix />
          <div className="shell">
            <div className="section-masthead">
              <p className="eyebrow">Current partners</p>
              <h2>Organisations we already work with.</h2>
              <p>
                These institutions and companies support teaching, research,
                equipment, internships, and graduate opportunities across the
                programme.
              </p>
            </div>

            {home.partners.length > 0 ? (
              <div className="partnership-partner-grid">
                {home.partners.map((partner) => {
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
                      key={partner.name}
                      target="_blank"
                      rel="noopener noreferrer"
                      aria-label={`Visit ${partner.name} website`}
                    >
                      {logo}
                    </a>
                  ) : (
                    <div className="partner-logo" key={partner.name}>
                      {logo}
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="content-empty-state">
                <h3>Partner organisations are being published.</h3>
                <p>
                  The partner directory is maintained in the programme CMS and
                  will appear here once entries are added.
                </p>
              </div>
            )}
          </div>
        </section>

        <section className="section navy partnership-cta">
          <div className="shell">
            <p className="eyebrow light">Start a conversation</p>
            <h2>Tell us what you want to build.</h2>
            <p>
              Whether you are an institution, a company, a public agency, or a
              community organisation, the programme office can scope a
              collaboration with you.
            </p>
            <div className="partnership-cta-actions">
              <a
                className="button button-gold"
                href={`mailto:${program.email}?subject=ME partnership enquiry`}
              >
                Email the programme <span>↗</span>
              </a>
              {program.phone ? (
                <a className="text-link light" href={`tel:${program.phone}`}>
                  {program.phone} <span>→</span>
                </a>
              ) : null}
            </div>
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={program} />
    </>
  );
}
