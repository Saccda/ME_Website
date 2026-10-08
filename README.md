# Mechanical Engineering Program — RUPP

Full-stack website foundation for the Mechanical Engineering Program at the
Royal University of Phnom Penh.

## Two systems in this repository

They share a repository and nothing else — no code, no database, no deployment.
One `git pull` brings both to the lab desktop, which is the only reason they sit
together.

| | The public website | Entrance Prep |
|---|---|---|
| Where | `backend/`, `frontend/`, this README | [`entrance-prep/`](entrance-prep/README.md) |
| What | The faculty's public site and its Wagtail CMS | A practice platform where students prepare for the entrance examination |
| Who uses it | Prospective students, parents, partners; staff author the content | Students who register; teachers review the question bank |
| Stack | Django 6 · Wagtail 7 · DRF · Next.js 16 | FastAPI · SQLAlchemy · Next.js 16 |
| Database | SQLite in the lab, PostgreSQL ready | PostgreSQL 17 in Docker |
| Deployment | Next.js on Vercel; API behind a Cloudflare Tunnel | Entirely in Docker on the lab desktop, behind its own Cloudflare Tunnel hostname |
| Compose project | `me-rupp` | `logic-studio` |

The only connection between them is one link: a button on the Admissions page
that appears when **Entrance preparation platform URL** is filled in under
Wagtail's Program settings, and is hidden when it is empty. Removing the
platform means clearing that one field.

Each has its own validation commands. The ones below are the website's; Entrance
Prep's are in its own [README](entrance-prep/README.md) and
[`docs/`](entrance-prep/docs/).

## Architecture

- **Frontend:** Next.js 16, React 19, TypeScript, App Router
- **Backend:** Python 3.14, Django 6, Django REST Framework
- **Content management:** Wagtail 7
- **Local database:** SQLite
- **Production database:** PostgreSQL through `DATABASE_URL`
- **Media:** Local filesystem in development; S3/R2-compatible storage can be
  configured for production

The homepage reads its content from Django. If the API is temporarily
unavailable, the frontend uses approved static fallback content so the public
page remains usable.

## Open in VS Code or Cursor

Open this folder as the workspace:

`C:\Users\USER\Documents\Mechanical Engineering Website`

The Python environment and JavaScript dependencies are already installed.

## Run locally

Use two integrated terminals.

### Terminal 1 — Django API and CMS

```powershell
cd backend
.\.venv\Scripts\python.exe src\manage.py runserver 127.0.0.1:8000
```

### Terminal 2 — Next.js frontend

```powershell
cd frontend
npm.cmd run dev
```

Then open:

- Public website: http://127.0.0.1:3000
- API health check: http://127.0.0.1:8000/api/v1/health/
- Wagtail CMS: http://127.0.0.1:8000/admin/

Create the first CMS administrator when needed:

```powershell
cd backend
.\.venv\Scripts\python.exe src\manage.py createsuperuser
```

## Validate changes

```powershell
cd backend
.\.venv\Scripts\python.exe src\manage.py check
.\.venv\Scripts\python.exe src\manage.py test program

cd ..\frontend
npm.cmd run lint
npm.cmd run build
```

## Initial content

The seed command is safe to run again; it updates the approved starter content
without creating duplicate records.

```powershell
cd backend
.\.venv\Scripts\python.exe src\manage.py seed_me_content
```

Local environment examples are provided in:

- `backend/.env.example`
- `frontend/.env.example`

Copy either file to `.env` only when you need to override the development
defaults. Never commit real passwords or production secret keys.

## Deploy

The production architecture and exact launch checklist are documented in
[`DEPLOYMENT.md`](DEPLOYMENT.md). The public Next.js site runs on Vercel; the
Django/Wagtail API runs behind an outbound-only Cloudflare Tunnel on the lab
desktop.
