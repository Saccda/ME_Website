/* eslint-disable @next/next/no-img-element */
import type { ReactNode } from "react";
import { Icon } from "@/components/flipbook/icons";
import type {
  Facility,
  FocusArea,
  NewsEvent,
  Partner,
  ResearchProject,
} from "@/lib/api";

/**
 * The twelve pages of the ME program brochure.
 *
 * Content only. The flipbook engine renders whatever this module describes and
 * knows nothing about mechanical engineering, so the copy and the pictures can
 * be rewritten, reordered or replaced without touching the page-turn mechanism.
 *
 * PICTURES COME FROM THE CMS. Every photograph here is one the program uploaded
 * -- its own laboratories, its own equipment, its own activities, its own
 * research, its own partners' marks. The brochure is read as a document about
 * this laboratory, so stock photography of somebody else's workshop has no
 * business in it. The local editorial files stay wired in behind each one, and
 * only appear if the CMS is unreachable, which is what keeps the page from
 * collapsing during an outage.
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
  /** Small uppercase label in the running head. */
  chapter: string;
  /** Contents-panel entry. Also what the search box matches on. */
  title: string;
  subtitle: string;
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

export function buildBrochurePages(src: BrochureSources): BrochurePage[] {
  const areas = AREA_ORDER.map((code) => {
    const area = src.focusAreas.find((a) => a.code === code);
    return {
      code,
      title: area?.title ?? code,
      image: pick(area?.image, AREA_FALLBACK[code]),
    };
  });

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
    // 1 ───────────────────────────────────────────────────────────────────
    {
      chapter: "Cover",
      title: "Mechanical Engineering",
      subtitle: "Royal University of Phnom Penh",
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

    // 2 ───────────────────────────────────────────────────────────────────
    {
      chapter: "01 · The program",
      title: "What we are for",
      subtitle: "Vision",
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

    // 3 ───────────────────────────────────────────────────────────────────
    {
      chapter: "01 · The program",
      title: "How we deliver it",
      subtitle: "Mission",
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

    // 4 ───────────────────────────────────────────────────────────────────
    {
      chapter: "02 · Areas of focus",
      title: "Four areas of focus",
      subtitle: "DMP · TES · MAS · ECM",
      tone: "dark",
      body: (
        <>
          <p className="fb-eyebrow fb-gold">AREAS OF FOCUS</p>
          <h2>One discipline, four directions</h2>
          <div className="fb-areas">
            {areas.map((a) => (
              <section key={a.code}>
                <img alt="" src={a.image} />
                <div>
                  <b>{a.code}</b>
                  <p>{a.title}</p>
                </div>
              </section>
            ))}
          </div>
          <p className="fb-note">
            The areas organise expertise without limiting collaboration across
            disciplines. Each one runs through the curriculum, the laboratories
            and the research programme alike.
          </p>
        </>
      ),
    },

    // 5 ───────────────────────────────────────────────────────────────────
    {
      chapter: "02 · Why this discipline",
      title: "Mechanical engineering and AI",
      subtitle: "Is it still relevant?",
      tone: "dark",
      body: (
        <>
          <p className="fb-eyebrow fb-gold">A QUESTION WORTH ASKING</p>
          <h2>
            Is mechanical engineering still relevant in the age of artificial
            intelligence?
          </h2>
          <p className="fb-answer">
            Yes. AI is a tool that complements the discipline rather than
            replacing it — and the engineers who use it will be the ones leading
            the work.
          </p>
          <div className="fb-reasons">
            {[
              ["Design and manufacturing", "AI can optimise a process, but materials, mechanics, thermodynamics and manufacturing technique are what make the object exist."],
              ["Integration with AI", "Autonomous robots, intelligent production equipment and aerospace vehicles need someone to embed the sensors, actuate the systems and write the control."],
              ["Robotics and automation", "The clearest intersection of the two: mechanical engineers design the robot that AI perceives and decides with."],
              ["Energy and sustainability", "Solar, wind, geothermal, storage and efficient thermodynamic systems. AI adds prediction and optimisation on top of engineering judgement."],
              ["Physical systems and materials", "How a material behaves under load and heat is not something a model can be asked to invent."],
              ["Solving real problems", "Data supports a decision. Insight rooted in physical principles is what makes it an engineering decision."],
            ].map(([t, d], i) => (
              <section key={t}>
                <span>{String(i + 1).padStart(2, "0")}</span>
                <b>{t}</b>
                <p>{d}</p>
              </section>
            ))}
          </div>
        </>
      ),
    },

    // 6 ───────────────────────────────────────────────────────────────────
    {
      chapter: "02 · Why this discipline",
      title: "Why study mechanical engineering",
      subtitle: "What each area offers",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">WHY STUDY IT</p>
          <h2>Four areas, four reasons</h2>
          <div className="fb-why">
            {[
              {
                code: "DMP",
                t: "Create things that did not exist",
                d: "Design everything from everyday objects to complex machines, and see ideas become prototypes and finished products. Skills valued across automotive, aerospace, robotics and consumer electronics.",
              },
              {
                code: "TES",
                t: "Work on the energy problem",
                d: "The science behind generating and moving energy — renewables, HVAC, thermal management. Efficient systems that waste less, on a planet shifting toward greener solutions.",
              },
              {
                code: "MAS",
                t: "Build machines that think",
                d: "Mechanical, electronic and computer systems integrated into one: robotics, automation and smart manufacturing. As industry moves toward Industry 4.0, these are the sought-after skills.",
              },
              {
                code: "ECM",
                t: "Take responsibility for it",
                d: "Ensuring designs meet safety standards, regulation and environmental requirements — and overseeing the projects, teams and production that deliver them. The route to leadership.",
              },
            ].map((r) => (
              <section key={r.code}>
                <b>{r.code}</b>
                <div>
                  <strong>{r.t}</strong>
                  <p>{r.d}</p>
                </div>
              </section>
            ))}
          </div>
          <div className="fb-strip">
            <Icon name="compass" />
            <p>
              Creative design, sustainable energy, cutting-edge automation and
              the leadership to carry them — a versatile field with room to make
              a meaningful difference.
            </p>
          </div>
        </>
      ),
    },

    // 7 ───────────────────────────────────────────────────────────────────
    {
      chapter: "03 · Curriculum",
      title: "The four-year path",
      subtitle: "Eight semesters, nine subject families",
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

    // 8 ───────────────────────────────────────────────────────────────────
    {
      chapter: "03 · Laboratories",
      title: "What you will work on",
      subtitle: "Equipment across the four areas",
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

    // 9 ───────────────────────────────────────────────────────────────────
    {
      chapter: "04 · Research",
      title: "What we are building",
      subtitle: "Four active projects",
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

    // 10 ───────────────────────────────────────────────────────────────────
    {
      chapter: "04 · Research",
      title: "Research that left the laboratory",
      subtitle: "Cooling and spraying, in Kampot",
      tone: "paper",
      body: (
        <>
          <p className="fb-eyebrow">IN PRACTICE</p>
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
        </>
      ),
    },

    // 11 ───────────────────────────────────────────────────────────────────
    {
      chapter: "05 · Collaboration",
      title: "Who we work with",
      subtitle: "The quadruple helix",
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

    // 12 ──────────────────────────────────────────────────────────────────
    {
      chapter: "Contact",
      title: "Talk to the program",
      subtitle: "Faculty of Engineering, RUPP",
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
