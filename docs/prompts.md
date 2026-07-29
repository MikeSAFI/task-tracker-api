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