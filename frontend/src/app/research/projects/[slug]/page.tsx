/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import StoryBody from "@/components/StoryBody";
import { getHomeData, getResearchProject } from "@/lib/api";
import { getResearchImage } from "@/lib/editorialImages";

export const dynamic = "force-dynamic";

type ProjectPageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({
  params,
}: ProjectPageProps): Promise<Metadata> {
  const { slug } = await params;
  const lookup = await getResearchProject(slug);
  if (lookup.status !== "found") {
    return { title: "Research | Mechanical Engineering RUPP" };
  }
  return {
    title: `${lookup.project.title} | Research | Mechanical Engineering RUPP`,
    description: lookup.project.summary,
  };
}

export default async function ResearchProjectPage({
  params,
}: ProjectPageProps) {
  const { slug } = await params;
  const [lookup, home] = await Promise.all([
    getResearchProject(slug),
    getHomeData(),
  ]);

  if (lookup.status === "not-found") notFound();

  if (lookup.status === "unavailable") {
    return (
      <>
        <SiteHeader settings={home.settings} />
        <main id="main-content" className="editorial-page">
          <section className="section white">
            <div className="shell">
              <div className="content-empty-state">
                <h1>This project is temporarily unavailable.</h1>
                <p>
                  The research directory could not be reached. Please try again
                  shortly, or return to Research &amp; Innovation.
                </p>
                <Link className="text-link" href="/research">
                  All research <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </section>
        </main>
        <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
      </>
    );
  }

  const project = lookup.project;
  const image =
    getResearchImage(project.title, project.image || "") ||
    "/assets/hero-lab.png";

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs
          trail={[
            { label: "Research & Collaboration" },
            { label: "Research", href: "/research" },
            { label: project.title },
          ]}
        />

        <section className="section white research-detail">
          <div className="shell">
            <header className="research-detail-head">
              <p className="eyebrow">Research project</p>
              <h1>{project.title}</h1>
              {/* Status first: whether the work is finished decides how every
                  result below it should be read. */}
              <p className="research-status" data-status={project.status}>
                {project.status === "completed"
                  ? "Completed"
                  : project.status === "proposed"
                    ? "Proposed"
                    : "Ongoing"}
                {project.period ? <span>{project.period}</span> : null}
              </p>
              {project.focus_areas.length > 0 ? (
                <ul className="research-detail-areas">
                  {project.focus_areas.map((area) => (
                    <li key={area.code}>
                      <Link href={`/research/${area.code.toLowerCase()}`}>
                        {area.code} — {area.title}
                      </Link>
                    </li>
                  ))}
                </ul>
              ) : null}
            </header>

            <figure className="research-detail-media">
              <img src={image} alt={project.title} />
            </figure>

            <div className="research-layout">
              <div className="research-main">
                <p className="research-detail-summary">{project.summary}</p>

                {project.body.length > 0 ? (
                  <StoryBody blocks={project.body} galleryTitle={project.title} />
                ) : (
                  <p className="research-detail-empty">
                    A full description of this project has not been published yet.
                  </p>
                )}
              </div>

              {/* Sticky beside the prose: a reader checking the status or the
                  focus area partway down should not have to scroll back. */}
              <aside className="research-aside">
                <dl className="research-facts">
              <div>
                <dt>Status</dt>
                <dd>
                  {project.status === "completed"
                    ? "Completed"
                    : project.status === "proposed"
                      ? "Proposed"
                      : "Ongoing"}
                </dd>
              </div>
              {project.period ? (
                <div>
                  <dt>Period</dt>
                  <dd>{project.period}</dd>
                </div>
              ) : null}
              {project.focus_areas.length > 0 ? (
                <div>
                  <dt>Focus area</dt>
                  <dd>
                    {project.focus_areas.map((area) => area.code).join(" · ")}
                  </dd>
                </div>
              ) : null}
                  {project.keywords ? (
                    <div>
                      <dt>Keywords</dt>
                      <dd>{project.keywords}</dd>
                    </div>
                  ) : null}
                </dl>

                {project.focus_areas.length > 0 ? (
                  <div className="research-aside-links">
                    <p>Explore the focus area</p>
                    <ul>
                      {project.focus_areas.map((area) => (
                        <li key={area.code}>
                          <Link href={`/research/${area.code.toLowerCase()}`}>
                            {area.code} — {area.title}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : null}
              </aside>
            </div>

            <p className="research-detail-back">
              <Link className="text-link" href="/research">
                <span aria-hidden="true">←</span> All research projects
              </Link>
            </p>
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
