FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends fonts-dejavu-core && rm -rf /var/lib/apt/lists/*
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY backend/alembic.ini .
COPY backend/migrations ./migrations
# Needed inside the container: approving machine-proved questions on a fresh
# install, importing a checked textbook selection, and the load test.
COPY backend/tools ./tools
COPY frontend/public/brand /app/frontend/public/brand
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
# One worker is one CPU core, and every request holds a database connection for
# its whole life, so a single worker caps concurrency at its pool size. Workers
# are configurable; startup seeding is serialised by an advisory lock so several
# of them can start safely.
CMD ["sh", "-c", "python -m alembic upgrade head && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers ${WEB_CONCURRENCY:-1}"]
