# Task Tracker Architecture

## What the app does

Task Tracker is a learning-focused REST API for creating, viewing, updating, deleting, and filtering tasks. It uses FastAPI and Pydantic v2, serves a static HTML/JavaScript frontend at `/`, and stores task data in memory rather than in a database.

## Data model

The central entity is a task. Important fields include:

- `id`: unique task identifier.
- `title`: required, non-blank, maximum 200 characters.
- `status`: task state, using `ToDo`, `InProgress`, or `Done`.
- `priority`: task priority, defined by the `TaskPriority` enum.
- `due_date`: optional date; new or changed dates must be today or later.
- `tags`: flat list of alphanumeric tag strings, each non-empty and at most 255 characters.
- `overdue`: derived when a task is read by comparing `due_date` with today; it is never stored.

Schemas include `TaskCreate`, `TaskUpdate`, and `TaskResponse`. Unknown request fields are rejected.

## Request flow

When a user creates a task, FastAPI parses the request into `TaskCreate`. Pydantic first validates individual fields such as the title and tags. The route handler then calls applicable business-rule validation, including validating that the due date is not in the past. If validation succeeds, storage adds the task to the in-memory dictionary and returns a `TaskResponse`.

## Key files

- `app/main.py` — FastAPI routes; coordinates validation and storage without containing business logic.
- `app/models.py` — Pydantic schemas, enums, and shared field validators.
- `app/business_rules.py` — Stateful validation for status transitions and due dates.
- `app/storage.py` — In-memory task CRUD and derived overdue-state calculation.
- `frontend/index.html` — Static HTML/JavaScript frontend served by the API.
- `tests/conftest.py` — Test client and automatic storage reset fixtures.
- `tests/test_tasks.py` — Task API tests, including validation and update behavior.
- `docs/mini-adr.md` — Records decisions on overdue handling and tag modeling.
- `docs/user-stories.md` — Course-deliverable user-story artifact.
- `pytest.ini` — Configures the project import path for tests.

## Conventions

Field-level validation belongs in Pydantic models; cross-field or stateful checks belong in `business_rules.py` and raise HTTP 422 errors. Route handlers call validation before persistence and should not embed business logic. Storage uses a module-level dictionary and applies partial updates with only explicitly supplied fields. Filtering supports `status`, `priority`, `overdue`, and `tag`, combined with AND logic. The frontend is static and is served directly by the backend.

## Not visible or assumptions

The available context does not confirm the precise set of priority values, the task ID generation mechanism, or the frontend’s exact API interactions and interface behavior. It also does not describe authentication, authorization, deployment, persistence beyond process memory, or production configuration.
