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

##########################################################################

You are a senior Python backend engineer.

Context:
- This project is a FastAPI Task Tracker application.
- The application uses:
  - app/models.py
  - app/storage.py
  - app/business_rules.py
  - app/main.py
- The Due Dates & Overdue Filter feature is already implemented.
- Tasks have:
  - due_date: Optional[date]
  - overdue: bool (calculated dynamically)

A new business rule must now be enforced.

============================================================
NEW BUSINESS RULE
============================================================

A task due date must be:

- today
OR
- a future date

Invalid:

- any due date earlier than today's date

This validation applies to:

- task creation
- task updates

If validation fails:

- the task must NOT be saved
- the update must NOT be applied
- the API must return the same validation style already used by the application for business rule violations

============================================================
TASK
============================================================

Update ONLY:

# app/business_rules.py
# app/main.py

Do NOT modify:

- app/models.py
- app/storage.py
- tests
- any other files

============================================================
FILE 1 - app/business_rules.py
============================================================

Add a new business rule function.

Example name:

validate_due_date_not_in_past()

Requirements:

- Accept an optional due_date.
- If due_date is None:
    validation passes.
- If due_date is today:
    validation passes.
- If due_date is in the future:
    validation passes.
- If due_date is before today:
    raise the same exception style already used in business_rules.py.

Validation message:

"Due date cannot be earlier than today"

Keep the implementation:
- small
- readable
- consistent with existing business rules

Do NOT:
- add classes
- add services
- add repositories

============================================================
FILE 2 - app/main.py
============================================================

Apply the new business rule:

1. POST /tasks

Before creating the task:
- validate due_date

If invalid:
- return the existing business validation error response style

2. PATCH /tasks/{id}

Before updating:
- validate due_date only when due_date is provided

Allow:
- due_date=None (removing due date)

Reject:
- past dates

3. Keep all existing behavior unchanged.

Do NOT:
- move business logic into endpoints
- duplicate validation logic
- calculate dates inside endpoints

Endpoints should only:
- receive request
- call business rule
- call storage
- return response

============================================================
HARD CONSTRAINTS
============================================================

- Do NOT modify models.py.
- Do NOT modify storage.py.
- Do NOT add databases.
- Do NOT add SQLAlchemy.
- Do NOT add ORM code.
- Do NOT add authentication.
- Do NOT add logging.
- Do NOT add services.
- Do NOT add repositories.
- Do NOT refactor unrelated code.
- Follow existing coding style.
- Keep the implementation simple.

============================================================
OUTPUT
============================================================

Output only:

# FILE: app/business_rules.py

# FILE: app/main.py

##############################################################################################

Before writing code, give me an incremental plan for adding Due Dates + Overdue Filter feature to the frontend in small Copilot/Codex loops.
Feature: [DESCRIBE FEATURE, e.g. Kanban board or create/edit modal]
Current file(s): [LIST FILES]
Output format:
Return a table with columns: Step, File or selection, What changes, How I verify it.

Constraints:
- Do not write code yet.
- Keep the plan : small changes, inspect the diff, run the app or tests, then refine.
- Do not introduce frameworks, new backend features, or unrelated files.
#####################################################################################
You are a senior Python backend engineer.

Context:
- This is a FastAPI Task Tracker application.
- The application already has the Due Dates & Overdue Filter feature.
- A business rule is already implemented:

Business Rule:
- A due date provided during creation or update must be today or a future date.
- A due date earlier than today is invalid and must be rejected.

However, an issue was identified in the PATCH endpoint.

============================================================
BUG DESCRIPTION
============================================================

When updating an existing task:

Example:
- Task already exists with:
    due_date = yesterday
    overdue = true

The team member updates another field:

Example:
{
    "status": "InProgress"
}

The current implementation incorrectly applies the "due date cannot be earlier than today" validation and rejects the update.

Expected behavior:

- If the due date is NOT changed:
    - Do not validate the existing due date.
    - Allow updating other fields normally.

- If the due date IS changed:
    - Apply the existing business rule.
    - Reject a new due date earlier than today.

============================================================
TASK
============================================================

Update ONLY the PATCH task flow.

Files to review:

- app/main.py
- app/business_rules.py (only if required)

