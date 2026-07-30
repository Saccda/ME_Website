export type ResearchAreaEditorial = {
  question: string;
  overview: string;
  themes: readonly string[];
};

export const researchAreaEditorial: Record<
  string,
  ResearchAreaEditorial
> = {
  DMP: {
    question:
      "How can an idea become a reliable, manufacturable, and more sustainable product?",
    overview:
      "Design and Manufacturing Process research connects product development, materials, digital engineering, and production. The work moves from defining a need to modelling, making, measuring, and improving a physical solution.",
    themes: [
      "Product and machine design",
      "Digital engineering and simulation",
      "Advanced and additive manufacturing",
      "Materials recovery and circular production",
    ],
  },
  TES: {
    question:
      "How can energy and thermal systems work more efficiently in Cambodia’s climate?",
    overview:
      "Thermofluid and Energy System research investigates heat, fluids, energy conversion, and environmental control. Projects connect fundamental analysis with cooling, renewable energy, storage, and practical efficiency.",
    themes: [
      "Thermal and fluid systems",
      "Cooling and heat-transfer technology",
      "Renewable energy and storage",
      "Energy measurement and efficiency",
    ],
  },
  MAS: {
    question:
      "How can machines sense, decide, and act with greater accuracy and autonomy?",
    overview:
      "Mechatronic and Automation System research brings mechanical systems together with electronics, control, computing, and data. The aim is to create useful intelligent machines for industry, infrastructure, and communities.",
    themes: [
      "Mechatronic and embedded systems",
      "Robotics and machine vision",
      "Automation and industrial control",
      "Intelligent monitoring and machine data",
    ],
  },
  ECM: {
    question:
      "How can engineering solutions remain safe, dependable, compliant, and well managed?",
    overview:
      "Engineering Compliance and Management research studies the systems around successful engineering: safety, standards, quality, reliability, project delivery, and responsible decision-making across a product or facility lifecycle.",
    themes: [
      "Safety, standards, and compliance",
      "Quality and reliability engineering",
      "Engineering project management",
      "Responsible and sustainable delivery",
    ],
  },
};

export function getResearchAreaEditorial(code: string) {
  return researchAreaEditorial[code.toUpperCase()] ?? null;
}
