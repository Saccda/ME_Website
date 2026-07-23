"use client";

import { useState } from "react";
import type { CurriculumYear } from "@/lib/api";

export default function CurriculumTabs({ years }: { years: CurriculumYear[] }) {
  const [activeYear, setActiveYear] = useState(years[0]?.year ?? 1);
  const selected = years.find((item) => item.year === activeYear) || years[0];

  if (!selected) {
    return <p>Curriculum information will be available soon.</p>;
  }

  const semesterGroups = [
    { key: "1", label: "Semester 1" },
    { key: "2", label: "Semester 2" },
    { key: "full", label: "Full-year courses" },
  ]
    .map((semester) => ({
      ...semester,
      courses: selected.courses.filter(
        (course) => course.semester === semester.key,
      ),
    }))
    .filter((semester) => semester.courses.length > 0);

  return (
    <div className="curriculum-card">
      <div className="year-panel">
        <small>Selected study plan</small>
        <h3>
          Year <strong>{selected.year}</strong>
        </h3>
        <h4>{selected.theme}</h4>
        <div className="credit-count">
          <strong>{selected.credit_count}</strong>
          <span>credits this year</span>
        </div>
        <p>{selected.description}</p>
      </div>
      <div className="course-panel">
        <div className="year-tabs" role="tablist" aria-label="Curriculum year">
          {years.map((item) => (
            <button
              className={item.year === selected.year ? "active" : ""}
              key={item.year}
              onClick={() => setActiveYear(item.year)}
              role="tab"
              aria-selected={item.year === selected.year}
            >
              Year {item.year}
            </button>
          ))}
        </div>
        <div className="semester-groups">
          {semesterGroups.map((semester) => {
            const semesterCredits = semester.courses.reduce(
              (total, course) => total + course.credits,
              0,
            );

            return (
              <section className="semester-block" key={semester.key}>
                <header className="semester-heading">
                  <h4>{semester.label}</h4>
                  <span>
                    {semester.courses.length} courses · {semesterCredits} credits
                  </span>
                </header>
                <div className="course-heading" aria-hidden="true">
                  <span>Code</span>
                  <span>Course name</span>
                  <span>Credits</span>
                </div>
                <div className="course-list">
                  {semester.courses.map((course) => (
                    <div className="course-row" key={course.code}>
                      <span className="course-code">{course.code}</span>
                      <strong>{course.title}</strong>
                      <span>{course.credits}</span>
                    </div>
                  ))}
                </div>
              </section>
            );
          })}
        </div>
      </div>
    </div>
  );
}