Do NOT modify:
- app/models.py
- app/storage.py
- unrelated endpoints

============================================================
REQUIRED BEHAVIOR
============================================================

For PATCH /tasks/{id}:

Case 1:
Existing task:

due_date = yesterday

Request:

{
    "status": "InProgress"
}

Expected:
- Update succeeds.
- Existing overdue due_date remains unchanged.
- Task remains overdue.

---

Case 2:
Existing task:

due_date = yesterday

Request:

{
    "due_date": "2026-08-01"
}

Expected:
- Update succeeds.
- New due_date is saved.

---

Case 3:
Existing task:

due_date = yesterday

Request:

{
    "due_date": "2025-01-01"
}

Expected:
- Update rejected.
- Existing task remains unchanged.

---

Case 4:
Existing task:

due_date = yesterday

Request:

{
    "due_date": null
}

Expected:
- Update succeeds.
- Due date is removed.

============================================================
IMPLEMENTATION RULES
============================================================

- Do not remove the existing due date validation rule.
- Only apply validation when the incoming PATCH request contains a new due_date value.
- Do not validate unchanged existing task data.
- Keep business logic inside business_rules.py if that is the existing pattern.
- Keep main.py responsible only for request handling and calling validation.
- Do not add new features.
- Do not refactor unrelated code.

============================================================
OUTPUT
============================================================

Output only the modified files:

# FILE: app/main.py

(and only include app/business_rules.py if it actually requires changes)

###############################################################################
Tags / Labels
###############################################################################

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
- The existing storage.py already contains:
  - In-memory task storage
  - add_task()
  - get_all_tasks()
  - get_task_by_id()
  - update_task()
  - delete_task()
  - _reset()

- Do NOT recreate or redesign the existing models or storage.
- Only update them to support the Tags / Labels feature.

Relevant User Stories:

US-TAG-01
As a team member, I want to add multiple tags to a task so that I can categorize and organize tasks more easily.

Acceptance Criteria:
- A team member can add one or more valid tags when creating a task.
- Added tags are displayed with the task.
- A task can be created without tags and continues to work like existing tasks.

US-TAG-02
As a team member, I want to update or remove task tags so that task categories remain accurate over time.

Acceptance Criteria:
- A team member can add new tags while editing an existing task.
- A team member can remove existing tags from a task.
- Updating tags does not change other task fields.

US-TAG-03
As a team member, I want tags to follow validation rules so that task labels remain consistent, clean, and easy to search.

Acceptance Criteria:
- A tag cannot be empty.
- A tag cannot contain only whitespace.
- A tag cannot exceed 255 characters.
- A tag can contain only letters (A-Z, a-z) and numbers (0-9).
- Tags containing spaces, symbols, or special characters are rejected.
- Valid alphanumeric tags are saved successfully.

US-TAG-04
As a team member, I want to filter tasks by tag so that I can quickly find related tasks.

Acceptance Criteria:
- Tasks containing the selected tag can be retrieved.
- Tasks without the selected tag are excluded from results.
- Existing filtering behavior remains unchanged.

============================================================
FILE 1 - app/models.py
============================================================

Update the existing models.py only.

Requirements:

1. Update TaskCreate

Add:

tags: Optional[list[str]] = None

Rules:
- Tags are optional.
- Creating a task without tags must continue working.
- Keep all existing fields and validators unchanged.
- Add tag validation only if validation already exists in the model pattern.

Tag validation requirements:
- Reject empty tags.
- Reject whitespace-only tags.
- Reject tags longer than 255 characters.
- Reject tags containing characters other than letters and numbers.
- Accept only:
  - A-Z
  - a-z
  - 0-9

Do not allow:
- spaces
- hyphens
- underscores
- symbols
- special characters


2. Update TaskUpdate

Add:

tags: Optional[list[str]] = None

Rules:
- Tags can be updated.
- Tags can be removed.
- Keep all existing update behavior unchanged.
- Do not add unrelated fields.


3. Update TaskResponse

Add:

tags: list[str] = []

Rules:
- Returned task responses include tags.
- Existing response fields remain unchanged.
- Do not add tag management information.
- Do not introduce global tags.


