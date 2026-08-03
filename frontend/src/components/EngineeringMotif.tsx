/**
 * Decorative technical-drawing marks — bolt circles, dimension lines with
 * arrow terminators, radius callouts and centre marks — drawn at very low
 * opacity behind profile content.
 *
 * Purely ornamental, so it is hidden from assistive tech. Strokes are navy at
 * low alpha rather than a flat grey, so the motif sits inside the brand palette
 * on both the cream and white grounds it is used on.
 */
export default function EngineeringMotif({
  side,
}: {
  side: "left" | "right";
}) {
  return (
    <svg
      className={`eng-motif eng-motif-${side}`}
      viewBox="0 0 240 620"
      aria-hidden="true"
      focusable="false"
    >
      {side === "left" ? (
        <g>
          {/* Bolt circle with centre marks */}
          <circle cx="66" cy="118" r="54" />
          <circle cx="66" cy="118" r="34" />
          <circle cx="66" cy="118" r="4" />
          <path d="M66,50 V186 M-2,118 H134" strokeDasharray="10 6 3 6" />

          {/* Vertical dimension line with arrow terminators */}
          <path d="M186,64 V292" />
          <path d="M180,72 L186,60 L192,72" />
          <path d="M180,284 L186,296 L192,284" />
          <path d="M164,60 H208 M164,296 H208" />

          {/* Radius callout */}
          <path d="M40,392 A76,76 0 0 1 158,352" />
          <path d="M40,392 L118,368" strokeDasharray="6 5" />
          <circle cx="40" cy="392" r="3" />

          {/* Section hatch */}
          <path
            d="M28,470 L92,470 M28,486 L92,486 M28,502 L92,502 M28,518 L92,518"
            strokeDasharray="3 7"
          />
        </g>
      ) : (
        <g>
          {/* Gear pitch circles */}
          <circle cx="164" cy="150" r="82" strokeDasharray="14 8" />
          <circle cx="164" cy="150" r="58" />
          <circle cx="164" cy="150" r="18" />
          <path d="M164,68 V232 M82,150 H246" strokeDasharray="12 7 3 7" />

          {/* Horizontal dimension line */}
          <path d="M56,318 H214" />
          <path d="M64,312 L52,318 L64,324" />
          <path d="M206,312 L218,318 L206,324" />
          <path d="M52,300 V336 M218,300 V336" />

          {/* Angle callout */}
          <path d="M74,470 L196,470 M74,470 L168,398" />
          <path d="M74,470 m34,0 a34,34 0 0 0 26,-26" strokeDasharray="5 4" />

          {/* Datum square */}
          <path d="M96,530 H180 V566 H96 Z" />
          <path d="M96,548 H180" strokeDasharray="4 5" />
        </g>
      )}
    </svg>
  );
}
