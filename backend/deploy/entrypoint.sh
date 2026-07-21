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

exec gunicorn me_backend.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${GUNICORN_WORKERS:-1}" \
  --threads "${GUNICORN_THREADS:-4}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --access-logfile - \
  --error-logfile -
