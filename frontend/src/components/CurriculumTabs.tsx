"use client";

import { useState } from "react";
import type { CurriculumYear } from "@/lib/api";

export default function CurriculumTabs({ years }: { years: CurriculumYear[] }) {
  const [activeYear, setActiveYear] = useState(years[0]?.year ?? 1);
  const selected = years.find((item) => item.year === activeYear) || years[0];

  if (!selected) {
    return <p>Curriculum information will be available soon.</p>;
  }

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
        <div className="course-heading">
          <span>Course</span>
          <span>Code</span>
          <span>Credits</span>
        </div>
        <div className="course-list">
          {selected.courses.map((course) => (
            <div className="course-row" key={course.code}>
              <strong>{course.title}</strong>
              <span>{course.code}</span>
              <span>{course.credits}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
