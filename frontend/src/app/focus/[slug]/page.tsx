/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getFocusArea, getHomeData, type FocusCourse } from "@/lib/api";
import { getFocusHeroImage, getResearchImage } from "@/lib/editorialImages";

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
        <Breadcrumbs
          trail={[
            { label: "Areas of focus", href: "/#focus" },
            { label: `${focus.code} — ${focus.title}` },
          ]}
        />
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
          <div className="shell">
            <div className="section-masthead focus-overview-lead">
              <p className="eyebrow">What this focus develops</p>
              <h2>{focus.overview_heading}</h2>
              <p>{focus.overview_intro}</p>
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

        <section className="section cream" id="focus-facilities">
          <div className="shell">
            <div className="equipment-section-heading">
              <div>
                <p className="eyebrow">Lab Equipment</p>
                <h2>{focus.facility_heading}</h2>
                <p className="equipment-intro">{focus.facility_intro}</p>
              </div>
              <div className="equipment-count" aria-label={`${focus.facilities.length} pieces of equipment`}>
                <strong>{focus.facilities.length}</strong>
                <span>{focus.code} equipment</span>
              </div>
            </div>
            <div className="focus-equipment-grid">
              {focus.facilities.map((facility, index) => (
                <article
                  className={`equipment-card status-${facility.availability_status}`}
                  key={facility.name}
                >
                  <div className="equipment-media">
                    {facility.image ? (
                      <img src={facility.image} alt={facility.name} />
                    ) : (
                      <div className="equipment-image-placeholder" aria-hidden="true">
                        <svg viewBox="0 0 64 64" focusable="false">
                          <path d="M13 51h38M17 47V14h30v33M22 20h20v16H22zM27 24h10v8H27zM23 42h18" />
                          <circle cx="42" cy="42" r="2" />
                        </svg>
                        <span>{focus.code}</span>
                      </div>
                    )}
                    <span className="equipment-index">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    {facility.availability_status !== "available" ? (
                      <small className="equipment-status">
                        {facility.availability_label}
                      </small>
                    ) : null}
                  </div>
                  <div className="equipment-card-body">
                    <h3>{facility.name}</h3>
                    <p>{facility.description}</p>
                  </div>
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
                <h2>{focus.curriculum_heading}</h2>
              </div>
              <p>{focus.curriculum_intro}</p>
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
                <h2>{focus.learning_heading}</h2>
              </div>
              <p>{focus.learning_intro}</p>
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

        <section className="section navy focus-careers">
          <div className="shell">
            <div className="detail-section-heading inverse">
              <div>
                <p className="eyebrow light">Career pathways</p>
                <h2>{focus.careers_heading}</h2>
              </div>
              <p>{focus.careers_intro}</p>
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

        {focus.research_projects.length > 0 && (
          <section className="section cream" id="focus-research">
            <div className="shell">
              <div className="section-masthead">
                <p className="eyebrow">Research & Innovation</p>
                <h2>{focus.research_heading}</h2>
                <p>{focus.research_intro}</p>
              </div>
              <div className="focus-research-preview-grid">
                {focus.research_projects.map((project) => (
                  <Link
                    className="focus-research-preview"
                    href={`/research/${focus.code.toLowerCase()}#${project.slug}`}
                    key={project.slug}
                  >
                    <div className="focus-research-preview-media">
                      <img
                        src={getResearchImage(
                          project.title,
                          project.image || focus.image || "",
                        )}
                        alt=""
                      />
                      <div className="research-focus-tags">
                        {project.focus_areas.map((area) => (
                          <span key={area.code}>{area.code}</span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <small>Current research</small>
                      <h3>{project.title}</h3>
                      <span className="focus-research-preview-link">
                        View in Research & Innovation <i>↗</i>
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </section>
        )}

        <section className="section gold focus-next">
          <div className="shell">
            <div className="focus-next-lead">
              <div>
                <p className="eyebrow">Continue exploring</p>
                <h2>Compare the other areas of focus.</h2>
              </div>
              <Link
                className="button button-navy"
                href={
                  home.settings.application_url ||
                  `mailto:${home.settings.email}?subject=ME program enquiry`
                }
              >
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

      <SiteFooter
        focusAreas={home.focus_areas}
        settings={home.settings}
      />
    </>
  );
}
