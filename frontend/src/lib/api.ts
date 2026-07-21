export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export type ProgramSettings = {
  program_name: string;
  program_short_name: string;
  established_year: number;
  hero_title: string;
  hero_emphasis: string;
  hero_description: string;
  hero_image: string | null;
  vision: string;
  mission_one: string;
  mission_two: string;
  program_years: number;
  credit_hours: number;
  address: string;
  email: string;
  phone: string;
  facebook_url: string;
  telegram_url: string;
  youtube_url: string;
  linkedin_url: string;
  application_url: string;
};

export type WhyChooseItem = {
  id?: number;
  title: string;
  description: string;
  media_kind: "photo" | "logo";
  image: string | null;
};

export type FocusArea = {
  code: string;
  title: string;
  slug: string;
  description: string;
  accent_color: string;
  image: string | null;
};

export type Course = {
  code: string;
  title: string;
  credits: number;
  semester: string;
};

export type CurriculumYear = {
  year: number;
  theme: string;
  credit_count: number;
  description: string;
  courses: Course[];
};

export type ResearchProject = {
  title: string;
  slug: string;
  summary: string;
  image: string | null;
  focus_area: FocusArea | null;
};

export type Partner = {
  name: string;
  partner_type: string;
  website: string;
  logo: string | null;
};

export type Facility = {
  name: string;
  description: string;
  image: string | null;
};

export type FocusDetailItem = {
  id?: number;
  title: string;
  description: string;
};

export type FocusCourse = Course & {
  year: number;
  year_theme: string;
};

export type FocusAreaDetail = FocusArea & {
  courses: FocusCourse[];
  facilities: Facility[];
  outcomes: FocusDetailItem[];
  learning_activities: FocusDetailItem[];
  career_paths: FocusDetailItem[];
  research_projects: ResearchProject[];
};

export type HomeData = {
  settings: ProgramSettings;
  why_choose: WhyChooseItem[];
  focus_areas: FocusArea[];
  curriculum: CurriculumYear[];
  research: ResearchProject[];
  partners: Partner[];
  facilities: Facility[];
};

const focusAreas: FocusArea[] = [
  {
    code: "DMP",
    title: "Design and Manufacturing Process",
    slug: "design-and-manufacturing-process",
    description:
      "Learn how ideas become real products—from creative design to modern manufacturing methods that shape everything we use.",
    accent_color: "#061b2b",
    image: "/assets/focus-dmp.png",
  },
  {
    code: "TES",
    title: "Thermofluid and Energy System",
    slug: "thermofluid-and-energy-system",
    description:
      "Engineer systems to utilize energy through generation, transfer, and storage—from cooling and heating to sustainable energy.",
    accent_color: "#dcae42",
    image: "/assets/focus-tes.png",
  },
  {
    code: "MAS",
    title: "Mechatronic and Automation System",
    slug: "mechatronic-and-automation-system",
    description:
      "Discover how mechanical, electrical, and computer systems work together—building smart machines for Industry 4.0.",
    accent_color: "#176ab5",
    image: "/assets/focus-mas.png",
  },
  {
    code: "ECM",
    title: "Engineering Compliance and Management",
    slug: "engineering-compliance-and-management",
    description:
      "Gain skills in safety, standards, and project management—ensuring solutions are reliable, efficient, and ready for the real world.",
    accent_color: "#3e8b56",
    image: "/assets/focus-ecm.png",
  },
];

const whyTitles = [
  ["Aligned with AUN–QA criteria", "Program quality is guided by recognized regional quality-assurance criteria.", "logo"],
  ["Job-ready Knowledge, Experiences, Skills and Attitudes", "Build practical knowledge, experience, technical skills, and professional attitudes through real engineering work.", "photo"],
  ["Strong Collaboration with Industrial & Academic Partner", "Learn through active relationships with industrial and academic partners, from joint projects to professional exchange.", "photo"],
  ["Member of CDIO Community", "Connect ideas to working outcomes by learning to conceive, design, implement, and operate real systems.", "logo"],
  ["Infused Technology into Teaching & Learning", "Use modern laboratory equipment, digital tools, and manufacturing technology throughout the learning experience.", "photo"],
  ["On par with emerging trends and Technologies: ML, AI, EV", "Explore machine learning, artificial intelligence, electric vehicles, automation, and Industry 4.0 applications.", "photo"],
  ["Adopt Cambodia FutureFit Framework", "Develop adaptable, resilient, and socially responsible engineering capabilities grounded in Cambodia’s future needs.", "logo"],
  ["Social Engagement and Community Services", "Connect engineering education with community service, empathy, teamwork, and meaningful social contribution.", "logo"],
  ["Active Experiential Learning beyond memorization", "Learn by building, testing, discussing, and improving through laboratories, workshops, site visits, and team projects.", "photo"],
] as const;

