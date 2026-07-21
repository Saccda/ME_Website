# Production deployment

This project uses two independently deployable parts:

- **Public website:** Next.js on Vercel
- **CMS and API:** Django/Wagtail on the lab desktop, reached through a
  Cloudflare Tunnel

The lab router should not expose ports 80, 443, or 8000. `cloudflared` makes an
outbound-only connection to Cloudflare, while Docker publishes the local web
service on `127.0.0.1:8080` only.

## Recommended launch addresses

For the first release, use the Vercel-generated address for the public site and
a private-looking API hostname such as:

- Public site: `https://me-rupp.vercel.app`
- Temporary API and CMS: `https://me-api.putsaccada.dpdns.org`
- Temporary CMS login: `https://me-api.putsaccada.dpdns.org/admin/`

The supplied `farmosmechanicalengineering.com` name currently returns NXDOMAIN,
so it cannot be connected yet. It is also better suited to temporary
infrastructure or staging than the public program identity. For the final
identity, request a university subdomain such as `me.fe.rupp.edu.kh` from RUPP
IT, or buy a shorter ME/RUPP-specific domain. The public domain can be changed
later without changing the application architecture.

## 1. Prepare the lab desktop

1. Install Docker Desktop and Cloudflare Tunnel (`cloudflared`).
2. In Docker Desktop, enable **Start Docker Desktop when you sign in**.
3. Copy `backend/.env.production.example` to `backend/.env.production`.
4. Replace the secret and host placeholders in `.env.production`.
5. Keep `backend/.env.production`, `backend/src/db.sqlite3`, and
   `backend/src/media/` out of Git.

Generate a Django secret without using an online generator:

```powershell
cd backend
.\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Start the production backend from the repository root:

```powershell
docker compose -f compose.production.yml up -d --build
docker compose -f compose.production.yml ps
```

Check the local API before configuring the tunnel:

```powershell
curl.exe -H "X-Forwarded-Proto: https" http://127.0.0.1:8080/api/v1/health/
```

## 2. Configure Cloudflare Tunnel

The launch tunnel is named `me-rupp-api`. Its DNS route is already configured.
When moving the backend to the lab desktop, configure that connector with the
following ingress and point it to the local Nginx service:

```text
Hostname: me-api.putsaccada.dpdns.org
Service:  http://127.0.0.1:8080
```

For a Windows machine using a locally managed tunnel, copy
`backend/deploy/cloudflared-config.example.yml` to the system service's
`.cloudflared/config.yml`, insert the tunnel UUID and credentials path, then
follow Cloudflare's Windows service installation procedure.

For a remotely managed connector created in the Cloudflare dashboard, install
its token as a Windows service from an Administrator terminal:

```powershell
cloudflared service install YOUR_TUNNEL_TOKEN
```

The token is a secret. Do not put it in this repository or a screenshot.

Verify these URLs after the tunnel connects:

- `/api/v1/health/` returns `{"status":"ok",...}`
- `/api/v1/home/` returns the program content
- `/admin/` shows the Wagtail sign-in page
- `/media/original_images/...` returns an uploaded image

## 3. Deploy the frontend to Vercel

Create a Vercel project with `frontend` as the **Root Directory**. Add this
environment variable to Production and Preview:

```text
NEXT_PUBLIC_API_URL=https://me-api.putsaccada.dpdns.org/api/v1
```

Vercel automatically detects Next.js. The required commands are already in
`frontend/package.json`:

```text
Build command:  npm run build
Output:         Next.js default
Install:        npm install
```

After Vercel assigns the real deployment hostname, update
`CORS_ALLOWED_ORIGINS` in `backend/.env.production` and restart the backend:

```powershell
docker compose -f compose.production.yml up -d
```

## 4. Domain cutover later

When the final public domain is approved:

1. Add it to the Vercel project.
2. Follow the exact DNS record Vercel provides in the project dashboard.
3. Add the new `https://...` origin to `CORS_ALLOWED_ORIGINS`.
4. Redeploy the frontend so metadata and canonical URLs can be finalized.

Do not place the Django admin on the public marketing hostname. Keeping the CMS
on the API hostname makes the architecture clearer and easier to protect with
Cloudflare Access later.

## 5. Operations and backups

The first release keeps the existing SQLite database because there is one
Django instance and traffic will be modest. Back up these together:

- `backend/src/db.sqlite3`
- `backend/src/media/`
- `backend/.env.production`

Before adding manufacturing orders, customer accounts, quotations, or payments,
migrate to PostgreSQL and add off-machine media/database backups. A lab desktop
outage will not remove the Vercel landing page because the frontend has approved
fallback content, but the CMS, live inquiries, and newly uploaded content will
be unavailable until the desktop and tunnel return.
