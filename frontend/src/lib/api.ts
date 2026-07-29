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
  career_paths: FocusDetailItem[];
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

export type OpportunityFocusArea = Pick<
  FocusArea,
  "code" | "title" | "slug" | "accent_color"
>;

export type Opportunity = {
  id?: number;
  title: string;
  slug: string;
  opportunity_type: "job" | "internship" | "scholarship" | "training";
  opportunity_type_label: string;
  partner: Partner | null;
  announcement_image: string | null;
  focus_areas: OpportunityFocusArea[];
  summary: string;
  location: string;
  application_deadline: string | null;
  application_url: string;
  is_featured: boolean;
};

export type FacultyMember = {
  id: number;
  name: string;
  role: string;
  bio: string;
  email: string;
  photo: string | null;
  focus_areas: FocusArea[];
};

export type NewsEvent = {
  id: number;
  content_type: "news" | "event";
  title: string;
  slug: string;
  excerpt: string;
  image: string | null;
  event_date: string | null;
  published_at: string;
};

export type Facility = {
  name: string;
  description: string;
  reference_url: string;
  availability_status: "available" | "new" | "commissioning" | "planned";
  availability_label: string;
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
  opportunities: Opportunity[];
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
    career_paths: [
      { title: "Design Engineer", description: "Develop products, mechanisms, and production-ready engineering documentation." },
      { title: "Manufacturing Engineer", description: "Improve processes, tooling, quality, efficiency, and production capability." },
      { title: "Process Engineer", description: "Design and optimize reliable industrial processes." },
      { title: "Product Engineer", description: "Guide a product from concept and testing through manufacture and improvement." },
    ],
  },
  {
    code: "TES",
    title: "Thermofluid and Energy System",
    slug: "thermofluid-and-energy-system",
    description:
      "Engineer systems to utilize energy through generation, transfer, and storage—from cooling and heating to sustainable energy.",
    accent_color: "#dcae42",
    image: "/assets/focus-tes.png",
    career_paths: [
      { title: "Energy Engineer", description: "Improve energy generation, conversion, efficiency, and sustainability." },
      { title: "Power Engineer", description: "Support reliable energy and power systems across facilities and industry." },
      { title: "HVAC Engineer", description: "Design and manage heating, ventilation, refrigeration, and cooling systems." },
      { title: "Plant Engineer", description: "Operate and improve complex thermal, fluid, and utility systems." },
    ],
  },
  {
    code: "MAS",
    title: "Mechatronic and Automation System",
    slug: "mechatronic-and-automation-system",
    description:
      "Discover how mechanical, electrical, and computer systems work together—building smart machines for Industry 4.0.",
    accent_color: "#176ab5",
    image: "/assets/focus-mas.png",
    career_paths: [
      { title: "Mechatronics Engineer", description: "Create integrated electromechanical products and intelligent machines." },
      { title: "Automation Engineer", description: "Design, program, commission, and improve automated systems." },
      { title: "Control Systems Engineer", description: "Develop reliable control strategies for machines, vehicles, and processes." },
      { title: "Systems Engineer", description: "Coordinate technical requirements, interfaces, verification, and delivery." },
    ],
  },
  {
    code: "ECM",
    title: "Engineering Compliance and Management",
    slug: "engineering-compliance-and-management",
    description:
      "Gain skills in safety, standards, and project management—ensuring solutions are reliable, efficient, and ready for the real world.",
    accent_color: "#3e8b56",
    image: "/assets/focus-ecm.png",
    career_paths: [
      { title: "Project Engineer", description: "Coordinate technical work, resources, risk, quality, and stakeholder delivery." },
      { title: "Quality Engineer", description: "Build systems that prevent defects and improve process capability." },
      { title: "Compliance Engineer", description: "Ensure products and operations meet standards, regulations, and documented requirements." },
      { title: "Facility Engineer", description: "Manage safe, reliable, and efficient engineering services and assets." },
    ],
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
  opportunities: [],
  facilities: [],
};

