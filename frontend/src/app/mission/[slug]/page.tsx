/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import {
  getHomeData,
  getNewsEvents,
  getResearchProjects,
  type NewsEvent,
  type ResearchProject,
} from "@/lib/api";
import { getResearchImage } from "@/lib/editorialImages";
import {
  activitiesByYear,
  activitiesFor,
  activityYear,
  getMission,
  missionStatement,
  otherMission,
  type Mission,
} from "@/lib/missions";

export const dynamic = "force-dynamic";

type MissionPageProps = { params: Promise<{ slug: string }> };

export async function generateMetadata({
  params,
}: MissionPageProps): Promise<Metadata> {
  const { slug } = await params;
  const mission = getMission(slug);

  if (!mission) {
    return { title: "Mission not found | Mechanical Engineering RUPP" };
  }

  return {
    title: `${mission.name} | Mechanical Engineering RUPP`,
    description: `${mission.code}: ${mission.premise} A record of what the Mechanical Engineering program has carried out under this mission.`,
  };
}

function formatWhen(story: NewsEvent) {
  if (story.period) return story.period;
  const value = story.event_date || story.published_at;
  const when = Date.parse(value);
  if (Number.isNaN(when)) return "Date to be announced";
  return new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(when));
}

/**
 * One activity in the log.
 *
 * The date leads, because the page is a record of what was done and when. The
 * story itself is one click away rather than retold here.
 */
function LogEntry({ story }: { story: NewsEvent }) {
  return (
    <li className="mission-log-entry">
      <p className="mission-log-when">
        {story.period ? (
          <span>{formatWhen(story)}</span>
        ) : (
          <time dateTime={story.event_date || story.published_at}>
            {formatWhen(story)}
          </time>
        )}
        {story.content_type === "event" ? <em>Event</em> : null}
      </p>
      <div className="mission-log-body">
        {story.category ? (
          <p className="mission-log-category">{story.category}</p>
        ) : null}
        <h3>
          <Link href={`/news-events/${story.slug}`}>{story.title}</Link>
        </h3>
        <p className="mission-log-excerpt">{story.excerpt}</p>
      </div>
      <div className="mission-log-media" aria-hidden="true">
        {story.image ? (
          <img src={story.image} alt="" loading="lazy" />
        ) : (
          <span>ME</span>
        )}
      </div>
    </li>
  );
}

