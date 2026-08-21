export type AdmissionMilestone = {
  step: number;
  title: string;
  date: string;
};

export type EntranceSubject = {
  code: string;
  name: string;
};

export const admissionsContent = {
  cycleLabel: "Current admission cycle",
  milestones: [
    // Non-breaking spaces keep each day+month together, so a range that has to
    // wrap breaks at the separator instead of splitting "30 September".
    { step: 1, title: "Registration", date: "17 August - 30 September" },
    { step: 2, title: "Entrance Exam", date: "10 October" },
    { step: 3, title: "Results Announcement", date: "07 November" },
    { step: 4, title: "Tuition Fee Payment", date: "07 - 21 November" },
    { step: 5, title: "Start of Academic Year", date: "26 November" },
  ] satisfies AdmissionMilestone[],
  subjects: [
    { code: "M", name: "Mathematics" },
    { code: "P", name: "Physics" },
    { code: "L", name: "Logic" },
  ] satisfies EntranceSubject[],
  pastExamsUrl: "https://gqr.sh/yGBu",
  applicationForm: {
    downloadUrl:
      "/assets/admissions/rupp-application-forms-sample.pdf" as string | null,
    previewImage: null as string | null,
    status: "hard-copy-only" as const,
    /**
     * Photographs of a completed set, so an applicant can see how much goes in
     * each field before they are handed the paper.
     *
     * Three things are covered and nothing else: the name in both scripts, the
     * signature, and the photograph. Everything else stays legible -- the
     * birthplace, the schools, the dates, the ticked faculty, the department --
     * because a sample an applicant cannot read teaches them nothing.
     *
     * Those three stay covered because they are what identifies a real person
     * rather than describing a form. A signature in particular is worth
     * keeping off a public page whatever else is shown.
     */
    sheets: [
      {
        image: "/assets/admissions/02-exam-application.webp",
        title: "Faculty choice",
        khmer: "ពាក្យសុំចុះឈ្មោះប្រឡង",
        note: "Tick one faculty. Engineering is ticked here, with the department written at the foot.",
      },
      {
        image: "/assets/admissions/03-registration.webp",
        title: "Application to sit the entrance examination",
        khmer: "ពាក្យសុំចុះឈ្មោះ",
        note: "Carries the checklist of documents to attach, including three 4x6 photographs.",
      },
      {
        image: "/assets/admissions/01-biography.webp",
        title: "Personal history",
        khmer: "ជីវប្រវត្តិសង្ខេប",
        note: "Family details, address, and the schools attended.",
      },
      {
        image: "/assets/admissions/04-identity-slips.webp",
        title: "Identity slips",
        khmer: "សលាកបត្រឯកត្តជន",
        note: "The same slip twice on one sheet; fill in both.",
      },
    ],
  },
};
