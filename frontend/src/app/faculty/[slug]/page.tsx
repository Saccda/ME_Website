/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import EngineeringMotif from "@/components/EngineeringMotif";
import ProfileDetailRow from "@/components/ProfileDetailRow";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getFacultyMember, getHomeData, type FacultyMember } from "@/lib/api";

export const dynamic = "force-dynamic";

type ProfilePageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({
  params,
}: ProfilePageProps): Promise<Metadata> {
  const { slug } = await params;
  const lookup = await getFacultyMember(slug);
  if (lookup.status !== "found") return { title: "Faculty | ME RUPP" };
  return {
    title: `${lookup.member.name} | Mechanical Engineering RUPP`,
    description: lookup.member.bio || lookup.member.role,
  };
}

function initials(name: string) {
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("");
}

/** "a, b, and c" — used for the one-line specialism summary. */
function toSentenceList(items: string[]) {
  const lower = items.map((item) => item.toLowerCase());
  if (lower.length === 1) return lower[0];
  return `${lower.slice(0, -1).join(", ")}, and ${lower[lower.length - 1]}`;
}

function chipsFor(member: FacultyMember) {
  const interests = member.research_interests.slice(0, 4);
  const codes = member.focus_areas.map((area) => area.code);
  return interests.length > 0 ? interests : codes;
}

export default async function FacultyProfilePage({ params }: ProfilePageProps) {
  const { slug } = await params;
  const [lookup, home] = await Promise.all([
    getFacultyMember(slug),
    getHomeData(),
  ]);

  if (lookup.status === "not-found") notFound();

  // The directory could not be reached; say so rather than claiming the person
  // does not exist, which is what a 404 would imply.
  if (lookup.status === "unavailable") {
    return (
      <>
        <SiteHeader settings={home.settings} />
        <main id="main-content" className="editorial-page">
          <section className="section white">
            <div className="shell">
              <div className="content-empty-state">
                <h1>This profile is temporarily unavailable.</h1>
                <p>
                  The faculty directory could not be reached. Please try again
                  shortly, or return to the full faculty list.
                </p>
                <Link className="text-link" href="/faculty">
                  All faculty <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </section>
        </main>
        <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
      </>
    );
  }

  const member = lookup.member;
  const chips = chipsFor(member);
  const summary =
    member.research_interests.length > 0
      ? `Specialising in ${toSentenceList(member.research_interests.slice(0, 4))}.`
      : "";
  const affiliation = [
    `${home.settings.program_name} Program`,
    member.focus_areas.map((area) => area.code).join(", "),
  ]
    .filter(Boolean)
    .join(" · ");

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="profile-page">
        <EngineeringMotif side="left" />
        <EngineeringMotif side="right" />

        <div className="shell profile-shell">
          <nav className="profile-crumb" aria-label="Breadcrumb">
            <Link href="/faculty">Faculty</Link>
            <span aria-hidden="true">/</span>
            <span aria-current="page">{member.name}</span>
          </nav>

          <section className="profile-hero">
            <div className="profile-portrait">
              {member.photo ? (
                <img src={member.photo} alt={member.name} />
              ) : (
                <span aria-hidden="true">{initials(member.name)}</span>
              )}
            </div>

            <div className="profile-intro">
              <p className="profile-eyebrow">Faculty profile</p>
              <h1>
                {member.name}
                {member.credentials ? (
                  <span className="profile-credentials">
                    , {member.credentials}
                  </span>
                ) : null}
              </h1>
              <p className="profile-role">{member.role}</p>
              <p className="profile-affiliation">{affiliation}</p>

              <span className="profile-rule" aria-hidden="true" />

              {summary ? <p className="profile-summary">{summary}</p> : null}

              {chips.length > 0 ? (
                <ul className="profile-chips">
                  {chips.map((chip) => (
                    <li key={chip}>{chip}</li>
                  ))}
                </ul>
              ) : null}

              {member.email || member.phone || member.profile_url ? (
                <div className="profile-contact-card">
                  <p className="profile-contact-label">Contact</p>
                  <div className="profile-contact-rows">
                    {member.email ? (
                      <p>
                        <span className="profile-contact-value">
                          <svg
                            className="profile-contact-icon"
                            viewBox="0 0 24 24"
                            aria-hidden="true"
                          >
                            <path d="M3 6h18v12H3z" />
                            <path d="M3 7l9 6 9-6" />
                          </svg>
                          {member.email}
                        </span>
                        <a href={`mailto:${member.email}`}>
                          Send an email <span aria-hidden="true">→</span>
                        </a>
                      </p>
                    ) : null}
                    {member.phone ? (
                      <p>
                        <span>{member.phone}</span>
                        <a href={`tel:${member.phone.replace(/[^\d+]/g, "")}`}>
                          Call <span aria-hidden="true">→</span>
                        </a>
                      </p>
                    ) : null}
                    {member.profile_url ? (
                      <p>
                        <a
                          className="profile-contact-external"
                          href={member.profile_url}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          Research profile <span aria-hidden="true">↗</span>
                        </a>
                      </p>
                    ) : null}
                  </div>
                </div>
              ) : null}
            </div>
          </section>

          <section className="profile-body">
            <div className="profile-about">
              <h2>About {member.name}</h2>
              {member.bio ? (
                <p>{member.bio}</p>
              ) : (
                <p className="profile-about-empty">
                  A biography for this member of staff has not been published
                  yet.
                </p>
              )}

              {member.publications.length > 0 ? (
                <div className="profile-publications-block">
                  <h2>Selected publications</h2>
                  <ul>
                    {member.publications.map((entry) => (
                      <li key={entry}>{entry}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>

            <aside className="profile-details" aria-label="Profile details">
              <h2>Profile details</h2>
              {member.research_interests.length > 0 ||
              member.education.length > 0 ||
              member.courses_taught.length > 0 ||
              member.office ? (
                <div className="profile-detail-rows">
                  <ProfileDetailRow
                    icon="expertise"
                    label="Areas of expertise"
                    items={member.research_interests}
                  />
                  <ProfileDetailRow
                    icon="education"
                    label="Education"
                    items={member.education}
                  />
                  <ProfileDetailRow
                    icon="courses"
                    label="Courses taught"
                    items={member.courses_taught}
                  />
                  <ProfileDetailRow
                    icon="office"
                    label="Office"
                    items={member.office ? [member.office] : []}
                  />
                </div>
              ) : (
                <p className="profile-details-empty">
                  Expertise, education, and teaching details will appear here
                  once they are added in the programme CMS.
                </p>
              )}
            </aside>
          </section>

          <p className="profile-back">
            <Link className="text-link" href="/faculty">
              <span aria-hidden="true">←</span> All faculty
            </Link>
          </p>
        </div>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
