/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import SiteHeader from "@/components/SiteHeader";
import { getFocusArea, getHomeData, type FocusCourse } from "@/lib/api";
import {
  getFocusFacilityImage,
  getFocusHeroImage,
  getResearchImage,
} from "@/lib/editorialImages";

export const dynamic = "force-dynamic";

type FocusPageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({
  params,
}: FocusPageProps): Promise<Metadata> {
  const { slug } = await params;
  const focus = await getFocusArea(slug);
  if (!focus) return { title: "Focus area not found | ME RUPP" };
  return {
    title: `${focus.code}: ${focus.title} | Mechanical Engineering RUPP`,
    description: focus.description,
  };
}

export default async function FocusAreaPage({ params }: FocusPageProps) {
  const { slug } = await params;
  const [focus, home] = await Promise.all([
    getFocusArea(slug),
    getHomeData(),
  ]);
  if (!focus) notFound();

  const coursesByYear = focus.courses.reduce<Record<number, FocusCourse[]>>(
    (groups, course) => {
      (groups[course.year] ||= []).push(course);
      return groups;
    },
    {},
  );
  const otherFocusAreas = home.focus_areas.filter(
    (area) => area.code !== focus.code,
  );

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main
        id="main-content"
        className="focus-detail-page"
        style={{ "--focus-accent": focus.accent_color } as React.CSSProperties}
      >
        <section className="focus-detail-hero">
          <img
            src={getFocusHeroImage(
              focus.code,
              focus.image || "/assets/hero-lab.png",
            )}
            alt={`${focus.title} learning environment`}
          />
          <div className="focus-detail-overlay" />
          <div className="focus-detail-pattern" aria-hidden="true" />
          <div className="shell focus-detail-hero-content">
            <nav className="focus-breadcrumb" aria-label="Breadcrumb">
              <Link href="/">Home</Link>
              <span>›</span>
              <Link href="/#focus">Areas of focus</Link>
              <span>›</span>
              <strong>{focus.code}</strong>
            </nav>
            <span className="focus-code">{focus.code}</span>
            <h1>{focus.title}</h1>
            <p>{focus.description}</p>
            <a className="button button-gold" href="#focus-curriculum">
              Explore the study path <span>↓</span>
            </a>
          </div>
          <div className="focus-detail-stats">
            <div className="shell">
              <div>
                <strong>{focus.courses.length}</strong>
                <span>Supporting courses</span>
              </div>
              <div>
                <strong>{focus.facilities.length}</strong>
                <span>Equipment & facilities</span>
              </div>
              <div>
                <strong>{focus.learning_activities.length}</strong>
                <span>Signature activities</span>
              </div>
              <div>
                <strong>{focus.research_projects.length}</strong>
                <span>Related research projects</span>
              </div>
            </div>
          </div>
        </section>

        <section className="section white">
          <div className="shell focus-overview">
            <div className="focus-overview-lead">
              <p className="eyebrow">What this focus develops</p>
              <h2>
                Knowledge that becomes
                <em>engineering ability.</em>
              </h2>
              <p>
                The {focus.code} pathway connects classroom fundamentals with
                practical investigation, modern tools, teamwork, and evidence-
                based engineering decisions.
              </p>
            </div>
            <div className="outcome-grid">
              {focus.outcomes.map((outcome, index) => (
                <article key={outcome.title}>
                  <span>0{index + 1}</span>
                  <h3>{outcome.title}</h3>
                  <p>{outcome.description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section cream">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Laboratories & equipment</p>
                <h2>Learn with the tools of the profession.</h2>
              </div>
              <p>
                Equipment is treated as a learning environment: students plan,
                operate, measure, interpret results, and improve their work.
              </p>
            </div>
            <div className="focus-equipment-grid">
              {focus.facilities.map((facility, index) => (
                <article key={facility.name}>
                  <div>
                    <img
                      src={getFocusFacilityImage(
                        focus.code,
                        facility.name,
                        facility.image || focus.image || "",
                      )}
                      alt=""
                    />
                    <span>{String(index + 1).padStart(2, "0")}</span>
                  </div>
                  <h3>{facility.name}</h3>
                  <p>{facility.description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section navy focus-curriculum" id="focus-curriculum">
          <div className="shell">
            <div className="detail-section-heading inverse">
              <div>
                <p className="eyebrow light">Supporting curriculum</p>
                <h2>Built progressively across four years.</h2>
              </div>
              <p>
                Foundation subjects support later specialist work, integrated
                projects, industry experience, and the final capstone.
              </p>
            </div>
            <div className="focus-course-years">
              {Object.entries(coursesByYear)
                .sort(([yearA], [yearB]) => Number(yearA) - Number(yearB))
                .map(([year, courses]) => (
                  <article key={year}>
                    <header>
                      <span>Year {year}</span>
                      <h3>{courses[0]?.year_theme}</h3>
                    </header>
                    <div>
                      {courses.map((course) => (
                        <div className="focus-course-row" key={course.code}>
                          <span>{course.code}</span>
                          <strong>{course.title}</strong>
                          <small>{course.credits} credits</small>
                        </div>
                      ))}
                    </div>
                  </article>
                ))}
            </div>
            <p className="curriculum-note">
              The course mapping is a program overview and can be updated in the
              CMS when the official study plan changes.
            </p>
          </div>
        </section>

        <section className="section white">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">How students learn</p>
                <h2>Active learning beyond memorization.</h2>
              </div>
              <p>
                Each activity combines technical knowledge with communication,
                iteration, safety, and reflection.
              </p>
            </div>
            <div className="activity-grid">
              {focus.learning_activities.map((activity, index) => (
                <article key={activity.title}>
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <div>
                    <h3>{activity.title}</h3>
                    <p>{activity.description}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        {focus.research_projects.length > 0 && (
          <section className="section cream">
            <div className="shell">
              <div className="detail-section-heading">
                <div>
                  <p className="eyebrow">Related applied research</p>
                  <h2>Questions connected to real needs.</h2>
                </div>
                <p>
                  Current work shows how the focus area contributes to
                  sustainability, industry, communities, and innovation.
                </p>
              </div>
              <div className="focus-research-grid">
                {focus.research_projects.map((project) => (
                  <article key={project.slug}>
                    <img
                      src={getResearchImage(
                        project.title,
                        project.image || focus.image || "",
                      )}
                      alt=""
                    />
                    <div>
                      <span>{focus.code} research</span>
                      <h3>{project.title}</h3>
                      <p>{project.summary}</p>
                    </div>
                  </article>
                ))}
              </div>
            </div>
          </section>
        )}

        <section className="section navy focus-careers">
          <div className="shell">
            <div className="detail-section-heading inverse">
              <div>
                <p className="eyebrow light">Career pathways</p>
                <h2>Where this focus can take you.</h2>
              </div>
              <p>
                Graduates can move across technical and leadership roles as
                their experience grows.
              </p>
            </div>
            <div className="career-path-grid">
              {focus.career_paths.map((career, index) => (
                <article key={career.title}>
                  <span>0{index + 1}</span>
                  <h3>{career.title}</h3>
                  <p>{career.description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section gold focus-next">
          <div className="shell">
            <div className="focus-next-lead">
              <div>
                <p className="eyebrow">Continue exploring</p>
                <h2>Compare the other areas of focus.</h2>
              </div>
              <Link className="button button-navy" href="/#contact">
                Ask the program <span>↗</span>
              </Link>
            </div>
            <div className="other-focus-grid">
              {otherFocusAreas.map((area) => (
                <Link href={`/focus/${area.slug}`} key={area.code}>
                  <span>{area.code}</span>
                  <strong>{area.title}</strong>
                  <i>↗</i>
                </Link>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="focus-footer">
        <div className="shell footer-bottom">
          <span>© {new Date().getFullYear()} Mechanical Engineering · RUPP</span>
          <Link href="/">Return to the program homepage</Link>
        </div>
      </footer>
    </>
  );
}
