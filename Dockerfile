# Task Tracker API — multi-stage image.
# Builder installs Python deps; runtime serves FastAPI + static frontend as non-root.

# ---------------------------------------------------------------------------
# Build stage: resolve and install dependencies into an isolated prefix
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# Dependency manifest only — keeps this layer cached when app code changes
COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------------------------------------------------------------------------
# Runtime stage: lean image with pre-installed deps and application code
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

# Same Python process behaviour as before (bytecode off, unbuffered stdout/stderr)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Non-root user to run the app
RUN groupadd --system app \
    && useradd --system --gid app --no-create-home app

WORKDIR /app

# Installed packages from the builder (invalidates only when requirements change)
COPY --from=builder /install /usr/local

# Runtime code only (tests/docs/.env etc. excluded via .dockerignore)
COPY app ./app
COPY frontend ./frontend

EXPOSE 8000

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
