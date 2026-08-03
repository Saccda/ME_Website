/**
 * Decorative mark for the vision statement: concentric rings closing on a
 * single gold core — a focal point being brought into view.
 *
 * The rings are navy rather than the gold used in the reference mock-up: that
 * design sits on a dark ground where gold reads clearly, but gold on white
 * scores 1.85:1 and thin rings would effectively disappear here.
 */
export default function VisionMark() {
  return (
    <svg
      className="vision-mark"
      viewBox="0 0 132 132"
      aria-hidden="true"
      focusable="false"
    >
      <circle className="vision-mark-ring ring-4" cx="66" cy="66" r="57" />
      <circle className="vision-mark-ring ring-3" cx="66" cy="66" r="44" />
      <circle className="vision-mark-ring ring-2" cx="66" cy="66" r="31" />
      <circle className="vision-mark-core" cx="66" cy="66" r="18" />
      <circle className="vision-mark-center" cx="66" cy="66" r="3.4" />
    </svg>
  );
}