const fallbackFocusDetails: Record<
  string,
  {
    outcomes: Array<[string, string]>;
    activities: Array<[string, string]>;
    careers: Array<[string, string]>;
    courseCodes: string[];
    equipment: Array<
      [string, string, string, Facility["availability_status"]]
    >;
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
      ["Excetek V400G Plus Wire-Cut EDM", "Cut complex profiles through controlled wire electrical-discharge machining.", "https://www.excetek.com/shop/v400g-plus-17#attr=", "available"],
      ["Rownd Desktop CNC Lathe", "Support compact CNC turning, small-part production, and manufacturing training.", "https://rowndprecision.com/en-us/products/rownd-desktop-cnc-lathe-compact-modular-high-precision-3", "available"],
      ["DMC2 Mini CNC", "Provide compact CNC machining for prototyping, setup, tooling, and process planning.", "https://shariffdmc.com/product/dmc2-mini-cnc/", "available"],
      ["Carbolite HTF High-Temperature Chamber Furnace", "Support high-temperature heat treatment, annealing, calcination, and sintering.", "https://www.carbolite.com/products/chamber-furnaces/laboratory-furnaces/htf-high-temperature-chamber-furnaces/", "available"],
      ["DECHANG GH4230 Metal Band Saw", "Prepare metal stock before turning, milling, forming, or fabrication.", "https://www.alibaba.com/product-detail/DECHANG-GH4230-High-Efficiency-Mini-Metal_1601387433469.html", "new"],
      ["InssTek MX-Lab Six-Nozzle Metal Additive Manufacturing System", "Build and investigate metal components through additive manufacturing.", "https://www.insstek.com/products/mx-lab?ckattempt=3", "new"],
      ["SYIL L3 CNC Lathe", "Support precision CNC turning, toolpath development, setup, and production.", "https://syil.com/L3", "new"],
      ["SYIL X9 5-Axis Vertical Machining Center", "Enable advanced multi-axis milling and complex-part production.", "https://syil.com/x9", "new"],
      ["500-Ton Servo CNC Hydraulic Press", "Compact metal powder and support forming research before sintering.", "https://www.yihui-press.com/dongguan-yihui-hydraulic-press-machine-for-metal-deep-drawing.html", "new"],
      ["Metal Powder Water Atomization System", "Produce metal powder feedstock through controlled water atomization.", "https://en.hncpie.com/products_detail/17.html", "new"],
      ["Anycubic FDM 3D Printing System with ACE Pro", "Support rapid prototyping and multicolor filament workflows.", "https://store.anycubic.com/products/anycubic-ace-pro", "available"],
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
      ["Automated Cooling and Spraying System", "Investigate cooling, spraying control, sensing, actuation, and efficient operation.", "", "available"],
      ["Solar Tracking System", "Study tracking control, energy capture, measurement, and renewable-system performance.", "", "available"],
      ["Wind Turbine System", "Extend future learning and research in wind-energy conversion and control.", "", "planned"],
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
      ["Robot with Artificial Vision System", "Combine robotics, machine vision, sensing, and control for Industry 4.0.", "", "available"],
      ["Four-Station Automation Simulation System", "Practice sequencing, sensing, handling, control, and troubleshooting.", "", "available"],
      ["Robot with Warehouse Automation System", "Explore robotic material handling, storage, retrieval, and coordination.", "", "available"],
      ["Industrial Electronic Circuit System", "Build and diagnose industrial circuits used in machines and automation.", "", "available"],
      ["PLC Panel with Simulation System", "Program, simulate, commission, and troubleshoot industrial controls.", "", "available"],
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
      ["Universal Testing Machine", "Measure mechanical properties and material strength through controlled testing.", "https://www.insize.com/testingmachines/UTM-GB.html", "available"],
      ["Handheld LIBS Spectrometer", "Identify and evaluate material composition through rapid LIBS analysis.", "https://m.insize.com/page-35-2542.html", "available"],
      ["Precision Metrology Equipment Package", "Verify dimensions, tolerances, quality, and engineering compliance.", "https://insizeus.com/tool.html", "available"],
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
    facilities: detail.equipment.map((
      [name, description, reference_url, availability_status],
    ) => ({
      name,
      description,
      reference_url,
      availability_status,
      availability_label: {
        available: "Available",
        new: "New equipment",
        commissioning: "Commissioning",
        planned: "Planned",
      }[availability_status],
      image: null,
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
    if (!data.settings) return fallbackData;

    return {
      ...fallbackData,
      ...data,
      settings: {
        ...fallbackData.settings,
        ...data.settings,
      },
      opportunities: data.opportunities ?? fallbackData.opportunities,
    };
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

async function getCollection<T>(path: string): Promise<T[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/${path}/`, {
      cache: "no-store",
      signal: AbortSignal.timeout(2500),
    });
    if (!response.ok) return [];
    const data = (await response.json()) as T[] | { results?: T[] };
    return Array.isArray(data) ? data : data.results ?? [];
  } catch {
    return [];
  }
}

export function getFacultyMembers(): Promise<FacultyMember[]> {
  return getCollection<FacultyMember>("faculty");
}

export function getNewsEvents(): Promise<NewsEvent[]> {
  return getCollection<NewsEvent>("news");
}

export function getFacilities(): Promise<Facility[]> {
  return getCollection<Facility>("facilities");
}
