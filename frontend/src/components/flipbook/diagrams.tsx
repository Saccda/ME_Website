/**
 * Engineering diagrams for the brochure pages.
 *
 * Drawn as inline SVG rather than photographed or imported. A publication that
 * explains where AI sits in an engineering workflow, what one system asks of
 * four disciplines, or which part of a car each area of focus touches needs
 * drawings labelled in its own type and coloured with the site's own focus-area
 * accents. No photograph says that, and stock illustration says it about
 * somebody else's factory.
 *
 * Every label lives inside the viewBox, so it scales with the page exactly as
 * the `cqi` type around it does: the same drawing serves a half-spread at
 * 1440px, a single page on a phone, and an A4 print. Strokes inherit
 * `currentColor`, so a diagram takes the ink of whichever page tone it sits on.
 */

export type AreaAccents = Record<"DMP" | "TES" | "MAS" | "ECM", string>;

/**
 * The program's own automated cooling and spraying rig, reduced to the parts
 * that carry the argument: one system, and all four areas of focus at work in
 * it at once.
 */
export function SystemCore({ accents }: { accents: AreaAccents }) {
  return (
    <svg
      className="fb-svg"
      role="img"
      aria-label="One cooling and spraying system: a steel frame and tank (design and manufacturing), water and heat moving through pump and pipes (thermofluid and energy), a sensor and controller deciding when to spray (mechatronics and automation), and a safety and maintenance check (compliance and management)."
      viewBox="0 0 300 168"
    >
      {/* Frame and tank — DMP */}
      <g stroke={accents.DMP} strokeWidth="1.8" fill="none">
        <path d="M22 132h126M30 132v12M140 132v12" />
        <rect x="34" y="62" width="70" height="70" rx="4" />
        <path d="M34 78h70" />
      </g>
      <text x="22" y="156" className="fb-svg-tag" fill={accents.DMP}>
        DMP · FRAME, TANK, FABRICATION
      </text>

      {/* Water, pump, pipework and spray — TES */}
      <g stroke={accents.TES} strokeWidth="1.8" fill="none">
        <path d="M38 96q8-6 16 0t16 0 16 0 14 0" />
        <path d="M38 108q8-6 16 0t16 0 16 0 14 0" />
        <circle cx="122" cy="132" r="11" />
        <path d="m118 126 9 6-9 6z" />
        <path d="M133 132h34M186 132V74h84" />
        <path d="M214 74v10m24-10v10m24-10v10" />
        <path d="m208 92 6-8 6 8m6 0 6-8 6 8m6 0 6-8 6 8" />
      </g>
      <text x="196" y="112" className="fb-svg-tag" fill={accents.TES}>
        TES · HEAT AND WATER
      </text>

      {/* Sensing and control — MAS */}
      <g stroke={accents.MAS} strokeWidth="1.8" fill="none">
        <path d="M167 132V96" />
        <circle cx="167" cy="90" r="5" />
        <path d="M156 82q4-8 0-16m22 16q-4-8 0-16" />
        <rect x="120" y="22" width="60" height="32" rx="3" />
        <path d="M132 34h12m-12 8h24" />
        <path d="M150 54v30M180 38h22v94h-30" strokeDasharray="4 4" />
      </g>
      <text x="120" y="16" className="fb-svg-tag" fill={accents.MAS}>
        MAS · SENSE, DECIDE, ACT
      </text>

      {/* Check and maintenance — ECM */}
      <g stroke={accents.ECM} strokeWidth="1.8" fill="none">
        <circle cx="272" cy="132" r="12" />
        <path d="m266 132 4 5 8-10" />
      </g>
      <text x="238" y="158" className="fb-svg-tag" fill={accents.ECM}>
        ECM · SAFE AND MAINTAINED
      </text>
    </svg>
  );
}

/**
 * CDIO as one closed loop rather than four boxes: each quarter hands over to
 * the next, and operating the system starts the next conception.
 */
