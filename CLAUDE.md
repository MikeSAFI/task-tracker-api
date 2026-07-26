# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A learning-focused Task Tracker REST API built with Python, FastAPI, and Pydantic v2. Storage is in-memory (a module-level dict in `app/storage.py`) — there is no database. A static HTML/JS frontend (`frontend/index.html`) is served directly by the API at `/`.

## Commands

```bash
# Install dependencies (from repo root, with venv activated)
pip install -r requirements.txt

# Run the dev server (reload on change)
uvicorn app.main:app --reload --port 8000

# Run the full test suite
pytest -q

# Run a single test file / test
pytest tests/test_tasks.py -q
pytest tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 -q

# Part A model verification script
python tests/verify_a.py
```

Swagger UI: http://localhost:8000/docs — ReDoc: http://localhost:8000/redoc

`pytest.ini` sets `pythonpath = .`, so tests import `app` as a top-level package without needing an install step.

## Architecture

Four modules under `app/`, each with a single responsibility:

- **`models.py`** — Pydantic schemas and enums (`TaskStatus`, `TaskPriority`, `TaskCreate`, `TaskUpdate`, `TaskResponse`). All models use `extra="forbid"`, so unknown request fields are rejected with 422. Field-level validation (title non-blank/≤200 chars, tag charset/length) lives here as `field_validator`s, factored into shared `_validate_title` / `_validate_tag` helpers used by both `TaskCreate` and `TaskUpdate`.
- **`business_rules.py`** — Cross-field/stateful validation that needs more than a single field to decide, raising `HTTPException` directly (422) rather than via Pydantic validators:
  - `validate_status_transition` — enforces the transition graph in `VALID_TRANSITIONS` (ToDo→InProgress→Done→InProgress; no same-state transition, no skipping states).
  - `validate_due_date_not_in_past` — due dates must be today or later.
- **`storage.py`** — The in-memory "database": a single `_tasks: dict[str, TaskResponse]` plus CRUD functions (`add_task`, `get_all_tasks`, `get_task_by_id`, `update_task`, `delete_task`). `overdue` is **never stored** — it's derived on every read via `_with_overdue()` / `_is_overdue()` by comparing `due_date` to `date.today()` (see `docs/mini-adr.md`, ADR-001). `update_task` applies partial updates via `payload.model_dump(exclude_unset=True)` so untouched fields are preserved. `_reset()` clears all state and is used by the test suite's autouse fixture — don't rely on task data persisting across test runs.
- **`main.py`** — FastAPI route handlers. Handlers call into `business_rules` for validation, then `storage` for persistence; they contain no business logic themselves. `/tasks` supports filtering by `status`, `priority`, `overdue`, and `tag` (combinable, all AND'd together). The `PATCH /tasks/{id}` handler has a subtlety worth preserving: due-date validation only fires when `due_date` is present in the request **and actually changed** — patching other fields on a task that already has a past due date must not be blocked.

### Request flow

```
route handler (main.py)
  → business_rules.validate_*()   (raises HTTPException on failure)
  → storage.add_task/update_task/...  (mutates _tasks, returns TaskResponse)
```

Pydantic field validators run first (during request parsing, before the handler body executes), then handler-level `business_rules` checks run against already-parsed/typed values.

### Tags

Tags are a flat `list[str]` on the task (no separate Tag entity — see ADR-002). Each tag must be non-empty, ≤255 chars, and alphanumeric only (no hyphens, underscores, or special characters). Filtering by tag (`?tag=`) matches tasks containing that exact tag.

## Testing conventions

- `tests/conftest.py` provides a `client` fixture (`TestClient(app)`) and an autouse fixture that resets `storage` before and after every test — tests don't need to manage cleanup themselves.
- Fixtures `created_task`, `created_task_with_due_date`, `created_task_with_tags` pre-create common task shapes via the API (not by writing to `storage` directly), so response JSON is the source of truth for comparisons.
- Tests are named descriptively as `test_<action>_<condition>_returns_<result>` — follow this pattern for new tests.
- When a test needs to seed data that the API itself would reject (e.g., a task with a past due date, to test overdue filtering), it calls `storage.add_task(...)` directly rather than going through `client.post`.

## Docs

`docs/mini-adr.md` records architecture decisions (and rejected alternatives) for each feature — check it before changing how due dates or tags are modeled. `docs/user-stories.md`, `docs/prompt-log.md`, and `docs/reflection.md` are course-deliverable artifacts from an AI-assisted-coding curriculum, not living technical docs.
