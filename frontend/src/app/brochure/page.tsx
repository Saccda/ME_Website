import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Breadcrumbs from "@/components/Breadcrumbs";
import Flipbook from "@/components/flipbook/Flipbook";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { features } from "@/config/features";
import { buildBrochurePages } from "@/data/brochurePages";
import {
  getFacilities,
  getHomeData,
  getNewsEvents,
  getResearchProjects,
} from "@/lib/api";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Program brochure | Mechanical Engineering RUPP",
  description:
    "The Mechanical Engineering program at the Royal University of Phnom Penh, as an illustrated page-turning brochure: vision and mission, engineering in the age of AI, the four areas of focus, the four-year curriculum, learning by doing with CDIO, research, collaboration and automotive career routes.",
};

export default async function BrochurePage() {
  // Unpublished: the page answers 404 on the published site, and renders as
  // usual wherever the site runs in development.
  if (!features.brochure) notFound();

  // The pictures are the program's own, so the brochure reads the CMS the way
  // every other page does. Each one falls back to a repository copy, so an
  // unreachable API costs the brochure its photographs and nothing else.
  const [home, facilities, research, news] = await Promise.all([
    getHomeData(),
    getFacilities(),
    getResearchProjects(),
    getNewsEvents(),
  ]);

  const pages = buildBrochurePages({
    focusAreas: home.focus_areas,
    research,
    facilities,
    news,
    partners: home.partners,
  });

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main className="editorial-page" id="main-content">
        <Breadcrumbs
          trail={[{ label: "About" }, { label: "Program brochure" }]}
        />
        <Flipbook
          pages={pages}
          subtitle="FACULTY OF ENGINEERING · RUPP"
          title="Mechanical Engineering — Program Brochure"
        />
      </main>
      <SiteFooter focusAreas={home.focus_areas} settings={home.settings} />
    </>
  );
}
