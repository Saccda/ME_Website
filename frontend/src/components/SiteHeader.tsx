/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import type { ProgramSettings } from "@/lib/api";
import AdmissionBar from "./AdmissionBar";

const navItems = [
  {
    label: "About",
    links: [
      ["What is mechanical engineering?", "/#what-is-me"],
      ["Why choose ME", "/#why-me"],
      ["Vision & mission", "/about"],
    ],
  },
  {
    label: "Academics",
    links: [
      ["Areas of focus", "/#focus"],
      ["Curriculum", "/curriculum"],
    ],
  },
  {
    label: "Research & Innovation",
    links: [
      ["Applied research", "/#research"],
      ["Partners & collaboration", "/#partners"],
      ["Job opportunities", "/#opportunities"],
    ],
  },
  {
    label: "People",
    links: [
      ["Faculty & staff", "/people#faculty-staff"],
      ["Alumni", "/people#alumni"],
    ],
  },
  {
    label: "News & Events",
    links: [
      ["Latest news", "/news-events#latest"],
      ["Upcoming events", "/news-events#events"],
      ["Seminars & publications", "/news-events#publications"],
    ],
  },
] as const;

type SiteHeaderProps = {
  settings: ProgramSettings;
};

export default function SiteHeader({ settings }: SiteHeaderProps) {
  return (
    <>
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>

      <header className="site-header">
        <div className="header-shell header-inner">
          <Link
            className="brand"
            href="/"
            aria-label="Mechanical Engineering Program home"
          >
            <span className="brand-marks" aria-hidden="true">
              <img
                className="rupp-mark"
                src="/assets/brand/rupp-logo.png"
                alt=""
              />
              <img
                className="fe-mark"
                src="/assets/brand/fe-logo-transparent.png"
                alt=""
              />
              <img className="me-mark" src="/assets/me-logo.png" alt="" />
            </span>
            <span className="brand-divider" aria-hidden="true" />
            <img
              className="me-wordmark"
              src="/assets/brand/me-wordmark.png"
              alt="Mechanical Engineering — Nature, Nurture, Nourish"
            />
          </Link>

          <nav className="desktop-nav" aria-label="Main navigation">
            {navItems.map((item) =>
              "links" in item ? (
                <div className="nav-dropdown" key={item.label}>
                  <button type="button" aria-haspopup="true">
                    {item.label}
                    <span className="nav-chevron" aria-hidden="true" />
                  </button>
                  <div className="nav-dropdown-menu">
                    {item.links.map(([label, href]) => (
                      <Link href={href} key={href}>
                        {label}
                      </Link>
                    ))}
                  </div>
                </div>
              ) : null,
            )}
          </nav>

          <details className="mobile-menu">
            <summary aria-label="Open navigation">
              <span />
              <span />
              <span />
            </summary>
            <nav>
              {navItems.map((item) =>
                "links" in item ? (
                  <details className="mobile-nav-group" key={item.label}>
                    <summary>
                      {item.label}
                      <span aria-hidden="true">+</span>
                    </summary>
                    <div>
                      {item.links.map(([label, href]) => (
                        <Link href={href} key={href}>
                          {label}
                        </Link>
                      ))}
                    </div>
                  </details>
                ) : null,
              )}
            </nav>
          </details>
        </div>
      </header>

      <AdmissionBar settings={settings} />
    </>
  );
}
