import Link from "next/link";

export type Crumb = {
  label: string;
  /** Omitted on the final crumb, which is the current page. */
  href?: string;
};

/**
 * Location trail shown directly beneath the fixed header. Each page passes its
 * own trail rather than deriving one from the URL, so dynamic routes can show a
 * real title ("Thermofluid and Energy System") instead of a slug.
 */
export default function Breadcrumbs({ trail }: { trail: Crumb[] }) {
  return (
    <nav className="breadcrumbs" aria-label="Breadcrumb">
      <ol className="shell">
        <li>
          <Link href="/">Home</Link>
        </li>
        {trail.map((crumb, index) => {
          const isCurrent = index === trail.length - 1;
          return (
            <li key={`${crumb.label}-${index}`}>
              {isCurrent || !crumb.href ? (
                <span aria-current={isCurrent ? "page" : undefined}>
                  {crumb.label}
                </span>
              ) : (
                <Link href={crumb.href}>{crumb.label}</Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
