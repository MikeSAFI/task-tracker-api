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
user stories here
>>>

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
   - Explain why it best fits this learning project.
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

########################################################################################################
You are a senior Python backend engineer.

Context:
- This project already has a working FastAPI Task Tracker application.
- The application uses in-memory storage only.
- The existing models.py already contains:
  - TaskStatus
  - TaskPriority
  - TaskCreate
  - TaskUpdate
  - TaskResponse
- Do NOT recreate or redesign the existing models.
- Only update them to support the Due Dates & Overdue Filter feature.

Relevant User Stories:

US-DD-01
As a team member, I want to set an optional due date when creating a task so that I can track when work needs to be completed.

Acceptance Criteria:
- A valid due date can be provided when creating a task.
- Creating a task without a due date still succeeds.
- Invalid dates are rejected with validation.

US-DD-02
As a team member, I want to view and update a task's due date.

Acceptance Criteria:
- Due date is returned with the task.
- Due date can be updated.
- Due date can be removed.

US-DD-03
As a team member, I want the application to identify overdue tasks.

Acceptance Criteria:
- A task is overdue when its due date is earlier than the current date.
- Tasks without a due date are never overdue.
- Tasks due today are not overdue.

============================================================
FILE - app/models.py
============================================================

Update the existing models.py only.

Requirements:

1. Import any additional standard library modules required for handling dates.

2. Update TaskCreate
- Add:
  due_date: Optional[date] = None
- The field must be optional.
- No custom validator is required for due_date.
- Keep all existing fields and validators unchanged.

3. Update TaskUpdate
- Add:
  due_date: Optional[date] = None
- Keep all existing behavior unchanged.
- The field must remain optional.

4. Update TaskResponse
- Add:
  due_date: Optional[date] = None
- Add:
  overdue: bool
- The overdue field represents the calculated overdue status returned by the API.
- Do not calculate overdue inside the Pydantic model.
- Do not use computed fields or model validators for overdue.

5. Do NOT modify:
- TaskStatus
- TaskPriority
- Existing title validation
- Existing ConfigDict configuration
- Existing field names
- Existing defaults
- Existing model behavior unless required for due_date support.

HARD CONSTRAINTS

- Use Pydantic v2 syntax only.
- Do not use @validator.
- Do not use class Config.
- Do not use computed_field.
- Do not add business logic.
- Do not calculate overdue inside the model.
- Do not modify storage.py.
- Do not modify API routes.
- Do not introduce database code.
- Do not change existing validation except for adding the new field.
- Keep the file style consistent with the existing code.

Output only one code block preceded by:

# FILE: app/models.py

#################################################################

You are a senior Python backend engineer.

Context:
- This project already has a working FastAPI Task Tracker application.
- The application uses in-memory storage only.
- app/models.py has already been updated with:
  - due_date: Optional[date] on TaskCreate, TaskUpdate, and TaskResponse
  - overdue: bool on TaskResponse
- app/storage.py already contains the following functions:
  - add_task(payload: TaskCreate) -> TaskResponse
  - get_all_tasks(status=None, priority=None) -> list[TaskResponse]
  - get_task_by_id(task_id: str) -> Optional[TaskResponse]
  - update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]
  - delete_task(task_id: str) -> bool
  - _reset() -> None
- Do NOT redesign the storage layer.
- Update the existing implementation only.

Relevant User Stories

US-DD-01
As a team member, I want to set an optional due date when creating a task.

Acceptance Criteria
- A valid due date can be provided.
- A task without a due date still works.
- Invalid dates are rejected by Pydantic before reaching storage.

US-DD-02
As a team member, I want to update or remove a task's due date.

Acceptance Criteria
- Due date can be changed.
- Due date can be removed.
- Existing fields continue to behave the same.

US-DD-03
As a team member, I want the application to identify overdue tasks.

Acceptance Criteria
- A task is overdue when its due date is earlier than today's date.
- Tasks without a due date are never overdue.
- Tasks due today are not overdue.

US-DD-04
As a team member, I want to filter tasks by overdue status.

Acceptance Criteria
- Return only overdue tasks when requested.
- Return only non-overdue tasks when requested.
- Existing status and priority filtering must continue to work.