export function CdioRing() {
  const stages = [
    { label: "CONCEIVE", x: 92, y: 26 },
    { label: "DESIGN", x: 166, y: 96 },
    { label: "IMPLEMENT", x: 92, y: 168 },
    { label: "OPERATE", x: 18, y: 96 },
  ];
  return (
    <svg
      className="fb-svg"
      role="img"
      aria-label="The CDIO cycle as a loop: conceive, then design, then implement, then operate, and operating returns to conceive."
      viewBox="0 0 184 184"
    >
      {/* Colours arrive by inline style rather than as presentation attributes:
          a custom property in `fill="var(--fb-gold)"` is not honoured
          everywhere, and a silently black arrowhead would be hard to spot. */}
      <defs>
        <marker
          id="fb-cdio-arrow"
          markerHeight="6"
          markerWidth="6"
          orient="auto"
          refX="4"
          refY="3"
        >
          <path d="M0 0.6 5 3 0 5.4z" style={{ fill: "var(--fb-gold)" }} />
        </marker>
      </defs>

      {/* Four arcs, one per stage, each ending in the next stage's arrowhead. */}
      <g
        fill="none"
        strokeWidth="7"
        style={{ stroke: "var(--fb-deep)" }}
      >
        <path d="M100 30a62 62 0 0 1 54 54" markerEnd="url(#fb-cdio-arrow)" />
        <path d="M154 100a62 62 0 0 1-54 54" markerEnd="url(#fb-cdio-arrow)" />
        <path d="M84 154a62 62 0 0 1-54-54" markerEnd="url(#fb-cdio-arrow)" />
        <path d="M30 84a62 62 0 0 1 54-54" markerEnd="url(#fb-cdio-arrow)" />
      </g>

      <circle
        cx="92"
        cy="92"
        fill="none"
        r="40"
        style={{ stroke: "var(--fb-line)" }}
      />
      <text x="92" y="88" className="fb-svg-core" textAnchor="middle">
        CDIO
      </text>
      <text x="92" y="104" className="fb-svg-note" textAnchor="middle">
        one project cycle
      </text>

      {stages.map((s) => (
        <text
          className="fb-svg-tag"
          key={s.label}
          style={{ fill: "var(--fb-deep)" }}
          textAnchor={s.x === 92 ? "middle" : s.x > 92 ? "start" : "end"}
          x={s.x}
          y={s.y}
        >
          {s.label}
        </text>
      ))}
    </svg>
  );
}

/**
 * A vehicle in section, with a leader line from each area of focus to the part
 * of the car it actually touches. The battery and the drive unit are drawn
 * because the electric argument is made on the same page: an EV changes what is
 * under the floor, not whether the floor has to carry it.
 */
