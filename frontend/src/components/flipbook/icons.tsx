/**
 * Line icons for the brochure pages.
 *
 * Drawn here rather than pulled from a package: the site has no icon
 * dependency and is not going to gain one for ten pages. Each is a 24x24
 * stroke path that inherits `currentColor` and `1em` sizing, so a page sets
 * its size in container units and the icon follows.
 */

export type IconName =
  | "gear"
  | "cpu"
  | "bot"
  | "net"
  | "factory"
  | "flask"
  | "book"
  | "people"
  | "leaf"
  | "compass";

const paths: Record<IconName, React.ReactNode> = {
  gear: (
    <>
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06-2.83 2.83-.06-.06a1.7 1.7 0 0 0-1.88-.34 1.7 1.7 0 0 0-1.03 1.55V21h-4v-.08A1.7 1.7 0 0 0 8.97 19.4a1.7 1.7 0 0 0-1.88.34l-.06.06-2.83-2.83.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.52-1H3v-4h.08A1.7 1.7 0 0 0 4.6 9a1.7 1.7 0 0 0-.34-1.88L4.2 7.06l2.83-2.83.06.06A1.7 1.7 0 0 0 8.97 4.6 1.7 1.7 0 0 0 10 3.08V3h4v.08a1.7 1.7 0 0 0 1.03 1.52 1.7 1.7 0 0 0 1.88-.34l.06-.06 2.83 2.83-.06.06A1.7 1.7 0 0 0 19.4 9 1.7 1.7 0 0 0 20.92 10H21v4h-.08A1.7 1.7 0 0 0 19.4 15Z" />
    </>
  ),
  cpu: (
    <>
      <rect height="10" rx="1" width="10" x="7" y="7" />
      <path d="M9 1v3m6-3v3M9 20v3m6-3v3M20 9h3m-3 6h3M1 9h3m-3 6h3M10 10h4v4h-4z" />
    </>
  ),
  bot: (
    <>
      <rect height="12" rx="3" width="16" x="4" y="8" />
      <path d="M12 4v4m-4 5h.01M16 13h.01M8 17h8M9 4h6" />
    </>
  ),
  net: (
    <>
      <rect height="5" width="6" x="9" y="2" />
      <rect height="5" width="6" x="2" y="17" />
      <rect height="5" width="6" x="16" y="17" />
      <path d="M12 7v5M5 17v-3h14v3" />
    </>
  ),
  factory: (
    <>
      <path d="M3 21V9l6 3V8l6 4V5h5v16H3Z" />
      <path d="M7 17h2m3 0h2m3 0h2" />
    </>
  ),
  flask: (
    <>
      <path d="M9 2v6L4 19a2 2 0 0 0 1.8 3h12.4A2 2 0 0 0 20 19L15 8V2" />
      <path d="M8 2h8M6.5 14h11" />
    </>
  ),
  book: (
    <>
      <path d="M4 4a2 2 0 0 1 2-2h13v18H6a2 2 0 0 0-2 2V4Z" />
      <path d="M8 7h7M8 11h7" />
    </>
  ),
  people: (
    <>
      <circle cx="9" cy="8" r="3" />
      <path d="M2 21v-1a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v1M16 3.5a3 3 0 0 1 0 9M22 21v-1a5 5 0 0 0-3-4.6" />
    </>
  ),
  leaf: (
    <>
      <path d="M4 20c0-9 6-15 16-16 0 10-5 15-11 15H4Z" />
      <path d="M4 20c4-6 8-9 12-10.5" />
    </>
  ),
  compass: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="m15.5 8.5-2 5.5-5.5 2 2-5.5 5.5-2Z" />
    </>
  ),
};

export function Icon({ name }: { name: IconName }) {
  return (
    <svg aria-hidden="true" className="fb-icon" viewBox="0 0 24 24">
      {paths[name]}
    </svg>
  );
}
