import type { CSSProperties } from "react";

import { quadrupleHelix } from "@/lib/quadrupleHelix";

// One half-period of the wave is 150 user units, so a full period is 300 —
// the exact distance each strand travels before the loop repeats seamlessly.
// A quadratic peaks at half its control offset, so -120 gives amplitude 60.
const WAVE = `q75,-120 150,0${" t150,0".repeat(13)}`;

type StrandStyle = CSSProperties & {
  "--strand": string;
  "--strand-delay": string;
  "--strand-duration": string;
};

/** Decorative background helix for the partnership band. */
export default function QuadrupleHelix() {
  return (
    <div className="helix-watermark" aria-hidden="true">
      <svg viewBox="0 0 1200 160" preserveAspectRatio="xMidYMid slice" focusable="false">
        {quadrupleHelix.map((strand, index) => (
          <path
            key={strand.id}
            className="helix-strand"
            d={`M${-600 - index * 75},80 ${WAVE}`}
            style={
              {
                "--strand": strand.onGold,
                "--strand-delay": `${index * -2.4}s`,
                "--strand-duration": `${20 + index * 3}s`,
              } as StrandStyle
            }
          />
        ))}
      </svg>
    </div>
  );
}
