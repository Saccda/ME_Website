export type HelixStrand = {
  id: string;
  title: string;
  role: string;
  description: string;
  accent: string;
  /** Darker variant that stays legible on the gold partnership band. */
  onGold: string;
  image: string;
  alt: string;
  /** Longer statement used on the Partnership page. */
  summary: string;
  /** What a partner of this kind can do with ME. */
  offers: readonly string[];
};

/**
 * The quadruple helix innovation model: four partners whose collaboration
 * drives engineering research and practice. Each strand maps to one of the
 * brand accents so the diagram, the chips, and the cards stay in sync.
 *
 * Ordered to match the Research & Collaboration navigation.
 */
export const quadrupleHelix: HelixStrand[] = [
  {
    id: "academic",
    title: "Academic",
    role: "Knowledge",
    description:
      "Universities and research institutes that advance engineering knowledge, train graduates, and test ideas before industry adopts them.",
    accent: "var(--accent-1-ink)",
    onGold: "var(--accent-1-on-gold)",
    image: "/assets/partnership/partnership-academia.jpg",
    alt: "A lecturer speaking with students in a university lecture hall",
    summary:
      "Academic partners keep the programme honest. Joint supervision, shared laboratories, and external review test our teaching and research against practice elsewhere, and give students and staff a route into wider research networks.",
    offers: [
      "Joint research projects and co-supervision of theses",
      "Student and staff exchange, and visiting lectures",
      "Curriculum benchmarking and accreditation review",
      "Shared access to laboratories and specialist equipment",
    ],
  },
  {
    id: "industry",
    title: "Industry",
    role: "Application",
    description:
      "Companies and manufacturers that turn research into products, processes, and the workplaces our graduates enter.",
    accent: "var(--accent-2-ink)",
    onGold: "var(--accent-2-on-gold)",
    image: "/assets/partnership/partnership-industry.jpg",
    alt: "A manufacturing hall lined with CNC machining centres",
    summary:
      "Industry partners tell us what engineering practice actually demands. Companies scope real problems as student projects, host internships, and use our laboratories for testing and prototyping that would be costly to run in-house.",
    offers: [
      "Final-year capstone projects scoped by your engineers",
      "Internship placements and graduate recruitment",
      "Testing, measurement, and prototyping services",
      "Short courses and technical training for your staff",
    ],
  },
  {
    id: "government",
    title: "Government",
    role: "Policy",
    description:
      "Ministries and public agencies that set national priorities, standards, and the regulation engineering work must meet.",
    accent: "var(--accent-3-ink)",
    onGold: "var(--accent-3-on-gold)",
    image: "/assets/partnership/partnership-government.jpg",
    alt: "Rows of desks and microphones in an empty legislative chamber",
    summary:
      "Government partners connect the programme to national priorities. Public agencies shape the standards our graduates must work to, and draw on the faculty for technical studies, testing, and workforce development.",
    offers: [
      "Technical studies supporting policy and standards",
      "Workforce and skills development programmes",
      "Laboratory testing aligned to national standards",
      "Advisory participation in curriculum review",
    ],
  },
  {
    id: "society",
    title: "Society",
    role: "Purpose",
    description:
      "Communities whose needs decide which problems matter, keeping engineering accountable to the people it serves.",
    accent: "var(--accent-4-ink)",
    onGold: "var(--accent-4-on-gold)",
    image: "/assets/partnership/partnership-society.jpg",
    alt: "An aerial view of Phnom Penh showing the city and the riverfront",
    summary:
      "Society decides what engineering is for. Working with communities, schools, and civil society keeps the programme pointed at problems that matter locally, and shows students that technical decisions carry public consequences.",
    offers: [
      "Community-defined design and improvement projects",
      "Public laboratory open days and school outreach",
      "Appropriate-technology research for local needs",
      "Student volunteering and service learning",
    ],
  },
];