export function VehicleSystems({ accents }: { accents: AreaAccents }) {
  return (
    <svg
      className="fb-svg"
      role="img"
      aria-label="A car in side section. Design and manufacturing covers the body structure and panels; thermofluid and energy the cooling, air conditioning and battery heat; mechatronics the sensors, motor control and driver assistance; compliance and management the crash safety, standards and quality checks."
      viewBox="0 0 340 174"
    >
      {/* Body shell */}
      <g fill="none" stroke="currentColor" strokeWidth="1.8">
        <path d="M22 128V104q0-9 9-11l64-11 28-26q6-6 15-6h68q10 0 17 8l20 24 46 9q10 2 10 12v25z" />
        <path d="M122 80l16-18h32v18zM182 62h24q6 0 10 5l11 13h-45z" />
        <circle cx="86" cy="128" r="19" />
        <circle cx="86" cy="128" r="8" />
        <circle cx="252" cy="128" r="19" />
        <circle cx="252" cy="128" r="8" />
      </g>

      {/* Battery and drive — TES */}
      <g fill="none" stroke={accents.TES} strokeWidth="1.8">
        <rect x="112" y="112" width="112" height="14" rx="2" />
        <path d="M126 112v14m14-14v14m14-14v14m14-14v14m14-14v14m14-14v14m14-14v14" />
        <rect x="266" y="92" width="44" height="20" rx="2" />
        <path d="M312 96v12M316 98v8" />
      </g>

      {/* Sensing and control — MAS */}
      <g fill="none" stroke={accents.MAS} strokeWidth="1.8">
        <circle cx="168" cy="66" r="4" />
        <circle cx="316" cy="118" r="4" />
        <path d="M320 112q8-4 12 0M320 124q8 4 12 0" />
      </g>

      {/* Structure — DMP */}
      <g fill="none" stroke={accents.DMP} strokeWidth="1.8">
        <path d="M95 82h28M170 62v26M226 80h26" />
      </g>

      {/* Leader lines and labels */}
      <g strokeWidth="1.2" fill="none">
        <path d="M150 62V34h-38" stroke={accents.DMP} />
        <path d="M168 126v34h-40" stroke={accents.TES} />
        <path d="M168 62V30h44" stroke={accents.MAS} />
        <path d="M252 147v15h30" stroke={accents.ECM} />
      </g>
      <text x="108" y="31" className="fb-svg-tag" fill={accents.DMP} textAnchor="end">
        BODY · PANELS · TOOLING
      </text>
      <text x="216" y="27" className="fb-svg-tag" fill={accents.MAS}>
        SENSORS · CONTROL
      </text>
      <text x="124" y="164" className="fb-svg-tag" fill={accents.TES} textAnchor="end">
        COOLING · BATTERY HEAT
      </text>
      <text x="286" y="166" className="fb-svg-tag" fill={accents.ECM}>
        SAFETY · QUALITY
      </text>
    </svg>
  );
}

/**
 * The line that builds the car. Four areas again, this time as a factory: the
 * point of the page is that the industry is a production system, not one job
 * description.
 */
export function PlantLine({ accents }: { accents: AreaAccents }) {
  return (
    <svg
      className="fb-svg"
      role="img"
      aria-label="An assembly line: a body shell on a conveyor, a robot cell welding it, and an inspection gate checking it before it moves on."
      viewBox="0 0 340 126"
    >
      {/* Conveyor */}
      <g fill="none" stroke="currentColor" strokeWidth="1.8">
        <path d="M14 96h312" />
        <circle cx="34" cy="106" r="6" />
        <circle cx="74" cy="106" r="6" />
        <circle cx="114" cy="106" r="6" />
        <circle cx="154" cy="106" r="6" />
        <circle cx="194" cy="106" r="6" />
        <circle cx="234" cy="106" r="6" />
        <circle cx="274" cy="106" r="6" />
        <circle cx="314" cy="106" r="6" />
      </g>

      {/* Body shell on the line — DMP */}
      <g fill="none" stroke={accents.DMP} strokeWidth="1.8">
        <path d="M40 96V76l16-14h44l14 14v20" />
        <path d="M56 62v14h44V62" />
      </g>
      <text x="40" y="122" className="fb-svg-tag" fill={accents.DMP}>
        BODY IN WHITE
      </text>

      {/* Robot cell — MAS */}
      <g fill="none" stroke={accents.MAS} strokeWidth="1.8">
        <rect x="176" y="70" width="26" height="26" rx="2" />
        <path d="M189 70 176 38l34-8" />
        <path d="m206 28 10 12-8 6" />
      </g>
      <text x="164" y="122" className="fb-svg-tag" fill={accents.MAS}>
        ROBOT CELL · PLC
      </text>

      {/* Inspection gate — ECM */}
      <g fill="none" stroke={accents.ECM} strokeWidth="1.8">
        <path d="M268 96V52h50v44" />
        <circle cx="293" cy="66" r="7" />
        <path d="M293 73v9" />
      </g>
      <text x="262" y="122" className="fb-svg-tag" fill={accents.ECM}>
        INSPECTION · QUALITY
      </text>
    </svg>
  );
}