Do NOT modify:
- TaskStatus
- TaskPriority
- Existing title validation
- Existing due_date behavior
- Existing ConfigDict configuration
- Existing field names
- Existing defaults unless required for tags support.

============================================================
FILE 2 - app/storage.py
============================================================

Update the existing storage.py only.

Requirements:

1. Task Creation

Update add_task():

- Store tags from TaskCreate.
- If tags are not provided, store an empty list.
- Preserve existing task creation behavior.


2. Task Retrieval

Update:

- get_all_tasks()
- get_task_by_id()

Ensure:
- Returned TaskResponse includes tags.
- Existing behavior remains unchanged.


3. Task Updates

Update update_task():

Requirements:
- Support updating tags.
- Allow adding tags.
- Allow replacing existing tags.
- Allow removing tags by providing an empty list.
- Do not modify other task fields unless provided.
- Continue using:

payload.model_dump(exclude_unset=True)

- Continue updating updated_at when changes occur.


4. Tag Filtering

Extend get_all_tasks() to support:

tag: Optional[str] = None

Filtering rules:

- tag=None:
  - Preserve existing behavior.

- tag provided:
  - Return only tasks containing that tag.

Tag matching:
- Exact match only.
- Do not implement partial search.
- Do not implement case conversion unless already supported by existing behavior.


5. Preserve Existing Functionality

Existing filters must continue working:

- status
- priority

The new tag filter should work together with existing filters.

Examples:
- status + tag
- priority + tag
- status + priority + tag


============================================================
HARD CONSTRAINTS
============================================================

- Do NOT modify API routes.
- Do NOT add endpoints.
- Do NOT introduce databases.
- Do NOT introduce SQLAlchemy.
- Do NOT introduce ORM code.
- Do NOT introduce services.
- Do NOT introduce repositories.
- Do NOT introduce global tag management.
- Do NOT add predefined tags.
- Do NOT add authentication.
- Do NOT add permissions.
- Do NOT add notifications.
- Do NOT add unrelated refactoring.
- Keep the implementation simple and consistent with the existing architecture.
- Use Pydantic v2 syntax only.
- Keep existing behavior unchanged for tasks without tags.

============================================================
OUTPUT
============================================================

Output only two code blocks, each preceded by:

# FILE: app/models.py

# FILE: app/storage.py

###############################################################

You are a senior Python backend code reviewer.

Review the generated implementation of:

- app/models.py
- app/storage.py

against the Tags / Labels feature requirements.

IMPORTANT:
- Do NOT modify any files.
- Do NOT generate code.
- Only review and report findings.
- Mark each checkpoint as PASS or FAIL.
- If FAIL, explain the issue briefly.

============================================================
REVIEW CHECKLIST
============================================================

1. Models Support Tags
- TaskCreate contains optional tags: list[str].
- TaskUpdate contains optional tags: list[str].
- TaskResponse contains tags.
- Existing task fields and validation remain unchanged.
- Existing due_date behavior remains unchanged.
- No unrelated fields were added.

2. Tag Validation Rules
- Tags are optional.
- Tasks can be created without tags.
- Empty tags are rejected.
- Whitespace-only tags are rejected.
- Tags longer than 255 characters are rejected.
- Tags containing special characters are rejected.
- Tags containing spaces are rejected.
- Only letters (A-Z, a-z) and numbers (0-9) are accepted.
- Valid alphanumeric tags are accepted.

3. Tag Creation & Updates
- Tasks can be created with one or multiple tags.
- Tags are stored correctly.
- Existing tasks without tags continue working.
- Tags can be updated.
- Existing tags can be replaced.
- Tags can be removed by providing an empty list.
- Updating tags does not modify other task fields.

4. Storage Filtering
- get_all_tasks supports an optional tag filter.
- Filtering by tag returns only tasks containing that exact tag.
- Tasks without the selected tag are excluded.
- Existing filters still work:
  - status
  - priority
- Tag filtering works together with existing filters.

5. Scope & Architecture
- Only models.py and storage.py were changed.
- No database, ORM, services, repositories, or unnecessary layers were introduced.
- No global tag management was added.
- No predefined tag list was added.
- No authentication or permissions were introduced.
- Existing task behavior remains unchanged.
- Implementation follows the mini-ADR decision.

