# Task Tracker API — Module 4

A learning-focused REST API built with **Python**, **FastAPI**, and **Pydantic v2**.
Task storage is in-memory (a module-level dict in `app/storage.py`) — there is no
database, and data does not persist across a server restart. A static HTML/JS
frontend (`frontend/index.html`) is served directly by the API at `/`.

This is a learning project. It is **not** deployed anywhere, has **no
authentication**, and is **not intended for production use**.

**GitHub repository:** https://github.com/MikeSAFI/task-tracker-api

---

## 1. Project Overview

The API exposes CRUD endpoints for tasks (`/tasks`), each with a title, status
(`ToDo` / `InProgress` / `Done`), priority (`Low` / `Medium` / `High`), optional
assignee, optional due date, and tags. Status changes are constrained to a fixed
transition graph, and `overdue` is derived on every read from `due_date` — it is
never stored. See [Project conventions and current limitations](#9-project-conventions-and-current-limitations)
for the full rule set.

---

## 2. Prerequisites

- **Python 3.11** — matches the version pinned in `.github/workflows/ci.yml`
  and `Dockerfile`. Also confirmed working locally on Python 3.13.
- **pip** (bundled with Python)
- **git**
- **Docker** — only required for [section 6](#6-run-with-docker); not needed
  for local development.

---

## 3. Local setup

### 1. Clone / enter the project directory

```bash
git clone https://github.com/MikeSAFI/task-tracker-api.git
cd task-tracker-api
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

`.env.example` is present in the repo, but nothing under `app/` reads
environment variables (no `os.environ`/`dotenv` usage found) — the app doesn't
currently need a `.env` file to run.

---

## 4. Run the app locally

From the repo root, with the virtual environment activated:

```bash
uvicorn app.main:app --reload --port 8000
```

| Flag          | Purpose                                          |
| ------------- | ------------------------------------------------ |
| `--reload`    | Auto-restarts on code changes (development only) |
| `--port 8000` | Local dev port                                   |

Default backend URL: http://localhost:8000

**Task board (frontend):** http://localhost:8000/ — the API serves
`frontend/index.html` directly from the root route.

**Interactive API docs:** http://localhost:8000/docs (Swagger UI) or
http://localhost:8000/redoc (ReDoc).

**Smoke-test the health endpoint:**

```bash
curl -s http://localhost:8000/health
```

Expected response shape:

```json
{
  "status": "ok",
  "timestamp": "2026-07-27T10:30:00.123456+00:00"
}
```

---

## 5. Run tests

From the repo root, with the virtual environment activated:

```bash
pytest -v
```

`pytest.ini` sets `pythonpath = .`, so tests import `app` as a top-level
package without an install step.

Run a single test file or test:

```bash
pytest tests/test_tasks.py -v
pytest tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 -v
```

Run the Part A model verification script:

```bash
python -m tests.verify_a
```

Run it as `python -m tests.verify_a`, not `python tests/verify_a.py` — the
script imports `app.models`, and running it as a bare script (rather than
`-m`) does not put the repo root on `sys.path`, so it fails with
`ModuleNotFoundError: No module named 'app'`. Confirmed by running both forms
from a clean checkout.

---

## 6. Run with Docker

From the repo root:

```bash
docker build -t task-tracker-api .
docker run --rm -p 8000:8000 task-tracker-api
```

Then open http://localhost:8000/ the same as the local run.

The image is a two-stage build (`python:3.11-slim`) that installs
dependencies in a builder stage, then copies only `app/` and `frontend/` into
a runtime stage that runs as a non-root user (`app`) and listens on port
8000. `tests/`, `docs/`, `deliverables/`, `.env`, and `CLAUDE.md` are excluded
from the image via `.dockerignore`. The container's `CMD` runs uvicorn
**without** `--reload` — this is a plain container run for local use, not a
deployment configuration.

---

## 7. CI workflow summary

`.github/workflows/ci.yml` defines a single `test` job that runs on every
`push` and `pull_request` (all branches, no path filters):

1. Check out the repository (`actions/checkout@v4`).
2. Set up Python 3.11 (`actions/setup-python@v5`).
3. `pip install -r requirements.txt`.
4. `pytest -v`.

There is no linting, Docker build/push, or deployment step.
CI runs only the test suite.
The latest successful CI evidence is recorded in `docs/release-evidence.md`.

---

## 8. Project structure

```
task-tracker-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI route handlers
│   ├── models.py          # Pydantic schemas / enums
│   ├── business_rules.py  # cross-field validation (status transitions, due dates)
│   └── storage.py         # in-memory "database" + CRUD functions
├── frontend/
│   └── index.html         # static task board UI, served at "/"
├── tests/
│   ├── conftest.py        # client fixture + autouse storage reset
│   ├── test_tasks.py
│   └── verify_a.py        # Part A model verification script
├── docs/
│   ├── mini-adr.md        # architecture decisions (see section 10)
│   ├── user-stories.md
│   ├── prompt-log.md
│   ├── prompts.md         # [VERIFY] purpose not documented in CLAUDE.md
│   ├── reflection.md
│   └── verification.md    # [VERIFY] purpose not documented in CLAUDE.md
├── deliverables/          # course submission artifacts (docx/xlsx/md)
├── .github/workflows/ci.yml
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── pytest.ini
├── .env.example
└── CLAUDE.md
```

---

## 9. Project conventions and current limitations

**Conventions**

- Four single-responsibility modules under `app/`: `models.py` (schemas),
  `business_rules.py` (cross-field/stateful validation, raises
  `HTTPException` directly), `storage.py` (in-memory CRUD), `main.py` (route
  handlers — no business logic of their own).
- All Pydantic models use `extra="forbid"`; unknown request fields get a 422.
- `overdue` is never stored — it's recomputed from `due_date` vs. today's
  date on every read.
- `PATCH /tasks/{id}` only re-validates `due_date` when it's present in the
  request **and** actually changed, so patching other fields on a task that
  already has a past due date is allowed.
- Status transitions are restricted to `ToDo→InProgress→Done→InProgress`; no
  same-state transition and no skipping states.
- Tags are a flat `list[str]`, alphanumeric only, ≤255 chars each.
- Tests follow `test_<action>_<condition>_returns_<result>` naming, and an
  autouse fixture resets in-memory storage before/after every test.

**Current limitations**

- **No persistence** — all data is lost on process restart; there is no
  database.
- **No authentication or authorization** on any endpoint.
- **Not deployed** — the Dockerfile and CI only build/test locally; there is
  no deployment or hosting configuration in this repo.
- CORS is restricted to a fixed list of local dev origins (`localhost`/
  `127.0.0.1` on ports `5500`, `5501`, `5173`, plus `null` for local file
  access) — not suitable for other origins without code changes.
- `requirements.txt` is UTF-16LE-encoded.
  `pip install -r requirements.txt` works, but normalize the file to UTF-8 if it is edited again.

---

## 10. Decisions and docs

Architecture decisions (and rejected alternatives) for due dates, overdue
filtering, and tags are recorded in [`docs/mini-adr.md`](docs/mini-adr.md) —
check it before changing how those features are modeled.

`docs/user-stories.md`, `docs/prompt-log.md`, `docs/prompts.md`,
`docs/reflection.md`, and `docs/verification.md` are course-deliverable
artifacts from an AI-assisted-coding curriculum, not living technical docs.

---

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and/or pull request.
- Docker image builds and runs with `/health` returning 200.
- AI review, security, and ownership evidence is in `docs/`.

### How to run locally

From repo root, with `venv` activated:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then open http://localhost:8000/ (Kanban board) and http://localhost:8000/health.

### How to run tests

```bash
pytest -q
```

On Windows, if `pytest` is not on PATH: `.\venv\Scripts\python.exe -m pytest -q`.

### How to run with Docker

```bash
docker build -t task-tracker-api .
docker run --rm -p 8000:8000 task-tracker-api
curl -s http://localhost:8000/health
```

PowerShell health check: `Invoke-RestMethod http://localhost:8000/health`.

### Evidence files

- [docs/release-evidence.md](docs/release-evidence.md)
- [docs/final-ai-review.md](docs/final-ai-review.md)
- [docs/ai-playbook.md](docs/ai-playbook.md)

### AI assistance summary

AI helped draft or review: CI, Docker, docs, security review grading, and debugging (including constrained FastAPI/tests/frontend work earlier in the course).

I verified the work by: running pytest, reviewing diffs against ADRs/stories, Docker build/run and `/health`, and manual security checks (e.g. create-status behavior).

One AI suggestion I rejected or corrected: Rejected storing an `overdue` flag (and a separate Tag entity) — overdue stays derived on read. Also corrected an early PATCH due-date gate so validation runs only when `due_date` is present **and** actually changed, so unrelated patches on already-past due dates are not blocked.
