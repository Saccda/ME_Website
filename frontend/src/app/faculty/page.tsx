/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getFacultyMembers, getHomeData, type FacultyMember } from "@/lib/api";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Faculty | Mechanical Engineering RUPP",
  description:
    "Teaching staff of the Mechanical Engineering programme at the Royal University of Phnom Penh.",
};

/**
 * Expertise chips. Research interests are the readable signal, but they only
 * exist once migration 0009 is deployed, so focus-area codes carry the card
 * until then. Capped at three so a well-filled profile cannot unbalance the row.
 */
function tagsFor(member: FacultyMember): string[] {
  const interests = member.research_interests.slice(0, 2);
  const codes = member.focus_areas.map((area) => area.code);
  return [...interests, ...codes].slice(0, 3);
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
              <p className="eyebrow">Our faculty</p>
              <h1>
                Meet the people <em>shaping future engineers.</em>
              </h1>
              <p>
                Our teaching staff combine academic expertise, laboratory
                practice, and applied research across the four ME focus areas.
              </p>
            </header>

            {faculty.length > 0 ? (
              <ul className="faculty-card-grid">
                {faculty.map((member) => (
                  <li key={member.id}>
                    <article className="faculty-card">
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
                        </h2>
                        <p className="faculty-card-role">{member.role}</p>

                        {tagsFor(member).length > 0 ? (
                          <ul className="faculty-card-tags">
                            {tagsFor(member).map((tag) => (
                              <li key={tag}>{tag}</li>
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
                <h2>Faculty profiles are being published.</h2>
                <p>
                  Staff profiles are maintained in the programme CMS and will
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
