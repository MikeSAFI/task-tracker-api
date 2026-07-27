# ---- Build stage: resolve and install dependencies ----
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---- Runtime stage ----
FROM python:3.11-slim

# Non-root user to run the app
RUN groupadd --system app && useradd --system --gid app --no-create-home app

WORKDIR /app

# Installed dependencies from the build stage
COPY --from=builder /install /usr/local

# Only the runtime code the app needs (no tests/docs/.env)
COPY app ./app
COPY frontend ./frontend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
