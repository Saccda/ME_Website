/* eslint-disable @next/next/no-img-element */
import type { ReactNode } from "react";
import {
  CdioRing,
  PlantLine,
  SystemCore,
  VehicleSystems,
  type AreaAccents,
} from "@/components/flipbook/diagrams";
import { Icon, type IconName } from "@/components/flipbook/icons";
import type {
  Facility,
  FocusArea,
  NewsEvent,
  Partner,
  ResearchProject,
} from "@/lib/api";

/**
 * The pages of the ME program brochure.
 *
 * Content only. The flipbook engine renders whatever this module describes and
 * knows nothing about mechanical engineering, so the copy and the pictures can
 * be rewritten, reordered or replaced without touching the page-turn mechanism.
 * The page count is whatever this array's length is; nothing downstream assumes
 * a number.
 *
 * PAIRING MATTERS. Two faces to a physical sheet, so page 2 faces page 3, page
 * 4 faces page 5, and so on. A chapter written as a spread has to start on an
 * even page or it will be split across a turn. The four student-facing chapters
 * -- AI, why the discipline, CDIO, automotive -- each occupy one spread.
 *
 * PICTURES COME FROM THE CMS. Every photograph here is one the program uploaded
 * -- its own laboratories, its own equipment, its own activities, its own
 * research, its own partners' marks. The brochure is read as a document about
 * this laboratory, so stock photography of somebody else's workshop has no
 * business in it. The local editorial files stay wired in behind each one, and
 * only appear if the CMS is unreachable, which is what keeps the page from
 * collapsing during an outage.
 *
 * WHERE A DRAWING IS HONEST AND A PHOTOGRAPH IS NOT, the page carries a drawing:
 * there is no photograph of an engineering workflow, of four disciplines meeting
 * in one machine, or of the parts of a car each area of focus touches.
 *
 * Every fact is likewise already published on this site: the vision and mission
 * verbatim from ProgramSettings, the focus areas, the first-year theme and
 * credit count, the course-code families, the equipment names, the research
 * summaries and the quadruple-helix copy.
 *
 * Deliberately absent: the Program Educational Objectives and Program Learning
 * Outcomes, which the About page still marks as "will be published here". A
 * brochure is the wrong place to guess.
 */

export type BrochurePage = {
  /** Stable identity: React key, print order key, contents key. */
  id: string;
  /** Small uppercase label in the running head. */
  chapter: string;
  /** Contents-panel entry. */
  title: string;
  subtitle: string;
  /**
   * What the page's graphic says, in words. Read to screen readers in place of
   * the diagram, and matched by the contents search.
   */
  description: string;
  /** Further words the search should match, beyond the visible titles. */
  keywords: string;
  /** `cover` and `back` drop the running head and foot. */
  tone: "cover" | "paper" | "dark" | "back";
  body: ReactNode;
};

export type BrochureSources = {
  focusAreas: FocusArea[];
  research: ResearchProject[];
  facilities: Facility[];
  news: NewsEvent[];
  partners: Partner[];
};

const editorial = (name: string) => `/assets/editorial/${name}.webp`;
const farmos = (name: string) => `/assets/research/farmos/${name}.webp`;

/** A CMS picture when there is one, the repository copy when there is not. */
const pick = (cms: string | null | undefined, fallback: string) => cms || fallback;

const AREA_ORDER = ["DMP", "TES", "MAS", "ECM"] as const;
const AREA_FALLBACK: Record<string, string> = {
  DMP: editorial("focus-dmp-hero"),
  TES: editorial("focus-tes-hero"),
  MAS: editorial("focus-mas-hero"),
  ECM: editorial("focus-ecm-hero"),
};
/** Only used if the CMS is unreachable; these are the published accents. */
const ACCENT_FALLBACK: Record<string, string> = {
  DMP: "#061b2b",
  TES: "#e6ad38",
  MAS: "#1667b1",
  ECM: "#3e8b56",
};

/**
 * Mixes an accent toward white.
 *
 * DMP's published accent is very nearly black, which is right on a white page
 * and invisible on the navy ones. A diagram that colour-codes four areas has to
 * keep all four legible on both grounds, so the dark pages take a lightened set
 * -- same hues, raised until they read.
 */
function towardWhite(hex: string, amount: number) {
  const clean = hex.replace("#", "");
  if (!/^[0-9a-f]{6}$/i.test(clean)) return hex;
  const channels = [0, 2, 4].map((offset) => {
    const value = parseInt(clean.slice(offset, offset + 2), 16);
    return Math.round(value + (255 - value) * amount);
  });
  return `#${channels.map((c) => c.toString(16).padStart(2, "0")).join("")}`;
}

