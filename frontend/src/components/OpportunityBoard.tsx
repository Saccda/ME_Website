/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import type { Opportunity } from "@/lib/api";

/**
 * The opportunity board: one continuously sliding row per type.
 *
 * Grouping by type replaces the filter buttons -- a row headed "Internships"
 * answers the same question without asking the reader to press anything.
 *
 * The rows use the same marquee as the partner logos: the list is rendered
 * twice and the track translates half its width, so the loop is seamless and
 * costs no JavaScript. It pauses on hover and on keyboard focus, and stops
 * entirely under a reduced-motion setting.
 */

type OpportunityType = Opportunity["opportunity_type"];

// Jobs and internships only. Scholarships and training remain in the CMS and
// on their own postings, but the board is what students come to it for.
const ROWS: { key: OpportunityType; label: string; singular: string }[] = [
  { key: "job", label: "Jobs", singular: "job" },
  { key: "internship", label: "Internships", singular: "internship" },
];

// A track has to be at least twice the widest viewport for the half-width
// translation to loop without showing its end, so a short row is repeated
// until it is long enough rather than left standing still.
const MIN_CARDS_PER_SET = 8;

/** Whole days from today, in UTC so the boundary does not drift by timezone. */
function daysUntil(deadline: string) {
  const end = Date.parse(`${deadline}T00:00:00Z`);
  const today = new Date();
  const start = Date.UTC(
    today.getUTCFullYear(),
    today.getUTCMonth(),
    today.getUTCDate(),
  );
  return Math.round((end - start) / 86_400_000);
}

/** The badge shows the date; this says how much time is left. */
function closingLabel(deadline: string | null) {
  if (!deadline) return { text: "Open until filled", urgency: "none" as const };

  const days = daysUntil(deadline);
  if (days < 0) return { text: "Closed", urgency: "closed" as const };
  if (days === 0) return { text: "Closes today", urgency: "urgent" as const };
  if (days === 1) return { text: "Closes tomorrow", urgency: "urgent" as const };
  if (days <= 7)
    return { text: `Closes in ${days} days`, urgency: "urgent" as const };
  return { text: "Applications open", urgency: "none" as const };
}

function deadlineBadge(deadline: string | null) {
  if (!deadline) return null;
  const date = new Date(`${deadline}T00:00:00Z`);
  return {
    day: new Intl.DateTimeFormat("en-GB", {
      day: "2-digit",
      timeZone: "UTC",
    }).format(date),
    month: new Intl.DateTimeFormat("en-GB", {
      month: "short",
      timeZone: "UTC",
    }).format(date),
  };
}

/** Soonest deadline first; undated last. */
function byClosingDate(a: Opportunity, b: Opportunity) {
  if (!a.application_deadline) return 1;
  if (!b.application_deadline) return -1;
  return a.application_deadline.localeCompare(b.application_deadline);
}