============================================================
FILE
============================================================

Update ONLY:

# app/storage.py

Do NOT modify any other file.

============================================================
REQUIREMENTS
============================================================

1. Preserve all existing function names.

2. Preserve all existing function signatures unless required below.

3. Continue using the existing module-level dictionary.

4. Continue creating TaskResponse objects.

5. Add support for the optional due_date field when creating tasks.

6. Ensure update_task() correctly:
- updates due_date,
- removes due_date when None is supplied,
- continues updating updated_at,
- keeps existing update behavior unchanged.

7. Implement overdue calculation in the storage layer.

Create a small private helper function, for example:

_is_overdue(task: TaskResponse) -> bool

The helper should:

- return False when due_date is None
- return True when due_date is earlier than today's date
- return False when due_date is today or later

8. Whenever TaskResponse objects are returned from storage functions:

- populate the overdue field using the helper
- do NOT permanently store overdue
- calculate it every time a task is returned

This applies to:
- add_task()
- get_all_tasks()
- get_task_by_id()
- update_task()

9. Extend get_all_tasks() to support an OPTIONAL parameter:

overdue: Optional[bool] = None

Filtering rules:

- overdue=None
  preserve existing behavior

- overdue=True
  return only overdue tasks

- overdue=False
  return only tasks that are not overdue

Filtering must continue to support the existing:
- status filter
- priority filter

All filters must work together.

10. delete_task() and _reset() should remain unchanged.

============================================================
HARD CONSTRAINTS
============================================================

- Do NOT modify app/models.py.
- Do NOT modify app/main.py.
- Do NOT change TaskResponse fields.
- Do NOT store overdue in the _tasks dictionary.
- Do NOT introduce new classes.
- Do NOT introduce services.
- Do NOT introduce repositories.
- Do NOT introduce SQLAlchemy.
- Do NOT introduce databases.
- Do NOT introduce caching.
- Do NOT introduce logging.
- Do NOT add reminder functionality.
- Do NOT change the existing architecture.
- Keep the implementation simple and readable.
- Follow existing coding style.

============================================================
OUTPUT
============================================================

Output only one code block preceded by:

# FILE: app/storage.py

##################################################################
You are a senior Python backend code reviewer.

Review the generated implementation of:

- app/models.py
- app/storage.py

against the Due Dates & Overdue Filter requirements.

IMPORTANT:
- Do NOT modify any files.
- Do NOT generate code.
- Only review and report findings.
- Mark each checkpoint as PASS or FAIL.
- If FAIL, explain the issue briefly.

============================================================
REVIEW CHECKLIST
============================================================

1. Models Support Due Dates
- TaskCreate, TaskUpdate, and TaskResponse contain optional due_date.
- TaskResponse contains overdue: bool.
- Existing task fields and validation remain unchanged.
- No overdue calculation exists inside models.py.

2. Due Date Creation & Updates
- Tasks can be created with or without a due date.
- Due dates can be updated.
- Due dates can be removed.
- Updating due dates does not affect other task fields.

3. Overdue Calculation
- Overdue is calculated dynamically and is not stored.
- No due date => overdue is false.
- Due date before today => overdue is true.
- Due date today or later => overdue is false.

4. Storage Filtering
- get_all_tasks supports an optional overdue filter.
- overdue=True returns only overdue tasks.
- overdue=False returns only non-overdue tasks.
- Existing status and priority filters still work with overdue filtering.

5. Scope & Architecture
- Only models.py and storage.py were changed.
- No database, ORM, services, repositories, or unnecessary layers were introduced.
- Existing task behavior remains unchanged.
- Implementation follows the mini-ADR decision.

============================================================
OUTPUT FORMAT
============================================================

# Due Dates Feature Review

| Checkpoint | Result | Notes |
|---|---|---|
| 1. Models Support Due Dates | PASS/FAIL | |
| 2. Due Date Creation & Updates | PASS/FAIL | |
| 3. Overdue Calculation | PASS/FAIL | |
| 4. Storage Filtering | PASS/FAIL | |
| 5. Scope & Architecture | PASS/FAIL | |

