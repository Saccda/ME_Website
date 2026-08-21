/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import FocusIcon, { type FocusCode } from "@/components/FocusIcon";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import {
  getFacultyMember,
  getHomeData,
  type FacultyMember,
} from "@/lib/api";
import {
  getFocusHeroImage,
  getResearchImage,
} from "@/lib/editorialImages";

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

function tagsFor(member: FacultyMember) {
  return member.research_interests.length > 0
    ? member.research_interests.slice(0, 4)
    : member.focus_areas.map((area) => area.code);
}

/** Titles and qualifications end in a full stop without ending a sentence. */
const ABBREVIATION =
  /(?:^|\s)(?:Dr|Mr|Mrs|Ms|Prof|Assoc|Asst|Eng|Sr|Jr|St|No|vs|approx|Ph\.D|D\.Eng|M\.Eng|M\.Sc|B\.Sc|B\.Eng|e\.g|i\.e)\.$/i;

function sentences(text: string): string[] {
  const parts = text.split(/(?<=[.!?])\s+/);
  const out: string[] = [];
  for (const part of parts) {
    const previous = out[out.length - 1];
    if (previous && ABBREVIATION.test(previous)) {
      out[out.length - 1] = `${previous} ${part}`;
    } else {
      out.push(part);
    }
  }
  return out.filter(Boolean);
}

/**
 * The profile section is a large statement followed by a short description.
 *
 * `statement` is an authored CMS field, but a member with only a biography
 * still needs the section to read correctly, so the opening sentence is
 * promoted to the statement and the remainder becomes the description. The
 * whole biography is kept when it is a single sentence — splitting it would
 * leave the description empty.
 */
function profileCopy(member: FacultyMember): {
  statement: string;
  paragraphs: string[];
} {
  const blocks = member.bio
    .split(/\n{2,}/)
    .map((block) => block.trim())
    .filter(Boolean);

  if (member.statement.trim()) {
    return { statement: member.statement.trim(), paragraphs: blocks };
  }
  if (blocks.length === 0) return { statement: "", paragraphs: [] };

  const [lead, ...rest] = sentences(blocks[0]);
  const remainder = rest.join(" ");
  if (!remainder) return { statement: blocks[0], paragraphs: blocks.slice(1) };

  return { statement: lead, paragraphs: [remainder, ...blocks.slice(1)] };
}

/** The gold-ruled facts under the description. */
function profilePoints(member: FacultyMember) {
  const research =
    member.research_interests.length > 0
      ? member.research_interests
      : member.focus_areas.map((area) => area.title);

  return [
    member.courses_taught.length > 0
      ? { label: "Teaching", value: member.courses_taught.join(" · ") }
      : null,
    research.length > 0
      ? { label: "Research", value: research.join(" · ") }
      : null,
    member.publications.length > 0
      ? {
          label: "Selected publications",
          value: member.publications.join(" · "),
        }
      : null,
  ].filter(Boolean) as Array<{ label: string; value: string }>;
}

type WorkCard = {
  key: string;
  badge: string;
  meta: string;
  title: string;
  summary: string;
  href: string;
  image: string;
  cta: string;
};

/** Cards written on the member's own record in Wagtail. */
function authoredWorkCards(member: FacultyMember): WorkCard[] {
  return member.work_items
    .filter((item) => item.title)
    .map((item) => ({
      key: `item-${item.id}`,
      badge: item.badge,
      meta: item.meta,
      title: item.title,
      summary: item.summary,
      href: item.link_url,
      image:
        item.image ||
        getFocusHeroImage(member.focus_areas[0]?.code ?? "") ||
        "/assets/hero-lab.webp",
      cta: item.link_label,
    }));
}

/**
 * What this person's Selected work row shows, in order of authority.
 *
 * Hand-written cards first, then the research projects ticked on their record,
 * then nothing at all.
 *
 * The row used to be assembled from the focus areas a member belongs to when
 * neither was set -- a research theme, a teaching blurb, whichever project
 * happened to share an area. Every member of the same area got the same cards,
 * under a heading naming them personally. That is not a layout problem: a page
 * saying "Learn more about Dr X's work" over the DMP area's own description is
 * asserting something untrue about a real person. An empty section is honest;
 * an invented one is not.
 */
