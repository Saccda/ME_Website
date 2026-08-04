/**
 * Icons for the four ME focus areas.
 *
 * Drawn from engineering-drawing vocabulary — dimension lines, witness ticks,
 * limit lines, centre marks — rather than generic pictograms, so the set reads
 * as this programme's own and matches the technical motifs used elsewhere.
 *
 * Design rules held across all four, so they behave as a family:
 *  - one idea per icon, legible down to 24px
 *  - a single 32x32 grid, uniform stroke weight, round caps and joins
 *  - comparable visual mass, so none dominates a row
 *  - exactly one accent element each, carrying that area's brand colour
 */
export type FocusCode = "DMP" | "TES" | "MAS" | "ECM";

const TITLES: Record<FocusCode, string> = {
  DMP: "Design and Manufacturing Process",
  TES: "Thermofluid and Energy System",
  MAS: "Mechatronic and Automation System",
  ECM: "Engineering Compliance and Management",
};

function Glyph({ code }: { code: FocusCode }) {
  switch (code) {
    // Caliper measuring a turned part: design intent becoming a made component.
    case "DMP":
      return (
        <>
          <path d="M4 8.5h24" />
          <path d="M8.5 8.5v12" />
          <path d="M21.5 8.5v12" />
          <path d="M21.5 4.5v4.5" />
          <circle cx="15" cy="16" r="4" />
          <path
            className="focus-icon-accent"
            d="M8.5 26h13M8.5 23.5v5M21.5 23.5v5"
          />
        </>
      );
    // Flow through a narrowing duct, with heat leaving it.
    case "TES":
      return (
        <>
          <path d="M4 7c5 0 7 3.5 12 3.5S23 7 28 7" />
          <path d="M4 22c5 0 7-3.5 12-3.5S23 22 28 22" />
          <path d="M10 14.5h9" />
          <path d="M17 11.8l2.8 2.7-2.8 2.7" />
          <path
            className="focus-icon-accent"
            d="M12 28.5c1.6-1.3 1.6-2.7 0-4M20 28.5c1.6-1.3 1.6-2.7 0-4"
          />
        </>
      );
    // Articulated linkage: mechanism plus the control node driving it.
    case "MAS":
      return (
        <>
          <path d="M4 27.5h17" />
          <circle cx="9" cy="22" r="3.2" />
          <circle cx="18" cy="13" r="3.2" />
          <path d="M11.3 19.7 15.7 15.3" />
          <path d="M20.4 11 24 7.6" />
          <circle cx="26" cy="6" r="2.6" className="focus-icon-accent" />
          <path className="focus-icon-accent" d="M26 8.6v4" />
        </>
      );
    // A part held inside its tolerance band: conformance to specification.
    case "ECM":
    default:
      return (
        <>
          <path d="M6 7h20M6 25h20" />
          <path d="M6 4.5v5M26 4.5v5M6 22.5v5M26 22.5v5" />
          <path d="M11 12h10v8H11z" />
          <path className="focus-icon-accent" d="m13.4 16.2 2.2 2.2 4.4-5" />
        </>
      );
  }
}

export default function FocusIcon({
  code,
  title,
}: {
  code: FocusCode;
  title?: string;
}) {
  return (
    <svg
      className={`focus-icon focus-icon-${code.toLowerCase()}`}
      viewBox="0 0 32 32"
      role="img"
      aria-label={title ?? TITLES[code]}
    >
      <Glyph code={code} />
    </svg>
  );
}
