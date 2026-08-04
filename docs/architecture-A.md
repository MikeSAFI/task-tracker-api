# Task Tracker Architecture

## What the app does

Task Tracker is a learning-focused REST API with a static browser-based task board. Users can create, view, filter, update, move, and delete tasks; the API serves the frontend at `/` and exposes task endpoints under `/tasks`.

## Data model

The main entity is **Task**: `id` (UUID string), `title`, `description`, `status` (`ToDo`, `InProgress`, `Done`), `priority` (`Low`, `Medium`, `High`), optional `assignee`, optional `due_date`, `tags` (a flat list of strings), `created_at`, and `updated_at`. `overdue` is a derived response field: it is true only when `due_date` is earlier than today and is not stored.

## Request flow: create a task

The browser submits JSON to `POST /tasks`. FastAPI parses it into `TaskCreate`, where field validation rejects unknown fields, blank or oversized titles, and invalid tags. The route then rejects past due dates. Storage generates a UUID and UTC timestamps, applies defaults, stores the `TaskResponse` in an in-memory dictionary, calculates `overdue`, and returns `201 Created` with the task.

## Key files

- `app/main.py` - FastAPI application, CORS setup, frontend route, and task HTTP endpoints.
- `app/models.py` - Pydantic request/response models and status/priority enums.
- `app/business_rules.py` - Due-date and status-transition rules.
- `app/storage.py` - In-memory task dictionary and CRUD operations.
- `frontend/index.html` - Static task-board UI and browser requests to the API.
- `tests/test_tasks.py` - API behavior and validation coverage.
- `tests/conftest.py` - Test client and automatic storage reset.
- `docs/mini-adr.md` - Recorded decisions for due dates, overdue behavior, and tags.
- `README.md` - Setup, usage, project structure, and limitations.

## Conventions

Validation is split between Pydantic field validation and route-invoked business rules. All models forbid unexpected request fields. Invalid input and invalid status transitions return HTTP 422; missing tasks return 404. Storage is process-local and resets when the server restarts. Partial updates preserve omitted fields; allowed status changes are `ToDo -> InProgress -> Done -> InProgress`. The frontend uses `fetch` against the same API, reloads task data after successful form submissions, and displays server errors to users.

## Not visible or assumptions

No database, authentication, authorization, deployment environment, or multi-user/concurrency strategy is implemented in the inspected application code. This document assumes the static frontend is the intended primary client; other API clients can use the documented REST endpoints.