export default async function MissionPage({ params }: MissionPageProps) {
  const { slug } = await params;
  const mission = getMission(slug);
  if (!mission) notFound();

  const [home, stories, projects] = await Promise.all([
    getHomeData(),
    getNewsEvents(),
    // Only the research mission lists projects, and asking for them on the
    // teaching page would be a request made to throw the answer away.
    mission.key === "research"
      ? getResearchProjects()
      : Promise.resolve([] as ResearchProject[]),
  ]);

  const activities = activitiesFor(mission, stories);
  const years = activitiesByYear(activities);
  const dated = activities
    .map(activityYear)
    .filter((year): year is number => year !== null);
  const earliest = dated.length > 0 ? Math.min(...dated) : null;
  const latest = dated.length > 0 ? Math.max(...dated) : null;
  const span =
    earliest === null || latest === null
      ? "—"
      : earliest === latest
        ? `${earliest}`
        : `${earliest}–${latest}`;

  const next: Mission = otherMission(mission);
  const nextRecorded = activitiesFor(next, stories).length;

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main
        id="main-content"
        className={`editorial-page mission-page is-${mission.key}`}
      >
        <Breadcrumbs
          trail={[
            { label: "About the program", href: "/about" },
            { label: "Mission", href: "/about#mission" },
            { label: mission.name },
          ]}
        />

        {/* No summary line under the title. One sentence in the hero and the
            approved statement in the band directly below it read as two
            competing versions of the mission, and a reader has no way to tell
            which one the program actually signed off. Only the statement is
            the statement. */}
        <section className="directory-hero is-compact mission-hero">
          <div className="shell">
            <p className="eyebrow light">
              {mission.code} · Mission of the program
            </p>
            <h1>{mission.name}</h1>
          </div>
        </section>

        <section className="section white mission-statement-section">
          <div className="shell mission-statement-grid">
            <div className="mission-statement-copy">
              <p className="eyebrow">What we committed to</p>
              <blockquote>{missionStatement(mission, home.settings)}</blockquote>
              <p className="mission-statement-source">
                Mission {mission.code.slice(1)} of two, as approved in the
                Mechanical Engineering program development document.
              </p>
            </div>
            <aside className="mission-tally" aria-label="What has been recorded">
              <div>
                <strong>{activities.length}</strong>
                <span>
                  {activities.length === 1 ? "activity" : "activities"} recorded
                </span>
              </div>
              <div>
                <strong>{span}</strong>
                <span>years covered</span>
              </div>
              {mission.key === "research" ? (
                <div>
                  <strong>{projects.length}</strong>
                  <span>
                    research {projects.length === 1 ? "project" : "projects"}
                  </span>
                </div>
              ) : null}
              <p>
                Counted from the activities published in News &amp; Events and
                filed against this mission.
              </p>
            </aside>
          </div>
        </section>

        <section className="mission-where-band">
          <div className="shell">
            <p>Where this mission is carried out</p>
            <ul>
              {mission.elsewhere.map((link) => (
                <li key={link.href}>
                  <Link href={link.href}>{link.label}</Link>
                </li>
              ))}
            </ul>
          </div>
        </section>

        {mission.key === "research" && projects.length > 0 ? (
          <section
            className="section cream research-current-section"
            id="projects"
          >
            <div className="shell">
              <header className="research-simple-heading">
                <p>Under way</p>
                <h2>The research itself</h2>
                <span>
                  The projects this mission is measured by: each one run with
                  partners outside the program, and taken far enough to work
                  outside the laboratory.
                </span>
              </header>
              <div className="research-current-grid">
                {projects.map((project, index) => (
                  <article className="research-current-card" key={project.slug}>
                    <Link href={`/research/projects/${project.slug}`}>
                      <div className="research-current-media">
                        <img
                          src={
                            getResearchImage(
                              project.title,
                              project.image || "",
                            ) || "/assets/hero-lab.webp"
                          }
                          alt=""
                        />
                        <span>{String(index + 1).padStart(2, "0")}</span>
                      </div>
                      <div className="research-current-copy">
                        <div className="research-focus-tags dark">
                          {project.focus_areas.map((area) => (
                            <span key={area.code}>{area.code}</span>
                          ))}
                        </div>
                        <h3>{project.title}</h3>
                        <p>{project.summary}</p>
                        <strong>
                          Explore the research <i>↗</i>
                        </strong>
                      </div>
                    </Link>
                  </article>
                ))}
              </div>
            </div>
          </section>
        ) : null}

        <section className="section white mission-log-section" id="activity-log">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Activity log</p>
                <h2>What the program has done</h2>
              </div>
              <p>
                Every published activity filed against this mission, most
                recent first. Each entry opens the full write-up in News &amp;
                Events.
              </p>
            </div>

            {years.length > 0 ? (
              <div className="mission-log">
                {years.map((group) => (
                  <section
                    className="mission-log-year"
                    key={group.year ?? "undated"}
                  >
                    <h3>
                      {group.year ?? "Undated"}
                      <span>
                        {group.items.length}{" "}
                        {group.items.length === 1 ? "entry" : "entries"}
                      </span>
                    </h3>
                    <ol>
                      {group.items.map((story) => (
                        <LogEntry key={story.id} story={story} />
                      ))}
                    </ol>
                  </section>
                ))}
              </div>
            ) : (
              <div className="content-empty-state">
                <h3>Nothing has been filed against this mission yet</h3>
                <p>
                  Activities appear here once a story in News &amp; Events is
                  marked in Wagtail as delivering this mission.
                </p>
              </div>
            )}
          </div>
        </section>

        <section className="mission-next-band">
          <div className="shell">
            <div>
              <p>The other half of the program&rsquo;s work</p>
              <h2>
                {next.code} · {next.name}
              </h2>
              {/* The count rather than a summary line: a sentence here would
                  be read as that mission's statement, which it is not. */}
              <p>
                {nextRecorded}{" "}
                {nextRecorded === 1 ? "activity" : "activities"} recorded
                against it so far.
              </p>
            </div>
            <Link className="button button-gold" href={`/mission/${next.slug}`}>
              Open {next.name}
            </Link>
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
