/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import type { ProgramSettings } from "@/lib/api";

type AdmissionBarProps = {
  settings: Pick<
    ProgramSettings,
    | "address"
    | "email"
    | "facebook_url"
    | "linkedin_url"
    | "phone"
    | "program_name"
    | "telegram_url"
    | "youtube_url"
  >;
};

export default function AdmissionBar({ settings }: AdmissionBarProps) {
  const phoneHref = `tel:${settings.phone.replace(/[^\d+]/g, "")}`;
  const contactLinks = [
    {
      label: `Email ${settings.email}`,
      href: `mailto:${settings.email}`,
      icon: "/assets/icons/mail.svg",
    },
    {
      label: `Call ${settings.phone}`,
      href: phoneHref,
      icon: "/assets/icons/phone.svg",
    },
    settings.facebook_url
      ? {
          label: "Join ME RUPP on Facebook",
          href: settings.facebook_url,
          icon: "/assets/icons/facebook.svg",
        }
      : null,
    settings.telegram_url
      ? {
          label: "Join ME RUPP on Telegram",
          href: settings.telegram_url,
          icon: "/assets/icons/telegram.svg",
        }
      : null,
    settings.youtube_url
      ? {
          label: "Watch ME RUPP on YouTube",
          href: settings.youtube_url,
          icon: "/assets/icons/youtube.svg",
        }
      : null,
    settings.linkedin_url
      ? {
          label: "Follow ME RUPP on LinkedIn",
          href: settings.linkedin_url,
          icon: "/assets/icons/linkedin.svg",
        }
      : null,
  ].filter(Boolean) as Array<{
    label: string;
    href: string;
    icon: string;
  }>;

  return (
    <aside className="admission-dock" aria-label="Admissions and program contact">
      <div className="admission-card">
        <div className="admission-identity">
          <strong>{settings.program_name} · ME@FE@RUPP</strong>
          <span>{settings.address}</span>
        </div>

        <Link className="admission-primary" href="/admissions">
          Admissions
          <span aria-hidden="true">→</span>
        </Link>

        <div className="admission-actions" aria-label="Contact and social media">
          {contactLinks.map((link) => {
            const external = link.href.startsWith("http");
            return (
              <a
                className="contact-icon"
                href={link.href}
                aria-label={link.label}
                title={link.label}
                target={external ? "_blank" : undefined}
                rel={external ? "noreferrer" : undefined}
                key={link.label}
              >
                <img src={link.icon} alt="" aria-hidden="true" />
              </a>
            );
          })}
        </div>
      </div>
    </aside>
  );
}
