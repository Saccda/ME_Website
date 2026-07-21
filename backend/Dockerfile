FROM python:3.12-slim-bookworm AS builder

RUN apt-get update --yes --quiet \
    && apt-get install --yes --quiet --no-install-recommends \
        build-essential \
        libpq-dev \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libwebp-dev \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt


FROM python:3.12-slim-bookworm AS runtime

RUN apt-get update --yes --quiet \
    && apt-get install --yes --quiet --no-install-recommends \
        libpq5 \
        libjpeg62-turbo \
        libwebp7 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 wagtail

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=me_backend.settings.production \
    PORT=8000 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=wagtail:wagtail src/ /app/
COPY --chown=wagtail:wagtail deploy/entrypoint.sh /app/deploy/entrypoint.sh

RUN chmod +x /app/deploy/entrypoint.sh \
    && mkdir -p /app/static /app/media /run/me-secrets \
    && chown -R wagtail:wagtail /app /run/me-secrets

USER wagtail
EXPOSE 8000

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
