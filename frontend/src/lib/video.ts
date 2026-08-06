/**
 * Video link handling, shared by the story body and the gallery.
 *
 * Authors paste the address from the browser bar, which is not the address a
 * player accepts and not a picture either. Both helpers return null for a host
 * we do not recognise, so callers fall back rather than render something broken.
 */

type Parsed = { host: string; url: URL } | null;

function parse(url: string): Parsed {
  try {
    const parsed = new URL(url);
    return { host: parsed.hostname.replace(/^www\./, ""), url: parsed };
  } catch {
    return null;
  }
}

function youTubeId(url: string): string | null {
  const parsed = parse(url);
  if (!parsed) return null;
  const { host, url: address } = parsed;

  if (host === "youtu.be") return address.pathname.slice(1) || null;
  if (host === "youtube.com" || host === "m.youtube.com") {
    const id = address.searchParams.get("v");
    if (id) return id;
    if (address.pathname.startsWith("/embed/")) {
      return address.pathname.split("/")[2] || null;
    }
  }
  return null;
}

export function videoEmbedUrl(url: string): string | null {
  const id = youTubeId(url);
  if (id) return `https://www.youtube.com/embed/${id}`;

  const parsed = parse(url);
  if (!parsed) return null;
  const { host, url: address } = parsed;

  if (host === "vimeo.com") {
    const videoId = address.pathname.split("/").filter(Boolean)[0];
    return videoId ? `https://player.vimeo.com/video/${videoId}` : null;
  }
  if (host === "facebook.com" || host === "fb.watch") {
    return `https://www.facebook.com/plugins/video.php?href=${encodeURIComponent(url)}`;
  }
  return null;
}

/** A still for a video the author gave no poster image for. */
export function videoThumbnail(url: string): string | null {
  const id = youTubeId(url);
  return id ? `https://img.youtube.com/vi/${id}/hqdefault.jpg` : null;
}
