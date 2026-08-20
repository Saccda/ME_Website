import Breadcrumbs from "@/components/Breadcrumbs";
import FacilityCatalog from "@/components/FacilityCatalog";
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
        {/* Compact: the full-height hero spent 60% of the first screen on a
            title and one sentence. */}
        <section className="directory-hero is-compact">
          <div className="shell">
            <p className="eyebrow light">Teaching & learning</p>
            <h1>Facilities</h1>
            <p>
              Laboratories, machines, and engineering systems used for
              teaching, prototyping, testing, and applied research.
            </p>
          </div>
        </section>

        <section className="section cream catalog-section">
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
              <FacilityCatalog facilities={facilities} />
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
