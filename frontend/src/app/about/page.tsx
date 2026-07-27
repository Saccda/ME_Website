import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function AboutPage() {
  const home = await getHomeData();
  const program = home.settings;

  return (
    <>
      <SiteHeader settings={program} />
      <main id="main-content" className="editorial-page">
        <section className="directory-hero">
          <div className="shell">
            <p className="eyebrow light">About the program</p>
            <h1>
              Engineering education
              <em>with purpose.</em>
            </h1>
            <p>
              Our vision and mission guide how Mechanical Engineering at RUPP
              connects technology, learning, research, and service to society.
            </p>
          </div>
        </section>

        <section className="section white about-vision">
          <div className="shell about-statement">
            <div>
              <p className="eyebrow">Our vision</p>
              <h2>The future we are working toward.</h2>
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
              {[program.mission_one, program.mission_two].map(
                (mission, index) => (
                  <article key={mission}>
                    <span>0{index + 1}</span>
                    <div className="mission-icon" aria-hidden="true">
                      {index === 0 ? "⌁" : "◎"}
                    </div>
                    <p>{mission}</p>
                  </article>
                ),
              )}
            </div>
          </div>
        </section>
      </main>

      <SiteFooter
        focusAreas={home.focus_areas}
        settings={program}
      />
    </>
  );
}
