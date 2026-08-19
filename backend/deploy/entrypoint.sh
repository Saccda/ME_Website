#!/bin/sh
set -eu

if [ -z "${DJANGO_SECRET_KEY:-}" ]; then
  secret_file="/run/me-secrets/django_secret_key"
  if [ ! -s "$secret_file" ]; then
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > "$secret_file"
    chmod 600 "$secret_file"
  fi
  DJANGO_SECRET_KEY="$(cat "$secret_file")"
  export DJANGO_SECRET_KEY
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

# Gunicorn's default access format records no timing, so a slow response could
# not be attributed. The API answers in about 300ms warm, but requests have
# been measured at 3.9s and 6.9s, and from outside the whole chain -- Vercel,
# Cloudflare edge, the tunnel, cloudflared here, Nginx, Gunicorn, Django,
# SQLite -- is timed as one number.
#
# The trailing %(L)s is how long this process took, in seconds. It excludes
# Nginx and the tunnel by design: a slow request logged as fast was slow on the
# network, and one logged as slow was slow here. The two want different fixes.
exec gunicorn me_backend.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${GUNICORN_WORKERS:-1}" \
  --threads "${GUNICORN_THREADS:-4}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --access-logfile - \
  --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s' \
  --error-logfile -