export function buildBrochurePages(src: BrochureSources): BrochurePage[] {
  const areas = AREA_ORDER.map((code) => {
    const area = src.focusAreas.find((a) => a.code === code);
    return {
      code,
      title: area?.title ?? code,
      image: pick(area?.image, AREA_FALLBACK[code]),
      accent: area?.accent_color || ACCENT_FALLBACK[code],
    };
  });

  const accentOf = (code: string) =>
    areas.find((a) => a.code === code)?.accent ?? ACCENT_FALLBACK[code];

  const accents: AreaAccents = {
    DMP: accentOf("DMP"),
    TES: accentOf("TES"),
    MAS: accentOf("MAS"),
    ECM: accentOf("ECM"),
  };
  const onDark: AreaAccents = {
    DMP: towardWhite(accents.DMP, 0.62),
    TES: towardWhite(accents.TES, 0.15),
    MAS: towardWhite(accents.MAS, 0.4),
    ECM: towardWhite(accents.ECM, 0.32),
  };

  const newsImage = (slug: string, fallback: string) => {
    const item = src.news.find((n) => n.slug === slug);
    return pick(item?.image_wide || item?.image, fallback);
  };

  const project = (match: string, fallback: string) => {
    const found = src.research.find((r) =>
      r.title.toLowerCase().includes(match),
    );
    return { item: found, image: pick(found?.image, fallback) };
  };

  // One machine from each area first, then whatever else there is, so the
  // equipment page spans the program rather than showing six lathes.
  const equipment = (() => {
    const chosen: Facility[] = [];
    for (const code of AREA_ORDER) {
      const hit = src.facilities.find(
        (f) => !chosen.includes(f) && f.focus_areas.some((a) => a.code === code),
      );
      if (hit) chosen.push(hit);
    }
    for (const f of src.facilities) {
      if (chosen.length >= 6) break;
      if (!chosen.includes(f)) chosen.push(f);
    }
    return chosen.slice(0, 6);
  })();

  const cooling = project("cooling", editorial("research-automated-cooling"));
  const board = project("particle board", editorial("research-particle-board"));
  const load = project("load monitoring", editorial("research-load-monitoring"));
  const metal = project("metal recycling", editorial("research-metal-recycling"));

  const partners = src.partners.filter((p) => p.logo).slice(0, 8);

  return [
    // 1 ───────────────────────────────────────────────────────── cover ──
    {
      id: "cover",
      chapter: "Cover",
      title: "Mechanical Engineering",
      subtitle: "Royal University of Phnom Penh",
      description:
        "Front cover: Mechanical Engineering at the Royal University of Phnom Penh, a four-year engineering degree covering design, energy, automation and responsible practice.",
      keywords: "brochure front cover RUPP faculty of engineering",
      tone: "cover",
      body: (
        <>
          <img
            alt=""
            className="fb-bleed"
            src={newsImage(
              "mechanical-engineering-laboratory-open-house",
              editorial("home-robot-vision"),
            )}
          />
          <span className="fb-veil" />
          <span className="fb-cover-grid" />
          <div className="fb-cover-mark">
            <span>ME</span>
            <p>
              ROYAL UNIVERSITY OF PHNOM PENH
              <br />
              FACULTY OF ENGINEERING
            </p>
          </div>
          <div className="fb-cover-copy">
            <p>PROGRAM BROCHURE</p>
            <h1>
              Mechanical
              <br />
              <em>Engineering</em>
            </h1>
            <span className="fb-cover-rule" />
            <h2>
              Design, energy, automation and responsible practice — a four-year
              engineering degree in Phnom Penh.
            </h2>
          </div>
          <div className="fb-cover-areas">
            {areas.map((a) => (
              <div key={a.code}>
                <b>{a.code}</b>
              </div>
            ))}
          </div>
          <p className="fb-cover-note">me-rupp.vercel.app</p>
        </>
      ),
    },

    // 2 ──────────────────────────────────────────────────────── vision ──
    {
      id: "vision",
      chapter: "01 · The program",
      title: "What we are for",
      subtitle: "Vision",
      description:
        "The program's vision, quoted in full: to become a leader in mechanical engineering education by infusing technology and social engagement into teaching, research and innovation.",
      keywords: "vision purpose mission statement leadership society",
      tone: "paper",
      body: (
        <>
          <figure className="fb-figure">
            <img
              alt=""
              src={newsImage(
                "sharing-the-cooling-and-spraying-system-with-communities",
                editorial("home-material-testing"),
              )}
            />
          </figure>
          <p className="fb-eyebrow">OUR VISION</p>
          <h2>Engineering education that serves the country it is in</h2>
          <blockquote className="fb-quote">
            To become a leader in Mechanical Engineering Education by infusing
            technology and social engagement into teaching and learning,
            research, and innovation for the advancement of society.
          </blockquote>
        </>
      ),
    },

    // 3 ─────────────────────────────────────────────────────── mission ──
    {
      id: "mission",
      chapter: "01 · The program",
      title: "How we deliver it",
      subtitle: "Mission",
      description:
        "Two commitments: a modern mechanical engineering education with social engagement and technology, and collaboration with university partners on research and innovation.",
      keywords: "mission teaching research collaboration commitments",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">OUR MISSION</p>
          <h2>Two commitments</h2>
          <div className="fb-duo">
            <section>
              <img
                alt=""
                src={newsImage(
                  "strengthening-practical-manufacturing-skills-with-vp-start",
                  editorial("ecm-project-workspace"),
                )}
              />
              <div>
                <span>01 · TEACHING</span>
                <p>
                  To provide a modern mechanical engineering education by
                  infusing social engagement and technology into educational
                  activity for an effective educational program.
                </p>
              </div>
            </section>
            <section>
              <img
                alt=""
                src={newsImage(
                  "me-team-leads-the-first-lex-program",
                  editorial("mas-robot-vision"),
                )}
              />
              <div>
                <span>02 · RESEARCH</span>
                <p>
                  To collaborate with university partners on mechanical
                  engineering to enforce proactive research activities that lead
                  to an advancement of research and innovation.
                </p>
              </div>
            </section>
          </div>
        </>
      ),
    },

    // 4 ────────────────────────────────────────── AI, left of spread ──
    {
      id: "ai-workflow",
      chapter: "02 · Engineering and AI",
      title: "Engineering in the age of AI",
      subtitle: "Where AI sits in the work",
      description:
        "An engineering workflow, top to bottom: a real-world need, then physics and engineering knowledge, then mechanical design, then AI-assisted analysis and optimisation, then build, test and verify, ending in a safe physical system. The engineer owns every stage; AI assists at one of them.",
      keywords:
        "artificial intelligence AI relevant future machine learning workflow physics forces motion materials heat fluid energy manufacturing sensors safety reliability",
      tone: "dark",
      body: (
        <>
          <p className="fb-eyebrow fb-gold">CHAPTER 02 · A QUESTION WORTH ASKING</p>
          <h2>
            Is mechanical engineering still relevant in the age of AI?
          </h2>
          <p className="fb-answer">
            Yes. AI strengthens mechanical engineering. It does not remove the
            need to understand physical systems.
          </p>
          <ol className="fb-pipeline">
            {[
              {
                id: "need",
                t: "Real-world need",
                d: "A farm loses fruit to heat.",
                who: "Engineer",
              },
              {
                id: "physics",
                t: "Physics and engineering knowledge",
                d: "Forces, materials, heat, fluids, energy.",
                who: "Engineer",
              },
              {
                id: "design",
                t: "Mechanical design",
                d: "Sizes, materials, mechanisms, safety margins.",
                who: "Engineer",
              },
              {
                id: "ai",
                t: "AI-assisted analysis and optimisation",
                d: "Compares options, finds patterns, predicts failures.",
                who: "AI assists",
                ai: true,
              },
              {
                id: "build",
                t: "Build, test and verify",
                d: "Prototype, measure, prove it behaves as designed.",
                who: "Engineer",
              },
              {
                id: "safe",
                t: "Safe physical system",
                d: "A machine people can depend on.",
                who: "Engineer",
              },
            ].map((step, i) => (
              <li className={step.ai ? "is-ai" : ""} key={step.id}>
                <span>{String(i + 1).padStart(2, "0")}</span>
                <div>
                  <b>{step.t}</b>
                  <p>{step.d}</p>
                </div>
                <em>{step.who}</em>
              </li>
            ))}
          </ol>
        </>
      ),
    },

    // 5 ─────────────────────────────────────── AI, right of spread ──
    {
      id: "ai-applications",
      chapter: "02 · Engineering and AI",
      title: "Where AI helps, and engineering decides",
      subtitle: "Six meeting points",
      description:
        "Six places AI and mechanical engineering meet: design and manufacturing, intelligent machines, robotics and automation, energy and sustainability, materials and physical systems, and problem-solving. In each, AI analyses and suggests while the engineer defines the problem, applies physical principles and verifies the result. Mechanical engineering knowledge plus AI and digital tools equals better engineering decisions.",
      keywords:
        "artificial intelligence AI applications robotics automation energy sustainability materials innovation optimisation prediction digital tools judgement",
      tone: "dark",
      body: (
        <>
          <p className="fb-eyebrow fb-gold">WHERE THE TWO MEET</p>
          <h2>AI analyses. Engineers decide.</h2>
          <div className="fb-apps">
            {(
              [
                [
                  "factory",
                  "Design and manufacturing",
                  "AI compares designs. Engineers choose materials, dimensions, methods and limits.",
                ],
                [
                  "cpu",
                  "Intelligent machines",
                  "Engineers join structures, motors, sensors and controllers to AI decision systems.",
                ],
                [
                  "bot",
                  "Robotics and automation",
                  "AI perceives and plans. Mechanics make the robot move, carry and stop safely.",
                ],
                [
                  "leaf",
                  "Energy and sustainability",
                  "AI predicts demand. Engineers design solar, cooling, storage and thermal systems.",
                ],
                [
                  "flask",
                  "Materials and physical systems",
                  "AI finds patterns. Engineers judge stress, temperature, vibration and failure.",
                ],
                [
                  "compass",
                  "Innovation and problem-solving",
                  "AI offers alternatives. Engineers test, verify and carry the responsibility.",
                ],
              ] as [IconName, string, string][]
            ).map(([icon, title, note]) => (
              <section key={title}>
                <Icon name={icon} />
                <b>{title}</b>
                <p>{note}</p>
              </section>
            ))}
          </div>
          <div className="fb-equation">
            <span>Mechanical engineering knowledge</span>
            <i aria-hidden="true">+</i>
            <span>AI and digital tools</span>
            <i aria-hidden="true">=</i>
            <strong>Better engineering decisions</strong>
          </div>
          <p className="fb-note">
            Engineers who understand both physical systems and modern digital
            tools are better prepared to develop the next generation of
            machines, energy systems and automated technologies.
          </p>
        </>
      ),
    },

    // 6 ───────────────────────────────── why ME, left of spread ──
    {
      id: "why-system",
      chapter: "03 · Why this discipline",
      title: "Why study mechanical engineering?",
      subtitle: "Four areas, one system",
      description:
        "One machine drawn with all four areas of focus at work in it: the steel frame and tank are design and manufacturing, the pump, pipework and spray are thermofluid and energy, the sensor and controller are mechatronics and automation, and the safety and maintenance check is engineering compliance and management.",
      keywords:
        "why study choose mechanical engineering areas of focus DMP TES MAS ECM design manufacturing thermofluid energy mechatronic automation compliance management",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">CHAPTER 03 · WHY THIS DISCIPLINE</p>
          <h2>Four areas of focus, meeting in one machine</h2>
          <figure className="fb-diagram">
            <SystemCore accents={accents} />
            <figcaption>
              The program&rsquo;s own cooling and spraying rig. No part of it
              belongs to a single area.
            </figcaption>
          </figure>
          <div className="fb-areas-row">
            {areas.map((a) => (
              <section key={a.code} style={{ ["--fb-accent" as string]: a.accent }}>
                <img alt="" src={a.image} />
                <b>{a.code}</b>
                <p>{a.title}</p>
              </section>
            ))}
          </div>
        </>
      ),
    },

    // 7 ──────────────────────────────── why ME, right of spread ──
    {
      id: "why-areas",
      chapter: "03 · Why this discipline",
      title: "What each area teaches",
      subtitle: "Four ways of working",
      description:
        "Each area of focus as a working sequence. Design and manufacturing: idea, CAD model, prototype, manufacture, test. Thermofluid and energy: source, conversion, heat and fluid flow, useful output. Mechatronics and automation: sense, decide, act, verify. Compliance and management: requirement, plan, implement, inspect, improve. Together they make one complete engineering system.",
      keywords:
        "CAD prototype manufacture test energy conversion cooling sensors actuators controllers standards quality safety project planning Cambodia motorcycle appliances irrigation",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">WHAT EACH AREA TEACHES</p>
          <h2>Four ways of working on the same machine</h2>
          <div className="fb-paths">
            {[
              {
                code: "DMP",
                steps: ["Idea", "CAD model", "Prototype", "Manufacture", "Test"],
                note: "Motorcycle parts, appliances and tools — and the local factories that make them.",
              },
              {
                code: "TES",
                steps: ["Energy source", "Conversion", "Heat and flow", "Useful output"],
                note: "Air conditioning, refrigeration, pumps and solar — cooling farms and buildings.",
              },
              {
                code: "MAS",
                steps: ["Sense", "Decide", "Act", "Verify"],
                note: "Automatic doors, lifts, robot arms and smart irrigation — automation at work.",
              },
              {
                code: "ECM",
                steps: ["Requirement", "Plan", "Implement", "Inspect", "Improve"],
                note: "Safety checks, quality control, maintenance and planning people can trust.",
              },
            ].map((path) => (
              <section
                key={path.code}
                style={{ ["--fb-accent" as string]: accentOf(path.code) }}
              >
                <b>{path.code}</b>
                <ol className="fb-chips">
                  {path.steps.map((step) => (
                    <li key={step}>{step}</li>
                  ))}
                </ol>
                <p>{path.note}</p>
              </section>
            ))}
          </div>
          <div className="fb-sum">
            <span>Design</span>
            <i aria-hidden="true">+</i>
            <span>Energy</span>
            <i aria-hidden="true">+</i>
            <span>Automation</span>
            <i aria-hidden="true">+</i>
            <span>Responsible management</span>
            <b>One complete engineering system</b>
          </div>
          <p className="fb-lead">
            The four areas connect rather than compete. A real project may use
            two, three or all four of them at once.
          </p>
        </>
      ),
    },

    // 8 ───────────────────────────────────────────────── curriculum ──
    {
      id: "curriculum",
      chapter: "04 · Curriculum",
      title: "The four-year path",
      subtitle: "Eight semesters, nine subject families",
      description:
        "Four years and eight semesters: a 36-credit foundation year of mathematics, engineering intuition and workshop skills, then applied engineering science, industry experience and professional practice. Four of the nine course-code families are the areas of focus themselves.",
      keywords:
        "curriculum four years eight semesters credits courses subjects BME PEE EMS LAC PAE foundation year",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">CURRICULUM</p>
          <h2>Four years, eight semesters</h2>
          <div className="fb-stack">
            <section>
              <span className="fb-stack-year">YEAR 1</span>
              <div>
                <b>Foundations &amp; discovery</b>
                <p>
                  Mathematical confidence, engineering intuition and essential
                  workshop skills.
                </p>
              </div>
              <strong>36</strong>
            </section>
            <section className="fb-stack-rest">
              <span className="fb-stack-year">YEARS 2–4</span>
              <div>
                <b>Toward integrated design and professional practice</b>
                <p>
                  Applied engineering science, industry experience and
                  professional practice.
                </p>
              </div>
              <strong>→</strong>
            </section>
          </div>
          <p className="fb-lead">
            Four of the nine course-code families are the areas of focus
            themselves — a student meets them as classes with credits, not as
            headings in a prospectus.
          </p>
          <div className="fb-families">
            {[
              { code: "DMP", label: "Design & manufacturing", focus: true },
              { code: "TES", label: "Thermofluid & energy", focus: true },
              { code: "MAS", label: "Mechatronics & automation", focus: true },
              { code: "ECM", label: "Compliance & management", focus: true },
              { code: "BME", label: "Basic mechanical engineering" },
              { code: "PEE", label: "Physics & electrical" },
              { code: "EMS", label: "Engineering mathematics" },
              { code: "LAC", label: "Language & communication" },
              { code: "PAE", label: "Professional & applied" },
            ].map((f) => (
              <span className={f.focus ? "is-focus" : ""} key={f.code}>
                <b>{f.code}</b>
                {f.label}
              </span>
            ))}
          </div>
        </>
      ),
    },

    // 9 ──────────────────────────────────────────────── laboratories ──
    {
      id: "laboratories",
      chapter: "04 · Laboratories",
      title: "What you will work on",
      subtitle: "Equipment across the four areas",
      description:
        "Six machines from the program's own catalogue, each named and marked with the focus area it belongs to.",
      keywords: "laboratory equipment machines workshop CNC facilities catalogue",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">LABORATORIES</p>
          <h2>Real machines, named and available</h2>
          <div className="fb-kit">
            {equipment.map((f) => (
              <figure key={f.id}>
                <img alt="" src={f.image ?? editorial("dmp-cnc")} />
                <figcaption>
                  <b>{f.name}</b>
                  <span>{f.focus_areas.map((a) => a.code).join(" · ")}</span>
                </figcaption>
              </figure>
            ))}
          </div>
          <div className="fb-strip">
            <Icon name="gear" />
            <p>
              The full equipment catalogue — machine by machine, with the focus
              area each belongs to and whether it is available — is published on
              the facilities page.
            </p>
          </div>
        </>
      ),
    },

    // 10 ─────────────────────────────────── CDIO, left of spread ──
    {
      id: "cdio-cycle",
      chapter: "05 · How you learn",
      title: "Learn engineering by doing",
      subtitle: "The CDIO cycle",
      description:
        "CDIO drawn as a closed loop: conceive the need, design the solution, implement and test it, operate and improve it — and what is learned in operation begins the next conception. Project work builds problem identification, analysis, practical skill, evidence-based decisions, teamwork, project management, systems thinking and reflection.",
      keywords:
        "CDIO conceive design implement operate learning by doing framework skills teamwork project management practical",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">CHAPTER 05 · HOW YOU LEARN</p>
          <h2>Learn engineering by doing</h2>
          <div className="fb-cycle">
            <CdioRing />
            <ol>
              {[
                ["Conceive", "Understand the need and shape an idea."],
                ["Design", "Calculate, model and plan the solution."],
                ["Implement", "Build, program, assemble and test it."],
                ["Operate", "Run it, maintain it, improve it."],
              ].map(([stage, note]) => (
                <li key={stage}>
                  <b>{stage}</b>
                  <p>{note}</p>
                </li>
              ))}
            </ol>
          </div>
          <div className="fb-skills">
            {[
              ["Investigating a need", "Problem identification"],
              ["Designing a solution", "Analysis and creativity"],
              ["Building a prototype", "Practical technical skill"],
              ["Testing performance", "Evidence-based decisions"],
              ["Working in a team", "Collaboration"],
              ["Planning the work", "Project management"],
              ["Operating the system", "Systems thinking"],
              ["Improving the design", "Reflection and innovation"],
            ].map(([activity, gain]) => (
              <section key={activity}>
                <span>{activity}</span>
                <b>{gain}</b>
              </section>
            ))}
          </div>
          <p className="fb-lead">
            CDIO is an engineering-education framework used internationally. It
            lets students show what they can design, build, test and improve —
            not only what they can remember for an examination.
          </p>
        </>
      ),
    },

    // 11 ────────────────────────────────── CDIO, right of spread ──
    {
      id: "cdio-project",
      chapter: "05 · How you learn",
      title: "One project, all four stages",
      subtitle: "Cooling and spraying, in Kampot",
      description:
        "The cooling and spraying system as a CDIO project: site visits to establish the need, a design joining storage, filtration, cooling, pumping and spraying, installation and connection on the farm, and operation with maintenance and community engagement after handover. What operation teaches begins the next conception.",
      keywords:
        "project example farm Kampot cooling spraying FarmOS conceive design implement operate maintenance handover",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">CDIO IN PRACTICE</p>
          <h2>Built here, installed on a farm, and still running</h2>
          <div className="fb-case">
            <figure>
              <img alt="" src={farmos("platform-control")} />
              <figcaption>
                The control screen: spraying system, cooling tank and pump, each
                relay live on the diagram.
              </figcaption>
            </figure>
            <figure>
              <img alt="" src={farmos("platform-data")} />
              <figcaption>
                A week of readings, with every spray event logged and the water
                used totalled.
              </figcaption>
            </figure>
          </div>
          <div className="fb-flow">
            {[
              ["01", "Conceive", "Site visits with partners to establish the real requirements."],
              ["02", "Design", "Water storage, filtration, cooling, pumping and spraying as one system."],
              ["03", "Implement", "Installed on site; mechanical, electrical and control components connected."],
              ["04", "Operate", "Operation, maintenance and community engagement continue after handover."],
            ].map(([n, t, d]) => (
              <section key={n}>
                <span>{n}</span>
                <b>{t}</b>
                <p>{d}</p>
              </section>
            ))}
          </div>
          <p className="fb-loop">
            <span aria-hidden="true">↺</span>
            What operating the system teaches is where the next conception
            starts.
          </p>
          <p className="fb-lead">
            Theory gives students the foundation. CDIO projects give them the
            chance to apply it to real engineering problems.
          </p>
        </>
      ),
    },

    // 12 ──────────────────────────────────────────────────── research ──
    {
      id: "research",
      chapter: "06 · Research",
      title: "What we are building",
      subtitle: "Four active projects",
      description:
        "Four active projects: automated cooling and spraying, composite particle board from agricultural and plastic waste, non-intrusive load monitoring, and metal recycling.",
      keywords:
        "research projects cooling spraying particle board bagasse load monitoring metal recycling sustainable",
      tone: "dark",
      body: (
        <>
          <p className="fb-eyebrow fb-gold">RESEARCH</p>
          <h2>Work under way in the laboratory and in the field</h2>
          <div className="fb-projects">
            {[
              { key: "cooling", a: "MAS", ...cooling, t: "Automated Cooling & Spraying System", d: "Sensor-based cooling and spraying controls for more consistent, efficient environmental management." },
              { key: "board", a: "DMP", ...board, t: "Composite Particle Board", d: "Sugarcane bagasse, coconut shell and small waste plastics as raw materials for lower-impact particle board." },
              { key: "load", a: "TES", ...load, t: "Non-Intrusive Load Monitoring", d: "Electrical measurement and analysis to identify appliance-level energy use without individual sensors." },
              { key: "metal", a: "DMP", ...metal, t: "Metal Recycling", d: "Practical processes for recovering, sorting and reusing metal to support sustainable manufacturing." },
            ].map((p) => (
              <section key={p.key}>
                <img alt="" src={p.image} />
                <div>
                  <span>{p.a}</span>
                  <b>{p.item?.title ?? p.t}</b>
                  <p>{p.d}</p>
                </div>
              </section>
            ))}
          </div>
        </>
      ),
    },

    // 13 ─────────────────────────────────────────────── collaboration ──
    {
      id: "collaboration",
      chapter: "06 · Collaboration",
      title: "Who we work with",
      subtitle: "The quadruple helix",
      description:
        "The quadruple helix: academia brings knowledge, industry application, government policy and society purpose, each accountable to the others.",
      keywords:
        "collaboration partners quadruple helix academia industry government society partnership",
      tone: "dark",
      body: (
        <>
          <p className="fb-eyebrow fb-gold">COLLABORATION</p>
          <h2>No single institution improves engineering practice on its own</h2>
          <div className="fb-strands">
            {[
              ["Academic", "Knowledge"],
              ["Industry", "Application"],
              ["Government", "Policy"],
              ["Society", "Purpose"],
            ].map(([t, s]) => (
              <section key={t}>
                <b>{t}</b>
                <span>{s}</span>
              </section>
            ))}
          </div>
          <p className="fb-note">
            The quadruple helix puts academia, industry, government and society
            in the same system, each shaping what engineering is for and each
            accountable to the others.
          </p>
          {partners.length > 0 ? (
            <div className="fb-logos">
              {partners.map((p) => (
                <span key={p.name}>
                  <img alt={p.name} src={p.logo ?? ""} />
                </span>
              ))}
            </div>
          ) : null}
        </>
      ),
    },

    // 14 ─────────────────────────── automotive, left of spread ──
    {
      id: "automotive-systems",
      chapter: "07 · Careers",
      title: "Mechanical engineering in a vehicle",
      subtitle: "Can ME graduates work in automotive?",
      description:
        "A car in section and the line that builds it, with each area of focus joined to the part it touches: design and manufacturing to the body, panels and tooling; thermofluid and energy to cooling, air conditioning and battery heat; mechatronics to sensors, motor control and the robot cell; compliance and management to safety, standards and inspection. Electric vehicles still need structures, materials, cooling, energy, manufacturing and safety.",
      keywords:
        "automotive vehicle car industry EV electric battery engine assembly plant factory robots inspection careers",
      tone: "dark",
      body: (
        <>
          <p className="fb-eyebrow fb-gold">CHAPTER 07 · CAREERS</p>
          <h2>Can ME @ RUPP graduates work in the automotive industry?</h2>
          <p className="fb-answer">
            Yes. Automotive is an industry, not a career reserved for one degree
            title.
          </p>
          <figure className="fb-auto">
            <VehicleSystems accents={onDark} />
            <PlantLine accents={onDark} />
            <figcaption>
              A vehicle, and the plant that builds it, need all four areas at
              once.
            </figcaption>
          </figure>
          <div className="fb-legend">
            {[
              ["DMP", "Body, panels, tooling, component manufacture"],
              ["TES", "Cooling, lubrication, air conditioning, battery heat"],
              ["MAS", "Sensors, motor control, robots, automated inspection"],
              ["ECM", "Safety, standards, quality, maintenance, production"],
            ].map(([code, note]) => (
              <span
                key={code}
                style={{ ["--fb-accent" as string]: onDark[code as "DMP"] }}
              >
                <b>{code}</b>
                {note}
              </span>
            ))}
          </div>
          <p className="fb-note">
            Electric vehicles still need mechanical engineering: structures,
            materials, cooling, energy, manufacturing, safety.
          </p>
        </>
      ),
    },

    // 15 ────────────────────────── automotive, right of spread ──
    {
      id: "automotive-routes",
      chapter: "07 · Careers",
      title: "Routes into the industry",
      subtitle: "Roles, and an honest comparison",
      description:
        "Routes into automotive work: a mechanical engineering foundation leads through design, manufacturing, energy, automation and quality into components, assembly, testing and plant systems, in roles from design and process engineer to automation, quality and maintenance engineer. A specialised automotive programme offers one direct route; mechanical engineering offers several into the same industry. Compare the actual curriculum, laboratories, projects and internships rather than the programme title.",
      keywords:
        "career pathways roles design product manufacturing process automation PLC quality compliance maintenance plant thermal production project engineer comparison specialised automotive degree Cambodia roadmap",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">ROUTES INTO THE INDUSTRY</p>
          <h2>More than one way in</h2>
          <ol className="fb-route">
            <li>
              <span>Foundation</span>
              <b>Mechanical engineering</b>
            </li>
            <li>
              <span>Strengths</span>
              <b>Design · Manufacturing · Energy · Automation · Quality</b>
            </li>
            <li>
              <span>Where the work is</span>
              <b>Components · Assembly · Testing · Plant systems</b>
            </li>
          </ol>
          <ul className="fb-roles">
            {[
              "Design engineer",
              "Product engineer",
              "Manufacturing engineer",
              "Process engineer",
              "Automation / PLC engineer",
              "Quality / compliance engineer",
              "Maintenance / plant engineer",
              "Thermal / energy systems engineer",
              "Production / project engineer",
            ].map((role) => (
              <li key={role}>{role}</li>
            ))}
          </ul>
          <p className="fb-lead">
            The job title may not contain the word &ldquo;automotive&rdquo;. A
            process, automation or quality engineer in a vehicle or component
            factory is still building a career in the industry.
          </p>
          <div className="fb-compare">
            <section>
              <b>Mechanical engineering @ RUPP</b>
              <ul>
                <li>Broad mechanical foundation</li>
                <li>Several routes into automotive</li>
                <li>Flexibility across manufacturing, energy and automation</li>
                <li>Direction built through projects and internships</li>
              </ul>
            </section>
            <section>
              <b>Specialised automotive programme</b>
              <ul>
                <li>Earlier concentration on vehicle systems</li>
                <li>One direct vehicle-centred route</li>
                <li>More automotive-specific coursework</li>
                <li>Greater early specialisation</li>
              </ul>
            </section>
          </div>
          <p className="fb-guide">
            Compare the actual curriculum, laboratories, projects and
            internships — not the programme title.
          </p>
          <p className="fb-source">
            Cambodia is developing its automotive and electronics sectors:
            component production, assembly, automation and quality systems.{" "}
            <a
              href="https://cdc.gov.kh/wp-content/uploads/2023/04/ENG_Auto__Electronics_Roadmap.pdf"
              rel="noopener noreferrer"
              target="_blank"
            >
              CDC Automotive &amp; Electronics Roadmap
            </a>
          </p>
        </>
      ),
    },

    // 16 ─────────────────────────────────────────────── back cover ──
    {
      id: "contact",
      chapter: "Contact",
      title: "Talk to the program",
      subtitle: "Faculty of Engineering, RUPP",
      description:
        "Back cover: everything in this brochure is published in full on the program website, with the address of the Faculty of Engineering at the Royal University of Phnom Penh.",
      keywords: "contact address admissions website back cover Phnom Penh",
      tone: "back",
      body: (
        <>
          <img
            alt=""
            className="fb-bleed"
            src={newsImage(
              "staff-training-on-cnc-milling-machine",
              editorial("home-cnc-machine"),
            )}
          />
          <span className="fb-veil" />
          <span className="fb-cover-grid" />
          <div className="fb-back-copy">
            <p className="fb-eyebrow fb-gold">FIND OUT MORE</p>
            <h2>
              Everything in this brochure is published in full on the program
              website.
            </h2>
            <div className="fb-back-links">
              {[
                ["Areas of focus, curriculum and facilities", "me-rupp.vercel.app"],
                ["Research projects and collaboration", "me-rupp.vercel.app/research"],
                ["Admissions and application forms", "me-rupp.vercel.app/admissions"],
              ].map(([label, href]) => (
                <span key={href}>
                  <b>{label}</b>
                  {href}
                </span>
              ))}
            </div>
            <div className="fb-back-address">
              <b>Mechanical Engineering · Faculty of Engineering</b>
              <p>
                Royal University of Phnom Penh, Russian Federation Boulevard
                (110), Phnom Penh, Cambodia
              </p>
            </div>
          </div>
          <p className="fb-cover-note">Nature · Nurture · Nourish</p>
        </>
      ),
    },
  ];
}
