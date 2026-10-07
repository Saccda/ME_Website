"use client";
import { useCallback, useEffect, useState, type ReactNode } from "react";
import {
  ArrowRight,
  BookOpen,
  Check,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Clock3,
  Download,
  FileCheck2,
  GraduationCap,
  Layers3,
  LayoutDashboard,
  Plus,
  RefreshCw,
  Search,
  Settings2,
  ShieldCheck,
  Sparkles,
  Target,
  Trash2,
  TrendingUp,
  X,
  Menu,
  BrainCircuit,
  CircleHelp,
  Shapes,
  Network,
  Binary,
  MessageSquareText,
  ListOrdered,
  LogOut,
  Users,
  XCircle,
  MinusCircle,
} from "lucide-react";
import katex from "katex";
import { api } from "@/lib/api";
import type {
  Analytics,
  Attempt,
  Blueprint,
  Catalog,
  Content,
  Domain,
  Question,
  Row,
  StudentDetail,
  StudentRow,
  User,
} from "@/lib/types";

const domainIcons = [
  TrendingUp,
  Shapes,
  Network,
  Binary,
  MessageSquareText,
  ListOrdered,
  BrainCircuit,
];
const human = (s: string) =>
  s.replaceAll("-", " ").replace(/\b\w/g, (c) => c.toUpperCase());
const date = (s: string) =>
  new Date(s).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });

function MathText({ text }: { text?: string | null }) {
  if (!text) return null;
  return (
    <span
      className="math"
      dangerouslySetInnerHTML={{
        __html: katex.renderToString(text, {
          throwOnError: false,
          trust: false,
          strict: false,
        }),
      }}
    />
  );
}
function RichText({ text }: { text: string }) {
  return (
    <>
      {text
        .split(/(\$[^$]+\$)/g)
        .map((part, i) =>
          part.startsWith("$") && part.endsWith("$") ? (
            <MathText key={i} text={part.slice(1, -1)} />
          ) : (
            <span key={i}>{part}</span>
          ),
        )}
    </>
  );
}
function Visual({ content }: { content: Content }) {
  if (content.presentation === "image" && content.asset)
    return (
      <img
        className="question-image"
        src={content.asset}
        alt={content.asset_alt}
      />
    );
  if (content.presentation === "diagram" && content.diagram)
    return (
      <div
        className="diagram"
        aria-label={
          content.diagram.kind === "stations"
            ? "Station positions from left to right"
            : "Reasoning diagram"
        }
      >
        {content.diagram.labels.map((x, i) => (
          <div key={i}>
            <span className="diagram-box">{x}</span>
            {i < content.diagram!.labels.length - 1 &&
              content.diagram!.kind !== "stations" && <ArrowRight size={16} />}
          </div>
        ))}
      </div>
    );
  return null;
}
function Badge({
  children,
  color = "blue",
}: {
  children: ReactNode;
  color?: string;
}) {
  return <span className={"badge " + color}>{children}</span>;
}
function Empty({ title, body }: { title: string; body: string }) {
  return (
    <div className="empty">
      <BookOpen size={32} />
      <h3>{title}</h3>
      <p>{body}</p>
    </div>
  );
}
function Modal({
  title,
  close,
  children,
}: {
  title: string;
  close: () => void;
  children: ReactNode;
}) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    document.addEventListener("keydown", onKey);
    const old = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = old;
    };
  }, [close]);
  return (
    <div className="modal-backdrop">
      <section
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="modal"
      >
        <div className="modal-heading">
          <h2>{title}</h2>
          <button
            className="icon-button"
            aria-label="Close dialog"
            onClick={close}
          >
            <X />
          </button>
        </div>
        {children}
      </section>
    </div>
  );
}

