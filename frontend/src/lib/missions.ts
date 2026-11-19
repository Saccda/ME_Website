import type { NewsEvent, ProgramSettings } from "@/lib/api";

export type MissionKey = "teaching" | "research" | "society";

/** What a story carries from the CMS: one mission, or nothing. */
export type MissionAlignment = MissionKey | "";

export type Mission = {
  key: MissionKey;
  /** How the program numbers them in the approved document. */
  code: string;
  slug: string;
  /** The names the program gave these: short, and the ones it uses. */
  name: string;
  /** Which ProgramSettings field holds the approved wording. */
  statementField: "mission_one" | "mission_two" | "mission_three";
  /**
   * The wording approved in November 2026, used when the CMS has nothing to
   * say or is still answering with a statement the program has replaced.
   */
  approvedStatement: string;
  /** The statement in five words, for the line under the card title. */
  tagline: string;
  /**
   * One line on what the mission asks of the program, for the page's meta
   * description only. Deliberately not rendered: on the page it sat a
   * paragraph away from the approved statement and read as a rival version
   * of it, and a reader cannot tell which one the program signed off.
   */
  premise: string;
  /** Where the work itself lives, for a reader who wants more than the log. */
  elsewhere: readonly { label: string; href: string }[];
};

/**
 * The program's three missions, as pages rather than as three paragraphs.
 *
 * Revised from two to three in November 2026. The statements themselves stay
 * in Wagtail -- they are approved wording and an editor must be able to
 * correct them -- so only what surrounds them is held here: the names the
 * program uses for the three parts of its work, and where on this site each
 * one is carried out.
 *
 * The research mission's slug keeps the name it was published under. It is
 * still accurate and a URL that has been given out is not worth breaking to
 * add a word.
 */
export const missions: readonly Mission[] = [
  {
    key: "teaching",
    code: "M1",
    slug: "teaching-and-learning",
    name: "Teaching & Learning",
    statementField: "mission_one",
    approvedStatement:
      "Equipping students with rigorous engineering fundamentals, practical hands-on competence, ethical values, and lifelong learning attitudes across all ME primary focuses.",
    tagline: "Fundamentals, hands-on competence, ethics",
    premise:
      "Equipping students across every ME focus, in the fundamentals and in the practice.",
    elsewhere: [
      { label: "Curriculum", href: "/curriculum" },
      { label: "Faculty", href: "/faculty" },
      { label: "Laboratory & equipment", href: "/facilities" },
    ],
  },
  {
    key: "research",
    code: "M2",
    slug: "research-and-innovation",
    name: "Applied Research & Innovation",
    statementField: "mission_two",
    approvedStatement:
      "Conducting high-quality, industry-relevant research and technological innovation to advance sustainable industrial productivity and engineering practices.",
    tagline: "Industry-relevant research and innovation",
    premise:
      "Research taken far enough to change how something is made or run outside the laboratory.",
    elsewhere: [
      { label: "Research areas", href: "/research" },
      { label: "Partnership", href: "/partnership" },
      { label: "Laboratory & equipment", href: "/facilities" },
    ],
  },
  {
    key: "society",
    code: "M3",
    slug: "societal-engagement",
    name: "Societal Engagement",
    statementField: "mission_three",
    approvedStatement:
      "Collaborating actively with industry, government, and local communities to develop practical, resilient engineering solutions.",
    tagline: "Solutions built with industry and community",
    premise:
      "Working with industry, government, and local communities on engineering that has to hold up in use.",
    elsewhere: [
      { label: "Partnership", href: "/partnership" },
      { label: "Industry partners", href: "/partnership#industry" },
      { label: "Society partners", href: "/partnership#society" },
    ],
  },
];

export function getMission(slug: string): Mission | undefined {
  return missions.find((mission) => mission.slug === slug);
}

/** The other two, in the order the program numbers them. */
export function otherMissions(mission: Mission): Mission[] {
  return missions.filter((item) => item.key !== mission.key);
}

/**
 * The wording the program replaced in November 2026, when it went from two
 * missions to three.
 *
 * A second bridge, for the same reason as the filing map below: the lab
 * backend is rebuilt by hand, so until it is, its API still answers with
 * these two -- and the page would show the superseded M1 and M2 beside a
 * correctly worded M3. Migration 0032 replaces them in the database; this
 * can go once it has run there.
 */
const supersededStatements = new Set([
  "To provide a modern mechanical engineering education by infusing social engagement and technology into educational activity for an effective educational program.",
  "To collaborate with university partners on mechanical engineering to enforce proactive research activities that lead to an advancement of research and innovation.",
]);

