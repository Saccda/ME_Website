import type { Metadata } from "next";
import Link from "next/link";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getFaqs, getHomeData, type FaqItem } from "@/lib/api";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Frequently asked questions | Mechanical Engineering RUPP",
  description:
    "Answers to the questions prospective and current students ask most often about the Mechanical Engineering program at RUPP.",
};

/** Groups in the order the CMS defines them, keeping the CMS ordering inside. */
function groupByCategory(items: FaqItem[]) {
  const groups = new Map<string, { label: string; items: FaqItem[] }>();
  for (const item of items) {
    const group = groups.get(item.category);
    if (group) group.items.push(item);
    else groups.set(item.category, { label: item.category_label, items: [item] });
  }
  return [...groups.entries()].map(([key, group]) => ({ key, ...group }));
}

/**
 * Search engines show these as expandable answers when the page declares them.
 * Only answered questions are ever served, so there is nothing empty to strip.
 */
function faqStructuredData(items: FaqItem[]) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: items.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: { "@type": "Answer", text: item.answer },
    })),
  };
}

export default async function FaqsPage() {
  const [home, faqs] = await Promise.all([getHomeData(), getFaqs()]);
  const groups = groupByCategory(faqs);

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs trail={[{ label: "FAQs" }]} />

        <section className="directory-hero is-compact">
          <div className="shell">
            <h1>Frequently Asked Questions</h1>
            <p>
              Answers to what prospective and current students ask us most
              often. If your question is not here, please get in touch.
            </p>
          </div>
        </section>

        <section className="section white faq-section">
          <div className="shell">
            {faqs.length === 0 ? (
              <div className="content-empty-state">
                <h2>No questions have been answered yet</h2>
                <p>
                  Questions and answers are published from the ME content
                  management system. In the meantime, the program is happy to
                  answer directly.
                </p>
                <a className="text-link" href={`mailto:${home.settings.email}`}>
                  Email the ME Program <span aria-hidden="true">→</span>
                </a>
              </div>
            ) : (
              <>
                {/* Jump links: with several groups the page is long enough that
                    scanning for a heading is slower than choosing one. */}
                {groups.length > 1 ? (
                  <nav className="faq-jump" aria-label="Question topics">
                    {groups.map((group) => (
                      <a href={`#${group.key}`} key={group.key}>
                        {group.label}
                        <span>{group.items.length}</span>
                      </a>
                    ))}
                  </nav>
                ) : null}

                <div className="faq-groups">
                  {groups.map((group) => (
                    <section
                      aria-labelledby={`${group.key}-heading`}
                      className="faq-group"
                      id={group.key}
                      key={group.key}
                    >
                      <h2 id={`${group.key}-heading`}>{group.label}</h2>
                      <div className="faq-list">
                        {group.items.map((item) => (
                          /* <details> rather than a scripted accordion: it
                             opens without JavaScript, is reachable by keyboard
                             and is announced correctly by screen readers. */
                          <details className="faq-item" key={item.id}>
                            <summary>
                              <span>{item.question}</span>
                              <i aria-hidden="true" />
                            </summary>
                            {/* Rich text from Wagtail, editable only by
                                authenticated staff. */}
                            <div
                              className="faq-answer"
                              dangerouslySetInnerHTML={{ __html: item.answer }}
                            />
                          </details>
                        ))}
                      </div>
                    </section>
                  ))}
                </div>

                <div className="faq-ask">
                  <h2>Still have a question?</h2>
                  <p>
                    If your question is not answered here, the ME Program will
                    answer it directly — and it may end up on this page.
                  </p>
                  <div className="faq-ask-actions">
                    <a
                      className="button button-navy"
                      href={`mailto:${home.settings.email}?subject=${encodeURIComponent(
                        "Question about the ME Program",
                      )}`}
                    >
                      Ask the program <span aria-hidden="true">→</span>
                    </a>
                    <Link className="text-link" href="/admissions">
                      Admissions details <span aria-hidden="true">→</span>
                    </Link>
                  </div>
                </div>

                <script
                  type="application/ld+json"
                  dangerouslySetInnerHTML={{
                    __html: JSON.stringify(faqStructuredData(faqs)),
                  }}
                />
              </>
            )}
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
