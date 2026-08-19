/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import type { FocusArea, ProgramSettings } from "@/lib/api";

type SiteFooterProps = {
  focusAreas: Array<
    Pick<FocusArea, "code" | "slug" | "title" | "accent_color">
  >;
  settings: ProgramSettings;
};

/**
 * A code chip readable against its own accent.
 *
 * The four accents cannot all carry white: the gold scores 2.02 and the green
 * 4.17, both under the 4.5 a chip this small needs. Whichever reads better
 * wins, and if neither clears the bar the accent darkens until white does.
 */
function readableChip(accent: string) {
  const luminance = (hex: string) => {
    const channels = [0, 2, 4].map((offset) => {
      const value = parseInt(hex.replace("#", "").substr(offset, 2), 16) / 255;
      return value <= 0.03928
        ? value / 12.92
        : Math.pow((value + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
  };
  const ratio = (a: string, b: string) => {
    const [light, dark] = [luminance(a), luminance(b)].sort((x, y) => y - x);
    return (light + 0.05) / (dark + 0.05);
  };

  if (!/^#[0-9a-f]{6}$/i.test(accent)) return { background: "#0a2164", color: "#fff" };

  for (const color of ["#ffffff", "#061a2a"]) {
    if (ratio(accent, color) >= 4.5) return { background: accent, color };
  }
  let background = accent;
  while (ratio(background, "#ffffff") < 4.5) {
    background =
      "#" +
      [0, 2, 4]
        .map((offset) =>
          Math.round(
            parseInt(background.replace("#", "").substr(offset, 2), 16) * 0.92,
          )
            .toString(16)
            .padStart(2, "0"),
        )
        .join("");
  }
  return { background, color: "#fff" };
}

export default function SiteFooter({
  focusAreas,
  settings,
}: SiteFooterProps) {
  const phoneHref = `tel:${settings.phone.replace(/[^\d+]/g, "")}`;
  const socialLinks = [
    {
      href: settings.facebook_url,
      icon: "/assets/icons/facebook.svg",
      label: "Facebook",
    },
    {
      href: settings.telegram_url,
      icon: "/assets/icons/telegram.svg",
      label: "Telegram",
    },
    {
      href: settings.youtube_url,
      icon: "/assets/icons/youtube.svg",
      label: "YouTube",
    },
    {
      href: settings.linkedin_url,
      icon: "/assets/icons/linkedin.svg",
      label: "LinkedIn",
    },
  ].filter((item) => item.href);

  return (
    <footer className="institutional-footer">
      <div className="shell footer-directory">
        <div className="footer-identity">
          <img
            src="/assets/brand/me-wordmark.webp"
            alt="Mechanical Engineering — Nature, Nurture, Nourish"
          />
          <address>
            <strong>Mechanical Engineering Program</strong>
            <span>Faculty of Engineering · RUPP</span>
            <span>{settings.address}</span>
          </address>
          <a href={`mailto:${settings.email}`}>{settings.email}</a>
          <a href={phoneHref}>{settings.phone}</a>
        </div>

        <nav aria-label="Program footer links">
          <h2>About</h2>
          <Link href="/admissions">Admissions</Link>
          <Link href="/#what-is-me">What is mechanical engineering?</Link>
          <Link href="/#why-me">Why choose ME</Link>
          <Link href="/about">Program profile</Link>
          <Link href="/curriculum">Curriculum</Link>
          <Link href="/people#faculty-staff">Faculty</Link>
          <Link href="/facilities">Facilities</Link>
        </nav>

        <nav aria-label="Focus-area footer links" className="footer-areas">
          <h2>Areas of Focus</h2>
          {focusAreas.map((area) => {
            const chip = readableChip(area.accent_color);
            return (
              <Link href={`/focus/${area.slug}`} key={area.code}>
                <span className="footer-area-code" style={chip}>
                  {area.code}
                </span>
                <span aria-hidden="true" className="footer-area-dash">
                  &ndash;
                </span>
                <span className="footer-area-title">{area.title}</span>
              </Link>
            );
          })}
        </nav>

        <div className="footer-connect">
          <h2>Research & Innovation</h2>
          <Link href="/research">Research areas</Link>
          <Link href="/#partners">Partnership</Link>
          <Link href="/#opportunities">Job opportunities</Link>
          <Link href="/news-events">News & events</Link>

          {socialLinks.length > 0 ? (
            <div className="footer-socials" aria-label="ME social media">
              {socialLinks.map((item) => (
                <a
                  href={item.href}
                  aria-label={`Follow ME RUPP on ${item.label}`}
                  title={item.label}
                  target="_blank"
                  rel="noreferrer"
                  key={item.label}
                >
                  <img src={item.icon} alt="" />
                </a>
              ))}
            </div>
          ) : null}
        </div>
      </div>

      <div className="shell footer-legal">
        <span>
          © {new Date().getFullYear()} Mechanical Engineering Program · RUPP
        </span>
        {/* The three logo colours, in the order they appear in the wordmark.
            Ink variants, because the vivid green scores 2.4 on white. */}
        <span className="footer-motto">
          <b>Nature</b>
          <i aria-hidden="true">·</i>
          <b>Nurture</b>
          <i aria-hidden="true">·</i>
          <b>Nourish</b>
        </span>
      </div>
    </footer>
  );
}
