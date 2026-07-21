# Mechanical Engineering Program — RUPP

Full-stack website foundation for the Mechanical Engineering Program at the
Royal University of Phnom Penh.

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