function OpportunityCard({
  duplicate = false,
  item,
}: {
  duplicate?: boolean;
  item: Opportunity;
}) {
  const badge = deadlineBadge(item.application_deadline);
  const closing = closingLabel(item.application_deadline);

  return (
    <article
      aria-hidden={duplicate ? true : undefined}
      className="opportunity-card"
      data-type={item.opportunity_type}
    >
      <div className="opportunity-media">
        {item.announcement_image ? (
          <img
            src={item.announcement_image}
            alt={`${item.title} announcement from ${item.partner?.name || "the ME Program"}`}
          />
        ) : (
          <div className="opportunity-poster-fallback">
            {item.partner?.logo ? (
              <img src={item.partner.logo} alt="" />
            ) : (
              <span>ME</span>
            )}
            <strong>
              {item.opportunity_type === "job" ? "We are hiring" : "Now open"}
            </strong>
            <small>{item.partner?.name || "ME Program"}</small>
          </div>
        )}
        <span className="opportunity-type">{item.opportunity_type_label}</span>
        {badge && (
          <time
            className="opportunity-deadline"
            dateTime={item.application_deadline || undefined}
            aria-label={closing.text}
          >
            <strong>{badge.day}</strong>
            <span>{badge.month}</span>
          </time>
        )}
      </div>

      <div className="opportunity-content">
        <p className="opportunity-partner">
          {item.partner?.name || "ME Program"}
        </p>
        <h4>{item.title}</h4>
        <p className="opportunity-summary">{item.summary}</p>

        {/* The facts that decide whether the posting is worth opening. */}
        <dl className="opportunity-facts">
          <div>
            <dt>Location</dt>
            <dd>{item.location || "To be confirmed"}</dd>
          </div>
          {item.employment_type ? (
            <div>
              <dt>Type</dt>
              <dd>{item.employment_type}</dd>
            </div>
          ) : null}
          {item.positions ? (
            <div>
              <dt>Openings</dt>
              <dd>{item.positions}</dd>
            </div>
          ) : null}
        </dl>

        <div className="opportunity-foot">
          {item.focus_areas.length > 0 ? (
            <ul className="opportunity-tags">
              {item.focus_areas.map((area) => (
                <li key={area.code}>{area.code}</li>
              ))}
            </ul>
          ) : (
            <span />
          )}
          {/* A date alone reads the same whether it is tomorrow or next month. */}
          <p className="opportunity-closing" data-urgency={closing.urgency}>
            {closing.text}
          </p>
        </div>

        {/* Goes to the posting on this site, so no external-link arrow. */}
        <Link
          className="opportunity-action"
          href={`/opportunities/${item.slug}`}
          tabIndex={duplicate ? -1 : undefined}
        >
          View full posting <span aria-hidden="true">→</span>
        </Link>
      </div>
    </article>
  );
}

function OpportunityRow({
  items,
  label,
  singular,
}: {
  items: Opportunity[];
  label: string;
  singular: string;
}) {
  // One set repeated until it is wide enough, then rendered twice: the track
  // is two identical halves, so translating by -50% lands exactly where it
  // began. Two internships loop as smoothly as four jobs this way.
  const repeats = Math.max(1, Math.ceil(MIN_CARDS_PER_SET / items.length));
  const set = Array.from({ length: repeats }, () => items).flat();
  const slides = [...set, ...set];

  return (
    <section className="opportunity-row" aria-label={label}>
      <div className="shell">
        <header className="opportunity-row-head">
          <h3>{label}</h3>
          {/* Each row counts its own, so a reader sees how many internships
              there are without inferring it from a section total. */}
          <p className="opportunity-count">
            <strong>{items.length}</strong>
            <span>
              active {items.length === 1 ? singular : label.toLowerCase()}
            </span>
          </p>
        </header>
      </div>

      <div className="marquee opportunity-marquee">
        <div
          className="marquee-track"
          style={{ animationDuration: `${set.length * 7}s` }}
        >
          {slides.map((item, index) => (
            <OpportunityCard
              duplicate={index >= items.length}
              item={item}
              key={`${item.slug}-${index}`}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function OpportunityBoard({
  email,
  facebookUrl,
  opportunities,
  telegramUrl,
}: {
  email: string;
  facebookUrl: string;
  opportunities: Opportunity[];
  telegramUrl: string;
}) {
  const all = [...(opportunities ?? [])].sort(byClosingDate);
  const rows = ROWS.map((row) => ({
    ...row,
    items: all.filter((item) => item.opportunity_type === row.key),
  })).filter((row) => row.items.length > 0);

  if (rows.length === 0) {
    return (
      <div className="shell opportunity-none-wrap">
        <div className="opportunity-none">
        <h3>No opportunities are open right now.</h3>
        <p>
          Openings from partner organizations are posted here as they are
          confirmed. Follow the program to hear about them first.
        </p>
        <div className="opportunity-none-actions">
          {telegramUrl ? (
            <a href={telegramUrl} target="_blank" rel="noopener noreferrer">
              Follow on Telegram
            </a>
          ) : null}
          {facebookUrl ? (
            <a href={facebookUrl} target="_blank" rel="noopener noreferrer">
              Follow on Facebook
            </a>
          ) : null}
          <a
            href={`mailto:${email}?subject=${encodeURIComponent(
              "Partner opportunity for ME students",
            )}`}
          >
            Offer an opportunity
          </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="opportunity-board">
      {rows.map((row) => (
        <OpportunityRow
          items={row.items}
          key={row.key}
          label={row.label}
          singular={row.singular}
        />
      ))}
    </div>
  );
}
