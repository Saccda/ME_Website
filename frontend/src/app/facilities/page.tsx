/* eslint-disable @next/next/no-img-element */
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getFacilities, getHomeData } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function FacilitiesPage() {
  const [home, facilities] = await Promise.all([
    getHomeData(),
    getFacilities(),
  ]);

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs
          trail={[{ label: "Teaching & Learning" }, { label: "Facilities" }]}
        />
        <section className="directory-hero">
          <div className="shell">
            <p className="eyebrow light">Teaching & learning</p>
            <h1>Facilities</h1>
            <p>
              Laboratories, machines, and engineering systems used for
              teaching, prototyping, testing, and applied research.
            </p>
          </div>
        </section>

        <section className="section cream">
          <div className="shell">
            <div className="equipment-section-heading">
              <div>
                <p className="eyebrow">Program facilities</p>
                <h2>Laboratory equipment</h2>
                <p className="equipment-intro">
                  Equipment across design, manufacturing, energy, automation,
                  testing, compliance, and engineering services.
                </p>
              </div>
              <div
                className="equipment-count"
                aria-label={`${facilities.length} facilities`}
              >
                <strong>{facilities.length}</strong>
                <span>facilities</span>
              </div>
            </div>

            {facilities.length > 0 ? (
              <div className="focus-equipment-grid">
                {facilities.map((facility, index) => (
                  <article
                    className={`equipment-card status-${facility.availability_status}`}
                    key={`${facility.name}-${index}`}
                  >
                    <div className="equipment-media">
                      {facility.image ? (
                        <img src={facility.image} alt={facility.name} />
                      ) : (
                        <div
                          className="equipment-image-placeholder"
                          aria-hidden="true"
                        >
                          <svg viewBox="0 0 64 64" focusable="false">
                            <path d="M13 51h38M17 47V14h30v33M22 20h20v16H22zM27 24h10v8H27zM23 42h18" />
                            <circle cx="42" cy="42" r="2" />
                          </svg>
                          <span>ME</span>
                        </div>
                      )}
                      <span className="equipment-index">
                        {String(index + 1).padStart(2, "0")}
                      </span>
                      {facility.availability_status !== "available" ? (
                        <small className="equipment-status">
                          {facility.availability_label}
                        </small>
                      ) : null}
                    </div>
                    <div className="equipment-card-body">
                      <h3>{facility.name}</h3>
                      <p>{facility.description}</p>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <div className="content-empty-state">
                <h3>The facility directory is being prepared.</h3>
                <p>
                  Machines and laboratory systems can be published from the
                  Facilities section in the ME content management system.
                </p>
              </div>
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
