### Project Identity

- **Product:** Public academic website + headless CMS for the Royal University of Phnom Penh (RUPP), Faculty of Engineering, Mechanical Engineering (ME) Program.
- **Audience:** Prospective/current students, parents, faculty, researchers, academic/industry partners, employers; later, external customers of the planned ME Manufacturing Station.
- **Current goal:** Deliver a modern, accessible, CMS-driven academic site emphasizing ME impact, four focus areas (DMP/TES/MAS/ECM), research, facilities, curriculum, partnerships, and opportunities. Keep academic content primary; manufacturing-service/e-commerce functionality is not yet built and requires verified equipment specifications.
- **Production:** frontend `https://me-rupp.vercel.app`; API `https://me-api.farmos-mechanicalengineering.com/api/v1`; Wagtail `https://me-api.farmos-mechanicalengineering.com/admin/`. `main` is the release branch. Agent pushes GitHub + deploys Vercel; user manually pulls/rebuilds/restarts the lab backend.

### Tech Stack

| Layer | Exact implementation |
|---|---|
| Frontend | Next.js `16.2.10` App Router + Turbopack, React/React DOM `19.2.4`, strict TypeScript, Node/npm |
| Rendering/data | Async React Server Components by default; dynamic routes use `export const dynamic = "force-dynamic"`; native `fetch` with `cache: "no-store"` + 2.5 s timeout + approved static fallback data |
| UI/CSS | Handwritten `frontend/src/app/globals.css`; CSS custom properties; no Tailwind, CSS-in-JS, component library, animation library, or icon package |
| State | No global store/React Query. Local `useState`/`useEffect` only in client components (`ImpactStory`, `CurriculumTabs`, `InquiryForm`) |
| Backend | Docker runtime Python `3.12`; Django `>=6.0,<6.1`; Wagtail `>=7.4,<7.5`; Django REST Framework `>=3.17,<3.18`; django-cors-headers, django-filter, Pillow |
| Persistence/media | Current lab deployment: SQLite bind-mounted at `backend/src/db.sqlite3`; PostgreSQL supported via `DATABASE_URL`; Wagtail images/media on bind-mounted filesystem `backend/src/media/` |
| Serving | Gunicorn (`1` worker/`4` threads defaults) behind Nginx; Docker Compose; Cloudflare Tunnel exposes lab API/CMS; no inbound router ports |
| Frontend hosting | Linked Vercel project `me-rupp`; root directory `frontend`; production alias `me-rupp.vercel.app` |
| QA | ESLint 9 + `eslint-config-next`; strict `tsc` during `next build`; Django `check` + `program` tests |

### System Architecture

