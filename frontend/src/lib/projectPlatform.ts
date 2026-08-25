import type { GalleryItem } from "./api";

/**
 * Working screens and site photography for research projects that have a
 * software side.
 *
 * These sit in the repository rather than the CMS on purpose. The body gallery
 * renders its pictures through a `fill-1200x800` rendition, which is a hard 3:2
 * crop at 1200px wide -- right for a photograph of people in a workshop, wrong
 * for a dashboard, where that crop clips the chrome and the downscale turns a
 * column of readings into grey texture. These are served at their own size and
 * aspect instead.
 *
 * The set is deliberately curated, and two of the supplied screenshots are not
 * in it. FarmOS reports itself offline between deployments, and the dashboard
 * captured during one such gap shows a grey "sensor data is not being received"
 * banner over five zeroed tiles -- a true picture of one moment and a false
 * picture of the project. The historical browser, which carries a week of
 * readings and every logged spray event, says the same thing accurately. The
 * sign-in screen is also out: its photograph is the one already serving as the
 * project's hero, and the half beside it is an empty login form.
 *
 * The link goes to that login form -- the site redirects the root straight to
 * `/login`, and there is no public view behind it. That is worth linking
 * anyway, because a real address is part of what makes the work checkable, but
 * the caption has to say so plainly rather than invite a reader to click
 * through to a wall.
 */

const farmos = (name: string) => `/assets/research/farmos/${name}.webp`;

const image = (name: string, caption: string, alt: string): GalleryItem => ({
  kind: "image",
  url: farmos(name),
  file_url: null,
  thumb: null,
  caption,
  alt_text: alt,
});

type PlatformSet = {
  heading: string;
  caption: string;
  /** The live platform. Overridden by the project's CMS `platform_url`. */
  url: string;
  label: string;
  items: GalleryItem[];
};

const platformSets: Record<string, PlatformSet> = {
  "automated-cooling-spraying-system": {
    heading: "FarmOS, the software that runs it",
    caption:
      "Building the equipment was half the work. The team also wrote the web " +
      "platform that operates it: live readings, direct control of each relay, " +
      "and a record of everything the system has done. It runs behind a " +
      "sign-in for the farms using it, so the screens here are the tour.",
    url: "https://farmos-mechanicalengineering.com/",
    label: "Visit FarmOS",
    items: [
      image(
        "platform-control",
        "Controller HMI",
        "The FarmOS control screen, showing the spraying system, cooling tank, " +
          "spray pump and control cabinet as a schematic, each with an " +
          "indicator lamp for the state of its relay.",
      ),
      image(
        "platform-data",
        "Seven days of readings",
        "The historical browser over a seven-day range, plotting temperature " +
          "and humidity, listing each logged spray event with its start, end " +
          "and duration, and totalling the estimated water used.",
      ),
      image(
        "platform-analytics",
        "Temperature and humidity statistics",
        "The analytics screen, reporting average, maximum, minimum and " +
          "standard deviation for temperature and humidity over the selected " +
          "period, above a trend chart for the last 24 hours.",
      ),
      image(
        "platform-design",
        "The CAD model it was built from",
        "Eight CAD renders of the design: the complete farm layout, a close-up " +
          "of the system, the solar power connection and tracker, the cooling " +
          "and spraying architecture, the main control box, the weather and " +
          "soil sensor station, and an overhead misting nozzle.",
      ),
      image(
        "platform-home",
        "Farm home screen",
        "The FarmOS home screen for the farm, with links to each part of the " +
          "platform, the current temperature and humidity, local weather, and " +
          "a photograph of the plantation under its misting lines.",
      ),
    ],
  },
};

/** The platform set for a project, or null when it has no software side. */
export function getProjectPlatform(slug: string): PlatformSet | null {
  return platformSets[slug] ?? null;
}
