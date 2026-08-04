# Task Tracker Architecture

## 1. What the app does

Task Tracker is a FastAPI REST API for creating, viewing, filtering, updating, and deleting tasks. It also serves a static browser frontend at `/` and exposes a `/health` liveness endpoint.

## 2. Data model

The primary entity is a **Task**. It has a UUID `id`; `title`; optional `description`, `assignee`, and `due_date`; `status` (`ToDo`, `InProgress`, `Done`); `priority` (`Low`, `Medium`, `High`); a list of `tags`; UTC `created_at` and `updated_at` timestamps; and an `overdue` flag. `overdue` is derived at read time from whether `due_date` is earlier than today, rather than being persisted.

## 3. Request flow

When a user creates a task with `POST /tasks`, FastAPI parses the request into `TaskCreate`. Model validation rejects unknown fields and validates the title and tags. The route then checks that a supplied due date is not in the past, delegates creation to storage, and returns the created task with its generated ID, timestamps, and calculated overdue state.

## 4. Key files

- `app/main.py` — API application, CORS configuration, frontend serving, and task routes.
- `app/models.py` — task request/response schemas, enums, and field validation.
- `app/storage.py` — in-memory task persistence, filtering, and CRUD operations.
- `app/business_rules.py` — referenced for due-date and status-transition checks; implementation is not visible from the files I read.
- `frontend/index.html` — served by the root route; its UI behavior is not visible from the files I read.

## 5. Conventions

- **Validation:** Pydantic models forbid extra request fields. Titles are trimmed, required, and limited to 200 characters. Tags must be nonblank, alphanumeric, and at most 255 characters.
- **Storage:** Tasks are held in a module-level dictionary keyed by generated UUIDs. Partial updates apply only explicitly supplied fields; an empty update does not change `updated_at`.
- **Errors:** Missing tasks return HTTP 404. Invalid due dates and invalid status transitions are documented as HTTP 422; detailed transition behavior is not visible from the files I read.
- **Frontend/backend interaction:** The API serves `frontend/index.html` at `/`; the actual browser requests and UI behavior are not visible from the files I read. CORS permits several local development origins.

## 6. Not visible or assumptions

Authentication, authorization, database persistence, deployment configuration, tests, API documentation behavior, frontend implementation, and the exact business-rule logic are not visible from the files I read.
