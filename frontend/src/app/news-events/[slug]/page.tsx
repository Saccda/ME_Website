/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Breadcrumbs from "@/components/Breadcrumbs";
import CardMedia from "@/components/CardMedia";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import StoryBody from "@/components/StoryBody";
import { getHomeData, getNewsEvent, getNewsEvents } from "@/lib/api";
import { formatDispatchDate } from "@/lib/homeDispatches";

export const dynamic = "force-dynamic";

type StoryPageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({
  params,
}: StoryPageProps): Promise<Metadata> {
  const { slug } = await params;
  const lookup = await getNewsEvent(slug);
  if (lookup.status !== "found") {
    return { title: "News & events | Mechanical Engineering RUPP" };
  }
  return {
    title: `${lookup.story.title} | Mechanical Engineering RUPP`,
    description: lookup.story.excerpt,
  };
}

export default async function StoryPage({ params }: StoryPageProps) {
  const { slug } = await params;
  const [lookup, home] = await Promise.all([getNewsEvent(slug), getHomeData()]);

  if (lookup.status === "not-found") notFound();

  if (lookup.status === "unavailable") {
    return (
      <>
        <SiteHeader settings={home.settings} />
        <main id="main-content" className="editorial-page">
          <section className="section white">
            <div className="shell">
              <div className="content-empty-state">
                <h1>This story is temporarily unavailable.</h1>
                <p>
                  The newsroom could not be reached. Please try again shortly,
                  or return to all news and events.
                </p>
                <Link className="text-link" href="/news-events">
                  All news &amp; events <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </section>
        </main>
        <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
      </>
    );
  }

  const story = lookup.story;
  const isEvent = story.content_type === "event";
  const date = formatDispatchDate(
    isEvent ? story.event_date ?? story.published_at : story.published_at,
  );

  const related = (await getNewsEvents())
    .filter((item) => item.slug !== story.slug)
    .slice(0, 3);

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page story-page">
        <Breadcrumbs
          trail={[
            { label: "News & Events", href: "/news-events" },
            { label: story.title },
          ]}
        />

        {/* The lead image runs to the window edge, ahead of the headline, so
            the story opens on the photograph rather than on type. */}
        {story.image_wide || story.image ? (
          <div className="story-lead-media">
            <img src={(story.image_wide || story.image) as string} alt="" />
          </div>
        ) : null}

        <article>
          <header className="story-header">
            <div className="shell">
              <p className="story-kicker">
                {story.category || (isEvent ? "Event" : "News")}
              </p>
              <h1>{story.title}</h1>
              {date || story.author ? (
                <p className="story-byline">
                  {date ? (
                    <time
                      dateTime={
                        (isEvent ? story.event_date : story.published_at) ??
                        undefined
                      }
                    >
                      {isEvent ? `Taking place ${date}` : date}
                    </time>
                  ) : null}
                  {date && story.author ? (
                    <span aria-hidden="true">|</span>
                  ) : null}
                  {story.author ? <span>By {story.author}</span> : null}
                </p>
              ) : null}
              {story.excerpt ? (
                <p className="story-standfirst">{story.excerpt}</p>
              ) : null}
            </div>
          </header>

          <div className="shell story-content">
            {story.body.length > 0 ? (
              <StoryBody blocks={story.body} />
            ) : (
              <p className="story-body-empty">
                The full story is being written. Check back shortly.
              </p>
            )}

            <p className="story-foot">
              <a className="story-top-link" href="#main-content">
                Back to top <span aria-hidden="true">↑</span>
              </a>
            </p>
          </div>
        </article>

        {related.length > 0 ? (
          <section className="section cream story-related">
            <div className="shell">
              <h2>More from ME</h2>
              <div className="home-feed-grid">
                {related.map((item) => (
                  <article className="news-card" key={item.id}>
                    <CardMedia
                      hasVideo={item.has_video}
                      slides={item.card_media}
                    />
                    <div className="news-card-body">
                      <p className="news-card-kicker">
                        {item.category ||
                          (item.content_type === "event" ? "Event" : "News")}
                      </p>
                      <h3>
                        <Link href={`/news-events/${item.slug}`}>
                          {item.title}
                        </Link>
                      </h3>
                      <p className="news-card-excerpt">{item.excerpt}</p>
                    </div>
                  </article>
                ))}
              </div>
            </div>
          </section>
        ) : null}
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
