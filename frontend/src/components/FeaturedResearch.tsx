/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import type { ResearchProject } from "@/lib/api";

/**
 * Current research, on the landing page.
 *
 * The page above this explains mechanical engineering with a NASA telescope, a
 * Mars rover and a 3D-printed car -- all borrowed, all credited to somebody
 * else. A reader could reach the footer without seeing one thing made here.
 * These cards answer the question those pictures provoke: yes, but what do
 * you do?
 *
 * The grid and the card are the news feed's, deliberately -- a landing page
 * that invents a new card for every band makes the reader learn each one. The
 * masthead is not. News opens with a centred display heading, which is the
 * page's top-tier device; running it twice makes the second band read as a
 * copy of the first, and at that size the label also outweighs the cards it
 * introduces. Research opens as a section instead: named on the left, the way
 * out on the right, closed with a rule.
 *
 * What separates a project card from a news card is the focus area it belongs
 * to, carried in the area's own colour -- the same four-way scheme the rest of
 * the site is built on. A featured project leads; the rest follow in their CMS
 * order. Nothing here claims a result, and no card carries a status: every
 * project in the CMS is "ongoing", so the word would be printed three times
 * and mean nothing.
 */

const SHOWN = 3;

export default function FeaturedResearch({
  projects,
  tone = "white",
}: {
  projects: ResearchProject[];
  /** Set by the page, so the band never shares a ground with the one above. */
  tone?: "cream" | "white";
}) {
  // Featured first, otherwise CMS order. `sort` is stable, so ties keep it.
  // Coerced through Boolean because a backend that predates the is_featured
  // field omits it, and Number(undefined) is NaN -- a comparator returning NaN
  // sorts by accident rather than by rule.
  const ordered = [...projects].sort(
    (a, b) => Number(Boolean(b.is_featured)) - Number(Boolean(a.is_featured)),
  );
  const shown = ordered.slice(0, SHOWN);
  if (shown.length === 0) return null;

  return (
    <section className={`section ${tone} home-feed`} id="featured-research">
      <div className="shell">
        <header className="home-feed-head split">
          <div className="home-feed-lead">
            <p className="eyebrow">Research</p>
            <h2>
              What we are <em>building</em>
            </h2>
            <p className="home-feed-intro">
              Work under way in the ME laboratory and in the field, from
              agricultural machinery to energy monitoring.
            </p>
          </div>
          {/* The one thing a grid of three cannot tell the reader is whether
              three is all of it. */}
          <div className="home-feed-aside">
            {projects.length > shown.length ? (
              <p className="home-feed-count">
                {shown.length} of {projects.length} projects
              </p>
            ) : null}
            <Link className="home-feed-all" href="/research">
              All research <span aria-hidden="true">→</span>
            </Link>
          </div>
        </header>

        <div className="home-feed-grid">
          {shown.map((project) => (
            <article className="news-card" key={project.slug}>
              <div className="news-card-media">
                {/* `is-current` is how .news-card-media marks the visible
                    slide; without it the image sits at opacity 0. A project
                    card holds one picture rather than a slideshow, so it is
                    always the current one. */}
                {project.image ? (
                  <img
                    className="is-current"
                    src={project.image}
                    alt=""
                    loading="lazy"
                  />
                ) : (
                  <span className="news-card-fallback">ME</span>
                )}
              </div>
              <div className="news-card-body">
                <p className="news-card-kicker research-areas">
                  {project.focus_areas.length > 0 ? (
                    project.focus_areas.map((area) => (
                      <span className="research-area" key={area.slug}>
                        <i
                          aria-hidden="true"
                          style={{
                            background: area.accent_color || "var(--brand-navy)",
                          }}
                        />
                        {area.code}
                      </span>
                    ))
                  ) : (
                    <span className="research-area">Research</span>
                  )}
                </p>
                {/* Only the title is a link; it stretches over the card, so the
                    row exposes one target per project. */}
                <h3>
                  <Link href={`/research/projects/${project.slug}`}>
                    {project.title}
                  </Link>
                </h3>
                <p className="news-card-excerpt">{project.summary}</p>
                <span className="news-card-cue" aria-hidden="true">
                  Explore the project <span>→</span>
                </span>
              </div>
            </article>
          ))}
        </div>

        {/* A reader who has scrolled three stacked cards on a phone has left
            the masthead link far behind, so the way out is repeated at the
            foot -- but only where the stacking happens. */}
        <p className="home-feed-tail">
          <Link className="button button-navy" href="/research">
            All research <span aria-hidden="true">→</span>
          </Link>
        </p>
      </div>
    </section>
  );
}
