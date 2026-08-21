/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { admissionsContent } from "@/lib/admissions";
import { getHomeData } from "@/lib/api";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Admissions | Mechanical Engineering RUPP",
  description:
    "Mechanical Engineering admission dates, entrance examination subjects, past examinations, and application-form guidance at RUPP.",
};

export default async function AdmissionsPage() {
  const home = await getHomeData();
  const { settings } = home;
  const registrationWindow = admissionsContent.milestones[0];
  const examDate = admissionsContent.milestones[1];

  return (
    <>
      <SiteHeader settings={settings} />
      <main id="main-content" className="admissions-page">
        <Breadcrumbs trail={[{ label: "Admissions" }]} />
        <section className="admissions-hero">
          <div className="shell admissions-hero-grid">
            <div className="admissions-hero-copy">
              <p className="admissions-kicker">Undergraduate admissions</p>
              <h1>Mechanical Engineering admissions</h1>
              <p>
                Follow the admission calendar, prepare for the entrance
                examination, and review the information requested on the
                hard-copy registration form.
              </p>
              <div className="admissions-hero-actions">
                <a className="button button-gold" href="#admission-calendar">
                  View important dates <span aria-hidden="true">↓</span>
                </a>
                <a
                  className="admissions-text-link"
                  href={admissionsContent.pastExamsUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  Access past examinations <span aria-hidden="true">↗</span>
                </a>
              </div>
            </div>

            <div className="admissions-quick-facts" aria-label="Key dates">
              <p>{admissionsContent.cycleLabel}</p>
              <div>
                <span>
                  <small>Registration</small>
                  <strong>{registrationWindow.date}</strong>
                </span>
                <span>
                  <small>Entrance exam</small>
                  <strong>{examDate.date}</strong>
                </span>
              </div>
              <em>
                Confirm the schedule with the ME Program before submitting an
                application.
              </em>
            </div>
          </div>
        </section>

        <section
          className="section white admissions-calendar-section"
          id="admission-calendar"
        >
          <div className="shell">
            <header className="admissions-section-heading">
              <p>01 · Admission calendar</p>
              <h2>Important dates</h2>
              <span>
                Five steps from registration to the start of the academic year.
              </span>
            </header>

            <ol className="admissions-timeline">
              {admissionsContent.milestones.map((milestone) => (
                <li key={milestone.step}>
                  <p className="admissions-timeline-step">
                    <span>{String(milestone.step).padStart(2, "0")}</span>
                    <strong>{milestone.title}</strong>
                  </p>
                  <time>{milestone.date}</time>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="section navy admissions-exam-section">
          <div className="shell">
            <header className="admissions-section-heading light">
              <p>02 · Entrance examination</p>
              <h2>Entrance examination subjects</h2>
              <span>
                The ME entrance examination covers Mathematics, Physics, and
                Logic.
              </span>
            </header>

            <div className="admissions-subject-grid">
              {admissionsContent.subjects.map((subject) => (
                <article key={subject.code}>
                  <h3>{subject.name}</h3>
                </article>
              ))}
            </div>

            {admissionsContent.applicationForm.downloadUrl ? (
              <p className="admissions-form-download">
                <a
                  className="button button-navy"
                  href={admissionsContent.applicationForm.downloadUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  All four sheets as one PDF{" "}
                  <span aria-hidden="true">&darr;</span>
                </a>
                <span>
                  For reference while you fill in the paper forms. It is not a
                  submission form &mdash; the university issues and accepts
                  only the printed originals.
                </span>
              </p>
            ) : null}

            <div className="admissions-past-exams">
              <div>
                <strong>Prepare with previous examinations.</strong>
                <span>
                  Review the available papers before the entrance examination.
                </span>
              </div>
              <a
                className="button button-gold"
                href={admissionsContent.pastExamsUrl}
                target="_blank"
                rel="noreferrer"
              >
                Open past exams <span aria-hidden="true">↗</span>
              </a>
            </div>
          </div>
        </section>

        <section className="section cream admissions-form-section">
          <div className="shell admissions-form-grid">
            <div className="admissions-form-copy">
              <p className="admissions-kicker">03 · Registration form</p>
              <h2>How the application forms are filled</h2>
              <p>
                The RUPP application is a set of four paper sheets, issued and
                submitted by hand. These are photographs of a completed set, so
                you can see what goes in each field before you are handed the
                paper.
              </p>
              <p className="admissions-form-privacy">
                Only the applicant&rsquo;s name, signature and photograph have
                been covered. Everything else is left as written, so you can
                see exactly what each field expects.
              </p>

              <div className="admissions-form-status">
                <span aria-hidden="true">i</span>
                <div>
                  <strong>Digital copy not yet available</strong>
                  <p>
                    Obtain and submit the official hard-copy form through the
                    ME Program or Faculty of Engineering office during the
                    registration period.
                  </p>
                </div>
              </div>

              <p className="admissions-form-note">
                Required supporting documents may change. Confirm the current
                requirements with the program office before applying.
              </p>
            </div>

            <div className="admissions-form-sheets">
              {admissionsContent.applicationForm.sheets.map((sheet, index) => (
                <figure className="admissions-sheet" key={sheet.image}>
                  <img
                    src={sheet.image}
                    alt={`${sheet.title} sheet, completed, with the applicant's personal details removed`}
                    loading={index === 0 ? undefined : "lazy"}
                  />
                  <figcaption>
                    <strong>
                      <span aria-hidden="true">
                        {String(index + 1).padStart(2, "0")}
                      </span>{" "}
                      {sheet.title}
                    </strong>
                    <span lang="km">{sheet.khmer}</span>
                    <small>{sheet.note}</small>
                  </figcaption>
                </figure>
              ))}
            </div>
          </div>
        </section>

        <section className="admissions-help-band">
          <div className="shell">
            <div>
              <p>Need to confirm this intake?</p>
              <h2>Contact the ME Program before applying</h2>
            </div>
            <div className="admissions-help-actions">
              <a href={`mailto:${settings.email}`}>{settings.email}</a>
              <a href={`tel:${settings.phone.replace(/[^\d+]/g, "")}`}>
                {settings.phone}
              </a>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={settings} />
    </>
  );
}
