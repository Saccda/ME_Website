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
        {/* Compact: at full height the band stood 430px tall to carry a
            title and one sentence, and the vision statement -- which is what
            the page opens with -- started 880px down a 900px screen. */}
        <section className="directory-hero is-compact">
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
            {/* The template supplies the full stop, so a statement that
                already ends in one came out "…of society..". */}
            <blockquote>“{program.vision.replace(/\s*\.+\s*$/, "")}.”</blockquote>
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
                The Bachelor of Engineering in Mechanical Engineering program
                at the Royal University of Phnom Penh is dedicated to three
                missions. Each one has a page of its own, recording what has
                actually been done against it.
              </p>
            </div>
            {/* A list, for the same reason the outcomes are one: three cards
                across the page left each statement in a column too narrow to
                read it in, and the three are read in order anyway. */}
            <ol className="mission-list">
              {missions.map((mission) => {
                const recorded = activitiesFor(mission, stories).length;
                return (
                  <li className="mission-card" key={mission.key}>
                    <Link href={`/mission/${mission.slug}`}>
                      <span className="mission-card-mark" aria-hidden="true">
                        <MissionIcon name={mission.key} />
                      </span>
                      <span className="mission-card-body">
                        <span className="mission-card-head">
                          <span className="mission-card-code">
                            {mission.code}
                          </span>
                          <h3>{mission.name}</h3>
                        </span>
                        <span className="mission-card-tagline">
                          {mission.tagline}
                        </span>
                        <span className="mission-card-statement">
                          {missionStatement(mission, program)}
                        </span>
                      </span>
                      <span className="mission-card-cue">
                        <strong>{recorded}</strong>
                        <span>
                          {recorded === 1 ? "activity" : "activities"} recorded
                        </span>
                        <em>
                          Open the mission <i aria-hidden="true">→</i>
                        </em>
                      </span>
                    </Link>
                  </li>
                );
              })}
            </ol>
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
            {/* The same rows as the outcomes below. They are the same kind of
                thing from the same document, and three objectives across the
                page while ten outcomes run down it made them look like two
                unrelated components. */}
            <ol className="outcome-list is-objectives">
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