function buildWorkCards(member: FacultyMember): WorkCard[] {
  const authored = authoredWorkCards(member);
  if (authored.length > 0) return authored;

  return member.research_projects.map((project) => ({
    key: `project-${project.slug}`,
    badge: project.status === "completed" ? "Research project" : "Current research",
    meta: project.focus_areas.map((area) => area.code).join(" · "),
    title: project.title,
    summary: project.summary,
    href: `/research/projects/${project.slug}`,
    // The project's own picture, then the editorial stand-in kept for projects
    // that have none. Both are real images of the work, not of its area.
    image:
      project.image ||
      getResearchImage(project.title) ||
      getFocusHeroImage(project.focus_areas[0]?.code ?? "") ||
      "/assets/hero-lab.webp",
    cta: "Explore the project",
  }));
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
  const workCards = buildWorkCards(member);
  const { statement, paragraphs } = profileCopy(member);
  const points = profilePoints(member);
  const tags = tagsFor(member);
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

  const contactActions = [
    member.email
      ? {
          key: "email",
          href: `mailto:${member.email}`,
          label: "Email",
          aria: `Email ${member.name}`,
          external: false,
          icon: (
            <>
              <path d="M4 7h24v18H4z" />
              <path d="m5 9 11 9L27 9" />
            </>
          ),
        }
      : null,
    member.phone
      ? {
          key: "phone",
          href: `tel:${member.phone.replace(/[^\d+]/g, "")}`,
          label: "Phone",
          aria: `Call ${member.name}`,
          external: false,
          icon: (
            <>
              <path d="M7 4h6l3 7-4 2a14 14 0 0 0 7 7l2-4 7 3v6a2 2 0 0 1-2 2C13 27 5 19 5 6a2 2 0 0 1 2-2z" />
            </>
          ),
        }
      : null,
    member.profile_url
      ? {
          key: "scholar",
          href: member.profile_url,
          label: "Scholar",
          aria: `View ${member.name}'s research profile`,
          external: true,
          icon: (
            <>
              <path d="m3 13 13-8 13 8-13 8z" />
              <path d="M8 17v7c5 4 11 4 16 0v-7M29 13v9" />
            </>
          ),
        }
      : null,
  ].filter(Boolean) as Array<{
    key: string;
    href: string;
    label: string;
    aria: string;
    external: boolean;
    icon: React.ReactNode;
  }>;

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="faculty-detail">
        <div className="shell">
          <nav className="faculty-crumb" aria-label="Breadcrumb">
            <Link href="/faculty">Faculty</Link>
            <span aria-hidden="true">/</span>
            <span aria-current="page">{member.name}</span>
          </nav>
        </div>

        <section className="shell faculty-hero" aria-labelledby="profile-title">
          <figure className="faculty-hero-portrait">
            {member.photo ? (
              <img
                src={member.photo}
                alt={`${member.name}, ${member.role}`}
              />
            ) : (
              <span aria-hidden="true">{initials(member.name)}</span>
            )}
          </figure>

          <div className="faculty-hero-identity">
            <p className="faculty-hero-eyebrow">Faculty profile</p>
            <h1 id="profile-title">
              {member.name}
              {member.credentials ? (
                <span className="faculty-hero-credentials">
                  , {member.credentials}
                </span>
              ) : null}
            </h1>
            <p className="faculty-hero-role">{member.role}</p>
            <p className="faculty-hero-affiliation">{affiliation}</p>

            {summary ? (
              <p className="faculty-hero-summary">{summary}</p>
            ) : null}

            {tags.length > 0 ? (
              <ul className="faculty-hero-tags">
                {tags.map((tag) => (
                  <li key={tag}>{tag}</li>
                ))}
              </ul>
            ) : null}

            <div className="faculty-academic">
              <div>
                <h2>Research interests</h2>
                {member.research_interests.length > 0 ? (
                  <ul>
                    {member.research_interests.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  <p>
                    Research interests will be added from the faculty record.
                  </p>
                )}
              </div>
              <div>
                <h2>Education</h2>
                {member.education.length > 0 ? (
                  <ul>
                    {member.education.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  <p>Education details will be added from the faculty record.</p>
                )}
              </div>
            </div>

            <div
              className="faculty-contact-band"
              aria-label="Contact and areas of focus"
            >
              {contactActions.map((action) => (
                <div className="faculty-contact-item" key={action.key}>
                  <a
                    className="faculty-contact-action"
                    href={action.href}
                    aria-label={action.aria}
                    target={action.external ? "_blank" : undefined}
                    rel={action.external ? "noopener noreferrer" : undefined}
                  >
                    <svg viewBox="0 0 32 32" aria-hidden="true">
                      {action.icon}
                    </svg>
                    <span>{action.label}</span>
                  </a>
                </div>
              ))}

              {member.focus_areas.length > 0 ? (
                <div className="faculty-contact-item faculty-contact-focus">
                  <small>Associated areas of focus</small>
                  <div className="faculty-focus-row">
                    {member.focus_areas.map((area) => (
                      <Link
                        className="faculty-focus-link"
                        href={`/research/${area.code.toLowerCase()}`}
                        key={area.code}
                      >
                        <FocusIcon
                          code={area.code as FocusCode}
                          title={`${area.code} — ${area.title}`}
                        />
                        <span>{area.code}</span>
                      </Link>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        </section>

        <section className="faculty-about" id="about">
          <div className="shell">
            <p className="faculty-section-label">Profile</p>
            {statement ? (
              <h2 className="faculty-statement">{statement}</h2>
            ) : null}
            <div className="faculty-narrative">
              {paragraphs.length > 0 ? (
                paragraphs.map((paragraph) => (
                  <p key={paragraph.slice(0, 48)}>{paragraph}</p>
                ))
              ) : statement ? null : (
                <p className="faculty-narrative-empty">
                  A biography for this member of staff has not been published
                  yet.
                </p>
              )}
            </div>

            {points.length > 0 ? (
              <div className="faculty-points">
                {points.map((point) => (
                  <div className="faculty-point" key={point.label}>
                    <strong>{point.label}</strong>
                    <span>{point.value}</span>
                  </div>
                ))}
              </div>
            ) : null}
          </div>
        </section>

        {workCards.length > 0 ? (
          <section className="faculty-work" id="work">
            <div className="shell">
              <header className="faculty-work-head">
                <div>
                  <p className="faculty-section-label">Selected work</p>
                  {/* Named rather than "his work": the same template renders for
                      every member, and a pronoun would be a guess. */}
                  <h2>Learn more about {member.name}&rsquo;s work</h2>
                </div>
                <p>
                  Research projects this member of staff works on, chosen on
                  their record in the CMS.
                </p>
              </header>

              <div className="faculty-work-grid">
                {workCards.map((card) => {
                  const body = (
                    <>
                      <div className="faculty-work-media">
                        {card.badge ? <span>{card.badge}</span> : null}
                        <img src={card.image} alt="" />
                      </div>
                      {card.meta ? (
                        <p className="faculty-work-meta">{card.meta}</p>
                      ) : null}
                      <h3>{card.title}</h3>
                      {card.summary ? <p>{card.summary}</p> : null}
                      {card.cta ? (
                        <span className="faculty-work-more">
                          {card.cta} <span aria-hidden="true">→</span>
                        </span>
                      ) : null}
                    </>
                  );

                  // An authored card may have no destination, or point off
                  // site; neither can go through the internal router.
                  if (!card.href) {
                    return (
                      <article className="faculty-work-card" key={card.key}>
                        {body}
                      </article>
                    );
                  }
                  if (/^https?:\/\//i.test(card.href)) {
                    return (
                      <a
                        className="faculty-work-card"
                        href={card.href}
                        key={card.key}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {body}
                      </a>
                    );
                  }
                  return (
                    <Link
                      className="faculty-work-card"
                      href={card.href}
                      key={card.key}
                    >
                      {body}
                    </Link>
                  );
                })}
              </div>
            </div>
          </section>
        ) : null}

        <section className="faculty-cta">
          <div className="shell faculty-cta-inner">
            <div>
              <h2>Interested in collaborating?</h2>
              <p>
                Contact the Mechanical Engineering program to discuss
                research, teaching, or industry collaboration.
              </p>
            </div>
            <a
              className="button button-navy"
              href={`mailto:${member.email || home.settings.email}`}
            >
              Send an email <span aria-hidden="true">→</span>
            </a>
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
