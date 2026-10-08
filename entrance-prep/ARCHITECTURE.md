# Architecture

```text
Browser (teacher / student)
    ↓ same-origin /api proxy
Next.js · responsive UI · KaTeX · install manifest
    ↓ private API service
FastAPI · HttpOnly session cookie · server role checks
    ├─ Original template generator → draft → deterministic checks → human review
    ├─ Question bank + immutable audit history
    ├─ Blueprint allocation → immutable attempt snapshots → server scoring
    ├─ Topic / difficulty / distractor analytics
    └─ DOCX / PDF adapter
         ↓
SQLAlchemy → SQLite (local) / PostgreSQL (deployment)
```

## Boundaries

`frontend/app/page.tsx` opens the student workspace directly, with a Student workspace / Teacher studio selector. There are no login or registration forms. `lib/types.ts` defines response shapes; `lib/api.ts` sends same-origin requests with an anonymous browser session. `next.config.ts` proxies `/api` to `API_URL` (default `http://127.0.0.1:8000`). Deploy behind one HTTPS origin. There are no frontend secrets.

`backend/app/catalog.py` defines the seven domains, precise source-set mapping, internal attribution, and the local level rubric. `generator.py` provides bounded original template families. `validation.py` recomputes supported answers and checks media/MCQ structure. An LLM provider could eventually implement the same content contract, but no provider is configured or needed in this version.

`POST /api/workspace` bootstraps an anonymous learner when `AUTH_MODE=open` (the default). It creates a random browser visitor identity and an opaque HttpOnly/SameSite=Strict cookie. Only the token's SHA-256 hash persists. Sessions last 30 days and renew when opened. A visitor's student and teacher identities are paired internally, so changing workspaces preserves student progress without mixing it with another browser or teacher-preview attempts. Guest records have randomly generated unusable credentials; visitors never provide names, emails, or passwords. Existing database tables support this without a schema migration.

Open-mode role selection is **not an authorization boundary**: any visitor can choose Teacher studio. Student-mode APIs still exclude keys/private metadata and reject direct teacher operations until that workspace is chosen. The raw textbook is never available in either workspace. Replace workspace bootstrapping / `current_user` with trusted ME-website identity, or restrict studio access at the website boundary, when integrating the official website. `AUTH_MODE=credentials` retains the earlier backend session contract for compatibility and disables open workspace switching; it does not add a login form back to this frontend. In that mode the frontend expects the host website to have established a session. No website integration has been implemented yet.

`models.py` retains credential-related tables for compatibility. Legacy account passwords use scrypt and legacy sessions expire in 12 hours. Login/registration endpoints are disabled in open mode. HTTP mutations require a custom request header and an allowed origin; secure cookies are enabled for deployment.

`main.py` implements REST contracts, source/key stripping, approval transitions, optimistic question versions, blueprint resolution, immutable attempt snapshots, and server deadlines. PostgreSQL locks attempts while answering; a revision check also prevents lost updates under SQLite. Scoring uses snapshot answer keys and accepts no client scores. Practice responses reveal feedback only for checked questions; exams reveal it only when submitted or expired. Editing a question never rewrites an existing attempt.

`exports.py` converts approved records to question papers, keys, or solutions. Export adapters deliberately exclude private source metadata. Current adapters include prose, media, and tables; they do not typeset arbitrary TeX. KaTeX renders browser math with `trust=false`. No arbitrary HTML/SVG from authors is inserted into question content; diagrams render escaped labels in a controlled component. Images are bounded data URIs with verified file signatures. For a larger bank, move media to authenticated object storage and introduce paginated question-bank queries.

Alembic `0001` is the initial schema. JSON content permits PostgreSQL and SQLite parity without vendor-specific operators. Migration execution is separated from multi-worker application startup in Docker. Local auto-creation is for fresh databases only. Startup seeds once per empty question bank; real installations create drafts, explicit demos create test approvals. Use separate databases for demo and real operation.

## Source map

| Student domain | Private book sets | Primary original template skills |
| --- | --- | --- |
| Number & Pattern Reasoning | 1–4 | Fixed step, growing differences, alternating operations, recurrence |
| Letter & Symbol Reasoning | 5–6 | Alphabet steps, cycles, paired letter/number, alternating jumps |
| Classification & Relationships | 7–17 | Classification, function analogy, essential properties, relationship chain |
| Coded Language Reasoning | 18–19 | Component meaning, ordered decoding, encoding, elimination |
| Applied Verbal Reasoning | 20–22 | Definitions, necessary conditions, must-be-true, combined conditions |
| Deductive Logic & Logic Games | 23–31 | Ordering, adjacency, conditional constraints, constrained arrangement |
| Critical & Argument Reasoning | 32–37 | Conclusion, assumption, weakening, causal confounding |

The generator creates original questions. A separate explicit private importer supports a small textbook selection after verifying transcription, the book key, and independent rules. Students receive selected questions and minimal attribution; the full PDF and private verification metadata are never served. The book's explanation approach informs the original answer → reasoning rule → application → distractor elimination structure. The four difficulty labels are local authoring categories, not labels asserted by the book or the real exam.

## Operational scope

Run a single API process for local SQLite. Use PostgreSQL and the initial migration for deployment. Back up the database and private references separately. The API docs are at `/api` proxy path only for routes; development OpenAPI docs are available directly at `http://127.0.0.1:8000/docs`. Use reverse-proxy limits for internet traffic and institutional account policies before rollout.

The service worker caches only a static reconnect page. It never caches sessions, question responses, answer keys, private sources, or attempt state. Installability is provided; offline exams are deliberately outside this version's scope because server authority is required for deadlines and scoring.
