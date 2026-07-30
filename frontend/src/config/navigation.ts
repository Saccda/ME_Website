export type NavigationLink = {
  label: string;
  href?: string;
  children?: readonly NavigationLink[];
};

export type NavigationSection = {
  label: string;
  href?: string;
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
    label: "Research",
    href: "/research",
    links: [
      {
        label: "DMP — Design & Manufacturing",
        href: "/research/dmp",
      },
      {
        label: "TES — Thermofluid & Energy",
        href: "/research/tes",
      },
      {
        label: "MAS — Mechatronics & Automation",
        href: "/research/mas",
      },
      {
        label: "ECM — Compliance & Management",
        href: "/research/ecm",
      },
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
