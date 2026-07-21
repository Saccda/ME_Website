const editorial = (name: string) => `/assets/editorial/${name}.jpg`;

const focusHeroImages: Record<string, string> = {
  DMP: editorial("focus-dmp-hero"),
  TES: editorial("focus-tes-hero"),
  MAS: editorial("focus-mas-hero"),
  ECM: editorial("focus-ecm-hero"),
};

const homeFacilityImages: Record<string, string> = {
  "Robot with Artificial Vision System": editorial("home-robot-vision"),
  "CNC Machines": editorial("home-cnc-machine"),
  "Universal Testing Machine": editorial("home-material-testing"),
};

const focusFacilityImages: Record<string, string> = {
  "DMP:CNC Machines": editorial("dmp-cnc"),
  "DMP:Universal Testing Machine": editorial("dmp-utm"),
  "DMP:Additive Manufacturing System": editorial("dmp-additive"),
  "DMP:Wire-cut EDM Machine": editorial("dmp-edm"),
  "DMP:Controlled Atmosphere Furnace": editorial("dmp-furnace"),
  "TES:Thermal and Heat-transfer Trainer": editorial("tes-heat-transfer"),
  "TES:Fluid Mechanics Bench": editorial("tes-fluid-bench"),
  "TES:Refrigeration and Cooling-system Rig": editorial("tes-refrigeration"),
  "TES:Renewable-energy Measurement Kit": editorial("tes-renewable-kit"),
  "MAS:Robot with Artificial Vision System": editorial("mas-robot-vision"),
  "MAS:PLC and Automation Workstations": editorial("mas-plc"),
  "MAS:Sensor and Data-acquisition Kits": editorial("mas-sensors"),
  "MAS:Electric-vehicle Control Platform": editorial("mas-ev-platform"),
  "ECM:Universal Testing Machine": editorial("ecm-utm"),
  "ECM:Precision Metrology and Inspection Tools": editorial("ecm-metrology"),
  "ECM:Safety and Compliance Resources": editorial("ecm-safety"),
  "ECM:Engineering Project Planning Workspace": editorial(
    "ecm-project-workspace",
  ),
};

export function getResearchImage(title: string, fallback = "") {
  const normalized = title.toLowerCase();
  if (normalized.includes("metal recycling")) {
    return editorial("research-metal-recycling");
  }
  if (normalized.includes("cooling") || normalized.includes("spraying")) {
    return editorial("research-automated-cooling");
  }
  if (
    normalized.includes("particle board") ||
    normalized.includes("particle-board")
  ) {
    return editorial("research-particle-board");
  }
  if (
    normalized.includes("load monitoring") ||
    normalized.includes("load-monitoring")
  ) {
    return editorial("research-load-monitoring");
  }
  return fallback;
}

export function getHomeFacilityImage(name: string, fallback = "") {
  return homeFacilityImages[name] || fallback;
}

export function getFocusHeroImage(code: string, fallback = "") {
  return focusHeroImages[code] || fallback;
}

export function getFocusFacilityImage(
  code: string,
  name: string,
  fallback = "",
) {
  return focusFacilityImages[`${code}:${name}`] || fallback;
}
