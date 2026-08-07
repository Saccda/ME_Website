/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getFacultyMembers, getHomeData } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function PeoplePage() {
  const [home, faculty] = await Promise.all([
    getHomeData(),
    getFacultyMembers(),
  ]);

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs trail={[{ label: "People" }]} />
        <section className="directory-hero">
          <div className="shell">
            <p className="eyebrow light">People</p>
            <h1>People</h1>
            <p>
              The educators, specialists, graduates, and collaborators of the
              Mechanical Engineering program at RUPP.
            </p>
          </div>
        </section>

        <section className="section white" id="faculty-staff">
          <div className="shell">
            <div className="detail-section-heading">
              <div>
                <p className="eyebrow">Faculty & staff</p>
                <h2>Faculty and teaching staff</h2>
              </div>
              <p>
                Our team connects disciplinary knowledge with laboratories,
                applied research, industry practice, and community engagement.
              </p>
            </div>

            {faculty.length > 0 ? (
              <div className="people-grid">
                {faculty.map((person) => (
                  <article className="person-card" key={person.id}>
                    <div className="person-photo">
                      {person.photo ? (
                        <img src={person.photo} alt={person.name} />
                      ) : (
                        <span aria-hidden="true">
                          {person.name
                            .split(" ")
                            .slice(0, 2)
                            .map((part) => part[0])
                            .join("")}
                        </span>
                      )}
                    </div>
                    <div>
                      <p>{person.role}</p>
                      <h3>{person.name}</h3>
                      <span>{person.bio}</span>
                      {person.email ? (
                        <a href={`mailto:${person.email}`}>Email profile</a>
                      ) : null}
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <div className="content-empty-state">
                <h3>No faculty profiles have been published yet</h3>
                <p>
                  Profiles can be published from the Faculty members section
                  in the ME content management system.
                </p>
              </div>
            )}
          </div>
        </section>

        <section className="section cream" id="alumni">
          <div className="shell alumni-feature">
            <div>
              <p className="eyebrow">Alumni</p>
              <h2>Graduate careers</h2>
            </div>
            <div>
              <p>
                We are building an alumni network that connects graduates with
                students, faculty, industry opportunities, and one another.
              </p>
              <Link
                className="button button-navy"
                href={`mailto:${home.settings.email}?subject=ME alumni network enquiry`}
              >
                Join the alumni network <span>↗</span>
              </Link>
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
