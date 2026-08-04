const editorial = (name: string) => `/assets/editorial/${name}.jpg`;

const focusHeroImages: Record<string, string> = {
  DMP: editorial("focus-dmp-hero"),
  TES: editorial("focus-tes-hero"),
  MAS: editorial("focus-mas-hero"),
  ECM: editorial("focus-ecm-hero"),
};

/**
 * Editorial stand-in artwork for research projects, matched on title.
 *
 * An image chosen in the CMS always wins: this map only covers projects that
 * have no image of their own. It used to take precedence, which meant every
 * seeded project title matched a hard-coded file and changing the image in
 * Wagtail had no visible effect.
 */
export function getResearchImage(title: string, cmsImage = "") {
  if (cmsImage) return cmsImage;

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
  return "";
}

export function getFocusHeroImage(code: string, fallback = "") {
  return focusHeroImages[code] || fallback;
}

/**
 * Laboratory artwork for the teaching side of a focus area. Deliberately
 * different from `focusHeroImages` so a card about teaching and one about
 * research can sit side by side without repeating the same picture.
 */
const focusTeachingImages: Record<string, string> = {
  DMP: editorial("dmp-cnc"),
  TES: editorial("tes-fluid-bench"),
  MAS: editorial("mas-robot-vision"),
  ECM: editorial("ecm-project-workspace"),
};

export function getFocusTeachingImage(code: string, fallback = "") {
  return focusTeachingImages[code] || fallback;
}
