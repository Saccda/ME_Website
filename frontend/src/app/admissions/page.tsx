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
              <h1>Mechanical Engineering admissions.</h1>
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
              <h2>Three subjects</h2>
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
              <h2>Application form preview</h2>
              <p>
                The official ME registration form is currently available only
                as a hard copy. This preview shows the types of information a
                student can prepare in advance; it is not an official
                submission form.
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

            <div
              className="admissions-form-preview"
              aria-label="Illustrative application form preview"
            >
              {admissionsContent.applicationForm.previewImage ? (
                <img
                  src={admissionsContent.applicationForm.previewImage}
                  alt="Sample Mechanical Engineering registration form"
                />
              ) : (
                <div className="sample-form-sheet">
                  <header>
                    <span>ME</span>
                    <div>
                      <strong>Registration form preview</strong>
                      <small>Preparation guide · not for submission</small>
                    </div>
                  </header>
                  <div className="sample-form-photo">Photo</div>
                  <div className="sample-form-field wide">
                    <span>Applicant name</span>
                  </div>
                  <div className="sample-form-field">
                    <span>Date of birth</span>
                  </div>
                  <div className="sample-form-field">
                    <span>Telephone</span>
                  </div>
                  <div className="sample-form-field wide">
                    <span>Email address</span>
                  </div>
                  <div className="sample-form-field wide">
                    <span>Previous school / education background</span>
                  </div>
                  <div className="sample-form-field">
                    <span>Applicant signature</span>
                  </div>
                  <div className="sample-form-field">
                    <span>Date</span>
                  </div>
                  <footer>Illustrative preview only</footer>
                </div>
              )}

              {admissionsContent.applicationForm.downloadUrl ? (
                <a
                  href={admissionsContent.applicationForm.downloadUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  Download the sample form <span aria-hidden="true">↗</span>
                </a>
              ) : null}
            </div>
          </div>
        </section>

        <section className="admissions-help-band">
          <div className="shell">
            <div>
              <p>Need to confirm this intake?</p>
              <h2>Contact the ME Program before applying.</h2>
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
