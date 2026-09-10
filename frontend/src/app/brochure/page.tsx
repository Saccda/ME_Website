import type { Metadata } from "next";
import Breadcrumbs from "@/components/Breadcrumbs";
import Flipbook from "@/components/flipbook/Flipbook";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
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
    "The Mechanical Engineering program at the Royal University of Phnom Penh, as a ten-page illustrated brochure: vision and mission, the four areas of focus, the four-year curriculum, research, and collaboration.",
};

export default async function BrochurePage() {
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
