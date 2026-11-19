/**
 * Marks for the program's two missions.
 *
 * Drawn to the same rules as the focus-area set in `FocusIcon`, so the two
 * families sit together: one 32x32 grid, one idea per icon, uniform stroke
 * with round caps and joins, and exactly one gold accent each.
 *
 * Drawn rather than typed. The pair these replace were the characters U+2301
 * and U+25CE, and the Segoe stack has no glyph for the first: M1 carried a
 * 4px speck where an icon was meant to be.
 */
export type MissionIconKey = "teaching" | "research";

function Glyph({ name }: { name: MissionIconKey }) {
  if (name === "teaching") {
    // A mortarboard over the head it sits on: education, conferred.
    return (
      <>
        <path d="M16 4.6 29 10.7 16 16.8 3 10.7Z" />
        <path d="M8.8 13.3v5.1c0 2.3 3.2 3.9 7.2 3.9s7.2-1.6 7.2-3.9v-5.1" />
        <path className="mission-icon-accent" d="M29 10.7v6.4" />
        <circle className="mission-icon-accent" cx="29" cy="19.3" r="2.1" />
      </>
    );
  }

  // Concentric rings closing on a centre, with sight marks: the research
  // vocabulary already used by the vision mark on this same page.
  return (
    <>
      <circle cx="16" cy="16" r="11.2" />
      <circle cx="16" cy="16" r="5.6" />
      <path d="M16 1.8v3.6M16 26.6v3.6M1.8 16h3.6M26.6 16h3.6" />
      <circle className="mission-icon-accent" cx="16" cy="16" r="1.9" />
    </>
  );
}

export default function MissionIcon({ name }: { name: MissionIconKey }) {
  return (
    <svg
      className="mission-icon"
      viewBox="0 0 32 32"
      aria-hidden="true"
      focusable="false"
    >
      <Glyph name={name} />
    </svg>
  );
}
