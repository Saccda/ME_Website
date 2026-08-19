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
  getResearchProjects,
  type FacultyMember,
  type ResearchProject,
} from "@/lib/api";
import {
  getFocusHeroImage,
  getFocusTeachingImage,
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

/** Projects from any of this member's focus areas, de-duplicated. */
async function relatedProjects(
  member: FacultyMember,
): Promise<ResearchProject[]> {
  if (member.focus_areas.length === 0) return [];

  const groups = await Promise.all(
    member.focus_areas.map((area) => getResearchProjects(area.code)),
  );

  const seen = new Set<string>();
  const projects: ResearchProject[] = [];
  for (const group of groups) {
    for (const project of group) {
      if (seen.has(project.slug)) continue;
      seen.add(project.slug);
      projects.push(project);
    }
  }
  return projects;
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
 * Cards authored on the member's record win outright — an author who has filled
 * the Selected work panel in gets exactly what they wrote, in their order.
 *
 * Otherwise the row is assembled, because a member's work is not only research:
 * it mixes the kinds of work the CMS already holds — published projects, the
 * research themes of their focus areas, and the teaching those areas are taught
 * through. One of each is taken first so the three cards are varied, then any
 * remaining slot is backfilled from whichever pool still has entries.
 */
function buildWorkCards(
  member: FacultyMember,
  projects: ResearchProject[],
): WorkCard[] {
  const authored = authoredWorkCards(member);
  if (authored.length > 0) return authored;

  const projectCards: WorkCard[] = projects.map((project) => ({
    key: `project-${project.slug}`,
    badge: "Research project",
    meta: project.focus_areas.map((area) => area.code).join(" · "),
    title: project.title,
    summary: project.summary,
    href: `/research/projects/${project.slug}`,
    image:
      getResearchImage(project.title, project.image || "") ||
      getFocusHeroImage(project.focus_areas[0]?.code ?? "") ||
      "/assets/hero-lab.webp",
    cta: "Explore the project",
  }));

  // Research themes are optional in the CMS, so an area without any still
  // contributes a card — the area itself — rather than leaving a gap.
  const themeCards: WorkCard[] = member.focus_areas.flatMap((area) => {
    const image = getFocusHeroImage(area.code, area.image || "/assets/hero-lab.webp");
    if (area.research_themes.length === 0) {
      return [
        {
          key: `area-${area.code}`,
          badge: "Research area",
          meta: area.code,
          title: area.research_question || area.title,
          summary: area.research_overview || area.description,
          href: `/research/${area.code.toLowerCase()}`,
          image,
          cta: "Explore the research",
        },
      ];
    }
    return area.research_themes.map((theme, index) => ({
      key: `theme-${area.code}-${index}`,
      badge: "Research theme",
      meta: area.title,
      title: theme.title,
      summary: theme.description,
      href: `/research/${area.code.toLowerCase()}`,
      image,
      cta: "Explore the work",
    }));
  });

  const teachingCards: WorkCard[] = member.focus_areas
    .filter((area) => area.learning_heading)
    .map((area) => ({
      key: `teaching-${area.code}`,
      badge: "Teaching & research",
      meta: area.title,
      title: area.learning_heading,
      summary: area.learning_intro,
      href: `/focus/${area.slug}`,
      image: getFocusTeachingImage(
        area.code,
        area.image || "/assets/hero-lab.webp",
      ),
      cta: "Explore the teaching",
    }));

  const pools = [projectCards, themeCards, teachingCards];
  const picked: WorkCard[] = [];
  for (const pool of pools) {
    const card = pool.shift();
    if (card) picked.push(card);
  }
  for (const pool of pools) {
    while (picked.length < 3 && pool.length > 0) picked.push(pool.shift()!);
  }
  return picked.slice(0, 3);
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
  const projects = await relatedProjects(member);
  const workCards = buildWorkCards(member, projects);
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
                  Research projects, research themes, and teaching from the
                  focus areas this member of staff works in.
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
