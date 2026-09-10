/* eslint-disable @next/next/no-img-element */
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import StoryBody from "@/components/StoryBody";
import { getFacility, getHomeData } from "@/lib/api";

export const dynamic = "force-dynamic";

type MachinePageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({
  params,
}: MachinePageProps): Promise<Metadata> {
  const { slug } = await params;
  const lookup = await getFacility(slug);
  if (lookup.status !== "found") {
    return { title: "Facilities | Mechanical Engineering RUPP" };
  }
  return {
    title: `${lookup.facility.name} | Facilities | Mechanical Engineering RUPP`,
    description: lookup.facility.description,
  };
}

export default async function MachinePage({ params }: MachinePageProps) {
  const { slug } = await params;
  const [lookup, home] = await Promise.all([getFacility(slug), getHomeData()]);

  if (lookup.status === "not-found") notFound();

  if (lookup.status === "unavailable") {
    return (
      <>
        <SiteHeader settings={home.settings} />
        <main className="editorial-page" id="main-content">
          <section className="section white">
            <div className="shell">
              <div className="content-empty-state">
                <h1>This machine is temporarily unavailable.</h1>
                <p>
                  The equipment catalogue could not be reached. Please try again
                  shortly, or return to the facilities page.
                </p>
                <Link className="text-link" href="/facilities">
                  All facilities <span aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          </section>
        </main>
        <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
      </>
    );
  }

  const machine = lookup.facility;

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main className="editorial-page" id="main-content">
        <Breadcrumbs
          trail={[
            { label: "Teaching & Learning" },
            { label: "Facilities", href: "/facilities" },
            { label: machine.name },
          ]}
        />

        <section className="section white machine-detail">
          <div className="shell">
            <header className="machine-head">
              <p className="eyebrow">Laboratory equipment</p>
              <h1>{machine.name}</h1>
              <p className="machine-summary">{machine.description}</p>
              <div className="machine-tags">
                <span
                  className="machine-status"
                  data-status={machine.availability_status}
                >
                  {machine.availability_label}
                </span>
                {machine.focus_areas.map((area) => (
                  <Link
                    className="machine-area"
                    href={`/focus/${area.slug}`}
                    key={area.code}
                    style={{ ["--chip" as string]: area.accent_color }}
                  >
                    {area.code} — {area.title}
                  </Link>
                ))}
              </div>
            </header>

            {machine.image ? (
              <figure className="machine-media">
                <img alt={machine.name} src={machine.image} />
              </figure>
            ) : null}

            {machine.detail.length > 0 ? (
              <StoryBody blocks={machine.detail} galleryTitle={machine.name} />
            ) : (
              <p className="machine-empty">
                A full description of this machine has not been published yet.
              </p>
            )}

            {machine.reference_url ? (
              <p className="machine-reference">
                <a
                  href={machine.reference_url}
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  Manufacturer reference <span aria-hidden="true">↗</span>
                </a>
              </p>
            ) : null}

            <p className="machine-back">
              <Link className="text-link" href="/facilities">
                <span aria-hidden="true">←</span> All laboratory equipment
              </Link>
            </p>
          </div>
        </section>
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
