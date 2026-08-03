/** Hand-drawn icon paths — no icon package, per project conventions. */
export const PROFILE_ICONS = {
  expertise: "M12 3l2.4 5.6L20 11l-5.6 2.4L12 19l-2.4-5.6L4 11l5.6-2.4z",
  education: "M3 9l9-4 9 4-9 4zM7 12v4c0 1.1 2.2 2 5 2s5-.9 5-2v-4",
  courses:
    "M4 5h6a2 2 0 012 2v12a3 3 0 00-3-2H4zM20 5h-6a2 2 0 00-2 2v12a3 3 0 013-2h5z",
  office:
    "M12 21s7-5.5 7-11a7 7 0 10-14 0c0 5.5 7 11 7 11zM12 12a2.5 2.5 0 100-5 2.5 2.5 0 000 5z",
} as const;

export type ProfileIcon = keyof typeof PROFILE_ICONS;

/**
 * One labelled detail row, matching the mock-up's icon + label + chevron.
 *
 * Built on native <details> so the chevron actually does something: a chevron
 * that only decorates is a promise the interface does not keep. No JavaScript,
 * and it stays keyboard- and screen-reader-operable for free.
 */
export default function ProfileDetailRow({
  icon,
  label,
  items,
}: {
  icon: ProfileIcon;
  label: string;
  items: string[];
}) {
  if (items.length === 0) return null;

  return (
    <details className="profile-detail-row">
      <summary>
        <span className="profile-detail-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24">
            <path d={PROFILE_ICONS[icon]} />
          </svg>
        </span>
        <span className="profile-detail-label">{label}</span>
        <span className="profile-detail-chevron" aria-hidden="true" />
      </summary>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </details>
  );
}
