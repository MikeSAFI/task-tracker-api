You are a product owner writing user stories for a small development team.

Context:
I am extending an existing Task Tracker web application with a Python/FastAPI backend and a simple web frontend.

Existing features:
- Create tasks with title, description, status (ToDo, InProgress, Done), priority (Low, Medium, High), and assignee.
- View all tasks in a list.
- Filter tasks by status and priority.
- Update task details, including status.
- Delete tasks.

New features to add:

1. Due Dates + Overdue Filter
Expected functionality:
- Tasks can optionally have a due date.
- Users can set a due date when creating or editing a task.
- Users can see the due date on task cards.
- The application should identify overdue tasks.
- Users should have a way to filter or identify overdue tasks.

2. Tags / Labels
Expected functionality:
- Tasks can have multiple tags/labels.
- Users can add tags when creating or editing a task.
- Tags should be displayed on task cards.
- Users can filter or search tasks by tag.

Important constraints:
- Do not add features outside the scope of these two enhancements.
- Do not introduce authentication, user accounts, notifications, reminders, mobile applications, real-time updates, or advanced project management features.
- Keep compatibility with the existing Task Tracker scope.
- Do not assume storage changes, APIs, or UI components unless required by the feature.
- If a design decision is needed (for example, where overdue calculation should happen), mention it as an assumption or decision point.

Target user:
A solo developer or small team managing work in a single shared task list.

Task:
Generate user stories for the two new features:
- Due Dates + Overdue Filter
- Tags / Labels

Generate 3-4 user stories per feature.

User story format:
As a [role], I want [feature] so that [benefit].

Constraints:
- Use "team member" as the main role unless another role is clearly needed.
- Each user story must include 2-3 acceptance criteria that are specific, clear, and testable.
- Include both successful scenarios and failure/validation cases.
- Cover backend behavior, frontend behavior, and user interactions where applicable.
- Do not write technical implementation details or code.
- Do not invent functionality that is not required.

Acceptance criteria should cover examples such as:
- Valid due date creation.
- Invalid date handling.
- Updating due dates.
- Detecting overdue tasks.
- Filtering overdue tasks.
- Adding tags.
- Rejecting empty or invalid tags.
- Updating tags.
- Filtering tasks by tag.
- Keeping existing behavior unchanged for tasks without due dates or tags.

Output format:
Return a table with columns:

| ID | Feature | Story | Acceptance Criteria | Notes / Assumptions |

Include any important product decisions or assumptions in the Notes / Assumptions column.

#######################################################################################################

You are a senior backend developer helping me write Architecture Decision Records (ADRs) for a learning project.

Context:
I am extending an existing Task Tracker application with a Python/FastAPI backend and a simple web frontend.

Reviewed requirements:
<<<
the user stories >>>

Constraints:
- This is a learning project, not production software.
- The backend uses Python, FastAPI, and Pydantic for validation.
- The frontend is a simple web application.
- Keep the architecture simple, easy to understand, and easy to maintain.
- No authentication or user accounts.
- No microservices, Docker, cloud deployment, caching, messaging systems, or production infrastructure.
- Do not introduce functionality that is not required by the supplied user stories.
- Base every architectural decision only on the requirements provided.

Task:

Based on the supplied user stories, create **two separate Architecture Decision Records (ADRs)**—one for each feature:

1. ADR: Due Dates & Overdue Filter
2. ADR: Tags / Labels

For each ADR include:

1. Title
2. Status (Proposed)
3. Context
   - Summarize the relevant user stories.
   - Explain the problem the feature introduces.

4. Decision
   - Describe the chosen approach.
   - Explain why it best fits this project.
   - Clearly state any assumptions.

5. Alternatives Considered
   - Describe at least two reasonable alternatives.
   - Explain why they were not selected.

6. Consequences
   - Benefits
   - Drawbacks
   - Future considerations

7. Impact
   - Backend changes
   - Frontend changes
   - API changes
   - Data model changes
   - Validation requirements
   - Testing impact

Constraints:
- Keep the ADRs concise but complete.
- Follow standard ADR structure.
- Do not include implementation code.
- Do not invent requirements beyond the supplied user stories.
- If a design choice is not specified in the stories (for example, how overdue is calculated or how tags are stored), explicitly document it as an architectural decision and explain the reasoning.

Output format:

Return two clearly separated sections:

# ADR-001: Due Dates & Overdue Filter

...

# ADR-002: Tags / Labels

...