Final Verdict:
- APPROVED if all checkpoints pass.
- NEEDS FIXES if any checkpoint fails.

##############################################################

You are a senior Python backend engineer.

Context:
- This project already has a working FastAPI Task Tracker REST API.
- The application uses in-memory storage only.
- app/models.py and app/storage.py have already been updated to support the Due Dates & Overdue Filter feature.
- Your task is ONLY to update the API endpoints in app/main.py to expose this feature.

Existing architecture:
- main.py contains FastAPI routes.
- Routes call storage functions.
- Business logic belongs in storage.py, not in main.py.

Relevant User Stories:

US-DD-01
As a team member, I want to set an optional due date when creating a task so that I can track when work needs to be completed.

Acceptance Criteria:
- A valid due date can be provided when creating a task.
- Creating a task without a due date still succeeds.
- Invalid dates are rejected.

US-DD-02
As a team member, I want to view and update a task's due date so that I can keep deadlines accurate.

Acceptance Criteria:
- Due date is returned when retrieving tasks.
- Due date can be updated.
- Due date can be removed.

US-DD-03
As a team member, I want the application to identify overdue tasks.

Acceptance Criteria:
- A task is overdue when due_date is earlier than today's date.
- Tasks without due dates are not overdue.
- Tasks due today are not overdue.

US-DD-04
As a team member, I want to filter tasks by overdue status.

Acceptance Criteria:
- Users can request overdue tasks only.
- Existing status and priority filters continue working.

============================================================
FILE
============================================================

Update ONLY:

# app/main.py

Do NOT modify:
- app/models.py
- app/storage.py
- tests
- any other file

============================================================
REQUIREMENTS
============================================================

1. Preserve all existing endpoints.

Do NOT:
- rename routes
- change HTTP methods
- remove existing functionality
- change existing response behavior unless required for due dates

---

2. Create Task Endpoint

Update the existing POST task endpoint.

Requirements:
- Continue using TaskCreate as the request model.
- Accept the optional due_date automatically.
- Pass the payload unchanged to storage.
- Return the existing TaskResponse.

Do NOT add validation logic here.

---

3. Get Tasks Endpoint

Update the existing GET tasks endpoint.

Add a new optional query parameter:

overdue: Optional[bool] = None

Behavior:

- overdue is not provided:
  - Keep existing behavior.

- overdue=true:
  - Return only overdue tasks.

- overdue=false:
  - Return only non-overdue tasks.

Existing filters must continue working:

- status
- priority

Example combinations that must work:
- status + overdue
- priority + overdue
- status + priority + overdue

The endpoint should only pass filtering parameters to storage.

Do NOT calculate overdue inside main.py.

---

4. Get Task By ID Endpoint

Update only if needed.

Requirements:
- Return due_date.
- Return overdue value from storage.
- Keep existing behavior unchanged.

---

5. Update Task Endpoint

Update the existing PATCH/PUT endpoint.

Requirements:
- Continue using TaskUpdate.
- Accept due_date updates.
- Allow removing due_date.
- Pass update payload to storage.
- Return updated TaskResponse.

Do NOT implement update logic inside main.py.

---

6. Delete Task Endpoint

Do not change behavior.

---

============================================================
HARD CONSTRAINTS
============================================================

- Do NOT modify models.py.
- Do NOT modify storage.py.
- Do NOT add new endpoints.
- Do NOT add authentication.
- Do NOT add users.
- Do NOT add permissions.
- Do NOT add reminders.
- Do NOT add notifications.
- Do NOT add background jobs.
- Do NOT add databases.
- Do NOT add ORM code.
- Do NOT add services or repositories.
- Do NOT refactor unrelated code.
- Do NOT move business logic into endpoints.
- Keep the implementation small and consistent with the existing project.

============================================================
OUTPUT
============================================================

Output only one code block preceded by:

# FILE: app/main.py

##############################################################

You are a senior Python developer reviewing and extending existing pytest tests for a FastAPI Task Tracker app.

Context files:
@app/main.py
@app/models.py
@app/storage.py
@app/business_rules.py
@tests/conftest.py
@tests/test_tasks.py

