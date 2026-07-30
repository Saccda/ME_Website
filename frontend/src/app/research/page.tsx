/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData, getResearchProjects } from "@/lib/api";
import { getResearchImage } from "@/lib/editorialImages";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Research & Innovation | Mechanical Engineering RUPP",
  description:
    "Explore Mechanical Engineering research areas and current projects at the Royal University of Phnom Penh.",
};

type ResearchPageProps = {
  searchParams: Promise<{ focus?: string }>;
};

export default async function ResearchPage({
  searchParams,
}: ResearchPageProps) {
  const { focus: legacyFocus } = await searchParams;

  if (legacyFocus) {
    redirect(`/research/${legacyFocus.toLowerCase()}`);
  }

  const [home, projects] = await Promise.all([
    getHomeData(),
    getResearchProjects(),
  ]);

  const projectCountByFocus = new Map(
    home.focus_areas.map((area) => [
      area.code,
      projects.filter((project) =>
        project.focus_areas.some((focus) => focus.code === area.code),
      ).length,
    ]),
  );

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page research-hub-page">
        <section className="research-showcase-hero">
          <img
            className="research-showcase-background"
            src={home.settings.hero_image || "/assets/hero-lab.png"}
            alt=""
          />
          <div className="research-showcase-overlay" />
          <div className="shell research-showcase-content">
            <p>Research at ME RUPP</p>
            <h1>Engineering research at the interface of ideas</h1>
            <span>
              Our work connects design, energy, automation, and responsible
              engineering to practical challenges in Cambodia and beyond.
            </span>
            <a href="#research-areas">
              Scroll to explore <i>↓</i>
            </a>
          </div>
        </section>

        <nav className="research-topic-rail" aria-label="Research areas">
          <div className="shell">
            <Link className="active" href="/research">
              Overview
            </Link>
            {home.focus_areas.map((area) => (
              <Link
                href={`/research/${area.code.toLowerCase()}`}
                key={area.code}
              >
                <strong>{area.code}</strong>
                <span>{area.title}</span>
              </Link>
            ))}
          </div>
        </nav>

        <section className="research-quote-panel">
          <div className="shell">
            <p>
              Mechanical engineering research is strongest where disciplines
              meet and useful solutions begin to take shape.
            </p>
            <span>Design · Energy · Automation · Responsible engineering</span>
          </div>
        </section>

        <section className="section white research-area-directory" id="research-areas">
          <div className="shell">
            <header className="research-simple-heading">
              <p>Explore research</p>
              <h2>Investigate our four research areas</h2>
              <span>
                Each area organizes expertise without limiting collaboration
                across disciplines.
              </span>
            </header>

            <div className="research-area-tile-grid">
              {home.focus_areas.map((area) => (
                <Link
                  className="research-area-tile"
                  href={`/research/${area.code.toLowerCase()}`}
                  key={area.code}
                  style={
                    {
                      "--research-accent": area.accent_color,
                    } as React.CSSProperties
                  }
                >
                  <div>
                    <img
                      src={
                        area.image ||
                        `/assets/focus-${area.code.toLowerCase()}.png`
                      }
                      alt=""
                    />
                    <span>{area.code}</span>
                  </div>
                  <footer>
                    <strong>{area.title}</strong>
                    <small>
                      {projectCountByFocus.get(area.code) || 0} current{" "}
                      {(projectCountByFocus.get(area.code) || 0) === 1
                        ? "project"
                        : "projects"}
                    </small>
                  </footer>
                </Link>
              ))}
            </div>
          </div>
        </section>

        <section className="section cream research-current-section" id="current-research">
          <div className="shell">
            <header className="research-simple-heading">
              <p>Current research</p>
              <h2>Explore current research projects</h2>
              <span>
                Open a project through its primary area to see its full context
                and connected disciplines.
              </span>
            </header>

            {projects.length > 0 ? (
              <div className="research-current-grid">
                {projects.map((project, index) => {
                  const primaryArea = project.focus_areas[0];
                  const href = primaryArea
                    ? `/research/${primaryArea.code.toLowerCase()}#${project.slug}`
                    : "/research";

                  return (
                    <article className="research-current-card" key={project.slug}>
                      <Link href={href}>
                        <div className="research-current-media">
                          <img
                            src={getResearchImage(
                              project.title,
                              project.image || "",
                            )}
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
                  );
                })}
              </div>
            ) : (
              <div className="content-empty-state">
                <h3>Research projects are being prepared.</h3>
                <p>
                  Published projects will appear here after they are added in
                  Wagtail.
                </p>
              </div>
            )}
          </div>
        </section>

        <section className="research-collaboration-band">
          <div className="shell">
            <div>
              <p>Research collaboration</p>
              <h2>Good research grows through shared expertise.</h2>
            </div>
            <Link className="button button-gold" href="/#partners">
              Explore our partnerships <span>↗</span>
            </Link>
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
