/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import Breadcrumbs from "@/components/Breadcrumbs";
import FocusIcon, { type FocusCode } from "@/components/FocusIcon";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getFacultyMembers, getHomeData, type FacultyMember } from "@/lib/api";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Faculty | Mechanical Engineering RUPP",
  description:
    "Teaching staff of the Mechanical Engineering program at the Royal University of Phnom Penh.",
};

/**
 * One line of substance under the role. The whole biography is passed through
 * and clamped in CSS rather than cut here, so the break lands on a line boundary
 * at whatever width the card ends up.
 */
function cardSummary(member: FacultyMember): string {
  if (member.research_interests.length > 0) {
    return member.research_interests.join(" · ");
  }
  return member.bio;
}

function initials(name: string) {
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("");
}

export default async function FacultyPage() {
  const [home, faculty] = await Promise.all([
    getHomeData(),
    getFacultyMembers(),
  ]);

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs
          trail={[{ label: "Teaching & Learning" }, { label: "Faculty" }]}
        />

        <section className="section white faculty-listing">
          <div className="shell">
            <header className="faculty-listing-head">
              <p className="eyebrow">
                Our faculty
                {faculty.length > 0 ? (
                  <span className="faculty-listing-count">
                    {faculty.length} members
                  </span>
                ) : null}
              </p>
              <h1>Faculty</h1>
              <p>
                Teaching staff across the four ME focus areas, combining
                academic expertise, laboratory practice, and applied research.
              </p>
            </header>

            {faculty.length > 0 ? (
              <ul className="faculty-card-grid">
                {faculty.map((member) => (
                  <li key={member.id}>
                    <article
                      className="faculty-card"
                      data-focus={member.focus_areas[0]?.code}
                    >
                      <div className="faculty-card-media">
                        {member.photo ? (
                          <img src={member.photo} alt="" loading="lazy" />
                        ) : (
                          <span aria-hidden="true">
                            {initials(member.name)}
                          </span>
                        )}
                      </div>
                      <div className="faculty-card-body">
                        <h2>
                          <Link href={`/faculty/${member.slug}`}>
                            {member.name}
                          </Link>
                          {member.credentials ? (
                            <span className="faculty-card-credentials">
                              , {member.credentials}
                            </span>
                          ) : null}
                        </h2>
                        <p className="faculty-card-role">{member.role}</p>

                        {cardSummary(member) ? (
                          <p className="faculty-card-summary">
                            {cardSummary(member)}
                          </p>
                        ) : null}

                        {/* The focus areas are the program's own taxonomy, so
                            they carry the icon set rather than a plain chip. */}
                        {member.focus_areas.length > 0 ? (
                          <ul className="faculty-card-focus">
                            {member.focus_areas.map((area) => (
                              <li key={area.code}>
                                <FocusIcon
                                  code={area.code as FocusCode}
                                  title={`${area.code} — ${area.title}`}
                                />
                                <span>{area.code}</span>
                              </li>
                            ))}
                          </ul>
                        ) : null}

                        <span className="faculty-card-cue" aria-hidden="true">
                          View profile <span>→</span>
                        </span>
                      </div>
                    </article>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="content-empty-state">
                <h2>No faculty profiles have been published yet</h2>
                <p>
                  Staff profiles are maintained in the program CMS and will
                  appear here once entries are added.
                </p>
              </div>
            )}
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
