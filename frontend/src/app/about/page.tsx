import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import VisionMark from "@/components/VisionMark";
import { getHomeData } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function AboutPage() {
  const home = await getHomeData();
  const program = home.settings;

  return (
    <>
      <SiteHeader settings={program} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs trail={[{ label: "About the program" }]} />
        <section className="directory-hero">
          <div className="shell">
            <p className="eyebrow light">About the program</p>
            <h1>About the Program</h1>
            <p>
              The vision, mission, and intended graduate outcomes of Mechanical
              Engineering at the Royal University of Phnom Penh.
            </p>
          </div>
        </section>

        <section className="section white about-vision" id="vision">
          <div className="shell vision-statement">
            <div className="vision-statement-head">
              <p className="eyebrow">Our vision</p>
              <VisionMark />
            </div>
            <blockquote>“{program.vision}.”</blockquote>
            <p className="vision-attribution">
              {program.program_name} · Faculty of Engineering, Royal University
              of Phnom Penh
            </p>
          </div>
        </section>

        <section className="section cream" id="mission">
          <div className="shell">
            <div className="section-intro compact">
              <div>
                <p className="eyebrow">Our mission</p>
                <h2>How we deliver the vision</h2>
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

        <section className="section white" id="peos">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Program Educational Objectives</p>
                <h2>What graduates are prepared to achieve</h2>
              </div>
              <p>
                The approved PEO statements from the Mechanical Engineering
                program development document will be published here.
              </p>
            </div>
          </div>
        </section>

        <section className="section cream" id="plos">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Program Learning Outcomes</p>
                <h2>What every graduate will know and be able to do</h2>
              </div>
              <p>
                The approved PLO statements from the Mechanical Engineering
                program development document will be published here.
              </p>
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
