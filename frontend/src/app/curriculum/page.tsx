import CurriculumTabs from "@/components/CurriculumTabs";
import Breadcrumbs from "@/components/Breadcrumbs";
import SiteFooter from "@/components/SiteFooter";
import SiteHeader from "@/components/SiteHeader";
import { getHomeData } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function CurriculumPage() {
  const home = await getHomeData();

  return (
    <>
      <SiteHeader settings={home.settings} />
      <main id="main-content" className="editorial-page">
        <Breadcrumbs
          trail={[{ label: "Teaching & Learning" }, { label: "Curriculum" }]}
        />
        <section className="directory-hero is-compact">
          <div className="shell">
            <p className="eyebrow light">Academics</p>
            <h1>Curriculum</h1>
            <p>
              The four-year study plan, from scientific foundations to
              integrated design, industry experience, and professional
              engineering practice.
            </p>
          </div>
        </section>

        <section className="section cream curriculum-page-section">
          <div className="shell">
            <div className="section-intro">
              <div>
                <p className="eyebrow">Four-year study plan</p>
                <h2>Courses by year and semester</h2>
              </div>
              <p>
                Select a year to review its theme, credit count, and courses by
                semester.
              </p>
            </div>
            <CurriculumTabs years={home.curriculum} />
          </div>
        </section>
      </main>

      <SiteFooter
        focusAreas={home.focus_areas}
        settings={home.settings}
      />
    </>
  );
}