const courseSets: Array<[number, string, number, string, Array<[string, string, number]>]> = [
  [1, "Foundations & discovery", 36, "Develop mathematical confidence, engineering intuition, and essential workshop skills.", [["MTH 101", "Calculus for Engineers I", 5], ["PHY 101", "Engineering Physics I", 5], ["ME 103", "Engineering Drawing & CAD", 4], ["ME 105", "Introduction to Mechanical Engineering", 3], ["ME 107", "Workshop Practice & Safety", 4], ["ENG 101", "Academic English for Engineers", 3], ["CHM 101", "General Chemistry", 4], ["GEN 101", "Khmer Culture & Society", 3]]],
  [2, "Core engineering systems", 36, "Connect mechanics, materials, thermofluids, electronics, and computation through lab-based study.", [["MTH 203", "Engineering Mathematics III", 4], ["ME 211", "Thermodynamics I", 4], ["ME 213", "Mechanics of Materials", 4], ["ME 215", "Dynamics of Machinery", 4], ["ME 217", "Fluid Mechanics", 4], ["ME 219", "Materials & Manufacturing", 4], ["EE 201", "Electrical Systems for ME", 4], ["ME 221", "Computational Methods", 4]]],
  [3, "Integration & specialization", 35, "Choose a focus area while integrating analysis, experimentation, design, and control.", [["ME 311", "Heat Transfer", 4], ["ME 313", "Machine Design", 4], ["ME 315", "Control Systems", 4], ["ME 317", "Mechatronics Laboratory", 4], ["ME 319", "Numerical Simulation", 4], ["ME 3E1", "Focus Area Elective I", 4], ["ME 3E2", "Focus Area Elective II", 4], ["GEN 301", "Engineering Economics", 3]]],
  [4, "Practice, leadership & impact", 36, "Apply the full engineering process through professional practice, research, and a major capstone project.", [["ME 401", "Capstone Design Project I", 5], ["ME 402", "Capstone Design Project II", 5], ["ME 403", "Industrial Internship", 6], ["ME 405", "Applied Research Methods", 3], ["ME 4E1", "Focus Area Elective III", 4], ["ME 4E2", "Focus Area Elective IV", 4], ["ME 411", "Sustainable Engineering", 3], ["GEN 401", "Leadership & Professional Ethics", 3]]],
];

