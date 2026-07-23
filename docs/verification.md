# 1. Baseline Check

**Date:** 2026-07-21

## Initial application state before feature work

Existing Task Tracker (FastAPI + in-memory storage + simple web frontend) supported:

- Create tasks (title, description, status, priority, assignee)
- List / view tasks
- Filter by status and priority
- Update tasks (including status transitions via business rules)
- Delete tasks
- Serve frontend HTML from `/`

## Existing functionality verified before adding features

| Check | Command / method | Result |
|---|---|---|
| Pytest suite | `pytest -q` | **19 passed** in 0.19s |
| App startup | `uvicorn app.main:app --host 127.0.0.1 --port 8000` | Server started; `/health` returned `{"status":"ok", ...}` |

Part A model contract (`tests/verify_a.py`) was also used during development as a baseline for title validation, defaults, `extra='forbid'`, and enum rejection (8 checks).


# 2. Backend Test Results

## Commands and files

| When | Command | Files |
|---|---|---|
| Baseline (pre-features) | `pytest -q` | Existing `tests/test_tasks.py` suite |
| After due-date tests added | `pytest` / `py -m pytest tests/test_tasks.py -v` | `tests/conftest.py`, `tests/test_tasks.py` |
| After past-due rule + test fixes | `pytest` on `tests/test_tasks.py` | Same |
| After tags tests added | `.venv` / `py -m pytest tests/test_tasks.py` | Same |
| Post-feature regression | `pytest -q` and `python tests/verify_a.py` | Full suite + Part A contract |
| Later re-run | `pytest` (after UI polish) | Full suite |

## Results (actual runs recorded in project history)

| Run | Result | Notes |
|---|---|---|
| Baseline | **19 passed** | Before due dates / tags |
| After due-date tests | **31 passed** | 12 due-date/overdue tests added |
| After past-due business-rule tests first run | **29 passed, 4 failed** | New past-due tests passed; older overdue tests still created yesterday via API and got `422` |
| After overdue seed fix | **33 passed** | Past dates seeded with `storage.add_task()` |
| Intentional validator break | **31 passed, 2 failed** | `validate_due_date_not_in_past` temporarily a no-op (`1==1`) |
| After restoring validator | **33 passed** | Past-due create/update tests green again |
| After tags tests | **47 passed** | 14 tag tests + prior suite |
| Behavior contract + full suite (2026-07-23) | `verify_a.py` **8/8 PASS**; `pytest -q` **47 passed** in 0.31s | |
| Later UI session | **47 passed** in 0.38s | |

## Fixes performed because of failing tests

1. Overdue tests that POSTed past dates were updated to seed overdue tasks through storage after the API began rejecting past due dates.
2. Past-due validation was restored after an intentional no-op break so create/update rejection tests passed again.


# 3. Manual Browser Checks

Detailed Pass/Fail notes for every checklist item were **not fully recorded** in project docs. Evidence below comes from implemented UI, follow-up fix prompts, and automated coverage where noted.

## Task Management

| Check | Evidence | Result |
|---|---|---|
| Create task | Covered by pytest + frontend create modal | Exercised via tests|
| Edit task | Covered by pytest + edit modal | Exercised via tests|
| Delete task | Covered by pytest | Exercised via tests|
| Filtering (status/priority) | Baseline + combined filter tests | Exercised via tests |

## Due Dates

| Check | Evidence | Result |
|---|---|---|
| Create with due date | Tests + frontend date input / POST | Automated: pass|
| Create without due date | Tests | Automated: pass |
| Update / remove due date | Tests + frontend PATCH (`null` to clear) | Automated: pass |
| Overdue identification | Tests + card overdue styling from API `overdue` | Automated: pass |
| Overdue filtering | Tests + “Overdue only” UI control | Automated: pass |

Additional UI fix observed in session: due-date API errors were moved from the top of the modal to under the due-date field.

## Tags

| Check | Evidence | Result |
|---|---|---|
| Create with tags | Tests + comma-separated Tags field | Automated: pass |
| Update tags | Tests + edit prefill / PATCH | Automated: pass |
| Remove tags | Tests + empty tags on edit | Automated: pass |
| Tag filtering | Tests + header tag filter (`?tag=`) | Automated: pass |
| Clear tag filter | Dedicated frontend prompt + Clear control in UI | Implemented after gap was identified|

## UI

| Check | Evidence | Result |
|---|---|---|
| Create/Edit modal usability | Prompted fix: form too tall; Save below fold | Modal updated for viewport height, scrollable body, actions kept visible |
| Save button visibility | Same modal-layout fix | Addressed in frontend change |
| Validation messages | Client + API messages (title, due date, tags) | Due-date field-level error placement corrected in a follow-up |

Static frontend was also served locally (`http://localhost:5500/index.html`) during due-date UI work.


# 4. Behavior Contract Before/After Refactor

## Behavior contract created before refactoring

A manual regression contract was generated (prompt in `docs/prompts.md`; output in development session) covering:

- Core task management
- Due dates / overdue rules and filters
- Tags / labels and tag filter clear behavior
- Frontend modal / validation / filter behaviors
- Backend/API stability expectations

Format: `| ID | Behavior | How to check manually | Pass/Fail notes |`

Earlier automated baseline: `tests/verify_a.py` (Part A title/defaults/`extra='forbid'`/enum checks).

## Behaviors verified after feature work

- `tests/verify_a.py`: **8/8 PASS**
- Full pytest suite: **47 passed**
- These confirm core model validation and feature acceptance tests still hold after due dates, tags, business-rule, and frontend changes.

## Changed behavior (intentional product changes, not accidental regressions)

- Optional `due_date` and calculated `overdue` on responses
- Optional `overdue` and `tag` list filters
- Past due dates rejected on create/update when the due date is being set/changed
- Optional `tags` with alphanumeric/length validation

## Confirmation existing behavior was preserved

Existing CRUD, status transitions, status/priority filters, and tasks without due dates/tags remain covered by the original tests plus extended suite.


# 5. Break Test Evidence

## Break 1 — Past-due validator intentionally disabled

- **What was changed/broken:** `validate_due_date_not_in_past()` temporarily became a no-op (`1==1`; real check commented out).
- **Expected failure behavior:** Create/update with yesterday’s date should return `422` but instead returned `201` / `200`.
- **Test that detected it:** `test_create_task_with_past_due_date_returns_validation_error` and `test_patch_task_with_past_due_date_returns_validation_error` (**31 passed, 2 failed**).
- **Fix applied:** Restored the real past-date check; suite returned to **33 passed**.

## Break 2 — Overdue tests broken by new past-due API rule

- **What was changed/broken:** After enforcing “due date cannot be earlier than today” on POST, existing overdue tests still created yesterday’s date through the HTTP API.
- **Expected failure behavior:** Those creates fail with `422`, so overdue/filter assertions cannot run.
- **Tests that detected it:** `test_task_with_past_due_date_is_overdue`, `test_filter_tasks_by_overdue_true_returns_only_overdue_tasks`, `test_filter_tasks_by_overdue_false_returns_only_non_overdue_tasks`, `test_filter_tasks_by_priority_and_overdue_returns_matching_tasks` (**29 passed, 4 failed**).
- **Fix applied:** Seed overdue tasks via `storage.add_task()` (bypass API create validation), then assert overdue behavior through GET/filter endpoints; suite returned to **33 passed**.
