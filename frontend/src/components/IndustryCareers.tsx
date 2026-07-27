/* eslint-disable @next/next/no-img-element */
import type { Opportunity } from "@/lib/api";

type JobOpportunitiesProps = {
  email: string;
  facebookUrl: string;
  opportunities: Opportunity[];
  telegramUrl: string;
};

function formatDeadline(deadline: string | null) {
  if (!deadline) return "Open until filled";
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(`${deadline}T00:00:00Z`));
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

function JobCard({
  duplicate = false,
  fallbackHref,
  opportunity,
}: {
  duplicate?: boolean;
  fallbackHref: string;
  opportunity: Opportunity;
}) {
  const deadline = deadlineBadge(opportunity.application_deadline);

  return (
    <article
      className="opportunity-card"
      aria-hidden={duplicate ? true : undefined}
    >
      <div className="opportunity-media">
        {opportunity.announcement_image ? (
          <img
            src={opportunity.announcement_image}
            alt={`${opportunity.title} announcement`}
          />
        ) : (
          <div className="opportunity-poster-fallback">
            {opportunity.partner?.logo ? (
              <img src={opportunity.partner.logo} alt="" />
            ) : (
              <span>ME</span>
            )}
            <strong>We are hiring</strong>
            <small>{opportunity.partner?.name || "ME Program"}</small>
          </div>
        )}
        <span className="opportunity-type">
          {opportunity.opportunity_type_label}
        </span>
        {deadline && (
          <time
            className="opportunity-deadline"
            dateTime={opportunity.application_deadline || undefined}
            aria-label={`Application deadline ${formatDeadline(opportunity.application_deadline)}`}
          >
            <strong>{deadline.day}</strong>
            <span>{deadline.month}</span>
          </time>
        )}
      </div>
      <div className="opportunity-content">
        <div className="opportunity-partner">
          <small>{opportunity.partner?.name || "ME Program"}</small>
        </div>
        <h4>{opportunity.title}</h4>
        <p>{opportunity.summary}</p>
        <div className="opportunity-tags">
          {opportunity.focus_areas.map((area) => (
            <span key={area.code}>{area.code}</span>
          ))}
        </div>
        <div className="opportunity-location">
          <span>Location</span>
          <strong>{opportunity.location || "To be confirmed"}</strong>
        </div>
        <a
          href={opportunity.application_url || fallbackHref}
          target={opportunity.application_url ? "_blank" : undefined}
          rel={opportunity.application_url ? "noreferrer" : undefined}
          tabIndex={duplicate ? -1 : undefined}
        >
          Read more <span aria-hidden="true">↗</span>
        </a>
      </div>
    </article>
  );
}

export default function JobOpportunities({
  email,
  facebookUrl,
  opportunities,
  telegramUrl,
}: JobOpportunitiesProps) {
  const jobs = (opportunities ?? []).slice(0, 10);
  const shouldAnimate = jobs.length > 4;
  const displayedJobs = shouldAnimate ? [...jobs, ...jobs] : jobs;

  return (
    <div className="industry-module job-opportunity-module" id="opportunities">
      <div className="industry-module-header job-board-header">
        <div>
          <p className="industry-kicker">Job opportunities</p>
          <h3>Current job openings from our partner network</h3>
          <p className="job-board-intro">
            Explore jobs, internships, scholarships, and professional training
            shared with the ME community.
          </p>
        </div>
        {jobs.length > 0 && (
          <p className="job-board-count">
            <strong>{jobs.length}</strong>
            <span>{jobs.length === 1 ? "active job" : "active jobs"}</span>
          </p>
        )}
      </div>

      {jobs.length > 0 ? (
        <>
          <div
            className={`opportunity-rail${shouldAnimate ? " has-motion" : ""}`}
            aria-label="Active partner job announcements"
            tabIndex={shouldAnimate ? 0 : undefined}
          >
            <div
              className={`opportunity-track${shouldAnimate ? " is-animated" : ""}`}
              style={
                {
                  "--job-duration": `${Math.max(36, jobs.length * 7)}s`,
                } as React.CSSProperties
              }
            >
              {displayedJobs.map((opportunity, index) => (
                <JobCard
                  opportunity={opportunity}
                  duplicate={shouldAnimate && index >= jobs.length}
                  fallbackHref={`mailto:${email}?subject=${encodeURIComponent(
                    `ME job enquiry: ${opportunity.title}`,
                  )}`}
                  key={`${opportunity.slug}-${index}`}
                />
              ))}
            </div>
          </div>
          {shouldAnimate && (
            <p className="job-rail-note">
              Hover or focus to pause. Swipe to explore on mobile.
            </p>
          )}
        </>
      ) : (
        <div className="opportunity-empty">
          <div className="opportunity-empty-mark" aria-hidden="true">ME</div>
          <div>
            <span>Opportunity board</span>
            <h4>No active announcements right now.</h4>
            <p>
              New partner jobs, internships, scholarships, and training
              opportunities will appear here when they are published.
            </p>
          </div>
          <div className="opportunity-empty-actions">
            {telegramUrl && (
              <a href={telegramUrl} target="_blank" rel="noreferrer">
                Follow on Telegram
              </a>
            )}
            {facebookUrl && (
              <a href={facebookUrl} target="_blank" rel="noreferrer">
                Follow on Facebook
              </a>
            )}
            <a href={`mailto:${email}?subject=Partner opportunity for ME students`}>
              Submit an opportunity
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
