/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
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

            <div className="research-detail-body">
              <p className="research-detail-summary">{project.summary}</p>

              {project.body ? (
                // Rich text authored in Wagtail; the CMS is the trusted source.
                <div
                  className="research-detail-rich"
                  dangerouslySetInnerHTML={{ __html: project.body }}
                />
              ) : (
                <p className="research-detail-empty">
                  A full description of this project has not been published yet.
                </p>
              )}
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