============================================================
OUTPUT FORMAT
============================================================

# Tags / Labels Feature Review

| Checkpoint | Result | Notes |
|---|---|---|
| 1. Models Support Tags | PASS/FAIL | |
| 2. Tag Validation Rules | PASS/FAIL | |
| 3. Tag Creation & Updates | PASS/FAIL | |
| 4. Storage Filtering | PASS/FAIL | |
| 5. Scope & Architecture | PASS/FAIL | |

Final Verdict:
- APPROVED if all checkpoints pass.
- NEEDS FIXES if any checkpoint fails.
################################################################

You are a senior Python backend engineer.

Context:
- This project already has a working FastAPI Task Tracker REST API.
- The application uses in-memory storage only.
- app/models.py and app/storage.py have already been updated to support the Tags / Labels feature.
- Your task is ONLY to update the API endpoints in app/main.py to expose this feature.

Existing architecture:
- main.py contains FastAPI routes.
- Routes call storage functions.
- Business logic belongs in storage.py, not in main.py.
- Validation belongs in models.py/business rules if already implemented.
- main.py should only handle request/response flow.

============================================================
RELEVANT USER STORIES
============================================================

US-TAG-01

As a team member, I want to add multiple tags to a task so that I can categorize and organize tasks more easily.

Acceptance Criteria:
- A team member can add one or more valid tags when creating a task.
- Added tags are returned with the task.
- A task can be created without tags and continues to work like existing tasks.

---

US-TAG-02

As a team member, I want to update or remove task tags so that task categories remain accurate over time.

Acceptance Criteria:
- A team member can add new tags while editing a task.
- A team member can remove existing tags from a task.
- Updating tags does not modify other task fields.

---

US-TAG-03

As a team member, I want tags to follow validation rules so that task labels remain consistent, clean, and easy to search.

Acceptance Criteria:
- Empty tags are rejected.
- Whitespace-only tags are rejected.
- Tags longer than 255 characters are rejected.
- Tags containing special characters are rejected.
- Only letters (A-Z, a-z) and numbers (0-9) are allowed.

---

US-TAG-04

As a team member, I want to filter tasks by tag so that I can quickly find related tasks.

Acceptance Criteria:
- Users can request tasks containing a specific tag.
- Tasks without the selected tag are excluded.
- Existing status and priority filtering continues working.

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
- change existing response behavior unless required for tags support

---

2. Create Task Endpoint

Update the existing POST /tasks endpoint.

Requirements:

- Continue using TaskCreate as the request model.
- Accept optional tags automatically.
- Pass the payload unchanged to storage.
- Return the existing TaskResponse.

Do NOT:
- validate tags manually in main.py.
- add tag processing logic.
- duplicate model validation.

---

3. Get Tasks Endpoint

Update the existing GET /tasks endpoint.

Add a new optional query parameter:

tag: Optional[str] = None

Behavior:

- tag is not provided:
  - Keep existing behavior.

- tag is provided:
  - Return only tasks containing that exact tag.

Existing filters must continue working:

- status
- priority

Example combinations that must work:

- status + tag
- priority + tag
- status + priority + tag

The endpoint should only pass filtering parameters to storage.

Do NOT:
- filter tags inside main.py.
- implement search logic in the route.

---

4. Get Task By ID Endpoint

Update only if needed.

Requirements:

- Return tags with the task response.
- Keep existing behavior unchanged.

---

5. Update Task Endpoint

Update the existing PATCH/PUT endpoint.

Requirements:

- Continue using TaskUpdate.
- Accept tags updates.
- Allow:
  - adding tags
  - replacing existing tags
  - removing tags using an empty list
- Pass update payload to storage.
- Return updated TaskResponse.

Do NOT:
- implement tag update logic inside main.py.
- manipulate tag lists in the endpoint.

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
- Do NOT add global tag management.
- Do NOT add predefined tags.
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

############################################################
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

Tags / Labels

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

Tags:

- Tasks can optionally have multiple tags.
- Tasks can be created with or without tags.
- Tags can be updated.
- Tags can be removed.
- Tags are returned with task responses.

Tag validation:

