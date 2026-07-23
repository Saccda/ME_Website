const editorial = (name: string) => `/assets/editorial/${name}.jpg`;

const focusHeroImages: Record<string, string> = {
  DMP: editorial("focus-dmp-hero"),
  TES: editorial("focus-tes-hero"),
  MAS: editorial("focus-mas-hero"),
  ECM: editorial("focus-ecm-hero"),
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

export function getFocusHeroImage(code: string, fallback = "") {
  return focusHeroImages[code] || fallback;
}
