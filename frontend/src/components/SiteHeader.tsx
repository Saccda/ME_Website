/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import {
  navigationItems,
  type NavigationLink,
} from "@/config/navigation";
import type { ProgramSettings } from "@/lib/api";
import AdmissionBar from "./AdmissionBar";

type SiteHeaderProps = {
  settings: ProgramSettings;
};

function DesktopNavigationLink({ item }: { item: NavigationLink }) {
  if (item.children) {
    return (
      <div className="nav-submenu">
        {item.href ? (
          <Link className="nav-submenu-trigger" href={item.href} aria-haspopup="true">
            {item.label}
            <span className="nav-submenu-chevron" aria-hidden="true" />
          </Link>
        ) : (
          <button type="button" aria-haspopup="true">
            {item.label}
            <span className="nav-submenu-chevron" aria-hidden="true" />
          </button>
        )}
        <div className="nav-submenu-menu">
          {item.children.map((child) => (
            <Link href={child.href || "/"} key={`${child.label}-${child.href}`}>
              {child.label}
            </Link>
          ))}
        </div>
      </div>
    );
  }

  return <Link href={item.href || "/"}>{item.label}</Link>;
}

function MobileNavigationLink({ item }: { item: NavigationLink }) {
  if (item.children) {
    return (
      <details className="mobile-nav-subgroup">
        <summary>
          {item.label}
          <span aria-hidden="true">+</span>
        </summary>
        <div>
          {item.href ? (
            <Link className="mobile-nav-overview" href={item.href}>
              {item.label} overview
            </Link>
          ) : null}
          {item.children.map((child) => (
            <Link href={child.href || "/"} key={`${child.label}-${child.href}`}>
              {child.label}
            </Link>
          ))}
        </div>
      </details>
    );
  }

  return <Link href={item.href || "/"}>{item.label}</Link>;
}

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
                src="/assets/brand/rupp-logo.webp"
                alt=""
              />
              <img
                className="fe-mark"
                src="/assets/brand/fe-logo-transparent.webp"
                alt=""
              />
              <img className="me-mark" src="/assets/me-logo.webp" alt="" />
            </span>
            <span className="brand-divider" aria-hidden="true" />
            <img
              className="me-wordmark"
              src="/assets/brand/me-wordmark.webp"
              alt="Mechanical Engineering — Nature, Nurture, Nourish"
            />
          </Link>

          <nav className="desktop-nav" aria-label="Main navigation">
            {navigationItems.map((item) => (
              <div className="nav-dropdown" key={item.label}>
                {item.href ? (
                  <Link
                    className="nav-dropdown-trigger"
                    href={item.href}
                    aria-haspopup="true"
                  >
                    {item.label}
                    <span className="nav-chevron" aria-hidden="true" />
                  </Link>
                ) : (
                  <button type="button" aria-haspopup="true">
                    {item.label}
                    <span className="nav-chevron" aria-hidden="true" />
                  </button>
                )}
                <div className="nav-dropdown-menu">
                  {item.links.map((link) => (
                    <DesktopNavigationLink
                      item={link}
                      key={`${link.label}-${link.href || "group"}`}
                    />
                  ))}
                </div>
              </div>
            ))}
          </nav>

          <details className="mobile-menu">
            <summary aria-label="Open navigation">
              <span />
              <span />
              <span />
            </summary>
            <nav>
              {navigationItems.map((item) => (
                <details className="mobile-nav-group" key={item.label}>
                  <summary>
                    {item.label}
                    <span aria-hidden="true">+</span>
                  </summary>
                  <div>
                    {item.href ? (
                      <Link className="mobile-nav-overview" href={item.href}>
                        {item.overviewLabel ?? `${item.label} overview`}
                      </Link>
                    ) : null}
                    {item.links.map((link) => (
                      <MobileNavigationLink
                        item={link}
                        key={`${link.label}-${link.href || "group"}`}
                      />
                    ))}
                  </div>
                </details>
              ))}
            </nav>
          </details>
        </div>
      </header>

      <AdmissionBar settings={settings} />
    </>
  );
}
