/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData, getResearchProjects } from "@/lib/api";
import { getResearchImage } from "@/lib/editorialImages";

export const dynamic = "force-dynamic";

type ResearchAreaPageProps = {
  params: Promise<{ focus: string }>;
};

export async function generateMetadata({
  params,
}: ResearchAreaPageProps): Promise<Metadata> {
  const { focus: requestedFocus } = await params;
  const home = await getHomeData();
  const area = home.focus_areas.find(
    (item) => item.code.toLowerCase() === requestedFocus.toLowerCase(),
  );

  if (!area) {
    return { title: "Research area not found | Mechanical Engineering RUPP" };
  }

  return {
    title: `${area.code} Research | Mechanical Engineering RUPP`,
    description: area.description,
  };
}

export default async function ResearchAreaPage({
  params,
}: ResearchAreaPageProps) {
  const { focus: requestedFocus } = await params;
  const focusCode = requestedFocus.toUpperCase();
  const [home, projects] = await Promise.all([
    getHomeData(),
    getResearchProjects(focusCode),
  ]);
  const area = home.focus_areas.find((item) => item.code === focusCode);

  if (!area) notFound();

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main
        id="main-content"
        className="editorial-page research-area-page"
        style={
          {
            "--research-accent": area.accent_color,
          } as React.CSSProperties
        }
      >
        <section className="research-area-showcase-hero">
          <img
            className="research-showcase-background"
            src={area.image || `/assets/focus-${area.code.toLowerCase()}.png`}
            alt=""
          />
          <div className="research-showcase-overlay" />
          <div className="shell research-area-showcase-content">
            <nav className="research-breadcrumb" aria-label="Breadcrumb">
              <Link href="/research">Research</Link>
              <span>/</span>
              <strong>{area.code}</strong>
            </nav>
            <p>Research area · {area.code}</p>
            <h1>{area.title}</h1>
            <span>{area.description}</span>
            <a href="#area-overview">
              Scroll to explore <i>↓</i>
            </a>
          </div>
        </section>

        <nav className="research-topic-rail" aria-label="Other research areas">
          <div className="shell">
            <Link href="/research">Overview</Link>
            {home.focus_areas.map((item) => (
              <Link
                className={item.code === area.code ? "active" : ""}
                href={`/research/${item.code.toLowerCase()}`}
                key={item.code}
              >
                <strong>{item.code}</strong>
                <span>{item.title}</span>
              </Link>
            ))}
          </div>
        </nav>

        <section
          className="section white research-area-overview"
          id="area-overview"
        >
          <div className="shell">
            <header className="research-simple-heading">
              <p>{area.code} research</p>
              <h2>What we investigate in {area.code}</h2>
              <span>{area.research_overview}</span>
            </header>
            {area.research_question ? (
              <p className="research-area-question">{area.research_question}</p>
            ) : null}
            <div className="research-theme-grid">
              {area.research_themes.map((theme, index) => (
                <article key={theme.title}>
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <strong>{theme.title}</strong>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section cream research-area-projects">
          <div className="shell">
            <header className="research-simple-heading">
              <p>{home.settings.research_area_projects_eyebrow}</p>
              <h2>Current {area.code} research projects</h2>
              <span>{home.settings.research_area_projects_intro}</span>
            </header>

            {projects.length > 0 ? (
              <div className="research-project-list">
                {projects.map((project, index) => (
                  <article
                    className="research-project-detail"
                    id={project.slug}
                    key={project.slug}
                  >
                    <div className="research-project-media">
                      <img
                        src={getResearchImage(
                          project.title,
                          project.image || area.image || "",
                        )}
                        alt=""
                      />
                      <span>{String(index + 1).padStart(2, "0")}</span>
                    </div>
                    <div className="research-project-copy">
                      <div className="research-focus-tags">
                        {project.focus_areas.map((focusArea) => (
                          <Link
                            href={`/research/${focusArea.code.toLowerCase()}`}
                            key={focusArea.code}
                          >
                            {focusArea.code}
                          </Link>
                        ))}
                      </div>
                      <h2>{project.title}</h2>
                      <p className="research-project-summary">
                        {project.summary}
                      </p>
                      {project.body ? (
                        <div
                          className="research-project-body"
                          dangerouslySetInnerHTML={{ __html: project.body }}
                        />
                      ) : (
                        <p className="research-project-placeholder">
                          Methodology, team information, findings, media, and
                          related publications can be added from Wagtail.
                        </p>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <div className="content-empty-state">
                <h3>No published {area.code} projects yet.</h3>
                <p>
                  Projects will appear here after they are assigned to this
                  research area and published in Wagtail.
                </p>
              </div>
            )}
          </div>
        </section>

        <section className="research-boundaries-band">
          <div className="shell">
            <p>{home.settings.research_boundaries_eyebrow}</p>
            <h2>{home.settings.research_boundaries_heading}</h2>
            <Link href="/research">
              Return to all research areas <span>↗</span>
            </Link>
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