const fallbackData: HomeData = {
  settings: {
    program_name: "Mechanical Engineering",
    program_short_name: "ME",
    established_year: 2015,
    hero_title: "Engineer Tomorrow,",
    hero_emphasis: "Serve Cambodia.",
    hero_description:
      "Build the machines, energy systems, and intelligent technologies that move our nation forward.",
    hero_image: "/assets/hero-lab.png",
    vision:
      "To become a leader in Mechanical Engineering Education by infusing technology and social engagement into teaching and learning, research, and innovation for the advancement of society",
    mission_one:
      "To provide a modern mechanical engineering education by infusing social engagement and technology into educational activity for an effective educational program.",
    mission_two:
      "To collaborate with university partners on mechanical engineering to enforce proactive research activities that lead to an advancement of research and innovation.",
    program_years: 4,
    credit_hours: 140,
    address:
      "Faculty of Engineering, Royal University of Phnom Penh, Russian Federation Boulevard (110), Phnom Penh, Cambodia",
    email: "me.fe.rupp@gmail.com",
    phone: "+855 78 727 085",
    facebook_url: "https://www.facebook.com/profile.php?id=61589041923041",
    telegram_url: "https://t.me/mechanical_rupp",
    youtube_url: "",
    linkedin_url: "",
    application_url: "",
  },
  why_choose: whyTitles.map(([title, description, kind], index) => ({
    id: index + 1,
    title,
    description,
    media_kind: kind,
    image: `/assets/why/${String(index + 1).padStart(2, "0")}-${["aunqa", "job-ready", "collaboration", "cdio", "technology", "emerging-tech", "futurefit", "social-engagement", "active-learning"][index]}.webp`,
  })),
  focus_areas: focusAreas,
  curriculum: courseSets.map(([year, theme, credit_count, description, courses]) => ({
    year,
    theme,
    credit_count,
    description,
    courses: courses.map(([code, title, credits], index) => ({
      code,
      title,
      credits,
      semester: index < 4 ? "1" : "2",
    })),
  })),
  research: [
    ["Metal Recycling", "DMP", "Exploring practical processes for recovering, sorting, and reusing metal resources to support more sustainable manufacturing."],
    ["Automated Cooling & Spraying System", "MAS", "Developing sensor-based cooling and spraying controls for consistent, efficient environmental management."],
    ["Sugarcane Particle Board", "DMP", "Investigating sugarcane residue as a useful raw material for lower-impact engineered particle board."],
    ["Non-Intrusive Load Monitoring System", "TES", "Using electrical measurements and intelligent analysis to identify appliance-level energy use without individual sensors."],
  ].map(([title, code, summary]) => {
    const focus = focusAreas.find((area) => area.code === code) || null;
    return {
      title,
      slug: title.toLowerCase().replaceAll(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""),
      summary,
      image: focus?.image || null,
      focus_area: focus,
    };
  }),
  partners: [
    ["CJDM Digitalized Manufacturing", "industry", "cjdm.png"],
    ["Dynamic Engineering Steels", "industry", "des.jpg"],
    ["GGEAR Group", "industry", "ggear.png"],
    ["Legrand", "industry", "legrand.png"],
    ["LG", "industry", "lg.png"],
    ["Université Sorbonne Paris Nord", "academic", "universite-sorbonne-paris-nord.jpg"],
    ["Saint-Gobain", "industry", "saint-gobain.png"],
    ["Singapore Polytechnic", "academic", "singapore-polytechnic.png"],
    ["Solar Green Energy Cambodia", "industry", "soge.png"],
    ["VP.Start", "industry", "vp-start.png"],
  ].map(([name, partner_type, file]) => ({
    name,
    partner_type,
    website: "",
    logo: `/assets/partners/${file}`,
  })),
  facilities: [
    {
      name: "Robot with Artificial Vision System",
      description: "Learn automation and robotics for Industry 4.0.",
      image: "/assets/why/06-emerging-tech.webp",
    },
    {
      name: "CNC Machines",
      description: "Precision lathe and vertical machining for modern manufacturing.",
      image: "/assets/why/05-technology.webp",
    },
    {
      name: "Universal Testing Machine",
      description: "Test mechanical properties and material strength.",
      image: "/assets/focus-ecm.png",
    },
  ],
};

const fallbackFocusDetails: Record<
  string,
  {
    outcomes: Array<[string, string]>;
    activities: Array<[string, string]>;
    careers: Array<[string, string]>;
    courseCodes: string[];
    equipment: Array<[string, string, string]>;
  }