#########################################################
I completed a Module 5 security review. Below are the AI findings and my own manual scan findings.
Task:
1. Group the findings into Agreement, AI-only, and You-only.
2. Write a two-line observation about the shape of AI coverage.
3. Create a top-3 security backlog from the Valid findings.
Definitions:
- Agreement: both AI and I noticed the issue or a closely related issue.
- AI-only: AI noticed it and I did not notice it during my manual scan.
- You-only: I noticed it and AI missed it. This is the most important learning column.
Constraints:
- Do not invent new findings.
- If a finding lacks file evidence, mark it "needs evidence" instead of treating it as confirmed.
- Suggested owners should be realistic, such as backend, frontend, DevOps, or course/project owner.
Output format:
1. Reconciliation table with columns: Agreement, AI-only, You-only
2. Two-line observation
3. Top-3 backlog table with columns: Rank, Finding, Why it matters, Suggested owner, Next action
AI findings:
# Module 5 Security Finding Grades

| Finding ID | Severity | File / location | grade | Reason | Evidence needed or evidence used | Student decision to confirm | Smallest next action |
|---|---|---|---|---|---|---|---|
| SEC-01 | High | `frontend/index.html:991` | Valid | The frontend inserts API-supplied task fields into `innerHTML` without HTML escaping. A task title, description, or assignee containing an event-handler payload could execute when the board renders. The title's 200-character limit reduces size, not XSS impact. | Used `frontend/index.html:991`-`1005` and `app/models.py:52`-`55`. | Confirm this is in scope as a real stored-XSS issue; High is reasonable if untrusted users can submit tasks. | Backlog: escape task fields before rendering with `innerHTML`; this needs a small frontend refactor, not a safe one-line change. |
| SEC-02 | Medium | `app/models.py:52` | Valid | The stated fields and tag list truly lack aggregate bounds, and storage is in-memory with unpaginated listing. This is a plausible resource-exhaustion risk outside coursework, though exploitation scale was not measured. | Used `app/models.py:52`-`57`, `app/models.py:101`-`107`, and `app/storage.py:74`-`83`. | Confirm whether to retain Medium or describe it as a production-hardening limitation, given the local learning scope. | Backlog: define maximum lengths/counts and pagination before shared deployment. |
| SEC-03 | Medium | `app/main.py:62` | Valid | This is intentionally absent, not a coding mistake. It is nevertheless a material production limitation because any caller can read, create, update, and delete tasks. | Used `README.md:8`-`9`, `README.md:240`, `docs/prompts.md:93`, and public route definitions in `app/main.py`. | Record as an accepted course-scope limitation / deployment blocker, rather than penalizing it as an accidental defect. | Documentation note: state that the app is for local learning use only and must not be deployed with real task data. |
| SEC-04 | Low | `app/main.py:18` | Valid | `"null"` is explicitly allowed by CORS, so opaque-origin pages can read permitted API responses. It is documented as local-file support; with no auth and a local-only app, impact is limited, but it should not carry into deployment. | Used `app/main.py:18`-`30` and `README.md:243`-`245`. | Keep as a Low development-configuration concern, or classify as accepted scope if Module 5 excludes production configuration review. | Optional one-line fix: remove `"null",` from `allow_origins` and use the API-served frontend. |
| SEC-05 | Low | `Dockerfile:7` | Noise | The facts are correct, but no vulnerable dependency, compromised action, or deployable production environment was identified. "No scans/hashes/digest pins" is generic supply-chain hardening, not a demonstrated repo vulnerability. | Used `Dockerfile:7`, `Dockerfile:19`, and `.github/workflows/ci.yml:20`-`26`; the finding itself states no specific vulnerable package was established. | Consider omitting it, or retain it only as a non-security future production-hardening note. | Not applicable. |

My manual scan findings:

