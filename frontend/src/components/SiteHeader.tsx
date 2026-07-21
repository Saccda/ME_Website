/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import type { ProgramSettings } from "@/lib/api";
import AdmissionBar from "./AdmissionBar";

const navItems = [
  ["Why ME", "why-me"],
  ["Vision & Mission", "vision"],
  ["Focus", "focus"],
  ["Curriculum", "curriculum"],
  ["Research", "research"],
  ["Partners", "partners"],
  ["Contact", "contact"],
];

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
            {navItems.map(([label, id]) => (
              <Link href={`/#${id}`} key={id}>
                {label}
              </Link>
            ))}
            <a
              className="nav-cta"
              href={settings.application_url || "/#contact"}
            >
              Apply
            </a>
          </nav>

          <details className="mobile-menu">
            <summary aria-label="Open navigation">
              <span />
              <span />
              <span />
            </summary>
            <nav>
              {navItems.map(([label, id]) => (
                <Link href={`/#${id}`} key={id}>
                  {label}
                </Link>
              ))}
              <a
                className="nav-cta"
                href={settings.application_url || "/#contact"}
              >
                Apply
              </a>
            </nav>
          </details>
        </div>
      </header>

      <AdmissionBar settings={settings} />
    </>
  );
}
