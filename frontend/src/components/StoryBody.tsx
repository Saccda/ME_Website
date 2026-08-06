/* eslint-disable @next/next/no-img-element */
import type { StoryBlock } from "@/lib/api";
import { videoEmbedUrl } from "@/lib/video";
import MediaGallery from "./MediaGallery";

export default function StoryBody({ blocks }: { blocks: StoryBlock[] }) {
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
            const src = videoEmbedUrl(block.url);
            return (
              <figure className="story-figure" key={key}>
                {src ? (
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