| Suggested ID | Severity | Location | Finding | Evidence |
|---|---|---|---|---|
| SEC-06 | Medium | `app/main.py` `create_task`; `app/business_rules.py`; `frontend/index.html` ~833–836, 1357–1358 | **Status-transition rules are bypassable on create.** `validate_status_transition` runs only on PATCH. `POST /tasks` accepts any `TaskStatus`, including `Done`. The UI status dropdown includes `Done` on create and sends it. | Live: `POST {"title":"x","status":"Done"}` → **201** with `status: "Done"`. Create path never calls `validate_status_transition` (confirmed in `claim-vs-reality.md` too). |
| SEC-07 | Low–Medium | `frontend/index.html:1080`, `1197`; `app/main.py` 404 `detail` | **Second unescaped `innerHTML` sink + reflected path id in errors.** Failed drag/PATCH sets `boardMessage = getErrorMessage(payload)` and injects it into `innerHTML`. API 404s embed raw `task_id` in `detail`. | Live: `GET /tasks/<img src=x onerror=alert(1)>` → `detail: "Task with id <img src=x onerror=alert(1)> not found"`. Normal UI uses UUIDs, so this is weaker than SEC-01, but the sink/reflection are real and not listed. |
| SEC-08 | Low | `app/main.py` `serve_frontend` / FastAPI defaults | **No browser security headers** on the served UI (`Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, etc.). | Live `GET /` response headers: only `content-type: text/html; charset=utf-8`. No CSP/frame options middleware in `app/`. CSP would also harden SEC-01. |
| SEC-09 | Low | FastAPI defaults (`/docs`, `/redoc`, `/openapi.json`) | **Interactive docs and OpenAPI schema are publicly reachable** with no auth (amplifies SEC-03). | Live: `GET /docs` → **200**, `GET /openapi.json` → **200**. |
| SEC-10 | Low | `Dockerfile:42` | **Container binds `0.0.0.0:8000`**, so on a shared/LAN host the unauthenticated API is reachable beyond localhost. | `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]` |
########################################################################

I want to consider one optional one-line fix from docs/security-review.md.
Finding:
| Suggested ID | Severity | Location | Finding | Evidence |
|---|---|---|---|---|
| SEC-06 | Medium | `app/main.py` `create_task`; `app/business_rules.py`; `frontend/index.html` ~833–836, 1357–1358 | **Status-transition rules are bypassable on create.** `validate_status_transition` runs only on PATCH. `POST /tasks` accepts any `TaskStatus`, including `Done`. The UI status dropdown includes `Done` on create and sends it. | Live: `POST {"title":"x","status":"Done"}` → **201** with `status: "Done"`. Create path never calls `validate_status_transition` (confirmed in `claim-vs-reality.md` too). |
AI-Assisted Coding - Module 5 Prompt Library
Task:
Propose the minimal diff that addresses only this finding. Do not apply the diff yet.
Constraints:
- One finding only.
- No refactoring.
- No unrelated validation changes.
- No new dependencies.
- Do not edit tests unless I explicitly ask.
- Explain why this is small enough for Module 5; if it is not small enough, say it belongs in the backlog.
Output format:
1. Decision: one-line fix or backlog
2. Minimal unified diff
3. Why this change is limited
4. Verification step I should run or document
##############################################################
Walk me through the following AI-generated code block line by line.
For each line or small group of lines, explain:
1. What it does.
2. Why it is written this way.
3. What would break if it were removed or changed.
4. Any assumption, risk, or library behavior I should verify.
Constraints:
- Use beginner-friendly but precise language.
- If the explanation would require seeing surrounding files, ask for them.
- If you are unsure, say so. Do not use vague phrases such as "this is standard" without explaining why.
- Do not rewrite the code unless I ask.
Output format:
Return a table with columns:
Line(s) | What it does | Why it is there | What could break | Do I own this yet?
Code block:
```
def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Ensure a status change follows the allowed transition graph.

    Valid transitions are ToDo->InProgress, InProgress->Done, and
    Done->InProgress. Same-state transitions and any transition not listed
    in ``VALID_TRANSITIONS`` (e.g. skipping a state) are rejected.

    Args:
        current: The task's current status.
        new: The requested new status.

    Raises:
        HTTPException: 422 if ``(current, new)`` is not in
            ``VALID_TRANSITIONS``.
    """
    # Same -> same is invalid. Anything not in VALID_TRANSITIONS is invalid.
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )


```
#################################################################

This is Strategy B: structured context.
Context:
Here is AGENTS.md:
<<
# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

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
>>
Here is a one-line summary of each important app file:
<<
main.py — FastAPI routes: validate via business_rules, persist via storage, no business logic in handlers.
models.py — Pydantic schemas/enums (TaskCreate/Update/Response, status, priority) with extra="forbid" and shared title/tag validators.
business_rules.py — Stateful checks that raise 422: status transitions and due dates not in the past.
storage.py — In-memory dict CRUD; overdue is derived on read, never stored.
>>
Task:
Using the structured context above, produce a one-page architecture doc for the Task Tracker app.
Required sections:
1. What the app does - one short paragraph.
2. Data model - entities and important fields.
3. Request flow - what happens when a user creates a task.
4. Key files - 5-10 important files, one line each.
5. Conventions - validation, storage, error handling, frontend/backend interaction.
6. Not visible or assumptions - anything you could not confirm.
Constraints:
- One page maximum.
- Output markdown.
- Do not produce code.
- Do not edit app/.
- If you save a file, save only to docs/architecture-B.md after showing me the draft.
AI-Assisted Coding - Module 5 Prompt Library
- Do not add details that are not supported by AGENTS.md, the file summaries, or files you explicitly inspect.
Output format:
Return:
1. Draft architecture-B.md
2. Which context item helped most
3. Any remaining assumptions or unsupported details
############################################################
I ran the same architecture-document task with three context strategies.
Strategy A: minimal context
Strategy B: structured context using AGENTS.md and file summaries
Strategy C: targeted context using a small set of anchor files
Task:
Compare the three outputs and help me write the comparison log for docs/architecture.md.
For each strategy, identify:
- What it got right.
- What it got wrong, missed, or invented.
- Which task shape it is best suited for.
Then help me write:
1. A verdict: which strategy I chose for the final architecture doc and why.
2. A two-sentence context-engineering rule in the form: "For task shape X, I use strategy Y because Z."
Constraints:
- Use only the three drafts I paste below.
- Do not invent repo facts.
- Do not rewrite the entire architecture document unless I ask.
- Make the comparison specific; avoid generic statements such as "context matters."
Output format:
1. Strategy comparison table
2. Verdict paragraph
3. Two-sentence context-engineering rule
Architecture A:
<<
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
>>
Architecture B:
<<
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

>>
Architecture C:
<<
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

>>
#############################################################

I wrote the playbook below myself. Review it for evidence and student voice, but do not rewrite it for me.
Task:
Check whether my playbook meets the Module 5 quality bar:
- It is one page or close to one page.
- It uses my own voice, not generic AI-policy language.
- Each rule is backed by a specific course incident or observation.
- It mentions practical review habits, not vague aspirations.
- The Decision Card is fully filled in.
- The never-paste rule names a concrete type of data.
- The 30-day re-read commitment is present.
Constraints:
- Do not produce a replacement playbook.
- Do not add evidence I did not provide.
- Suggest minimal edits only.
- If a rule lacks evidence, mark it "needs course evidence".
Output format:
Return a checklist table with columns:
AI-Assisted Coding - Module 5 Prompt Library
Requirement | Present / Missing | Evidence from my draft | Minimal edit
My playbook draft:
<<
# Personal AI Coding Playbook

## 1. When I reach for AI first

- Drafting user stories, Mini ADRs, and strong constrained prompts before I touch code (ChatGPT helped me get acceptance criteria and prompt structure ready for Cursor Agent).
- Project template that must stay consistent with the existing FastAPI style adding fields, wiring query params, fixtures, and named pytest cases once the ADR and stories are done.
- Planning a feature against this repo (repo grounded plans, structured architecture context with AGENTS.md) and grading security findings so I can decide keep backlog noise instead of guessing.

## 2. When I do not reach for AI

- Final product calls: what “valid” means: no past due dates, tags alphanumeric ≤255, rejecting ADR alternatives like storing an overdue flag or adding a separate Tag entity.
- Bugs that need me to own the path ex: PATCH still validating an unchanged past due date when the edit form resubmitted it, I tightened that myself after AI’s first approach.
- Making a fix when the product rule is unclear ex: SEC-06 create-status / ToDo only. I backlog it instead of accepting a one line change I do not stand behind.

## 3. My non-negotiables

- I never paste real customer data, production logs, credentials, or third party personal information into an AI prompt.
- Narrow prompts with hard file/scope limits, run pytest right after AI edits, treat output as a draft until stories, ADRs, and failing/passing tests agree.
- Before I accept a change, I review the diff against the current requirement and decide whether I understand the changed path and if not, follow up or backlog, not ship.

## 4. My review rules

- Check AI output against acceptance criteria and Mini ADRs, reject scope drift and out of scope extras.
- Prefer evidence: green suite, break test recovery, and live checks for security grades not “AI said so.”
- For plans and architecture, prefer structured / repo grounded context over vague chat, drop noise (ex: SEC-05) and accept course scope limits no auth explicitly.

## 5. What I am still figuring out

- Fully owning every frontend innerHTML path (SEC-01 / SEC-07). I can explain the board flow but XSS escaping is still on my security backlog.
- When create must force ToDo vs allowing any initial status confirmed behavior, but no safe one line fix until the product rule is decided.
- How much context to give for each job (Strategy B for architecture docs vs targeted anchor files for a single business rule wiring task). I have a rule, but I still calibrate it task by task.

## Decision Card

- For a new feature I reach for: ChatGPT for stories/ADRs/strong prompts, then Cursor Agent with constrained, file scoped implementation (and a repo-grounded plan when sequencing matters).
- For a code review I reach for: checklist / security review prompts, then my own grade (Valid / Noise / course scope) with file evidence before keep or backlog.
- For debugging I reach for: failing pytest and stack traces first, AI to propose a fix and me to verify the path and correct it when the first draft misses a real edge case like PATCH + unchanged due date.
- For infrastructure I reach for: AI assisted Dockerfile / CI YAML drafts, then I verify they match how I run tests locally and treat the image as local packaging, not production deploy.
- I will never paste real customer data, production logs, credentials, or third party personal info into an AI tool.
- My one rule is: AI output is a draft until the requirement, the ADR, and the tests agree and I understand the path I am shipping.

>>
