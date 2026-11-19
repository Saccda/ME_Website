import Link from "next/link";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import MissionIcon from "@/components/MissionIcon";
import SiteHeader from "@/components/SiteHeader";
import VisionMark from "@/components/VisionMark";
import { getHomeData, getNewsEvents } from "@/lib/api";
import { activitiesFor, missions, missionStatement } from "@/lib/missions";
import {
  programEducationalObjectives,
  programLearningOutcomes,
  splitOutcomeCode,
} from "@/lib/programOutcomes";

export const dynamic = "force-dynamic";

export default async function AboutPage() {
  // The stories are read here only to count them. A mission card that says
  // how much has been filed under it is worth opening; one that does not is
  // a statement with an arrow after it.
  const [home, stories] = await Promise.all([getHomeData(), getNewsEvents()]);
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
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Our mission</p>
                <h2>How we deliver the vision</h2>
              </div>
              <p>
                The work of the program falls into two halves. Each one has a
                page of its own recording what has actually been done against
                it.
              </p>
            </div>
            <div className="mission-grid">
              {missions.map((mission) => {
                const recorded = activitiesFor(mission, stories).length;
                return (
                  <article className="mission-card" key={mission.key}>
                    <Link href={`/mission/${mission.slug}`}>
                      <div className="mission-card-head">
                        <p className="mission-card-code">{mission.code}</p>
                        <h3>{mission.name}</h3>
                        <MissionIcon name={mission.key} />
                      </div>
                      <p className="mission-card-tagline">{mission.tagline}</p>
                      <p className="mission-card-statement">
                        {missionStatement(mission, program)}
                      </p>
                      <p className="mission-card-cue">
                        <span>
                          {recorded}{" "}
                          {recorded === 1 ? "activity" : "activities"} recorded
                        </span>
                        <strong>
                          Open the mission <i aria-hidden="true">→</i>
                        </strong>
                      </p>
                    </Link>
                  </article>
                );
              })}
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
                What the program sets out to equip its graduates for, as
                approved in the Mechanical Engineering program development
                document.
              </p>
            </div>
            <ol className="objective-grid">
              {programEducationalObjectives.map((objective) => {
                const { scheme, number } = splitOutcomeCode(objective.code);
                return (
                  <li key={objective.code}>
                    <p className="outcome-index">
                      <span>{scheme}</span>
                      <strong>{number}</strong>
                    </p>
                    <p>{objective.statement}</p>
                  </li>
                );
              })}
            </ol>
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
                Ten outcomes every graduate of the program is expected to
                demonstrate, as approved in the Mechanical Engineering program
                development document.
              </p>
            </div>
            <ol className="outcome-list">
              {programLearningOutcomes.map((outcome) => {
                const { scheme, number } = splitOutcomeCode(outcome.code);
                return (
                  <li key={outcome.code}>
                    <p className="outcome-index">
                      <span>{scheme}</span>
                      <strong>{number}</strong>
                    </p>
                    <div>
                      <h3>{outcome.title}</h3>
                      <p>{outcome.statement}</p>
                    </div>
                  </li>
                );
              })}
            </ol>
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
