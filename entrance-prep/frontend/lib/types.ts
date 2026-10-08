export type User = {
  id: string;
  name: string;
  email: string;
  role: "teacher" | "student";
};
export type Domain = {
  id: string;
  subject: string;
  name: string;
  description: string;
  skills: string[];
};
export type Subject = {
  id: string;
  short: string;
  name: string;
  description: string;
  domains: string[];
};
export type Catalog = {
  subjects: Subject[];
  domains: Domain[];
  levels: string[];
  level_guide: Record<string, string>;
};
export type Option = {
  id: string;
  text: string;
  rationale?: string;
  error?: string;
};
export type Content = {
  stem: string;
  options: Option[];
  correct?: string;
  explanation?: string;
  math?: string | null;
  presentation: "text" | "image" | "diagram";
  asset: string | null;
  asset_alt: string;
  diagram: { kind: string; labels: string[] } | null;
  validator?: Record<string, unknown> | null;
};
export type Question = {
  id: string;
  subject: string;
  domain: string;
  difficulty: string;
  skill: string;
  status: string;
  version: number;
  content: Content;
  source: Record<string, unknown>;
  validation: {
    passed: boolean;
    method: string;
    proof: string;
    errors: string[];
    note: string;
  };
};
export type AttemptQuestion = {
  id: string;
  domain: string;
  difficulty: string;
  skill: string;
  content: Content;
  attribution?: string | null;
  feedback?: {
    correct: string;
    explanation: string;
    math: string | null;
    options: Option[];
    is_correct: boolean;
  };
};
export type Attempt = {
  id: string;
  title: string;
  mode: string;
  questions: AttemptQuestion[];
  answers: Record<string, string>;
  deadline: string | null;
  submitted: string | null;
  score: number | null;
  server_time: string;
};
export type Row = {
  domain: string;
  difficulty: string;
  count: number;
  options: number;
  skill?: string;
};
export type Blueprint = {
  id: string;
  name: string;
  minutes: number;
  rows: Row[];
  published: boolean;
};
export type StudentRow = {
  id: string;
  name: string;
  email: string;
  anonymous: boolean;
  registered: string | null;
  sessions: number;
  answered: number;
  correct: number;
  accuracy: number | null;
  last_active: string | null;
  subjects: { subject: string; answered: number; correct: number }[];
};
export type StudentDetail = {
  id: string;
  name: string;
  email: string;
  registered: string | null;
  sessions: {
    id: string;
    title: string;
    mode: string;
    score: number;
    total: number;
    submitted: string;
  }[];
  topics: {
    domain: string;
    subject: string;
    answered: number;
    correct: number;
  }[];
};
export type Analytics = {
  scope: string;
  attempts: number;
  questions: number;
  correct: number;
  groups: { kind: string; label: string; total: number; correct: number }[];
  errors: { label: string; count: number }[];
  note: string;
};