- Empty tags are rejected.
- Whitespace-only tags are rejected.
- Tags longer than 255 characters are rejected.
- Tags containing spaces are rejected.
- Tags containing special characters are rejected.
- Only letters (A-Z, a-z) and numbers (0-9) are accepted.

Filtering:

- GET /tasks supports:
  tag=<tag>

- Tag filtering:
  - returns only tasks containing the selected tag.
  - does exact tag matching only.

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
created_task_with_tags

Behavior:
- Creates a task using POST /tasks
- Payload:

{
    "title": "task with tags",
    "tags": [
        "backend",
        "FastAPI123"
    ]
}

- Assert status_code == 201
- Return response JSON

Do not modify existing fixtures unless required.

============================================================
FILE 2 - tests/test_tasks.py
============================================================

Add the following tests.

Use the existing naming and style.

============================================================
POST /tasks - Tags Creation
============================================================

1. test_create_task_with_valid_tags_returns_201

Verify:
- Task creation succeeds.
- Response contains the provided tags.
- Multiple tags are stored correctly.

---

2. test_create_task_without_tags_returns_201

Verify:
- Task creation succeeds without tags.
- Response contains an empty list or expected default value.
- Existing task behavior remains unchanged.

---

3. test_create_task_with_empty_tag_returns_422

Verify:
- Empty tag value is rejected.

Example:

{
    "tags": [""]
}

---

4. test_create_task_with_whitespace_tag_returns_422

Verify:
- Whitespace-only tags are rejected.

Example:

{
    "tags": ["   "]
}

---

5. test_create_task_with_tag_over_255_characters_returns_422

Verify:
- A tag longer than 255 characters is rejected.

---

6. test_create_task_with_special_character_tag_returns_422

Verify:
- Tags containing special characters are rejected.

Examples:

"backend-api"
"test_tag"
"api@123"

---

7. test_create_task_with_alphanumeric_tag_returns_201

Verify:
- Tags containing only letters and numbers are accepted.

Examples:

"Backend"
"API123"

============================================================
GET /tasks - Tag Response
============================================================

8. test_get_task_returns_tags

Verify:
- Task response includes tags.

============================================================
PATCH /tasks/{id} - Tags Updates
============================================================

9. test_patch_task_updates_tags_returns_200

Verify:
- Existing task tags can be replaced or updated.
- Response contains the new tags.

---

10. test_patch_task_removes_tags_returns_200

Verify:
- Existing tags can be removed by sending an empty list.
- Response contains no tags.

---

11. test_patch_task_with_invalid_tag_returns_422

Verify:
- Updating a task with invalid tags is rejected.
- Existing tags remain unchanged.

============================================================
GET /tasks - Tag Filtering
============================================================

12. test_filter_tasks_by_tag_returns_matching_tasks

Create:

- Task with tag "backend"
- Task with tag "frontend"
- Task without tags

Call:

GET /tasks?tag=backend

Verify:
- Only tasks containing "backend" are returned.

---

13. test_filter_tasks_by_unknown_tag_returns_empty_list

Create:
- Tasks with different tags.

Call:

GET /tasks?tag=unknown

Verify:
- Empty list is returned.

---

============================================================
Combined filters
============================================================

14. test_filter_tasks_by_priority_and_tag_returns_matching_tasks

Create:

- HIGH priority task with tag "backend"
- LOW priority task with tag "backend"
- HIGH priority task with tag "frontend"

Call:

GET /tasks?priority=High&tag=backend

Verify:
- Only HIGH priority tasks containing "backend" are returned.

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
- Keep tests focused only on Tags / Labels.

Output only the modified files:

# FILE: tests/conftest.py

# FILE: tests/test_tasks.py
#####################################################################
Before writing code, give me an incremental plan for adding Tags / Labels feature to the frontend in small Copilot/Codex loops.
Feature: [DESCRIBE FEATURE, e.g. Kanban board or create/edit modal]
Current file(s): [LIST FILES]
Output format:
Return a table with columns: Step, File or selection, What changes, How I verify it.

Constraints:
- Do not write code yet.
- Keep the plan : small changes, inspect the diff, run the app or tests, then refine.
- Do not introduce frameworks, new backend features, or unrelated files.

############################################################################################
You are a senior frontend developer reviewing a Task Tracker web application UI.