/**
 * The approved statement, from the CMS wherever the CMS has something to say.
 *
 * An editor's own wording always wins. What does not win is a statement the
 * program has already superseded, or no statement at all.
 */
export function missionStatement(
  mission: Mission,
  settings: ProgramSettings,
): string {
  const stored = (settings[mission.statementField] ?? "").trim();
  if (!stored || supersededStatements.has(stored)) {
    return mission.approvedStatement;
  }
  return stored;
}

/**
 * Where the fifteen stories published before the CMS field existed belong.
 *
 * A bridge, not a second source of truth. The same filing is written into
 * migration 0031 and the CMS is authoritative the moment the backend carries
 * the field: a story that arrives with a mission set is never looked up here.
 * It exists so the two pages are not empty between the frontend deploying and
 * the lab backend being rebuilt, and so an older API cannot blank them.
 *
 * It can be deleted once every published story carries its own alignment.
 */
const alignmentBeforeTheField: Record<string, MissionAlignment> = {
  // M1 -- equipping ME students, and the staff capability behind it.
  "students-train-on-cnc-machines": "teaching",
  "staff-training-on-cnc-milling-machine": "teaching",
  "strengthening-practical-manufacturing-skills-with-vp-start": "teaching",
  "me-team-leads-the-first-lex-program": "teaching",
  "preparing-industry-connected-learning-with-lg-at-campus-iii": "teaching",
  // M2 -- the research, and what it produced.
  "fairfarms-site-assessment-and-system-design": "research",
  "installing-cooling-and-spraying-systems-at-two-farms": "research",
  "connecting-field-data-with-engineering-decisions": "research",
  "stem-fair": "research",
  // M3 -- work done with people outside the program.
  "mechanical-engineering-laboratory-open-house": "society",
  "me-laboratory-welcomes-students-from-battambang-high-school": "society",
  "mou-high-school": "society",
  "focus-area-laboratories-expand-their-teaching-equipment": "society",
  "mechanical-engineering-strengthens-its-industry-partnerships": "society",
  "sharing-the-cooling-and-spraying-system-with-communities": "society",
};

/**
 * The six activities that change hands when two missions become three.
 *
 * The lab backend is already answering with the two-mission filing, and will
 * keep doing so until migration 0032 is applied there -- which would leave
 * M3 showing an empty log beside its own statement. Each entry fires only
 * while the story still carries exactly what the two-mission filing gave it,
 * so once 0032 has run every one of these is a no-op and the map can go.
 */
const refiledForThreeMissions: Record<
  string,
  { from: MissionAlignment; to: MissionAlignment }
> = {
  "mechanical-engineering-laboratory-open-house": {
    from: "teaching",
    to: "society",
  },
  "me-laboratory-welcomes-students-from-battambang-high-school": {
    from: "teaching",
    to: "society",
  },
  "mou-high-school": { from: "teaching", to: "society" },
  "focus-area-laboratories-expand-their-teaching-equipment": {
    from: "teaching",
    to: "society",
  },
  "mechanical-engineering-strengthens-its-industry-partnerships": {
    from: "research",
    to: "society",
  },
  "sharing-the-cooling-and-spraying-system-with-communities": {
    from: "research",
    to: "society",
  },
};

export function alignmentOf(story: NewsEvent): MissionAlignment {
  const refiled = refiledForThreeMissions[story.slug];
  if (refiled && story.mission === refiled.from) return refiled.to;
  if (story.mission) return story.mission;
  return alignmentBeforeTheField[story.slug] ?? "";
}

/**
 * The activities filed under one mission, newest first.
 *
 * A story dated by its activity period rather than by a day still sorts by
 * `published_at`, which is the date the program put on it.
 */
export function activitiesFor(
  mission: Mission,
  stories: readonly NewsEvent[],
): NewsEvent[] {
  return stories
    .filter((story) => alignmentOf(story) === mission.key)
    .sort(
      (a, b) =>
        Date.parse(b.event_date ?? b.published_at) -
        Date.parse(a.event_date ?? a.published_at),
    );
}

/** The calendar year an activity counts towards, or null if it has no date. */
export function activityYear(story: NewsEvent): number | null {
  const when = Date.parse(story.event_date ?? story.published_at);
  return Number.isNaN(when) ? null : new Date(when).getFullYear();
}

/** Activities grouped into years, newest year first, for the log. */
export function activitiesByYear(
  stories: readonly NewsEvent[],
): { year: number | null; items: NewsEvent[] }[] {
  const years: { year: number | null; items: NewsEvent[] }[] = [];
  for (const story of stories) {
    const year = activityYear(story);
    const group = years.find((entry) => entry.year === year);
    if (group) group.items.push(story);
    else years.push({ year, items: [story] });
  }
  return years;
}
