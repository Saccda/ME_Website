export type NavigationLink = {
  label: string;
  href?: string;
  children?: readonly NavigationLink[];
};

export type NavigationSection = {
  label: string;
  links: readonly NavigationLink[];
};

export const navigationItems: readonly NavigationSection[] = [
  {
    label: "About",
    links: [
      { label: "Vision", href: "/about#vision" },
      { label: "Mission", href: "/about#mission" },
      {
        label: "PEOs (Program Educational Objectives)",
        href: "/about#peos",
      },
      {
        label: "PLOs (Program Learning Outcomes)",
        href: "/about#plos",
      },
      { label: "Area of Focus", href: "/#focus" },
    ],
  },
  {
    label: "Teaching & Learning",
    links: [
      { label: "Curriculum", href: "/curriculum" },
      { label: "Faculty", href: "/people#faculty-staff" },
      { label: "Facility", href: "/facilities" },
    ],
  },
  {
    label: "Research & Innovation",
    links: [
      {
        label: "Research Area",
        children: [
          {
            label: "DMP",
            href: "/focus/design-and-manufacturing-process#focus-research",
          },
          {
            label: "TES",
            href: "/focus/thermofluid-and-energy-system#focus-research",
          },
          {
            label: "MAS",
            href: "/focus/mechatronic-and-automation-system#focus-research",
          },
          {
            label: "ECM",
            href: "/focus/engineering-compliance-and-management#focus-research",
          },
        ],
      },
      { label: "Partnership", href: "/#partners" },
    ],
  },
  {
    label: "News & Events",
    links: [
      { label: "Job Opportunities", href: "/#opportunities" },
      { label: "Lab Open House", href: "/news-events#lab-openhouse" },
      { label: "Seminar Series", href: "/news-events#seminar-series" },
      { label: "Publication", href: "/news-events#publication" },
      { label: "Latest News", href: "/news-events#latest" },
    ],
  },
];