> = {
  DMP: {
    outcomes: [
      ["Design for manufacture", "Translate user needs into manufacturable components, assemblies, drawings, and specifications."],
      ["Digital engineering workflow", "Use CAD, simulation, CAM, and data to move confidently from concept to production."],
      ["Materials and process selection", "Choose suitable materials and processes using performance, cost, and sustainability criteria."],
      ["Quality through testing", "Measure, inspect, test, and improve products using evidence from the workshop and laboratory."],
    ],
    activities: [
      ["CAD-to-component design sprint", "Develop a part from an initial brief, validate it digitally, and prepare it for manufacture."],
      ["CNC and workshop practice", "Set up machining operations while applying safe working methods and process controls."],
      ["Materials testing investigation", "Compare material behavior and connect test results to practical design decisions."],
      ["Industry design challenge", "Respond to a partner problem through teamwork, prototyping, review, and iteration."],
    ],
    careers: [
      ["Design Engineer", "Develop products, mechanisms, and production-ready engineering documentation."],
      ["Manufacturing Engineer", "Improve processes, tooling, quality, efficiency, and production capability."],
      ["Process Engineer", "Design and optimize reliable industrial processes."],
      ["Product Engineer", "Guide a product from concept and testing through manufacture and improvement."],
    ],
    courseCodes: ["ME 103", "ME 107", "ME 213", "ME 219", "ME 313", "ME 319", "ME 3E1", "ME 3E2", "ME 401", "ME 402", "ME 403", "ME 4E1", "ME 4E2"],
    equipment: [
      ["CNC Machines", "Precision lathe and vertical machining for modern manufacturing.", "/assets/why/05-technology.webp"],
      ["Universal Testing Machine", "Test mechanical properties and material strength.", "/assets/focus-ecm.png"],
      ["Additive Manufacturing System", "Create and evaluate rapid prototypes with multi-nozzle 3D printing.", "/assets/focus-dmp.png"],
      ["Wire-cut EDM Machine", "Study ultra-precise metal cutting through controlled spark erosion.", "/assets/focus-dmp.png"],
      ["Controlled Atmosphere Furnace", "Conduct heat-treatment experiments and investigate material-property changes.", "/assets/focus-dmp.png"],
    ],
  },
  TES: {
    outcomes: [
      ["Thermal system analysis", "Model heat, work, energy conversion, and system performance using engineering fundamentals."],
      ["Fluid and heat-transfer design", "Evaluate flow, pressure, cooling, heating, and heat-exchanger behavior."],
      ["Energy performance improvement", "Measure consumption, identify losses, and propose practical efficiency improvements."],
      ["Sustainable energy integration", "Assess renewable generation, storage, and responsible energy use for Cambodian needs."],
    ],
    activities: [
      ["Thermal and fluid laboratory", "Test real systems, compare measurements with theory, and communicate uncertainty."],
      ["Cooling-system build", "Design and test a controlled cooling or spraying solution for a practical application."],
      ["Campus energy audit", "Collect energy-use evidence and turn it into prioritized improvement recommendations."],
      ["Renewable-energy field study", "Evaluate operating conditions, performance, maintenance, and community context on site."],
    ],
    careers: [
      ["Energy Engineer", "Improve energy generation, conversion, efficiency, and sustainability."],
      ["Power Engineer", "Support reliable energy and power systems across facilities and industry."],
      ["HVAC Engineer", "Design and manage heating, ventilation, refrigeration, and cooling systems."],
      ["Plant Engineer", "Operate and improve complex thermal, fluid, and utility systems."],
    ],
    courseCodes: ["PHY 101", "ME 211", "ME 217", "ME 311", "ME 319", "ME 3E1", "ME 3E2", "ME 401", "ME 402", "ME 403", "ME 4E1", "ME 4E2", "ME 411"],
    equipment: [
      ["Thermal and Heat-transfer Trainer", "Measure conduction, convection, and heat-exchanger performance.", "/assets/focus-tes.png"],
      ["Fluid Mechanics Bench", "Investigate flow rate, pressure loss, pumps, and fluid-system behavior.", "/assets/focus-tes.png"],
      ["Refrigeration and Cooling-system Rig", "Test cooling cycles, controls, efficiency, and operating conditions.", "/assets/focus-tes.png"],
      ["Renewable-energy Measurement Kit", "Monitor generation and system performance for solar and other energy applications.", "/assets/focus-tes.png"],
    ],
  },
  MAS: {
    outcomes: [
      ["Integrated system design", "Combine mechanical, electrical, sensing, control, and software elements into working machines."],
      ["Automation and control", "Develop control logic and tune automated systems for reliable performance."],
      ["Sensors and intelligent data", "Acquire, interpret, and use machine data for monitoring and decision-making."],
      ["Robotics and Industry 4.0", "Apply robotics, artificial vision, connected systems, and digital manufacturing concepts."],
    ],
    activities: [
      ["Sensor-and-actuator prototype", "Build a closed-loop system that senses its environment and responds predictably."],
      ["Robot vision programming", "Configure a vision-assisted robot task and improve its accuracy through testing."],
      ["PLC automation challenge", "Create, document, and troubleshoot an industrial sequence using safe automation practice."],
      ["EV control experiment", "Investigate electric mobility subsystems, control behavior, and system integration."],
    ],
    careers: [
      ["Mechatronics Engineer", "Create integrated electromechanical products and intelligent machines."],
      ["Automation Engineer", "Design, program, commission, and improve automated systems."],
      ["Control Systems Engineer", "Develop reliable control strategies for machines, vehicles, and processes."],
      ["Systems Engineer", "Coordinate complex technical requirements, interfaces, verification, and delivery."],
    ],
    courseCodes: ["ME 105", "ME 215", "EE 201", "ME 221", "ME 315", "ME 317", "ME 319", "ME 3E1", "ME 3E2", "ME 401", "ME 402", "ME 403", "ME 4E1", "ME 4E2"],
    equipment: [
      ["Robot with Artificial Vision System", "Learn automation and robotics for Industry 4.0.", "/assets/why/06-emerging-tech.webp"],
      ["PLC and Automation Workstations", "Program, commission, and troubleshoot industrial automation sequences.", "/assets/focus-mas.png"],
      ["Sensor and Data-acquisition Kits", "Connect sensors, acquire signals, and evaluate machine behavior.", "/assets/focus-mas.png"],
      ["Electric-vehicle Control Platform", "Explore integrated electric powertrain, sensing, and control systems.", "/assets/focus-mas.png"],
    ],
  },
  ECM: {
    outcomes: [
      ["Standards and compliance", "Interpret relevant standards and translate them into clear engineering requirements."],
      ["Safety and risk management", "Identify hazards, evaluate risk, and design practical controls throughout a project."],
      ["Quality and reliability", "Plan inspection, verification, documentation, and continuous improvement activities."],
      ["Engineering project leadership", "Balance scope, time, cost, people, quality, and professional responsibility."],
    ],
    activities: [
      ["Safety and risk assessment", "Inspect an engineering activity and prepare a practical hierarchy of controls."],
      ["Standards compliance review", "Assess a design or process against selected requirements and document evidence."],
      ["Project planning simulation", "Build a delivery plan with resources, schedule, risk, quality, and stakeholder actions."],
      ["Industry quality audit", "Observe a real process and report improvement opportunities using structured evidence."],
    ],
    careers: [
      ["Project Engineer", "Coordinate technical work, resources, risk, quality, and stakeholder delivery."],
      ["Quality Engineer", "Build systems that prevent defects and improve process capability."],
      ["Compliance Engineer", "Ensure products and operations meet standards, regulations, and documented requirements."],
      ["Facility Engineer", "Manage safe, reliable, and efficient engineering services and assets."],
    ],
    courseCodes: ["ME 107", "GEN 301", "ME 401", "ME 402", "ME 403", "ME 405", "ME 411", "GEN 401", "ME 4E1", "ME 4E2"],
    equipment: [
      ["Universal Testing Machine", "Test mechanical properties and material strength.", "/assets/focus-ecm.png"],
      ["Precision Metrology and Inspection Tools", "Verify dimensions, tolerances, quality, and documented requirements.", "/assets/focus-ecm.png"],
      ["Safety and Compliance Resources", "Practice structured hazard identification, risk assessment, and standards review.", "/assets/why/03-collaboration.webp"],
      ["Engineering Project Planning Workspace", "Plan scope, resources, schedule, risk, quality, and team delivery.", "/assets/why/09-active-learning.webp"],
    ],
  },
};

