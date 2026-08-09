/* eslint-disable @next/next/no-img-element */
import type { StoryBlock } from "@/lib/api";
import { videoEmbedUrl } from "@/lib/video";
import MediaGallery from "./MediaGallery";

export default function StoryBody({
  blocks,
  galleryTitle,
}: {
  blocks: StoryBlock[];
  /** Passed to any gallery in the body as the activity name. */
  galleryTitle?: string;
}) {
  if (blocks.length === 0) return null;

  return (
    <div className="story-body">
      {blocks.map((block, index) => {
        const key = `${block.type}-${index}`;

        switch (block.type) {
          case "heading":
            return <h2 key={key}>{block.value}</h2>;

          // The markup comes from Wagtail's rich-text editor, which is only
          // reachable by authenticated staff.
          case "paragraph":
            return (
              <div
                className="story-rich-text"
                key={key}
                dangerouslySetInnerHTML={{ __html: block.value }}
              />
            );

          case "image":
            return (
              <figure className="story-figure" key={key}>
                <img src={block.url} alt={block.alt_text} loading="lazy" />
                {block.caption ? (
                  <figcaption>{block.caption}</figcaption>
                ) : null}
              </figure>
            );

          case "gallery":
            return (
              <figure className="story-gallery" key={key}>
                <div data-count={block.images.length}>
                  {block.images.map((entry) => (
                    <img
                      alt={entry.alt_text}
                      key={entry.url}
                      loading="lazy"
                      src={entry.url}
                    />
                  ))}
                </div>
                {block.caption ? (
                  <figcaption>{block.caption}</figcaption>
                ) : null}
              </figure>
            );

          case "media_gallery":
            return (
              <MediaGallery
                caption={block.caption}
                galleryTitle={galleryTitle}
                heading={block.heading}
                items={block.items}
                key={key}
              />
            );

          case "quote":
            return (
              <blockquote className="story-quote" key={key}>
                <p>{block.value}</p>
                {block.attribution ? <cite>{block.attribution}</cite> : null}
              </blockquote>
            );

          case "video": {
            const src = block.url ? videoEmbedUrl(block.url) : null;
            return (
              <figure className="story-figure" key={key}>
                {block.file_url ? (
                  <video controls poster={block.poster ?? undefined}>
                    <source src={block.file_url} />
                  </video>
                ) : src ? (
                  <div className="story-video">
                    <iframe
                      src={src}
                      title={block.caption || "Video"}
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    />
                  </div>
                ) : (
                  <a
                    className="text-link"
                    href={block.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Watch the video <span aria-hidden="true">↗</span>
                  </a>
                )}
                {block.caption ? (
                  <figcaption>{block.caption}</figcaption>
                ) : null}
              </figure>
            );
          }

          case "key_facts":
            return (
              <section className="story-facts" key={key}>
                {block.heading ? <h3>{block.heading}</h3> : null}
                <dl>
                  {block.facts.map((fact) => (
                    <div key={`${fact.label}-${fact.value}`}>
                      <dt>{fact.label}</dt>
                      <dd>{fact.value}</dd>
                    </div>
                  ))}
                </dl>
              </section>
            );

          case "stats":
            return (
              <section className="story-stats" key={key}>
                {block.heading ? <h3>{block.heading}</h3> : null}
                <div data-count={block.stats.length}>
                  {block.stats.map((stat) => (
                    <p key={`${stat.value}-${stat.label}`}>
                      <strong>{stat.value}</strong>
                      <span>{stat.label}</span>
                    </p>
                  ))}
                </div>
              </section>
            );

          case "steps":
            return (
              <section className="story-steps" key={key}>
                {block.heading ? <h3>{block.heading}</h3> : null}
                <ol>
                  {block.steps.map((step) => (
                    <li key={step.title}>
                      <strong>{step.title}</strong>
                      {step.description ? <p>{step.description}</p> : null}
                    </li>
                  ))}
                </ol>
              </section>
            );

          case "table": {
            const [firstRow, ...restRows] = block.rows;
            const headerRow = block.first_row_is_header ? firstRow : null;
            const bodyRows = block.first_row_is_header ? restRows : block.rows;
            const Cell = ({
              value,
              index,
            }: {
              value: string;
              index: number;
            }) =>
              block.first_col_is_header && index === 0 ? (
                <th scope="row">{value}</th>
              ) : (
                <td>{value}</td>
              );

            return (
              <section className="story-table" key={key}>
                {block.heading ? <h3>{block.heading}</h3> : null}
                {/* Tables can be wider than the reading measure, so the table
                    scrolls inside its own box rather than the page. */}
                <div>
                  <table>
                    {headerRow ? (
                      <thead>
                        <tr>
                          {headerRow.map((cell, column) => (
                            <th key={`h-${column}`} scope="col">
                              {cell}
                            </th>
                          ))}
                        </tr>
                      </thead>
                    ) : null}
                    <tbody>
                      {bodyRows.map((row, rowIndex) => (
                        <tr key={`r-${rowIndex}`}>
                          {row.map((cell, column) => (
                            <Cell
                              index={column}
                              key={`c-${rowIndex}-${column}`}
                              value={cell}
                            />
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                {block.caption ? <p>{block.caption}</p> : null}
              </section>
            );
          }

          case "callout":
            return (
              <aside className="story-callout" key={key}>
                {block.label ? <strong>{block.label}</strong> : null}
                <p>{block.value}</p>
              </aside>
            );

          case "references":
            return (
              <section className="story-references" key={key}>
                {block.heading ? <h3>{block.heading}</h3> : null}
                <ol>
                  {block.entries.map((entry) => (
                    <li key={entry.citation}>
                      {entry.url ? (
                        <a
                          href={entry.url}
                          rel="noopener noreferrer"
                          target="_blank"
                        >
                          {entry.citation}
                        </a>
                      ) : (
                        entry.citation
                      )}
                    </li>
                  ))}
                </ol>
              </section>
            );

          case "document":
            return (
              <a
                className="story-document"
                href={block.url}
                key={key}
                target="_blank"
                rel="noopener noreferrer"
              >
                <span className="story-document-label">{block.label}</span>
                <span className="story-document-file">{block.filename}</span>
              </a>
            );

          default:
            return null;
        }
      })}
    </div>
  );
}
