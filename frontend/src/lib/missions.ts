import type { NewsEvent, ProgramSettings } from "@/lib/api";

export type MissionKey = "teaching" | "research";

/** What a story carries from the CMS: a mission, both, or nothing. */
export type MissionAlignment = MissionKey | "both" | "";

export type Mission = {
  key: MissionKey;
  /** How the program numbers them in the approved document. */
  code: string;
  slug: string;
  /** The two headings the program gave these: short, and the ones it uses. */
  name: string;
  /** Which ProgramSettings field holds the approved wording. */
  statementField: "mission_one" | "mission_two";
  /** One line on what the mission asks of the program. Ours, not the document's. */
  premise: string;
  /** Where the work itself lives, for a reader who wants more than the log. */
  elsewhere: readonly { label: string; href: string }[];
};

/**
 * The program's two missions, as pages rather than as two paragraphs.
 *
 * The statements themselves stay in Wagtail -- they are approved wording and
 * an editor must be able to correct them -- so only what surrounds them is
 * held here: the names the program uses for the two halves of its work, and
 * where on this site each one is carried out.
 */
export const missions: readonly Mission[] = [
  {
    key: "teaching",
    code: "M1",
    slug: "teaching-and-learning",
    name: "Teaching & Learning",
    statementField: "mission_one",
    premise:
      "Education that reaches students through modern equipment, industry practice, and engagement beyond the campus.",
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
    name: "Research & Innovation",
    statementField: "mission_two",
    premise:
      "Research carried out with partners, and taken far enough to work outside the laboratory.",
    elsewhere: [
      { label: "Research areas", href: "/research" },
      { label: "Partnership", href: "/partnership" },
      { label: "Laboratory & equipment", href: "/facilities" },
    ],
  },
];

export function getMission(slug: string): Mission | undefined {
  return missions.find((mission) => mission.slug === slug);
}

export function otherMission(mission: Mission): Mission {
  return missions.find((item) => item.key !== mission.key) ?? mission;
}

export function missionStatement(
  mission: Mission,
  settings: ProgramSettings,
): string {
  return settings[mission.statementField];
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
  "mou-high-school": "teaching",
  "mechanical-engineering-laboratory-open-house": "teaching",
  "me-team-leads-the-first-lex-program": "teaching",
  "focus-area-laboratories-expand-their-teaching-equipment": "teaching",
  "preparing-industry-connected-learning-with-lg-at-campus-iii": "teaching",
  "strengthening-practical-manufacturing-skills-with-vp-start": "teaching",
  "students-train-on-cnc-machines": "teaching",
  "staff-training-on-cnc-milling-machine": "teaching",
  "me-laboratory-welcomes-students-from-battambang-high-school": "teaching",
  "stem-fair": "research",
  "mechanical-engineering-strengthens-its-industry-partnerships": "research",
  "connecting-field-data-with-engineering-decisions": "research",
  "sharing-the-cooling-and-spraying-system-with-communities": "research",
  "installing-cooling-and-spraying-systems-at-two-farms": "research",
  "fairfarms-site-assessment-and-system-design": "research",
};

export function alignmentOf(story: NewsEvent): MissionAlignment {
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
    .filter((story) => {
      const alignment = alignmentOf(story);
      return alignment === mission.key || alignment === "both";
    })
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