Context:
- The application has a Create Task form and an Update Task form.
- The forms are displayed inside modal/dialog components.
- The current issue is that the form content is too large for the screen.
- On smaller screens, the user cannot see or access the Save button because it is below the visible area.

============================================================
TASK
============================================================

Fix the Create Task and Update Task modal layout so the forms are fully usable on all screen sizes.

============================================================
REQUIREMENTS
============================================================

1. Modal/Dialog Layout

Update the modal/dialog configuration to:

- Fit within the viewport height.
- Allow scrolling only inside the form content area.
- Keep the action buttons (Save/Cancel) always visible.

Expected behavior:

- User opens Create Task modal:
  - All fields are accessible.
  - Save button is visible without needing browser zoom.

- User opens Update Task modal:
  - All fields are accessible.
  - Save button is visible.

---

2. Responsive Behavior

Ensure the dialogs work on:

- Desktop screens.
- Laptop screens.
- Smaller resolutions.
- Mobile/tablet widths if supported by the existing application.

Do not break the existing responsive design.

---

3. Form Behavior

Do NOT:
- remove fields.
- change validation rules.
- change API calls.
- change form submission logic.
- change existing functionality.

Only update the layout and scrolling behavior.

---

4. UI Requirements

The preferred structure:

- Dialog container:
  - limited maximum height based on viewport.

- Form content:
  - scrollable area.

- Action section:
  - fixed/visible at the bottom.

Example behavior:

+-------------------------+
| Create Task             |
|-------------------------|
| Title                   |
| Description             |
| Status                  |
| Priority                |
| Assignee                |
| Due Date                |
| Tags                    |
|                         |
|   (scroll area)         |
|-------------------------|
| Cancel       Save       |
+-------------------------+

---

============================================================
CONSTRAINTS
============================================================

- Do not redesign the UI.
- Do not change colors, themes, or components unnecessarily.
- Do not change backend code.
- Do not change API contracts.
- Keep the existing component structure.
- Make the smallest change required to fix the usability issue.

============================================================
OUTPUT
============================================================

Output only the modified frontend files.
For each file, prefix with:

# FILE: path/to/file

##################################################################

You are a senior frontend developer updating an existing Task Tracker web application.

Context:
- The application already supports filtering tasks by tag.
- The tag filter is already implemented in the frontend.
- Users can select a tag and view filtered tasks.
- The current issue is that there is no simple way to clear the selected tag filter.

============================================================
TASK
============================================================

Add a "Clear" button for the Tag Filter.

The change should only affect the tag filtering UI behavior.

============================================================
REQUIREMENTS
============================================================

1. Tag Filter UI

Update the existing tag filter component/control.

Add a Clear button that:

- Is visible when a tag filter is selected.
- Clears the selected tag when clicked.
- Restores the normal task list without tag filtering.

Expected behavior:

Before:

Selected tag:
backend

Task list:
Only tasks with "backend"

After clicking Clear:

Selected tag:
(empty)

Task list:
All tasks (respecting other active filters)

---

2. Interaction with Existing Filters

The Clear Tag Filter button must:

- Remove only the tag filter.
- Keep other filters unchanged.

Examples:

If the user has:

- Status = InProgress
- Priority = High
- Tag = backend

Clicking Clear:

Result:
- Status remains InProgress.
- Priority remains High.
- Tag is cleared.

---

3. UI Behavior

Requirements:

- Match the existing application style.
- Use existing UI components and patterns.
- Do not redesign the filter section.
- Do not add unnecessary components.

The button can:
- Be hidden when no tag is selected.
OR
- Be disabled when no tag is selected.

Follow the existing filter behavior.

---

4. Data/API Behavior

Do NOT:
- Modify backend endpoints.
- Modify API contracts.
- Add new API calls.

When clearing the tag:
- Update the frontend filter state.
- Trigger the existing task loading/filtering mechanism.

---

============================================================
CONSTRAINTS
============================================================

- Do not modify backend code.
- Do not change tag filtering logic.
- Do not change other filters.
- Do not change task CRUD functionality.
- Keep the implementation minimal.
- Follow the existing frontend architecture and coding style.

============================================================
OUTPUT
============================================================

Output only the modified frontend files.

For each file, prefix with:

# FILE: path/to/file