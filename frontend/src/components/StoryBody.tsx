/* eslint-disable @next/next/no-img-element */
import type { StoryBlock } from "@/lib/api";

/**
 * Turns a watch link into an embeddable one.
 *
 * Authors paste the address from the browser bar, which is not the address a
 * player accepts. An unrecognised host returns null and the block falls back to
 * a plain link rather than an iframe that would silently refuse to load.
 */
function embedUrl(url: string): string | null {
  try {
    const parsed = new URL(url);
    const host = parsed.hostname.replace(/^www\./, "");

    if (host === "youtu.be") {
      const id = parsed.pathname.slice(1);
      return id ? `https://www.youtube.com/embed/${id}` : null;
    }
    if (host === "youtube.com" || host === "m.youtube.com") {
      const id = parsed.searchParams.get("v");
      if (id) return `https://www.youtube.com/embed/${id}`;
      if (parsed.pathname.startsWith("/embed/")) return url;
      return null;
    }
    if (host === "vimeo.com") {
      const id = parsed.pathname.split("/").filter(Boolean)[0];
      return id ? `https://player.vimeo.com/video/${id}` : null;
    }
    if (host === "facebook.com" || host === "fb.watch") {
      return `https://www.facebook.com/plugins/video.php?href=${encodeURIComponent(url)}`;
    }
    return null;
  } catch {
    return null;
  }
}

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

          case "quote":
            return (
              <blockquote className="story-quote" key={key}>
                <p>{block.value}</p>
                {block.attribution ? <cite>{block.attribution}</cite> : null}
              </blockquote>
            );

          case "video": {
            const src = embedUrl(block.url);
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