function AuthGate({
  demo,
  onSignedIn,
}: {
  demo: boolean;
  onSignedIn: (user: User) => void;
}) {
  const [mode, setMode] = useState<"signup" | "signin">("signup");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const signup = mode === "signup";
  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (busy) return;
    setBusy(true);
    setError("");
    try {
      onSignedIn(
        signup
          ? await api<User>("/auth/register", "POST", {
              name: name.trim(),
              email: email.trim(),
              password,
            })
          : await api<User>("/auth/login", "POST", {
              email: email.trim(),
              password,
            }),
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="login-shell">
      <div className="login-story">
        <div className="login-brand">
          <img src="/brand/me-logo.png" alt="Mechanical Engineering @ RUPP" />
          <div>
            ME @ RUPP<span>LOGIC STUDIO</span>
          </div>
        </div>
        <h1>Prepare with reasoning you can check.</h1>
        <p>
          Practise the reasoning the entrance exam asks for, with a worked
          explanation behind every answer.
        </p>
        <div className="login-principles">
          <span>
            <ShieldCheck size={19} /> Every question is reviewed before it
            reaches you.
          </span>
          <span>
            <GraduationCap size={19} /> Guided practice first, timed exams when
            you are ready.
          </span>
          <span>
            <TrendingUp size={19} /> See which reasoning patterns to revisit.
          </span>
        </div>
        <div className="login-bottom">
          Mechanical Engineering · Faculty of Engineering · Royal University of
          Phnom Penh
        </div>
      </div>
      <div className="login-form">
        <div>
          <h2>{signup ? "Create your account" : "Sign in"}</h2>
          <p className="help">
            {signup
              ? "Your account keeps your practice history and results on this site."
              : "Welcome back. Continue where you left off."}
          </p>
          <form onSubmit={submit}>
            {signup && (
              <label>
                Full name
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  maxLength={100}
                  autoComplete="name"
                />
              </label>
            )}
            <label>
              Email
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                maxLength={254}
                autoComplete="email"
              />
            </label>
            <label>
              Password
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={signup ? 12 : 1}
                autoComplete={signup ? "new-password" : "current-password"}
              />
              {signup && (
                <span className="help">
                  At least 12 characters. Do not reuse a password from another
                  site.
                </span>
              )}
            </label>
            {error && (
              <p className="help" role="alert" style={{ color: "var(--red)" }}>
                {error}
              </p>
            )}
            <button className="button" type="submit" disabled={busy}>
              {busy
                ? "Please wait…"
                : signup
                  ? "Create account"
                  : "Sign in"}
            </button>
          </form>
          <button
            className="button secondary login-toggle"
            onClick={() => {
              setMode(signup ? "signin" : "signup");
              setError("");
            }}
          >
            {signup
              ? "I already have an account"
              : "I need to create an account"}
          </button>
          {demo && (
            <div className="demo-login">
              <strong>Demonstration site</strong>
              <p className="help">
                Sample questions are pre-approved for testing. Do not enter a
                password you use anywhere else.
              </p>
            </div>
          )}
          <div className="login-logos">
            <img src="/brand/rupp-logo.png" alt="Royal University of Phnom Penh" />
            <img src="/brand/fe-logo.png" alt="Faculty of Engineering" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [user, setUser] = useState<User | null>(null),
    [authMode, setAuthMode] = useState("open"),
    [catalog, setCatalog] = useState<Catalog | null>(null),
    [loading, setLoading] = useState(true),
    [demo, setDemo] = useState(false),
    [view, setView] = useState("overview"),
    [error, setError] = useState(""),
    [notice, setNotice] = useState(""),
    [busy, setBusy] = useState(false),
    [mobile, setMobile] = useState(false);
  const [bank, setBank] = useState<Question[]>([]),
    [blueprints, setBlueprints] = useState<Blueprint[]>([]),
    [analytics, setAnalytics] = useState<Analytics | null>(null),
    [attempts, setAttempts] = useState<
      {
        id: string;
        title: string;
        mode: string;
        submitted: boolean;
        started: string;
        count: number;
      }[]
    >([]);
  const [editing, setEditing] = useState<Question | null>(null),
    [detail, setDetail] = useState<Question | null>(null),
    [selected, setSelected] = useState<string[]>([]),
    [attempt, setAttempt] = useState<Attempt | null>(null),
    [index, setIndex] = useState(0);
  const [students, setStudents] = useState<StudentRow[]>([]),
    [studentDetail, setStudentDetail] = useState<StudentDetail | null>(null);
  const [bankSubject, setBankSubject] = useState(""),
    [domain, setDomain] = useState(""),
    [level, setLevel] = useState(""),
    [skill, setSkill] = useState(""),
    [status, setStatus] = useState(""),
    [search, setSearch] = useState("");
  const [gen, setGen] = useState({
    domain: "patterns",
    difficulty: "Foundation",
    options: 4,
    count: 5,
    presentation: "text",
    skill: "",
  });
  const [practice, setPractice] = useState({
    mode: "practice",
    subject: "",
    domain: "",
    difficulty: "",
    skill: "",
    options: 4,
    count: 5,
    minutes: 15,
    origin: "all",
  });
  const [bpEdit, setBpEdit] = useState<string | null>(null);
  const [bpName, setBpName] = useState("Logic readiness"),
    [bpMinutes, setBpMinutes] = useState(25),
    [bpRows, setBpRows] = useState<Row[]>([
      { domain: "patterns", difficulty: "Practice", count: 2, options: 4 },
    ]),
    [bpPublished, setBpPublished] = useState(true);
  const [availability, setAvailability] = useState<
    {
      subject: string;
      domain: string;
      difficulty: string;
      skill: string;
      options: number;
      count: number;
      origin: string;
    }[]
  >([]);
  const [exportKind, setExportKind] = useState("paper");
  const refresh = useCallback(async (u: User) => {
    const results = await Promise.all([
      api<Blueprint[]>("/blueprints"),
      api<Analytics>("/analytics"),
      api<typeof attempts>("/attempts"),
      api<typeof availability>("/availability"),
      u.role === "teacher"
        ? api<Question[]>("/questions")
        : Promise.resolve([]),
    ]);
    setBlueprints(results[0]);
    setAnalytics(results[1]);
    setAttempts(results[2]);
    setAvailability(results[3]);
    setBank(results[4]);
  }, []);
  useEffect(() => {
    (async () => {
      try {
        const [c, h] = await Promise.all([
          api<Catalog>("/catalog"),
          api<{ demo: boolean; auth_mode: string }>("/health"),
        ]);
        setCatalog(c);
        setDemo(h.demo);
        setAuthMode(h.auth_mode);
        // Outside open mode a visitor who has not signed in yet is the normal
        // first case, not a failure: show the sign-up screen rather than an error.
        const u =
          h.auth_mode === "open"
            ? await api<User>("/workspace", "POST", {})
            : await api<User>("/auth/me").catch(() => null);
        setUser(u);
        if (u) await refresh(u);
      } catch (e) {
        setError((e as Error).message);
      } finally {
        setLoading(false);
      }
    })();
    if ("serviceWorker" in navigator)
      navigator.serviceWorker.register("/sw.js").catch(() => {});
  }, [refresh]);
  // The cohort is only needed on its own screen, so it is left out of the
  // workspace refresh that runs after every action.
  useEffect(() => {
    if (view !== "students" || user?.role !== "teacher") return;
    setStudentDetail(null);
    api<StudentRow[]>("/students")
      .then(setStudents)
      .catch((e) => setError((e as Error).message));
  }, [view, user?.role]);
  async function run(task: () => Promise<void>) {
    if (busy) return;
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await task();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  function go(next: string) {
    setView(next);
    setMobile(false);
    setError("");
    setNotice("");
    setAttempt(null);
  }
  async function switchWorkspace(role: "student" | "teacher") {
    await run(async () => {
      const next = await api<User>("/workspace", "POST", { role });
      setUser(next);
      setBank([]);
      setAttempt(null);
      setDetail(null);
      setEditing(null);
      setSelected([]);
      setView("overview");
      setMobile(false);
      await refresh(next);
    });
  }
  const domainName = (id: string) =>
    catalog?.domains.find((d) => d.id === id)?.name || id;
  async function review(
    q: Question,
    action: string,
    note = "",
    attested = false,
  ) {
    await run(async () => {
      const updated = await api<Question>(`/questions/${q.id}/review`, "POST", {
        action,
        version: q.version,
        note,
        attested,
      });
      setDetail(updated);
      await refresh(user!);
      setNotice(
        `Question ${action === "review" ? "sent for review" : action === "regenerate" ? "regenerated as a draft" : action + "d"}.`,
      );
    });
  }
  async function download(format: string) {
    await run(async () => {
      const ids = selected.length
        ? selected
        : filtered.filter((q) => q.status === "approved").map((q) => q.id);
      if (!ids.length) throw new Error("Select approved questions to export.");
      const response = await fetch("/api/export", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-App-Request": "1" },
        body: JSON.stringify({ ids, format, kind: exportKind }),
        credentials: "same-origin",
      });
      if (!response.ok) {
        const e = await response.json();
        throw new Error(e.detail);
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `rupp-logic-${exportKind}.${format}`;
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      setNotice("Export downloaded.");
    });
  }
  const filtered = bank.filter(
    (q) =>
      (!bankSubject || q.subject === bankSubject) &&
      (!domain || q.domain === domain) &&
      (!level || q.difficulty === level) &&
      (!skill || q.skill === skill) &&
      (!status || q.status === status) &&
      (!search || q.content.stem.toLowerCase().includes(search.toLowerCase())),
  );
  // Anonymous open-mode workspaces are browser sessions, not students: counted
  // so nothing is hidden, but not listed, since they carry no name or address.
  const roster = students.filter((s) => !s.anonymous),
    anonymousCount = students.length - roster.length;
  if (loading)
    return (
      <div className="loading">
        <img src="/brand/me-logo.png" width="70" alt="ME @ RUPP" />
        <p>Opening Logic Studio…</p>
      </div>
    );
  if (!user && authMode !== "open")
    return (
      <AuthGate
        demo={demo}
        onSignedIn={async (signed) => {
          setUser(signed);
          setError("");
          await refresh(signed);
        }}
      />
    );
  if (!user)
    return (
      <div className="loading">
        <img src="/brand/me-logo.png" width="70" alt="ME @ RUPP" />
        <h2>Open your Logic workspace</h2>
        <p role="alert">{error || "Connecting to your learning workspace…"}</p>
        <button className="button" onClick={() => window.location.reload()}>
          Try again
        </button>
      </div>
    );
  const nav = [
    { id: "overview", label: "Overview", icon: LayoutDashboard },
    { id: "practice", label: "Student practice", icon: GraduationCap },
    ...(user.role === "teacher"
      ? [
          { id: "generate", label: "Generation studio", icon: Sparkles },
          { id: "bank", label: "Question bank", icon: Layers3 },
          { id: "blueprints", label: "Mock exam blueprints", icon: Target },
          { id: "students", label: "Students", icon: Users },
        ]
      : [{ id: "blueprints", label: "Mock exams", icon: Target }]),
    { id: "analytics", label: "Learning insights", icon: TrendingUp },
  ];
  const approved = bank.filter((q) => q.status === "approved").length,
    pending = bank.filter(
      (q) => q.status === "draft" || q.status === "review",
    ).length;
  return (
    <div className="app-shell">
      <aside className={"sidebar " + (mobile ? "open" : "")}>
        <a
          href="#"
          className="brand"
          onClick={(e) => {
            e.preventDefault();
            go("overview");
          }}
        >
          <img src="/brand/me-logo.png" alt="Mechanical Engineering logo" />
          <div>
            ME @ RUPP<span>LOGIC STUDIO</span>
          </div>
        </a>
        <div className="workspace-label">
          {user.role === "teacher" ? "TEACHER WORKSPACE" : "STUDENT WORKSPACE"}
        </div>
        {/* Choosing a workspace is only a convenience in open mode. Once people
            sign in, the role comes from the account and must not be switchable
            from the browser, or a student could open the answer key. */}
        {authMode === "open" && (
          <div
            className="segmented workspace-switch"
            aria-label="Choose workspace"
          >
            <button
              disabled={busy}
              className={user.role === "student" ? "active" : ""}
              onClick={() => switchWorkspace("student")}
            >
              Student workspace
            </button>
            <button
              disabled={busy}
              className={user.role === "teacher" ? "active" : ""}
              onClick={() => switchWorkspace("teacher")}
            >
              Teacher studio
            </button>
          </div>
        )}
        <nav>
          {nav.map((n) => (
            <button
              key={n.id}
              className={view === n.id ? "active" : ""}
              onClick={() => go(n.id)}
            >
              <n.icon size={19} />
              {n.label}
              {n.id === "bank" && pending > 0 && (
                <span className="nav-count">{pending}</span>
              )}
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="foundation-note">
            <ShieldCheck size={21} />
            <strong>Learn. Review. Improve.</strong>
            <p>Strong reasoning starts with a strong foundation.</p>
          </div>
          <div className="user-chip">
            <div className="avatar">{user.name[0]}</div>
            <div>
              <strong>{user.name}</strong>
              <span>
                {authMode === "open" ? "No sign-in required" : user.email}
              </span>
            </div>
            {authMode === "open" ? (
              <button
                className="icon-button"
                title="Switch workspace"
                aria-label="Switch workspace"
                onClick={() =>
                  switchWorkspace(
                    user.role === "teacher" ? "student" : "teacher",
                  )
                }
              >
                <RefreshCw size={18} />
              </button>
            ) : (
              <button
                className="icon-button"
                title="Sign out"
                aria-label="Sign out"
                onClick={() =>
                  run(async () => {
                    await api("/auth/logout", "POST", {});
                    window.location.reload();
                  })
                }
              >
                <LogOut size={18} />
              </button>
            )}
          </div>
        </div>
      </aside>
      <div className="main-shell">
        <header className="topbar">
          <div className="breadcrumbs">
            <button
              className="mobile-menu icon-button"
              aria-label="Open menu"
              onClick={() => setMobile(!mobile)}
            >
              <Menu />
            </button>
            <span>Entrance preparation</span>
            <ChevronRight size={14} />
            <strong>{nav.find((n) => n.id === view)?.label}</strong>
          </div>
          <div className="topbar-right">
            <span className="live-dot" />
            <span>Logic · First edition</span>
            <img
              src="/brand/rupp-logo.png"
              alt="Royal University of Phnom Penh"
            />
            <img src="/brand/fe-logo.png" alt="Faculty of Engineering" />
          </div>
        </header>
        <main>
          {demo && (
            <div className="demo-banner">
              Demonstration workspace · Original sample questions are
              pre-approved for testing. Review them locally before real student
              use.
            </div>
          )}
          {error && (
            <div role="alert" className="alert error">
              <CircleHelp size={18} />
              {error}
              <button aria-label="Dismiss error" onClick={() => setError("")}>
                <X size={16} />
              </button>
            </div>
          )}
          {notice && (
            <div role="status" className="alert success">
              <CheckCircle2 size={18} />
              {notice}
            </div>
          )}
          {attempt ? (
            <AttemptPlayer
              attempt={attempt}
              index={index}
              setIndex={setIndex}
              busy={busy}
              update={setAttempt}
              act={run}
              refresh={() => refresh(user)}
              exit={() => {
                setAttempt(null);
                refresh(user);
              }}
              domainName={domainName}
            />
          ) : (
            <>
              {view === "overview" && (
                <>
                  <div className="page-heading">
                    <div>
                      <p className="eyebrow">
                        THEORY → PRACTICE → REFLECTION → IMPROVEMENT
                      </p>
                      <h1>
                        A stronger foundation,
                        <br />
                        one question at a time.
                      </h1>
                      <p>
                        Welcome back, {user.name}. Build the reasoning behind
                        every answer.
                      </p>
                    </div>
                    <Badge color="gold">
                      {(catalog?.subjects?.map((s) => s.short).join(" · ") ||
                        "Entrance preparation").toUpperCase()}
                    </Badge>
                  </div>
                  <section className="hero">
                    <div>
                      <Badge color="hero-badge">THINK LIKE AN ENGINEER</Badge>
                      <h2>
                        Observe the pattern.
                        <br />
                        Explain the reasoning.
                      </h2>
                      <p>
                        Checked multiple-choice practice, guided explanations,
                        <br className="desktop-break" /> and a clear path from
                        foundation to challenge.
                      </p>
                      <button
                        className="button gold-button"
                        onClick={() =>
                          go(user.role === "teacher" ? "generate" : "practice")
                        }
                      >
                        {user.role === "teacher"
                          ? "Create a practice set"
                          : "Start practicing"}
                        <ArrowRight size={18} />
                      </button>
                    </div>
                    <div className="hero-art" aria-hidden="true">
                      <div className="art-orbit one" />
                      <div className="art-orbit two" />
                      <div className="art-node n1">
                        01<span>OBSERVE</span>
                      </div>
                      <div className="art-node n2">
                        02<span>REASON</span>
                      </div>
                      <div className="art-node n3">
                        <Check size={26} />
                        <span>UNDERSTAND</span>
                      </div>
                      <div className="art-caption">
                        A → B → C<br />
                        <small>Every conclusion needs a reason.</small>
                      </div>
                    </div>
                  </section>
                  <div className="stat-grid">
                    {(user.role === "teacher"
                      ? [
                          {
                            label: "Approved questions",
                            value: approved,
                            note: "Ready for student practice",
                            icon: FileCheck2,
                          },
                          {
                            label: "Awaiting review",
                            value: pending,
                            note: "Your quality checkpoint",
                            icon: ShieldCheck,
                          },
                          {
                            label: "Topics",
                            value: catalog?.domains.length ?? 0,
                            note: "One connected learning path",
                            icon: BookOpen,
                          },
                          {
                            label: "Published mock exams",
                            value: blueprints.filter((b) => b.published).length,
                            note: "Blueprints with timed delivery",
                            icon: Target,
                          },
                        ]
                      : [
                          {
                            label: "Completed sessions",
                            value: analytics?.attempts || 0,
                            note: "Practice creates understanding",
                            icon: CheckCircle2,
                          },
                          {
                            label: "Questions attempted",
                            value: analytics?.questions || 0,
                            note: "From completed sessions",
                            icon: BookOpen,
                          },
                          {
                            label: "Accuracy",
                            value: analytics?.questions
                              ? `${Math.round((analytics.correct / analytics.questions) * 100)}%`
                              : "—",
                            note: "A starting point for reflection",
                            icon: TrendingUp,
                          },
                          {
                            label: "Topics",
                            value: catalog?.domains.length ?? 0,
                            note: "Explore your next skill",
                            icon: Target,
                          },
                        ]
                    ).map((s) => (
                      <div className="stat" key={s.label}>
                        <div>
                          <span>{s.label}</span>
                          <s.icon size={19} />
                        </div>
                        <strong>{s.value}</strong>
                        <p>{s.note}</p>
                      </div>
                    ))}
                  </div>
                  <div className="section-heading">
                    <div>
                      <h2>
                        Explore every topic
                        {catalog?.subjects?.length
                          ? ` in ${catalog.subjects.map((s) => s.name).join(" and ")}`
                          : ""}
                      </h2>
                      <p>
                        Understand the skill. Practice it. Reflect on the
                        result.
                      </p>
                    </div>
                    <button
                      className="text-button"
                      onClick={() => go("practice")}
                    >
                      Explore practice <ArrowRight size={16} />
                    </button>
                  </div>
                  <div className="domain-grid">
                    {catalog?.domains.map((d, i) => {
                      // Wraps, so adding a subject's domains cannot land on an
                      // undefined icon and take the whole page down.
                      const Icon = domainIcons[i % domainIcons.length];
                      const total = availability
                        .filter((x) => x.domain === d.id)
                        .reduce((a, b) => a + b.count, 0);
                      return (
                        <button
                          key={d.id}
                          className="domain-card"
                          onClick={() => {
                            setPractice({
                              ...practice,
                              domain: d.id,
                              skill: "",
                            });
                            go("practice");
                          }}
                        >
                          <div className="domain-card-top">
                            <span className="domain-icon">
                              <Icon size={23} />
                            </span>
                            <span className="domain-number">0{i + 1}</span>
                          </div>
                          <h3>{d.name}</h3>
                          <p>{d.description}</p>
                          <div className="domain-card-bottom">
                            <span>{total} approved questions</span>
                            <ArrowRight size={18} />
                          </div>
                        </button>
                      );
                    })}
                    <div className="learning-card">
                      <ShieldCheck size={27} />
                      <h3>Reasoning you can trust</h3>
                      <p>
                        Students receive approved questions. Teachers review the
                        wording, correct answer, and every distractor.
                      </p>
                      <span>Clear thinking, by design.</span>
                    </div>
                  </div>
                  {attempts.length > 0 && (
                    <section className="panel recent">
                      <h2>Your recent sessions</h2>
                      {attempts.slice(0, 4).map((a) => (
                        <div className="recent-row" key={a.id}>
                          <BookOpen size={18} />
                          <div>
                            <strong>{a.title}</strong>
                            <span>
                              {date(a.started)} · {a.count} questions
                            </span>
                          </div>
                          <Badge color={a.submitted ? "green" : "gold"}>
                            {a.submitted ? "Completed" : "In progress"}
                          </Badge>
                          <button
                            className="text-button"
                            onClick={() =>
                              run(async () => {
                                setAttempt(
                                  await api<Attempt>("/attempts/" + a.id),
                                );
                                setIndex(0);
                                setView("practice");
                              })
                            }
                          >
                            {a.submitted ? "Review" : "Resume"}
                            <ArrowRight size={15} />
                          </button>
                        </div>
                      ))}
                    </section>
                  )}
                </>
              )}
              {view === "generate" && (
                <>
                  <PageHeading
                    label="TEACHER STUDIO"
                    title="Build questions with intention."
                    description="Choose a reasoning skill. Generate originals. Review before students see them."
                  />
                  <div className="two-column">
                    <section className="panel">
                      <div className="panel-title">
                        <Sparkles size={20} />
                        <h2>Generation settings</h2>
                      </div>
                      <div className="form-grid">
                        <label>
                          Topic
                          <select
                            value={gen.domain}
                            onChange={(e) =>
                              setGen({
                                ...gen,
                                domain: e.target.value,
                                skill: "",
                              })
                            }
                          >
                            {catalog?.subjects?.map((s) => (
                              <optgroup label={s.name} key={s.id}>
                                {catalog.domains
                                  .filter((d) => d.subject === s.id)
                                  .map((d) => (
                                    <option value={d.id} key={d.id}>
                                      {d.name}
                                    </option>
                                  ))}
                              </optgroup>
                            ))}
                          </select>
                        </label>
                        <label>
                          Difficulty
                          <select
                            value={gen.difficulty}
                            onChange={(e) =>
                              setGen({
                                ...gen,
                                difficulty: e.target.value,
                                skill: "",
                              })
                            }
                          >
                            {catalog?.levels.map((l) => (
                              <option key={l}>{l}</option>
                            ))}
                          </select>
                        </label>
                        <label>
                          Skill
                          <select
                            value={gen.skill}
                            onChange={(e) =>
                              setGen({ ...gen, skill: e.target.value })
                            }
                          >
                            <option value="">Level-appropriate skill</option>
                            {catalog?.domains
                              .find((d) => d.id === gen.domain)
                              ?.skills.map((s) => (
                                <option value={s} key={s}>
                                  {human(s)}
                                </option>
                              ))}
                          </select>
                        </label>
                        <label>
                          Options per question
                          <select
                            value={gen.options}
                            onChange={(e) =>
                              setGen({ ...gen, options: +e.target.value })
                            }
                          >
                            <option value={4}>4 options · A–D</option>
                            <option value={5}>5 options · A–E</option>
                          </select>
                        </label>
                        <label>
                          Number of questions
                          <input
                            type="number"
                            min="1"
                            max="30"
                            value={gen.count}
                            onChange={(e) =>
                              setGen({ ...gen, count: +e.target.value })
                            }
                          />
                        </label>
                        <label>
                          Presentation
                          <select
                            value={gen.presentation}
                            onChange={(e) =>
                              setGen({ ...gen, presentation: e.target.value })
                            }
                          >
                            <option value="text">Text</option>
                            <option value="diagram">Text + diagram</option>
                          </select>
                        </label>
                      </div>
                      <p className="help">
                        Image questions: generate a draft, then attach an
                        original or credited image in the editor.
                      </p>
                      <div className="info-box">
                        <Target size={19} />
                        <div>
                          <strong>{gen.difficulty}</strong>
                          <p>{catalog?.level_guide[gen.difficulty]}</p>
                        </div>
                      </div>
                      <button
                        className="button full"
                        disabled={busy}
                        onClick={() =>
                          run(async () => {
                            const created = await api<Question[]>(
                              "/questions/generate",
                              "POST",
                              { ...gen, skill: gen.skill || null },
                            );
                            await refresh(user);
                            setStatus("draft");
                            setDomain(gen.domain);
                            setLevel("");
                            setSkill("");
                            setView("bank");
                            setNotice(
                              `${created.length} original drafts created. Review each question before approval.`,
                            );
                          })
                        }
                      >
                        <Sparkles size={18} />
                        {busy ? "Generating…" : "Generate original drafts"}
                      </button>
                    </section>
                    <div>
                      <section className="panel">
                        <Badge color="gold">QUALITY BY DESIGN</Badge>
                        <h2 className="mt">Every distractor has a purpose.</h2>
                        <p>
                          Incorrect options target a plausible reasoning
                          mistake, such as reversing a condition or missing a
                          constraint.
                        </p>
                        <ol className="steps">
                          <li>
                            <strong>Generate a draft</strong>
                            <span>
                              Bounded original templates, using a local
                              difficulty rubric.
                            </span>
                          </li>
                          <li>
                            <strong>Check the reasoning</strong>
                            <span>
                              Sequences and supported puzzles are checked
                              deterministically.
                            </span>
                          </li>
                          <li>
                            <strong>Review and approve</strong>
                            <span>
                              Verify the stem, answer, explanation, and
                              alternatives yourself.
                            </span>
                          </li>
                        </ol>
                        <div className="private-note">
                          <ShieldCheck size={17} />
                          Reference attribution stays in the teacher workspace.
                        </div>
                      </section>
                      <p className="help outside">
                        These are preparation exercises. They do not reproduce
                        past RUPP entrance papers or claim official exam
                        difficulty.
                      </p>
                    </div>
                  </div>
                </>
              )}
              {view === "bank" && (
                <>
                  <PageHeading
                    label="TEACHER WORKSPACE"
                    title="Your question bank."
                    description="Make every question clear, correct, and ready to teach."
                    action={
                      <button className="button" onClick={() => go("generate")}>
                        <Plus size={17} />
                        Generate questions
                      </button>
                    }
                  />
                  <div className="bank-summary">
                    <button
                      onClick={() => setStatus("")}
                      className={!status ? "selected" : ""}
                    >
                      All questions <strong>{bank.length}</strong>
                    </button>
                    {["draft", "review", "approved", "rejected"].map((s) => (
                      <button
                        key={s}
                        onClick={() => setStatus(s)}
                        className={status === s ? "selected" : ""}
                      >
                        {human(s)}{" "}
                        <strong>
                          {bank.filter((q) => q.status === s).length}
                        </strong>
                      </button>
                    ))}
                  </div>
                  <section className="panel bank-panel">
                    <div className="filters">
                      <label className="search-field">
                        <Search size={17} />
                        <input
                          aria-label="Search questions"
                          placeholder="Search question text…"
                          value={search}
                          onChange={(e) => setSearch(e.target.value)}
                        />
                      </label>
                      <select
                        aria-label="Filter subject"
                        value={bankSubject}
                        onChange={(e) => {
                          setBankSubject(e.target.value);
                          setDomain("");
                          setSkill("");
                        }}
                      >
                        <option value="">All subjects</option>
                        {catalog?.subjects?.map((s) => (
                          <option key={s.id} value={s.id}>
                            {s.name}
                          </option>
                        ))}
                      </select>
                      <select
                        aria-label="Filter domain"
                        value={domain}
                        onChange={(e) => {
                          setDomain(e.target.value);
                          setSkill("");
                        }}
                      >
                        <option value="">All topics</option>
                        {catalog?.domains
                          .filter((d) => !bankSubject || d.subject === bankSubject)
                          .map((d) => (
                            <option key={d.id} value={d.id}>
                              {d.name}
                            </option>
                          ))}
                      </select>
                      <select
                        aria-label="Filter difficulty"
                        value={level}
                        onChange={(e) => setLevel(e.target.value)}
                      >
                        <option value="">All difficulties</option>
                        {catalog?.levels.map((l) => (
                          <option key={l}>{l}</option>
                        ))}
                      </select>
                      <select
                        aria-label="Filter skill"
                        value={skill}
                        onChange={(e) => setSkill(e.target.value)}
                      >
                        <option value="">All skills</option>
                        {catalog?.domains
                          .filter(
                            (d) =>
                              (!bankSubject || d.subject === bankSubject) &&
                              (!domain || d.id === domain),
                          )
                          .flatMap((d) => d.skills)
                          .map((s) => (
                            <option key={s} value={s}>
                              {human(s)}
                            </option>
                          ))}
                      </select>
                    </div>
                    <div className="export-bar">
                      <span>
                        {filtered.length} questions · {selected.length} selected
                      </span>
                      <div>
                        <select
                          aria-label="Export content"
                          value={exportKind}
                          onChange={(e) => setExportKind(e.target.value)}
                        >
                          <option value="paper">Question paper</option>
                          <option value="key">Answer key</option>
                          <option value="solutions">Worked solutions</option>
                        </select>
                        <button
                          className="button secondary small"
                          disabled={busy}
                          onClick={() => download("docx")}
                        >
                          <Download size={15} />
                          Word
                        </button>
                        <button
                          className="button secondary small"
                          disabled={busy}
                          onClick={() => download("pdf")}
                        >
                          <Download size={15} />
                          PDF
                        </button>
                      </div>
                    </div>
                    {filtered.length === 0 ? (
                      <Empty
                        title="No questions match"
                        body="Broaden the filters or create a new draft set."
                      />
                    ) : (
                      <div className="question-list">
                        {filtered.map((q) => (
                          <div className="question-row" key={q.id}>
                            <input
                              type="checkbox"
                              aria-label={"Select " + q.id}
                              checked={selected.includes(q.id)}
                              disabled={q.status !== "approved"}
                              onChange={(e) =>
                                setSelected(
                                  e.target.checked
                                    ? [...selected, q.id]
                                    : selected.filter((id) => id !== q.id),
                                )
                              }
                            />
                            <button
                              className="question-link"
                              onClick={() => setDetail(q)}
                            >
                              <div className="question-meta">
                                {q.source.kind === "textbook-excerpt" && (
                                  <Badge color="gold">
                                    Textbook · Q
                                    {String(q.source.question_number)}
                                  </Badge>
                                )}
                                {q.source.kind === "adapted-textbook" && (
                                  <Badge color="gold">
                                    Adapted from textbook
                                  </Badge>
                                )}
                                <Badge
                                  color={
                                    q.status === "approved"
                                      ? "green"
                                      : q.status === "rejected"
                                        ? "red"
                                        : q.status === "review"
                                          ? "gold"
                                          : "gray"
                                  }
                                >
                                  {human(q.status)}
                                </Badge>
                                <span>{domainName(q.domain)}</span>
                                <span>· {q.difficulty}</span>
                              </div>
                              <h3>{q.content.stem}</h3>
                              <div className="question-submeta">
                                <span>{human(q.skill)}</span>
                                <span>{q.content.options.length} options</span>
                                <span>
                                  {q.validation.method === "deterministic"
                                    ? "Rule checked"
                                    : "Editorial review"}
                                </span>
                                <span>v{q.version}</span>
                              </div>
                            </button>
                            <button
                              className="button secondary small"
                              onClick={() => setEditing(q)}
                            >
                              Edit
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </section>
                </>
              )}
              {view === "practice" && (
                <>
                  <PageHeading
                    label="LEARN BY DOING"
                    title="Practice the reasoning."
                    description="Focus on one skill or combine domains. Take time to understand your answer."
                  />
                  <div className="two-column">
                    <section className="panel">
                      <div className="segmented">
                        <button
                          className={
                            practice.mode === "practice" ? "active" : ""
                          }
                          onClick={() =>
                            setPractice({ ...practice, mode: "practice" })
                          }
                        >
                          Guided practice
                        </button>
                        <button
                          className={practice.mode === "exam" ? "active" : ""}
                          onClick={() =>
                            setPractice({ ...practice, mode: "exam" })
                          }
                        >
                          Exam practice
                        </button>
                      </div>
                      <div className="info-box">
                        <BookOpen size={20} />
                        <div>
                          <strong>
                            {practice.mode === "practice"
                              ? "Understand as you go"
                              : "Test your independent reasoning"}
                          </strong>
                          <p>
                            {practice.mode === "practice"
                              ? "Your answer is locked when checked. You will immediately see the explanation."
                              : "A timed session. Answers can be changed; explanations appear after submission."}
                          </p>
                        </div>
                      </div>
                      <div className="form-grid">
                        <label>
                          Subject
                          <select
                            value={practice.subject}
                            onChange={(e) =>
                              setPractice({
                                ...practice,
                                subject: e.target.value,
                                // The topic list belongs to the subject, so a
                                // leftover choice from another one must clear.
                                domain: "",
                                skill: "",
                              })
                            }
                          >
                            <option value="">All subjects</option>
                            {catalog?.subjects?.map((s) => (
                              <option value={s.id} key={s.id}>
                                {s.name}
                              </option>
                            ))}
                          </select>
                        </label>
                        <label>
                          Question source
                          <select
                            value={practice.origin}
                            onChange={(e) =>
                              setPractice({
                                ...practice,
                                origin: e.target.value,
                                domain: "",
                                difficulty: "",
                                skill: "",
                                options: 4,
                                count: e.target.value === "textbook" ? 3 : 5,
                              })
                            }
                          >
                            <option value="all">All approved questions</option>
                            <option value="textbook">Textbook selection</option>
                            <option value="original">
                              Original authored questions
                            </option>
                          </select>
                        </label>
                        <label>
                          Topic
                          <select
                            value={practice.domain}
                            onChange={(e) =>
                              setPractice({
                                ...practice,
                                domain: e.target.value,
                                skill: "",
                              })
                            }
                          >
                            <option value="">Mixed · all topics</option>
                            {catalog?.domains
                              .filter(
                                (d) =>
                                  !practice.subject ||
                                  d.subject === practice.subject,
                              )
                              .map((d) => (
                                <option value={d.id} key={d.id}>
                                  {d.name}
                                </option>
                              ))}
                          </select>
                        </label>
                        <label>
                          Difficulty
                          <select
                            value={practice.difficulty}
                            onChange={(e) =>
                              setPractice({
                                ...practice,
                                difficulty: e.target.value,
                              })
                            }
                          >
                            <option value="">All levels</option>
                            {catalog?.levels.map((l) => (
                              <option key={l}>{l}</option>
                            ))}
                          </select>
                        </label>
                        <label>
                          Skill
                          <select
                            value={practice.skill}
                            onChange={(e) =>
                              setPractice({
                                ...practice,
                                skill: e.target.value,
                              })
                            }
                          >
                            <option value="">All matching skills</option>
                            {catalog?.domains
                              .filter(
                                (d) =>
                                  !practice.domain || d.id === practice.domain,
                              )
                              .flatMap((d) => d.skills)
                              .map((s) => (
                                <option key={s} value={s}>
                                  {human(s)}
                                </option>
                              ))}
                          </select>
                        </label>
                        <label>
                          Options
                          <select
                            value={practice.options}
                            onChange={(e) =>
                              setPractice({
                                ...practice,
                                options: +e.target.value,
                              })
                            }
                          >
                            <option value={4}>4 options</option>
                            <option value={5}>5 options</option>
                          </select>
                        </label>
                        <label>
                          Question count
                          <input
                            type="number"
                            min="1"
                            max="50"
                            value={practice.count}
                            onChange={(e) =>
                              setPractice({
                                ...practice,
                                count: +e.target.value,
                              })
                            }
                          />
                        </label>
                        {practice.mode === "exam" && (
                          <label>
                            Time limit (minutes)
                            <input
                              type="number"
                              min="1"
                              max="180"
                              value={practice.minutes}
                              onChange={(e) =>
                                setPractice({
                                  ...practice,
                                  minutes: +e.target.value,
                                })
                              }
                            />
                          </label>
                        )}
                      </div>
                      <p className="help">
                        {availability
                          .filter(
                            (x) =>
                              (!practice.subject ||
                                x.subject === practice.subject) &&
                              (!practice.domain ||
                                x.domain === practice.domain) &&
                              (!practice.difficulty ||
                                x.difficulty === practice.difficulty) &&
                              (!practice.skill || x.skill === practice.skill) &&
                              x.options === practice.options &&
                              (practice.origin === "all" ||
                                x.origin === practice.origin),
                          )
                          .reduce((a, b) => a + b.count, 0)}{" "}
                        approved questions match your selection.
                      </p>
                      <button
                        className="button full"
                        disabled={busy}
                        onClick={() =>
                          run(async () => {
                            setAttempt(
                              await api<Attempt>("/attempts", "POST", {
                                ...practice,
                                subject: practice.subject || null,
                                domain: practice.domain || null,
                                difficulty: practice.difficulty || null,
                                skill: practice.skill || null,
                              }),
                            );
                            setIndex(0);
                          })
                        }
                      >
                        Start {practice.mode === "practice" ? "guided" : "exam"}{" "}
                        practice
                        <ArrowRight size={17} />
                      </button>
                    </section>
                    <section className="panel">
                      <h2>Make practice count.</h2>
                      <ol className="steps">
                        <li>
                          <strong>Observe carefully</strong>
                          <span>
                            Read all the conditions before choosing an answer.
                          </span>
                        </li>
                        <li>
                          <strong>Test your rule</strong>
                          <span>
                            Check every term, relationship, or constraint.
                          </span>
                        </li>
                        <li>
                          <strong>Reflect on mistakes</strong>
                          <span>Ask which assumption led to your choice.</span>
                        </li>
                      </ol>
                      <div className="private-note">
                        <Clock3 size={17} />
                        Saved attempts can be resumed from Overview.
                      </div>
                    </section>
                  </div>
                </>
              )}
              {view === "blueprints" && (
                <>
                  <PageHeading
                    label="EXAM PREPARATION"
                    title={
                      user.role === "teacher"
                        ? "Design the practice blueprint."
                        : "Put your reasoning to the test."
                    }
                    description="Timed mock exams use teacher-defined topic and difficulty allocations."
                  />
                  {user.role === "teacher" && (
                    <section className="panel blueprint-panel">
                      <div className="form-grid">
                        <label>
                          Exam title
                          <input
                            value={bpName}
                            onChange={(e) => setBpName(e.target.value)}
                          />
                        </label>
                        <label>
                          Time limit (minutes)
                          <input
                            type="number"
                            min="1"
                            max="180"
                            value={bpMinutes}
                            onChange={(e) => setBpMinutes(+e.target.value)}
                          />
                        </label>
                      </div>
                      <h3 className="mt">Question allocation</h3>
                      <div className="blueprint-rows">
                        {bpRows.map((r, i) => (
                          <div className="blueprint-row" key={i}>
                            <select
                              aria-label={`Row ${i + 1} domain`}
                              value={r.domain}
                              onChange={(e) =>
                                setBpRows(
                                  bpRows.map((x, j) =>
                                    i === j
                                      ? { ...x, domain: e.target.value }
                                      : x,
                                  ),
                                )
                              }
                            >
                              {catalog?.subjects?.map((s) => (
                                <optgroup label={s.name} key={s.id}>
                                  {catalog.domains
                                    .filter((d) => d.subject === s.id)
                                    .map((d) => (
                                      <option key={d.id} value={d.id}>
                                        {d.name}
                                      </option>
                                    ))}
                                </optgroup>
                              ))}
                            </select>
                            <select
                              aria-label={`Row ${i + 1} difficulty`}
                              value={r.difficulty}
                              onChange={(e) =>
                                setBpRows(
                                  bpRows.map((x, j) =>
                                    i === j
                                      ? { ...x, difficulty: e.target.value }
                                      : x,
                                  ),
                                )
                              }
                            >
                              {catalog?.levels.map((l) => (
                                <option key={l}>{l}</option>
                              ))}
                            </select>
                            <select
                              aria-label={`Row ${i + 1} options`}
                              value={r.options}
                              onChange={(e) =>
                                setBpRows(
                                  bpRows.map((x, j) =>
                                    i === j
                                      ? { ...x, options: +e.target.value }
                                      : x,
                                  ),
                                )
                              }
                            >
                              <option value={4}>4 options</option>
                              <option value={5}>5 options</option>
                            </select>
                            <input
                              aria-label={`Row ${i + 1} count`}
                              type="number"
                              min="1"
                              max="50"
                              value={r.count}
                              onChange={(e) =>
                                setBpRows(
                                  bpRows.map((x, j) =>
                                    i === j
                                      ? { ...x, count: +e.target.value }
                                      : x,
                                  ),
                                )
                              }
                            />
                            <button
                              className="icon-button"
                              aria-label={`Remove row ${i + 1}`}
                              disabled={bpRows.length === 1}
                              onClick={() =>
                                setBpRows(bpRows.filter((_, j) => j !== i))
                              }
                            >
                              <Trash2 size={18} />
                            </button>
                          </div>
                        ))}
                      </div>
                      <div className="blueprint-footer">
                        <button
                          className="text-button"
                          onClick={() =>
                            setBpRows([
                              ...bpRows,
                              {
                                domain: "patterns",
                                difficulty: "Foundation",
                                count: 1,
                                options: 4,
                              },
                            ])
                          }
                        >
                          <Plus size={16} />
                          Add allocation
                        </button>
                        <span>
                          {bpRows.reduce((a, b) => a + b.count, 0)} questions
                          total
                        </span>
                        <label className="checkbox-label">
                          <input
                            type="checkbox"
                            checked={bpPublished}
                            onChange={(e) => setBpPublished(e.target.checked)}
                          />
                          Publish to students
                        </label>
                        <button
                          className="button"
                          disabled={busy}
                          onClick={() =>
                            run(async () => {
                              await api(
                                bpEdit
                                  ? "/blueprints/" + bpEdit
                                  : "/blueprints",
                                bpEdit ? "PATCH" : "POST",
                                {
                                  name: bpName,
                                  minutes: bpMinutes,
                                  rows: bpRows,
                                  published: bpPublished,
                                },
                              );
                              await refresh(user);
                              setBpEdit(null);
                              setNotice(
                                "Blueprint saved. Published blueprints check the available approved bank.",
                              );
                            })
                          }
                        >
                          {bpEdit ? "Update blueprint" : "Save blueprint"}
                        </button>
                      </div>
                    </section>
                  )}
                  <div className="section-heading">
                    <h2>
                      {user.role === "teacher"
                        ? "Saved blueprints"
                        : "Available mock exams"}
                    </h2>
                  </div>
                  <div className="blueprint-grid">
                    {blueprints.length ? (
                      blueprints.map((b) => (
                        <section className="panel" key={b.id}>
                          <div className="spread">
                            <Target size={23} />
                            <Badge color={b.published ? "green" : "gray"}>
                              {b.published ? "Published" : "Draft"}
                            </Badge>
                          </div>
                          <h3 className="mt">{b.name}</h3>
                          {user.role === "teacher" && (
                            <button
                              className="text-button"
                              onClick={() => {
                                setBpEdit(b.id);
                                setBpName(b.name);
                                setBpMinutes(b.minutes);
                                setBpRows(structuredClone(b.rows));
                                setBpPublished(b.published);
                                window.scrollTo({ top: 0, behavior: "smooth" });
                              }}
                            >
                              Edit blueprint / publication
                            </button>
                          )}
                          <p>
                            {b.rows.reduce((a, r) => a + r.count, 0)} questions
                            · {b.minutes} minutes · delayed feedback
                          </p>
                          <div className="allocation-list">
                            {b.rows.map((r, i) => (
                              <div key={i}>
                                <span>
                                  {domainName(r.domain)}
                                  <small>
                                    {r.difficulty} · {r.options} options
                                  </small>
                                </span>
                                <strong>{r.count}</strong>
                              </div>
                            ))}
                          </div>
                          <button
                            className="button secondary full"
                            disabled={busy}
                            onClick={() =>
                              run(async () => {
                                setAttempt(
                                  await api<Attempt>("/attempts", "POST", {
                                    mode: "mock",
                                    blueprint_id: b.id,
                                  }),
                                );
                                setIndex(0);
                              })
                            }
                          >
                            Start mock exam
                            <ArrowRight size={16} />
                          </button>
                        </section>
                      ))
                    ) : (
                      <Empty
                        title="No mock exams yet"
                        body={
                          user.role === "teacher"
                            ? "Create a blueprint above."
                            : "Your teacher will publish mock exams here."
                        }
                      />
                    )}
                  </div>
                </>
              )}
              {view === "students" && (
                <>
                  <PageHeading
                    label="COHORT"
                    title="Students and their results."
                    description="Every figure counts completed sessions only."
                  />
                  {!roster.length ? (
                    <Empty
                      title="No students have registered yet"
                      body={
                        anonymousCount
                          ? `A student appears here once they create an account. There are ${anonymousCount} anonymous workspaces, which carry no name or address because sign-in was not required when they were used.`
                          : "A student appears here as soon as they create an account. Their results fill in once they complete a session."
                      }
                    />
                  ) : (
                    <>
                      <div className="export-bar">
                        <span>
                          {roster.length} registered ·{" "}
                          {roster.filter((s) => s.sessions).length} have
                          practised
                          {anonymousCount
                            ? ` · ${anonymousCount} anonymous workspaces not shown`
                            : ""}
                        </span>
                        <a
                          className="button secondary small"
                          href="/api/students/export.csv"
                        >
                          <Download size={15} /> Export CSV
                        </a>
                      </div>
                      <section className="panel">
                        <div className="table-scroll">
                          <table className="data-table">
                            <thead>
                              <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th className="numeric">Sessions</th>
                                <th className="numeric">Answered</th>
                                <th className="numeric">Accuracy</th>
                                <th>Last active</th>
                              </tr>
                            </thead>
                            <tbody>
                              {roster.map((s) => (
                                <tr
                                  key={s.id}
                                  className={
                                    studentDetail?.id === s.id ? "current" : ""
                                  }
                                >
                                  <td>
                                    <button
                                      className="text-button"
                                      onClick={() =>
                                        run(async () =>
                                          setStudentDetail(
                                            await api<StudentDetail>(
                                              "/students/" + s.id,
                                            ),
                                          ),
                                        )
                                      }
                                    >
                                      {s.name}
                                    </button>
                                  </td>
                                  <td>{s.email}</td>
                                  <td className="numeric">{s.sessions}</td>
                                  <td className="numeric">{s.answered}</td>
                                  <td className="numeric">
                                    {s.accuracy === null
                                      ? "—"
                                      : `${s.accuracy}%`}
                                  </td>
                                  <td>
                                    {s.last_active ? date(s.last_active) : "—"}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </section>
                      {studentDetail && (
                        <section className="panel">
                          <div className="panel-title">
                            <Users size={20} />
                            <h2>{studentDetail.name}</h2>
                          </div>
                          <p className="help">{studentDetail.email}</p>
                          {!studentDetail.sessions.length ? (
                            <p className="help">
                              This student has not completed a session yet.
                            </p>
                          ) : (
                            <>
                              <h2>Completed sessions</h2>
                              <div className="table-scroll">
                                <table className="data-table">
                                  <thead>
                                    <tr>
                                      <th>Session</th>
                                      <th>Mode</th>
                                      <th className="numeric">Score</th>
                                      <th>Submitted</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {studentDetail.sessions.map((a) => (
                                      <tr key={a.id}>
                                        <td>{a.title}</td>
                                        <td>{human(a.mode)}</td>
                                        <td className="numeric">
                                          {a.score} / {a.total}
                                        </td>
                                        <td>{date(a.submitted)}</td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                              <h2>Accuracy by topic</h2>
                              <div className="bars">
                                {studentDetail.topics.map((t) => (
                                  <div key={t.domain}>
                                    <div className="spread">
                                      <span>{domainName(t.domain)}</span>
                                      <strong>
                                        {Math.round(
                                          (t.correct / t.answered) * 100,
                                        )}
                                        %
                                      </strong>
                                    </div>
                                    <div className="bar-track">
                                      <div
                                        style={{
                                          width: `${(t.correct / t.answered) * 100}%`,
                                        }}
                                      />
                                    </div>
                                    <small>
                                      {t.correct} correct / {t.answered}{" "}
                                      questions
                                    </small>
                                  </div>
                                ))}
                              </div>
                            </>
                          )}
                        </section>
                      )}
                    </>
                  )}
                </>
              )}
              {view === "analytics" && (
                <>
                  <PageHeading
                    label="REFLECT & IMPROVE"
                    title="Understand your next step."
                    description={analytics?.scope || "Learning insights"}
                  />
                  {!analytics?.questions ? (
                    <Empty
                      title="Your learning insights start with practice"
                      body="Complete and submit a session to see topic accuracy and patterns in incorrect choices."
                    />
                  ) : (
                    <>
                      <div className="stat-grid three">
                        <div className="stat">
                          <span>Completed sessions</span>
                          <strong>{analytics.attempts}</strong>
                        </div>
                        <div className="stat">
                          <span>Questions in completed sessions</span>
                          <strong>{analytics.questions}</strong>
                        </div>
                        <div className="stat">
                          <span>Accuracy</span>
                          <strong>
                            {Math.round(
                              (analytics.correct / analytics.questions) * 100,
                            )}
                            %
                          </strong>
                        </div>
                      </div>
                      <div className="two-column">
                        {["domain", "difficulty"].map((kind) => (
                          <section className="panel" key={kind}>
                            <h2>
                              Accuracy by{" "}
                              {kind === "domain" ? "topic" : "difficulty"}
                            </h2>
                            <div className="bars">
                              {analytics.groups
                                .filter((g) => g.kind === kind)
                                .map((g) => (
                                  <div key={g.label}>
                                    <div className="spread">
                                      <span>
                                        {kind === "domain"
                                          ? domainName(g.label)
                                          : g.label}
                                      </span>
                                      <strong>
                                        {Math.round(
                                          (g.correct / g.total) * 100,
                                        )}
                                        %
                                      </strong>
                                    </div>
                                    <div className="bar-track">
                                      <div
                                        style={{
                                          width: `${(g.correct / g.total) * 100}%`,
                                        }}
                                      />
                                    </div>
                                    <small>
                                      {g.correct} correct / {g.total} questions
                                    </small>
                                  </div>
                                ))}
                            </div>
                          </section>
                        ))}
                      </div>
                      <section className="panel mt">
                        <h2>Patterns to revisit</h2>
                        <p>{analytics.note}</p>
                        {analytics.errors.length ? (
                          <div className="error-tags">
                            {analytics.errors.map((e) => (
                              <div key={e.label}>
                                <span>{human(e.label)}</span>
                                <strong>{e.count}</strong>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p>
                            All answers were correct in your completed sessions.
                          </p>
                        )}
                      </section>
                    </>
                  )}
                </>
              )}
            </>
          )}
          <footer className="footer">
            Mechanical Engineering @ RUPP
            <span>Great engineers build on theory and hands-on practice.</span>
          </footer>
        </main>
      </div>
      {editing && (
        <QuestionEditor
          question={editing}
          busy={busy}
          error={error}
          close={() => setEditing(null)}
          save={(content) =>
            run(async () => {
              const q = await api<Question>(
                `/questions/${editing.id}`,
                "PATCH",
                { version: editing.version, content },
              );
              setEditing(null);
              setDetail(q);
              await refresh(user);
              setNotice(
                "Changes saved as a draft. Teacher review is required again.",
              );
            })
          }
        />
      )}
      {detail && !editing && (
        <QuestionDetail
          question={detail}
          busy={busy}
          error={error}
          close={() => setDetail(null)}
          edit={() => setEditing(detail)}
          review={(a, n, t) => review(detail, a, n, t)}
          domainName={domainName(detail.domain)}
        />
      )}
    </div>
  );
}

function PageHeading({
  label,
  title,
  description,
  action,
}: {
  label: string;
  title: string;
  description: string;
  action?: ReactNode;
}) {
  return (
    <div className="page-heading">
      <div>
        <p className="eyebrow">{label}</p>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {action}
    </div>
  );
}

function QuestionDetail({
  question: q,
  busy,
  error,
  close,
  edit,
  review,
  domainName,
}: {
  question: Question;
  busy: boolean;
  error: string;
  close: () => void;
  edit: () => void;
  review: (action: string, note: string, attested: boolean) => void;
  domainName: string;
}) {
  const [attest, setAttest] = useState(false),
    [note, setNote] = useState(""),
    [history, setHistory] = useState<
      { action: string; at: string; detail: { note?: string } }[] | null
    >(null),
    [historyError, setHistoryError] = useState("");
  useEffect(() => {
    setAttest(false);
    setNote("");
    setHistory(null);
  }, [q.version, q.id]);
  return (
    <Modal title="Review question" close={close}>
      {error && (
        <div className="alert error" role="alert">
          {error}
        </div>
      )}
      <div className="question-meta">
        <Badge color={q.status === "approved" ? "green" : "gold"}>
          {human(q.status)}
        </Badge>
        <span>
          {domainName} · {q.difficulty} · v{q.version}
        </span>
      </div>
      <h3 className="question-stem">
        <RichText text={q.content.stem} />
      </h3>
      <Visual content={q.content} />
      <div className="option-preview">
        {q.content.options.map((o) => (
          <div
            className={o.id === q.content.correct ? "correct" : ""}
            key={o.id}
          >
            <span>{o.id}</span>
            <div>
              <strong>
                <RichText text={o.text} />
              </strong>
              <p>{o.rationale}</p>
              <small>{o.error && human(o.error)}</small>
            </div>
            {o.id === q.content.correct && <CheckCircle2 size={18} />}
          </div>
        ))}
      </div>
      <div className="explanation">
        <h3>Worked explanation</h3>
        <p>
          {q.content.explanation && <RichText text={q.content.explanation} />}
        </p>
        <MathText text={q.content.math} />
      </div>
      <div
        className={"validation " + (q.validation.passed ? "passed" : "failed")}
      >
        <ShieldCheck size={20} />
        <div>
          <strong>
            {q.validation.passed
              ? "Structural checks passed"
              : "Validation needs attention"}
          </strong>
          <p>
            {q.validation.proof ||
              "Editorial reasoning requires human verification."}
          </p>
          {q.validation.errors.map((e) => (
            <p key={e}>{e}</p>
          ))}
          <small>{q.validation.note}</small>
        </div>
      </div>
      <details className="source-detail">
        <summary>Private source attribution</summary>
        <dl>
          {Object.entries(q.source).map(([k, v]) => (
            <div key={k}>
              <dt>{human(k)}</dt>
              <dd>{String(v)}</dd>
            </div>
          ))}
        </dl>
      </details>
      <label>
        Review note / rejection reason
        <textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          rows={2}
          placeholder="Explain changes needed or record your review."
        />
      </label>
      {q.status === "review" && (
        <label className="checkbox-label attestation">
          <input
            type="checkbox"
            checked={attest}
            onChange={(e) => setAttest(e.target.checked)}
          />
          I checked the wording, unique answer, explanation, and distractor
          rationale.
        </label>
      )}
      <div className="review-actions">
        <button className="button secondary" disabled={busy} onClick={edit}>
          Edit question
        </button>
        <button
          className="button secondary"
          disabled={busy}
          onClick={() => review("regenerate", note, false)}
        >
          <RefreshCw size={15} />
          Regenerate
        </button>
        {["draft", "rejected"].includes(q.status) && (
          <button
            className="button"
            disabled={busy}
            onClick={() => review("review", note, false)}
          >
            Send for review
          </button>
        )}
        {q.status === "review" && (
          <button
            className="button"
            disabled={busy || !attest || !q.validation.passed}
            onClick={() => review("approve", note, attest)}
          >
            <Check size={16} />
            Approve
          </button>
        )}
        {q.status !== "rejected" && (
          <button
            className="button danger"
            disabled={busy || !note.trim()}
            onClick={() => review("reject", note, false)}
          >
            Reject
          </button>
        )}
      </div>
      <button
        className="text-button mt"
        onClick={async () => {
          try {
            setHistory(await api(`/questions/${q.id}/history`));
          } catch (e) {
            setHistoryError((e as Error).message);
          }
        }}
      >
        View review history
      </button>
      {historyError && <p className="error">{historyError}</p>}
      {history && (
        <div className="history-list">
          {history.map((h, i) => (
            <div key={i}>
              <strong>{human(h.action)}</strong>
              <span>{date(h.at)}</span>
              <p>{h.detail.note}</p>
            </div>
          ))}
        </div>
      )}
    </Modal>
  );
}

function QuestionEditor({
  question,
  busy,
  error,
  close,
  save,
}: {
  question: Question;
  busy: boolean;
  error: string;
  close: () => void;
  save: (c: Content) => void;
}) {
  const [c, setC] = useState<Content>(structuredClone(question.content)),
    [validator, setValidator] = useState(
      JSON.stringify(question.content.validator, null, 2),
    ),
    [localError, setLocalError] = useState("");
  return (
    <Modal title="Edit question" close={close}>
      {error && (
        <div className="alert error" role="alert">
          {error}
        </div>
      )}
      <p className="help">
        Saving creates a draft and removes student eligibility until
        re-approved. Use $...$ for inline LaTeX.
      </p>
      <label>
        Question stem
        <textarea
          rows={4}
          value={c.stem}
          onChange={(e) => setC({ ...c, stem: e.target.value })}
        />
      </label>
      <div className="form-grid">
        <label>
          Presentation
          <select
            value={c.presentation}
            onChange={(e) =>
              setC({
                ...c,
                presentation: e.target.value as Content["presentation"],
                diagram:
                  e.target.value === "diagram"
                    ? c.diagram || {
                        kind: "flow",
                        labels: ["Observe", "Reason", "Conclude"],
                      }
                    : c.diagram,
              })
            }
          >
            <option value="text">Text</option>
            <option value="image">Image</option>
            <option value="diagram">Diagram</option>
          </select>
        </label>
        <label>
          Option count
          <select
            value={c.options.length}
            onChange={(e) => {
              const size = +e.target.value;
              const opts =
                size === 5
                  ? [
                      ...c.options,
                      {
                        id: "E",
                        text: "",
                        rationale: "",
                        error: "other-misconception",
                      },
                    ]
                  : c.options.slice(0, 4);
              setC({
                ...c,
                options: opts,
                correct: c.correct === "E" && size === 4 ? "A" : c.correct,
              });
            }}
          >
            <option value={4}>4</option>
            <option value={5}>5</option>
          </select>
        </label>
      </div>
      {c.presentation === "image" && (
        <>
          <label>
            Original or licensed image
            <input
              type="file"
              accept="image/png,image/jpeg,image/webp"
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (!f) return;
                if (f.size > 2000000) {
                  setLocalError("Choose an image under 2 MB.");
                  return;
                }
                const reader = new FileReader();
                reader.onload = () =>
                  setC({ ...c, asset: String(reader.result) });
                reader.readAsDataURL(f);
              }}
            />
          </label>
          <label>
            Image description and credit
            <input
              value={c.asset_alt}
              onChange={(e) => setC({ ...c, asset_alt: e.target.value })}
            />
          </label>
        </>
      )}
      {c.presentation === "diagram" && (
        <>
          <label>
            Diagram style
            <select
              value={c.diagram?.kind || "flow"}
              onChange={(e) =>
                setC({
                  ...c,
                  diagram: {
                    kind: e.target.value,
                    labels: c.diagram?.labels || [],
                  },
                })
              }
            >
              <option value="flow">Flow</option>
              <option value="stations">Station positions</option>
              <option value="cycle">Cycle</option>
            </select>
          </label>
          <label>
            Diagram labels (separate with |)
            <input
              value={c.diagram?.labels.join("|") || ""}
              onChange={(e) =>
                setC({
                  ...c,
                  diagram: {
                    kind: c.diagram?.kind || "flow",
                    labels: e.target.value.split("|"),
                  },
                })
              }
            />
          </label>
        </>
      )}
      <Visual content={c} />
      <h3 className="mt">Options and reasoning</h3>
      {c.options.map((o, i) => (
        <fieldset className="option-editor" key={o.id}>
          <legend>Option {o.id}</legend>
          <label>
            Answer text
            <input
              value={o.text}
              onChange={(e) =>
                setC({
                  ...c,
                  options: c.options.map((x, j) =>
                    i === j ? { ...x, text: e.target.value } : x,
                  ),
                })
              }
            />
          </label>
          <div className="form-grid">
            <label>
              Rationale
              <textarea
                rows={2}
                value={o.rationale || ""}
                onChange={(e) =>
                  setC({
                    ...c,
                    options: c.options.map((x, j) =>
                      i === j ? { ...x, rationale: e.target.value } : x,
                    ),
                  })
                }
              />
            </label>
            <label>
              Error pattern
              <input
                value={o.error || ""}
                onChange={(e) =>
                  setC({
                    ...c,
                    options: c.options.map((x, j) =>
                      i === j ? { ...x, error: e.target.value } : x,
                    ),
                  })
                }
              />
            </label>
          </div>
        </fieldset>
      ))}
      <label>
        Correct answer
        <select
          value={c.correct}
          onChange={(e) => setC({ ...c, correct: e.target.value })}
        >
          {c.options.map((o) => (
            <option key={o.id}>{o.id}</option>
          ))}
        </select>
      </label>
      <label>
        Worked explanation
        <textarea
          rows={4}
          value={c.explanation || ""}
          onChange={(e) => setC({ ...c, explanation: e.target.value })}
        />
      </label>
      <label>
        Explanation formula (LaTeX)
        <input
          value={c.math || ""}
          onChange={(e) => setC({ ...c, math: e.target.value || null })}
        />
      </label>
      <MathText text={c.math} />
      <details className="source-detail">
        <summary>Deterministic rule specification</summary>
        <p className="help">
          Keep the rule synchronized with the question. Clear it to require
          editorial validation. This checker cannot verify that prose matches
          the specification.
        </p>
        <textarea
          className="code-input"
          rows={8}
          value={validator}
          onChange={(e) => setValidator(e.target.value)}
        />
      </details>
      {localError && (
        <p role="alert" className="alert error">
          {localError}
        </p>
      )}
      <div className="review-actions">
        <button className="button secondary" onClick={close}>
          Cancel
        </button>
        <button
          className="button"
          disabled={busy}
          onClick={() => {
            try {
              const v = validator.trim() ? JSON.parse(validator) : null;
              setLocalError("");
              save({ ...c, validator: v });
            } catch {
              setLocalError(
                "The rule specification must be valid JSON or empty.",
              );
            }
          }}
        >
          Save as draft
        </button>
      </div>
    </Modal>
  );
}

function AttemptPlayer({
  attempt: a,
  index,
  setIndex,
  busy,
  update,
  act,
  refresh,
  exit,
  domainName,
}: {
  attempt: Attempt;
  index: number;
  setIndex: (i: number) => void;
  busy: boolean;
  update: (a: Attempt) => void;
  act: (t: () => Promise<void>) => Promise<void>;
  refresh: () => Promise<void>;
  exit: () => void;
  domainName: (s: string) => string;
}) {
  const [choice, setChoice] = useState(""),
    [remaining, setRemaining] = useState(0),
    [confirm, setConfirm] = useState(false);
  const q = a.questions[index],
    done = !!a.submitted;
  useEffect(() => {
    setChoice(a.answers[q.id] || "");
  }, [q.id, a.answers]);
  useEffect(() => {
    if (!a.deadline || done) return;
    const offset = new Date(a.server_time).getTime() - Date.now();
    let triggered = false;
    const tick = () => {
      const left = Math.max(
        0,
        Math.ceil(
          (new Date(a.deadline!).getTime() - Date.now() - offset) / 1000,
        ),
      );
      setRemaining(left);
      if (left === 0 && !triggered) {
        triggered = true;
        act(async () => {
          update(await api<Attempt>(`/attempts/${a.id}/submit`, "POST"));
          await refresh();
        });
      }
    };
    tick();
    const timer = setInterval(tick, 1000);
    return () => clearInterval(timer);
  }, [a.deadline, a.submitted, a.id, a.server_time]);
  async function save() {
    await act(async () => {
      update(
        await api<Attempt>(`/attempts/${a.id}/answer`, "POST", {
          question_id: q.id,
          option_id: choice,
        }),
      );
    });
  }
  const answered = Object.keys(a.answers).length;
  const correctCount = a.questions.filter((x) => x.feedback?.is_correct).length;
  const wrongCount = a.questions.filter(
    (x) => a.answers[x.id] && !x.feedback?.is_correct,
  ).length;
  const missedCount = a.questions.length - answered;
  const percent = a.questions.length
    ? Math.round(((a.score ?? correctCount) / a.questions.length) * 100)
    : 0;
  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">
            {done
              ? "SESSION COMPLETE"
              : a.mode === "practice"
                ? "GUIDED PRACTICE"
                : "TIMED EXAM PRACTICE"}
          </p>
          <h1>{a.title}</h1>
          <p>
            {done
              ? `${a.score} / ${a.questions.length} correct${missedCount ? ` · ${missedCount} not answered` : ""} · Review the reasoning below.`
              : a.mode === "practice"
                ? "Check your answer to learn the reasoning."
                : "Explanations are available after you submit."}
          </p>
        </div>
        {a.deadline && !done && (
          <div className={"timer " + (remaining < 60 ? "urgent" : "")}>
            <Clock3 size={19} />
            {Math.floor(remaining / 60)}:
            {String(remaining % 60).padStart(2, "0")}
            <span>remaining</span>
          </div>
        )}
      </div>
      <div className="player-layout">
        <section className="panel player">
          <div className="spread">
            <Badge>
              QUESTION {index + 1} OF {a.questions.length}
            </Badge>
            <span className="help">
              {q.difficulty} · {q.content.options.length} options
            </span>
          </div>
          <p className="eyebrow mt">{domainName(q.domain)}</p>
          {q.attribution && (
            <p className="help source-credit">{q.attribution}</p>
          )}
          <h2 className="question-stem">
            <RichText text={q.content.stem} />
          </h2>
          <Visual content={q.content} />
          <div className="answer-options">
            {q.content.options.map((o) => {
              const selected = choice === o.id;
              const correct = q.feedback?.correct === o.id;
              const wrong = !!q.feedback && selected && !correct;
              return (
                <button
                  key={o.id}
                  disabled={busy || done || !!q.feedback}
                  onClick={() => setChoice(o.id)}
                  className={
                    (selected ? "selected " : "") +
                    (correct ? "correct " : "") +
                    (wrong ? "wrong" : "")
                  }
                >
                  <span className="option-letter">{o.id}</span>
                  <span>
                    <RichText text={o.text} />
                  </span>
                  {correct && <CheckCircle2 size={19} />}
                </button>
              );
            })}
          </div>
          {q.feedback && (
            <div className="explanation">
              <h3>
                {q.feedback.is_correct
                  ? "Correct. Keep testing your reasoning."
                  : `The correct answer is ${q.feedback.correct}.`}
              </h3>
              <p>
                <RichText text={q.feedback.explanation} />
              </p>
              <MathText text={q.feedback.math} />
              {a.answers[q.id] && a.answers[q.id] !== q.feedback.correct && (
                <p className="mistake-rationale">
                  <strong>Why your choice misses the rule:</strong>{" "}
                  {
                    q.feedback.options.find((o) => o.id === a.answers[q.id])
                      ?.rationale
                  }
                </p>
              )}
            </div>
          )}
          <div className="player-actions">
            <button
              className="button secondary"
              disabled={index === 0 || busy}
              onClick={() => setIndex(index - 1)}
            >
              <ChevronLeft size={17} />
              Previous
            </button>
            {!done && !q.feedback && (
              <button
                className="button"
                disabled={!choice || busy || a.answers[q.id] === choice}
                onClick={save}
              >
                {busy
                  ? "Saving…"
                  : a.mode === "practice"
                    ? "Check answer"
                    : "Save answer"}
                <Check size={16} />
              </button>
            )}
            <button
              className="button secondary"
              disabled={index === a.questions.length - 1 || busy}
              onClick={() => setIndex(index + 1)}
            >
              Next
              <ChevronRight size={17} />
            </button>
          </div>
        </section>
        <aside className="panel navigator">
          <h3>{done ? "Your result" : "Your progress"}</h3>
          {done ? (
            <>
              <p className="result-score">
                <strong>{a.score}</strong>
                <span className="result-total">
                  / {a.questions.length}
                </span>
                <span className="result-percent">{percent}%</span>
              </p>
              <ul className="result-breakdown">
                <li className="is-correct">
                  <CheckCircle2 size={15} />
                  {correctCount} correct
                </li>
                <li className="is-wrong">
                  <XCircle size={15} />
                  {wrongCount} incorrect
                </li>
                {missedCount > 0 && (
                  <li className="is-missed">
                    <MinusCircle size={15} />
                    {missedCount} not answered
                  </li>
                )}
              </ul>
            </>
          ) : (
            <>
              <p>
                {answered} of {a.questions.length} answered
              </p>
              <div className="progress">
                <span
                  style={{ width: `${(answered / a.questions.length) * 100}%` }}
                />
              </div>
            </>
          )}
          <div className="question-grid">
            {a.questions.map((x, i) => (
              <button
                key={x.id}
                className={
                  (index === i ? "current " : "") +
                  (done
                    ? x.feedback?.is_correct
                      ? "correct"
                      : a.answers[x.id]
                        ? "wrong"
                        : "missed"
                    : a.answers[x.id]
                      ? "answered"
                      : "")
                }
                aria-label={
                  done
                    ? `Question ${i + 1}: ${
                        x.feedback?.is_correct
                          ? "correct"
                          : a.answers[x.id]
                            ? "incorrect"
                            : "not answered"
                      }`
                    : `Go to question ${i + 1}`
                }
                onClick={() => setIndex(i)}
              >
                {i + 1}
              </button>
            ))}
          </div>
          <p className="help">
            {done
              ? "Green is correct, red is incorrect, grey was left unanswered. Choose a number to review that question."
              : "Filled numbers have a saved answer. Selecting an option does not save it until you press the answer button."}
          </p>
          {!done ? (
            <>
              <button
                className="button full"
                disabled={busy}
                onClick={() => setConfirm(true)}
              >
                Finish & see results
              </button>
              <button className="text-button full mt" onClick={exit}>
                Save and leave
              </button>
            </>
          ) : (
            <button className="button full" onClick={exit}>
              Back to workspace
            </button>
          )}
        </aside>
      </div>
      {confirm && (
        <Modal title="Finish this session?" close={() => setConfirm(false)}>
          <p>
            You have saved {answered} of {a.questions.length} answers.
            Unanswered questions count as incorrect. Submission is final.
          </p>
          <div className="review-actions">
            <button
              className="button secondary"
              onClick={() => setConfirm(false)}
            >
              Keep working
            </button>
            <button
              className="button"
              disabled={busy}
              onClick={() =>
                act(async () => {
                  update(
                    await api<Attempt>(`/attempts/${a.id}/submit`, "POST"),
                  );
                  setConfirm(false);
                  // Land on the result rather than on whichever question
                  // happened to be open when the session was submitted.
                  setIndex(0);
                  window.scrollTo({ top: 0, behavior: "smooth" });
                  await refresh();
                })
              }
            >
              Submit session
            </button>
          </div>
        </Modal>
      )}
    </>
  );
}
