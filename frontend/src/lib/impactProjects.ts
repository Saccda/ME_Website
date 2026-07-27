export type ImpactProject = {
  id: string;
  title: string;
  field: string;
  description: string;
  image: string;
  alt: string;
  accent: string;
  accentText: "light" | "dark";
  actionLabel: "Watch video" | "Read article";
  actionKind: "video" | "article";
  actionUrl: string;
  sourceLabel: string;
  sourceUrl: string;
};

export const impactProjects: ImpactProject[] = [
  {
    id: "drone-design",
    title: "Designing aircraft without a pilot",
    field: "Drone design",
    description:
      "Aerodynamics, lightweight structures, propulsion, sensors, and controls work together so unmanned aircraft can fly farther and perform missions too risky for pilots.",
    image: "/assets/impact/drone-global-hawk.jpg",
    alt: "A NASA Global Hawk unmanned aircraft being prepared before sunrise",
    accent: "#2387c9",
    accentText: "light",
    actionLabel: "Watch video",
    actionKind: "video",
    actionUrl:
      "https://science.nasa.gov/eclips/videos/designing-unmanned-aerial-vehicles/",
    sourceLabel: "NASA / Michael Bereda",
    sourceUrl:
      "https://www.nasa.gov/image-article/as-sun-rises-nasas-global-hawk-being-prepared-flight/",
  },
  {
    id: "automotive-manufacturing",
    title: "Printing a driveable car",
    field: "Automotive manufacturing",
    description:
      "The Strati showed how mechanical design, materials, large-scale 3D printing, machining, and assembly can radically shorten the path from concept to vehicle.",
    image: "/assets/impact/automotive-strati.jpg",
    alt: "The Strati, a driveable car with a 3D-printed body developed with Oak Ridge National Laboratory",
    accent: "#d73528",
    accentText: "light",
    actionLabel: "Read article",
    actionKind: "article",
    actionUrl: "https://www.ornl.gov/content/future-foundries",
    sourceLabel: "ORNL",
    sourceUrl: "https://www.ornl.gov/content/future-foundries",
  },
  {
    id: "satellite-engineering",
    title: "Building machines for space",
    field: "Satellite engineering",
    description:
      "A satellite must survive launch, deploy precisely, and manage extreme temperatures—demanding lightweight structures, reliable mechanisms, vibration control, and thermal engineering.",
    image: "/assets/impact/james-webb-space-telescope.png",
    alt: "The fully deployed James Webb Space Telescope against a field of stars",
    accent: "#e5b84f",
    accentText: "dark",
    actionLabel: "Watch video",
    actionKind: "video",
    actionUrl: "https://science.nasa.gov/mission/webb/webb-videos/",
    sourceLabel: "NASA",
    sourceUrl:
      "https://science.nasa.gov/asset/webb/james-webb-space-telescope/",
  },
  {
    id: "robotics",
    title: "Giving machines physical intelligence",
    field: "Robotics",
    description:
      "Actuators, joints, sensors, controls, and durable structures turn software into motion, helping robots work alongside people or enter hazardous environments.",
    image: "/assets/impact/robotics-valkyrie.jpg",
    alt: "NASA's white and gold Valkyrie humanoid robot",
    accent: "#2c39c9",
    accentText: "light",
    actionLabel: "Watch video",
    actionKind: "video",
    actionUrl: "https://robotics.nasa.gov/online-video-reliable-robots/",
    sourceLabel: "NASA",
    sourceUrl: "https://www.nasa.gov/technology/r5/",
  },
  {
    id: "datacenter-cooling",
    title: "Cooling the computing behind AI",
    field: "Data-center thermal systems",
    description:
      "Pumps, fluid loops, heat exchangers, cold plates, and immersion systems remove intense heat so high-density servers can operate safely and efficiently.",
    image: "/assets/impact/datacenter-liquid-cooling.jpg",
    alt: "Two Microsoft engineers working inside a two-phase immersion cooling tank",
    accent: "#3aaa55",
    accentText: "light",
    actionLabel: "Read article",
    actionKind: "article",
    actionUrl:
      "https://news.microsoft.com/source/features/innovation/datacenter-liquid-cooling/",
    sourceLabel: "Microsoft / Gene Twedt",
    sourceUrl:
      "https://news.microsoft.com/source/features/innovation/datacenter-liquid-cooling/",
  },
];
