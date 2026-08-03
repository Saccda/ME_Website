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
    downloadUrl: null as string | null,
    previewImage: null as string | null,
    status: "hard-copy-only" as const,
  },
};
