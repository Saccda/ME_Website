/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import type { FocusArea, ProgramSettings } from "@/lib/api";

type SiteFooterProps = {
  focusAreas: Array<Pick<FocusArea, "code" | "slug" | "title">>;
  settings: ProgramSettings;
};

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
            src="/assets/brand/me-wordmark.png"
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
          <Link href="/#what-is-me">What is mechanical engineering?</Link>
          <Link href="/#why-me">Why choose ME</Link>
          <Link href="/about">Program profile</Link>
          <Link href="/curriculum">Curriculum</Link>
          <Link href="/people#faculty-staff">Faculty</Link>
          <Link href="/facilities">Facilities</Link>
        </nav>

        <nav aria-label="Focus-area footer links">
          <h2>Areas of focus</h2>
          {focusAreas.map((area) => (
            <Link href={`/focus/${area.slug}`} key={area.code}>
              <span>{area.code}</span> {area.title}
            </Link>
          ))}
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
        <span>Nature · Nurture · Nourish</span>
      </div>
    </footer>
  );
}