```text
Content author
└─ HTTPS /admin/ (Wagtail)
   ├─ ProgramSettings (site settings: identity/home copy/research copy/social/contact)
   ├─ Snippets (WhyChooseItem, FocusArea, CurriculumYear/Course,
   │            ResearchProject, Partner, Opportunity, Facility,
   │            FocusAreaDetailItem, FacultyMember, NewsEvent)
   └─ Wagtail Images/Documents
      └─ Django ORM
         ├─ SQLite now / PostgreSQL when DATABASE_URL is set
         └─ media filesystem

Public browser
└─ Vercel → Next.js App Router (`frontend/src/app/**/page.tsx`)
   ├─ shared shell
   │  ├─ `components/SiteHeader.tsx`
   │  │  └─ `config/navigation.ts` (desktop hover/focus dropdown + mobile disclosure)
   │  └─ `components/SiteFooter.tsx`
   ├─ server-side data
   │  └─ `lib/api.ts`
   │     ├─ NEXT_PUBLIC_API_URL
   │     ├─ no-store fetch + timeout
   │     ├─ normalizes legacy `focus_area` → `focus_areas`
   │     ├─ backfills focus areas missing newer CMS fields from fallback
   │     └─ falls back to approved in-file content if API fails/is empty
   ├─ editorial/static mappings
   │  ├─ `lib/impactProjects.ts`
   │  └─ `lib/editorialImages.ts`
   └─ UI → `app/globals.css` + `public/assets/**`
      └─ responsive/a11y/reduced-motion behavior

NEXT_PUBLIC_API_URL
└─ Cloudflare Tunnel
   └─ `127.0.0.1:8080` Nginx (`backend/deploy/nginx.conf`)
      ├─ `/static/`, `/media/`
      └─ Gunicorn :8000
         └─ Django URLConf (`backend/src/me_backend/urls.py`)
            └─ `/api/v1/` (`backend/src/program/urls.py`)
               ├─ `health/`, `home/`, `inquiries/`
               └─ DRF ViewSets: focus-areas, curriculum, research, partners,
                  facilities, faculty, news, opportunities
                  └─ `program/api.py` → `serializers.py` → `models.py`
```

### Completed Features

| Feature Name | Exact File Path(s) | Current Status |
|---|---|---|
| Responsive branded fixed header, accessible hover/focus dropdowns, mobile navigation | `frontend/src/components/SiteHeader.tsx`; `frontend/src/config/navigation.ts`; `frontend/src/app/globals.css`; `frontend/public/assets/brand/**` | Production |
| Homepage hero, program metrics, “What is ME?”, focus areas, nine reasons, partners | `frontend/src/app/page.tsx`; `frontend/src/components/ImpactStory.tsx`; `frontend/src/lib/impactProjects.ts`; `frontend/src/app/globals.css` | Production; mixed CMS/static content |
| Four academic focus-area detail pages with curriculum, equipment, activities, careers, related research | `frontend/src/app/focus/[slug]/page.tsx`; `frontend/src/lib/api.ts`; `frontend/src/lib/editorialImages.ts`; `backend/src/program/models.py`; `backend/src/program/serializers.py`; `backend/src/program/api.py` | Production |
| Research landing page + direct Research → DMP/TES/MAS/ECM navigation | `frontend/src/app/research/page.tsx`; `frontend/src/app/research/[focus]/page.tsx`; `frontend/src/config/navigation.ts`; `frontend/src/app/globals.css` | Production; API-compatible with old/new research schemas |
| Wagtail-editable research copy: landing sections, per-area question/overview, ordered research themes | `backend/src/program/models.py` (`ProgramSettings.research_*`, `FocusArea.research_question`/`research_overview`, `FocusAreaDetailItem` `theme` type); `backend/src/program/serializers.py`; `backend/src/program/migrations/0008_research_editorial_content.py`; `frontend/src/lib/api.ts`; `frontend/src/app/research/page.tsx`; `frontend/src/app/research/[focus]/page.tsx` | Production; no hard-coded research copy remains |
| Curriculum by year/semester with course code/title/credits | `frontend/src/app/curriculum/page.tsx`; `frontend/src/components/CurriculumTabs.tsx`; `backend/src/program/models.py`; `backend/src/program/serializers.py` | Production |
| Facility/equipment catalog linked to focus areas and availability | `frontend/src/app/facilities/page.tsx`; `backend/src/program/models.py`; `backend/src/program/api.py`; `backend/src/program/serializers.py` | Production; catalog, not commerce |
| Faculty and news/events directory pages | `frontend/src/app/people/page.tsx`; `frontend/src/app/news-events/page.tsx`; `backend/src/program/models.py`; `backend/src/program/api.py` | Production; no standalone article/profile detail routes |
| Partner logo marquee with external website links | `frontend/src/app/page.tsx`; `backend/src/program/models.py`; `backend/src/program/serializers.py`; `frontend/public/assets/partners/**` | Production |
| CMS-driven job/internship/scholarship/training cards | `frontend/src/components/IndustryCareers.tsx`; `frontend/src/app/page.tsx`; `backend/src/program/models.py`; `backend/src/program/api.py`; `backend/src/program/serializers.py` | Production |
| Compact academic footer + admissions/social links | `frontend/src/components/SiteFooter.tsx`; `frontend/src/components/AdmissionBar.tsx`; `frontend/public/assets/icons/**` | Production |
| Headless Wagtail CMS, ordered snippets, image uploads, REST API, seed data, migrations | `backend/src/program/models.py`; `backend/src/program/wagtail_hooks.py`; `backend/src/program/serializers.py`; `backend/src/program/api.py`; `backend/src/program/management/commands/seed_me_content.py`; `backend/src/program/migrations/**` | Implemented; user deploys lab backend manually |
| Resilient API/fallback layer and legacy research response normalization | `frontend/src/lib/api.ts` | Production |
| Docker/Nginx/Gunicorn/Cloudflare + Vercel deployment | `compose.production.yml`; `backend/Dockerfile`; `backend/deploy/**`; `DEPLOYMENT.md`; `frontend/.vercel/project.json` (local link metadata) | Production |

### Code Conventions

- **Read first:** `frontend/AGENTS.md`; Next 16 APIs may differ from prior knowledge—consult `frontend/node_modules/next/dist/docs/` before framework changes.
- **TypeScript:** strict; 2-space indent; semicolons; double quotes; PascalCase components/types, camelCase functions/variables, kebab-case URL segments and CSS classes. `@/*` aliases `frontend/src/*`.
- **API naming:** Preserve backend `snake_case` in frontend DTOs (`focus_areas`, `accent_color`, `published_at`) to avoid translation layers. Normalize version differences only inside `frontend/src/lib/api.ts`.
- **React:** Server Components by default; add `"use client"` only for browser state/events. Fetch in server pages/helpers, not presentation components. Prefer typed props and pure mapping; no global mutable state.
- **Next routes:** `src/app/<route>/page.tsx`; dynamic segments `[slug]`/`[focus]`; define metadata where useful; public content is force-dynamic because CMS data uses `no-store`.
- **CSS:** All production styling is in `frontend/src/app/globals.css`; semantic kebab-case selectors; reuse root tokens (`--brand-navy`, `--brand-gold`, `--cream`, `--ink`, `--shell`, `--font-sans`, `--font-serif`). Brand palette is navy/gold/cream/white with focus accents. Typography is Segoe UI Variable/Segoe UI/Arial + Georgia only; avoid oversized headings that force unnecessary 2–3-line wraps. Maintain responsive breakpoints, visible keyboard focus, `prefers-reduced-motion`, semantic HTML, ARIA labels, and alt text.
- **Assets:** Public runtime paths start `/assets/...`; source assets live under `frontend/public/assets/**`. Keep attribution files for externally sourced images. Do not reuse an image in unrelated sections.
- **Python:** PEP 8, 4-space indent, snake_case fields/functions, PascalCase models/serializers/viewsets. CMS collections are Wagtail `@register_snippet` models inheriting `OrderedModel`; expose fields via explicit serializers/panels.
- **Schema:** Create a new numbered migration for every model change; never rewrite applied migrations. Update `seed_me_content.py`, serializers, API/query prefetches, tests, and frontend DTO/fallbacks together.
- **Reliability/security:** Never commit `.env`, credentials, tunnel tokens, `db.sqlite3`, or uploaded media. Public GET APIs are open; inquiry POST is throttled. Frontend must remain usable if API/media is temporarily unavailable.
- **Validation before release:** `backend\.venv\Scripts\python.exe backend\src\manage.py check`; `backend\.venv\Scripts\python.exe backend\src\manage.py test program`; from `frontend`: `npm.cmd run lint` then `npm.cmd run build`; `git diff --check`; verify public routes after Vercel deployment.
- **Release ownership:** Commit/push `main` to GitHub and deploy only `frontend` to linked Vercel. Do not operate the lab desktop; tell the user exactly when to `git pull` and run `docker compose -f compose.production.yml up -d --build`.

### Immediate Next Steps

1. **Create canonical research-project detail pages.** Create `frontend/src/app/research/projects/[slug]/page.tsx`; add `getResearchProject(slug)` to `frontend/src/lib/api.ts`; ensure `ResearchProjectViewSet.lookup_field = "slug"` and full rich-text/image/focus serialization in `backend/src/program/api.py` + `serializers.py`; update project links in `frontend/src/app/research/page.tsx` and `[focus]/page.tsx` to `/research/projects/<slug>`; add detail-page styles to `frontend/src/app/globals.css` and API/route tests to `backend/src/program/tests.py`.
2. **Integrate research faculty by area (MIT-inspired but ME/RUPP-branded).** Extend `getFacultyMembers(focusCode?)` in `frontend/src/lib/api.ts`; add optional `?focus=` filtering/prefetch to `FacultyMemberViewSet` in `backend/src/program/api.py`; render a compact faculty strip on `frontend/src/app/research/page.tsx` and filtered faculty cards on `frontend/src/app/research/[focus]/page.tsx`; reuse `FacultyMember.focus_areas`, add responsive/accessibility styles in `frontend/src/app/globals.css`, and cover filtering in `backend/src/program/tests.py`.
