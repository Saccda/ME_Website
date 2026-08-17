/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData, getOpportunity } from "@/lib/api";

export const dynamic = "force-dynamic";

type OpportunityPageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({
  params,
}: OpportunityPageProps): Promise<Metadata> {
  const { slug } = await params;
  const lookup = await getOpportunity(slug);
  if (lookup.status !== "found") {
    return { title: "Opportunities | Mechanical Engineering RUPP" };
  }
  return {
    title: `${lookup.opportunity.title} | Mechanical Engineering RUPP`,
    description: lookup.opportunity.summary,
  };
}

function closingText(deadline: string | null) {
  if (!deadline) return "Open until filled";
  return `Closes ${new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(`${deadline}T00:00:00Z`))}`;
}

/** A section is only rendered when the author has written it. */
function RichSection({ heading, html }: { heading: string; html: string }) {
  if (!html) return null;
  return (
    <section className="posting-section">
      <h2>{heading}</h2>
      {/* Markup comes from Wagtail's rich-text editor, reachable only by
          authenticated staff. */}
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </section>
  );
}

export default async function OpportunityPage({ params }: OpportunityPageProps) {
  const { slug } = await params;
  const [lookup, home] = await Promise.all([getOpportunity(slug), getHomeData()]);

  if (lookup.status === "not-found") notFound();

  if (lookup.status === "unavailable") {
    return (
      <>
        <SiteHeader settings={home.settings} />
        <main id="main-content" className="editorial-page">
          <section className="section white">
            <div className="shell">
              <div className="content-empty-state">
                <h1>This posting is temporarily unavailable.</h1>
                <p>
                  The opportunity board could not be reached. Please try again
                  shortly, or return to the list of current openings.
                </p>
                <Link className="text-link" href="/#opportunities">
                  All opportunities <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </section>
        </main>
        <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
      </>
    );
  }

  const item = lookup.opportunity;
  const organisation = item.partner?.name || "Mechanical Engineering Program";
  const enquiry = `mailto:${home.settings.email}?subject=${encodeURIComponent(
    `Enquiry: ${item.title}`,
  )}`;

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page posting-page">
        <Breadcrumbs
          trail={[
            { label: "Opportunities", href: "/#opportunities" },
            { label: item.title },
          ]}
        />

        <section className="section white">
          <div className="shell">
            <header className="posting-head" data-type={item.opportunity_type}>
              <p className="posting-chip">{item.opportunity_type_label}</p>
              <h1>{item.title}</h1>
              <p className="posting-org">{organisation}</p>
              <p className="posting-summary">{item.summary}</p>
            </header>

            {/* The facts an applicant checks before reading anything else. */}
            <dl className="posting-facts">
              <div>
                <dt>Organisation</dt>
                <dd>{organisation}</dd>
              </div>
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
              {item.focus_areas.length > 0 ? (
                <div>
                  <dt>Focus areas</dt>
                  <dd>{item.focus_areas.map((a) => a.code).join(" · ")}</dd>
                </div>
              ) : null}
              <div>
                <dt>Deadline</dt>
                <dd>
                  {item.application_deadline ? (
                    <time dateTime={item.application_deadline}>
                      {closingText(item.application_deadline)}
                    </time>
                  ) : (
                    closingText(null)
                  )}
                </dd>
              </div>
            </dl>

            <div className="posting-body">
              <RichSection heading="About the role" html={item.body} />
              <RichSection
                heading="Responsibilities"
                html={item.responsibilities}
              />
              <RichSection heading="Requirements" html={item.requirements} />
              <RichSection heading="How to apply" html={item.how_to_apply} />

              {item.announcement_image ? (
                <figure className="posting-figure">
                  <img
                    src={item.announcement_image}
                    alt={`Announcement for ${item.title}`}
                  />
                </figure>
              ) : null}
            </div>

            <div className="posting-actions">
              {item.application_url ? (
                <a
                  className="posting-apply"
                  href={item.application_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Apply <span aria-hidden="true">↗</span>
                </a>
              ) : (
                <a className="posting-apply" href={enquiry}>
                  Enquire by email
                </a>
              )}
              <Link className="text-link" href="/#opportunities">
                All opportunities <span aria-hidden="true">→</span>
              </Link>
            </div>

            {/* Credited rather than hidden: a reader deciding whether to act on
                a posting is entitled to know where it came from. */}
            {item.source_url || item.source_name ? (
              <p className="posting-source">
                Announced by {organisation}
                {item.source_name ? ` on ${item.source_name}` : ""}.{" "}
                {item.source_url ? (
                  <a
                    href={item.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View the original announcement{" "}
                    <span aria-hidden="true">↗</span>
                  </a>
                ) : null}
              </p>
            ) : null}
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