function getFallbackFocusArea(slug: string): FocusAreaDetail | null {
  const focusArea = focusAreas.find((area) => area.slug === slug);
  if (!focusArea) return null;
  const detail = fallbackFocusDetails[focusArea.code];
  const courses = fallbackData.curriculum.flatMap((year) =>
    year.courses
      .filter((course) => detail.courseCodes.includes(course.code))
      .map((course) => ({
        ...course,
        year: year.year,
        year_theme: year.theme,
      })),
  );
  const toItems = (items: Array<[string, string]>): FocusDetailItem[] =>
    items.map(([title, description], index) => ({
      id: index + 1,
      title,
      description,
    }));

  return {
    ...focusArea,
    courses,
    facilities: detail.equipment.map(([name, description, image]) => ({
      name,
      description,
      image,
    })),
    outcomes: toItems(detail.outcomes),
    learning_activities: toItems(detail.activities),
    career_paths: toItems(detail.careers),
    research_projects: fallbackData.research.filter(
      (project) => project.focus_area?.code === focusArea.code,
    ),
  };
}

export async function getHomeData(): Promise<HomeData> {
  try {
    const response = await fetch(`${API_BASE_URL}/home/`, {
      cache: "no-store",
      signal: AbortSignal.timeout(2500),
    });
    if (!response.ok) return fallbackData;
    const data = (await response.json()) as Partial<HomeData>;
    return data.settings ? (data as HomeData) : fallbackData;
  } catch {
    return fallbackData;
  }
}

export async function getFocusArea(
  slug: string,
): Promise<FocusAreaDetail | null> {
  const fallback = getFallbackFocusArea(slug);
  if (!fallback) return null;

  try {
    const response = await fetch(
      `${API_BASE_URL}/focus-areas/${encodeURIComponent(slug)}/`,
      {
        cache: "no-store",
        signal: AbortSignal.timeout(2500),
      },
    );
    if (!response.ok) return fallback;
    return (await response.json()) as FocusAreaDetail;
  } catch {
    return fallback;
  }
}