The existing test suite already covers the current Task Tracker functionality.

Your task:
Update the existing tests to add coverage for the new feature:

Due Dates & Overdue Filter

IMPORTANT:
- Do NOT rewrite the existing tests.
- Do NOT remove existing tests.
- Do NOT rename existing tests.
- Keep all current test behavior unchanged.
- Add only the required tests for this new feature.
- Follow the existing test style and structure.

============================================================
FEATURE REQUIREMENTS TO TEST
============================================================

Due Dates:

- Tasks can optionally have a due_date.
- Tasks can be created with or without due_date.
- Due dates can be updated.
- Due dates can be removed.
- Invalid due dates are rejected.

Overdue:

- A task is overdue when:
  due_date < today

- A task is NOT overdue when:
  - no due_date exists
  - due_date is today
  - due_date is in the future

Filtering:

- GET /tasks supports:
  overdue=true
  overdue=false

- Existing filters must continue working:
  - status
  - priority

============================================================
UPDATE FILES
============================================================

Update only:

# tests/conftest.py
# tests/test_tasks.py

============================================================
FILE 1 - tests/conftest.py
============================================================

Review the existing fixtures.

Add only if needed:

Fixture:
created_task_with_due_date

Behavior:
- Creates a task using POST /tasks
- Payload:

{
    "title": "task with due date",
    "due_date": "2099-01-01"
}

- Assert status_code == 201
- Return response JSON

Do not modify existing fixtures unless required.

============================================================
FILE 2 - tests/test_tasks.py
============================================================

Add the following tests.

Use the existing naming and style.

Add:

POST /tasks:

1. test_create_task_with_valid_due_date_returns_201

Verify:
- Task creation succeeds.
- Response contains due_date.
- overdue is false for future date.

2. test_create_task_without_due_date_returns_201

Verify:
- Task creation succeeds.
- due_date is null.
- overdue is false.

3. test_create_task_invalid_due_date_returns_422

Verify:
- Invalid date format returns 422.

------------------------------------------------------------

GET /tasks:

4. test_get_task_returns_due_date_and_overdue_fields

Verify:
- Response includes:
  - due_date
  - overdue

------------------------------------------------------------

PATCH /tasks/{id}:

5. test_patch_task_updates_due_date_returns_200

Verify:
- Existing task due_date can be updated.

6. test_patch_task_removes_due_date_returns_200

Verify:
- Existing due_date can be removed.

------------------------------------------------------------

Overdue calculation:

7. test_task_with_past_due_date_is_overdue

Verify:
- Yesterday's due date returns overdue=true.

8. test_task_with_due_date_today_is_not_overdue

Verify:
- Today's due date returns overdue=false.

9. test_task_without_due_date_is_not_overdue

Verify:
- Missing due_date returns overdue=false.

------------------------------------------------------------

Overdue filtering:

10. test_filter_tasks_by_overdue_true_returns_only_overdue_tasks

Create:
- one overdue task
- one future task
- one task without due_date

Call:
GET /tasks?overdue=true

Verify:
- Only overdue task returned.

11. test_filter_tasks_by_overdue_false_returns_only_non_overdue_tasks

Create:
- one overdue task
- one future task
- one task without due_date

Call:
GET /tasks?overdue=false

Verify:
- Overdue task excluded.

------------------------------------------------------------

Combined filters:

12. test_filter_tasks_by_priority_and_overdue_returns_matching_tasks

Create:
- HIGH priority overdue task
- LOW priority overdue task
- HIGH priority future task

Call:

GET /tasks?priority=High&overdue=true

Verify:
- Only HIGH priority overdue task returned.

============================================================
HARD CONSTRAINTS
============================================================

- Use pytest only.
- Use TestClient only.
- Do not use AsyncClient.
- Do not mock storage.
- Keep using the existing reset fixture.
- Do not modify application code.
- Do not add unrelated tests.
- Do not duplicate existing CRUD tests unnecessarily.
- Keep tests focused only on Due Dates & Overdue Filter.

Output only the modified files:

# FILE: tests/conftest.py

# FILE: tests/test_tasks.py