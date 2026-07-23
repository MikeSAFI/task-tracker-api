# Feature: Due Dates & Overdue Filter

## Prompt 1 - Generate user stories

**Prompt purpose:** Define product requirements before implementation.

**Short summary:** Asked AI (product-owner role) to produce 3–4 user stories per new feature with testable acceptance criteria for optional due dates, overdue identification, and overdue filtering—without inventing out-of-scope functionality.

**Why used:** Needed clear acceptance criteria before changing models, storage, or UI.

**AI Output Summary:** Table of stories (US-DD-01 through US-DD-04) covering create/view/update due dates, overdue rules, and filtering. Initial US-DD-01 did not define what a “valid” due date means.

**Review Decision:**
- **Accepted:** Overall story structure and overdue assumptions (date-based, not time-of-day).
- **Edited manually:** US-DD-01 rewritten so a valid due date cannot be earlier than the current date (see Weak vs Strong example).
- **Rejected:** None beyond that clarification.

## Prompt 2 - Update `app/models.py` and `app/storage.py`

**Prompt purpose:** Implement due-date fields and dynamic overdue calculation in the backend data layer.

**Short summary:** Constrained prompts to add optional `due_date`, response `overdue: bool` (not calculated in the Pydantic model), `_is_overdue` helper, and optional `overdue` filter on `get_all_tasks`—without redesigning architecture or storing overdue permanently.

**Why used:** Keep changes scoped to models/storage and align with Mini-ADR-001.

**AI Output Summary:** `due_date` on create/update/response; `overdue` on response; storage populates overdue on return and filters by overdue when requested.

**Review Decision:**
- **Accepted without changes:** Field shapes, dynamic overdue helper, filter composition with status/priority.
- **Edited manually:** Not available for this step.
- **Rejected / corrected:** ADR alternatives to *store* an overdue boolean or let users mark overdue manually were rejected in Mini-ADR-001.

## Prompt 3 - Wire API (`app/main.py`) and extend pytest

**Prompt purpose:** Expose overdue filtering on `GET /tasks` and lock behavior with tests.

**Short summary:** Update list endpoint with optional `overdue` query param; add fixture `created_task_with_due_date` and twelve due-date/overdue tests without rewriting existing CRUD tests.

**Why used:** Confirm API contract and prevent regressions.

**AI Output Summary:** `overdue` query param passed through to storage; tests for create/update/remove due date, overdue calculation, and combined filters. Initial run after due-date tests: **31 passed**.

**Review Decision:**
- **Accepted:** Endpoint wiring and most new tests.
- **Edited later:** Overdue tests that created past dates via HTTP were adjusted after the past-due business rule was added (seed via `storage.add_task()` instead).
- **Rejected:** None at this step.

## Prompt 4 - Past-due business rule + PATCH correction

**Prompt purpose:** Enforce “due date must be today or future” and fix false rejections on unrelated PATCH updates.

**Short summary:** Add `validate_due_date_not_in_past` in `business_rules.py` and call it from create/update. Follow-up prompt: only validate when the PATCH request actually changes `due_date` (so existing overdue tasks remain editable for other fields).

**Why used:** Product rule from clarified user stories; a real PATCH bug was found when editing other fields on overdue tasks (including UI resubmitting an unchanged past due date).

**AI Output Summary:** Business-rule function and endpoint wiring; PATCH gated so unchanged past due dates are not re-validated.

**Review Decision:**
- **Accepted:** Message `"Due date cannot be earlier than today"` and create/update validation.
- **Edited manually:** PATCH logic tightened to compare against stored due date (not only `model_fields_set`), after the UI still failed Case 1-style updates.
- **Rejected / corrected:** Temporary no-op of the validator (`1==1` / commented check) during break testing—restored so validation tests pass again.


# Feature: Tags / Labels

## Prompt 1 - Generate / refine tag user stories

**Prompt purpose:** Specify tag CRUD, validation, and filtering behavior.

**Short summary:** Same product-owner prompt batch as due dates; later rewrite of US-TAG-03 for explicit validation rules.

**Why used:** First AI draft only stressed empty tags; product needed alphanumeric + length rules before coding validators.

**AI Output Summary:** US-TAG-01–04 for add/update/remove tags and filter-by-tag. Initial US-TAG-03 validation was incomplete.

**Review Decision:**
- **Accepted:** Optional multi-tag model; filter alongside status/priority.
- **Edited manually:** US-TAG-03 rewritten: max 255 characters; letters and numbers only.
- **Rejected:** Global tag administration / predefined tag lists (out of scope).

## Prompt 2 - Models + storage + API for tags

**Prompt purpose:** Implement tags end-to-end on the backend.

**Short summary:** Add optional `tags` on create/update, `tags: list[str]` on response with alphanumeric/length validators; store tags (default `[]`); exact-match `tag` filter on `get_all_tasks`; expose `tag` query param on `GET /tasks`.

**Why used:** Implement Mini-ADR-002 without new entities or database layers.

**AI Output Summary:** Tag validators in models; storage create/update/filter; main.py passes `tag` through. Code review checklist: all checkpoints **PASS / APPROVED**.

**Review Decision:**
- **Accepted without changes:** Per-task string list, exact tag match, composition with existing filters.
- **Edited manually:** Not available for this step.
- **Rejected:** ADR alternatives—separate Tag entity and comma-separated single string—documented as rejected in Mini-ADR-002.

## Prompt 3 - Tag pytest coverage + frontend loops

**Prompt purpose:** Automate tag acceptance criteria and add board UI support.

**Short summary:** Fourteen tag-focused tests (create/validate/update/remove/filter/combined filters) plus incremental frontend plan/implement prompts for chips, form field, client validation, `?tag=` filter, Clear button, and modal scroll so Save stays visible.

**Why used:** Backend was ready; UI still needed tags, clear-filter UX, and usable create/edit modals after more fields were added.

**AI Output Summary:** `created_task_with_tags` fixture and 14 tests; frontend tags on cards/forms/filters; Clear tag-filter control; scrollable modal with fixed actions. Full suite later: **47 passed**.

**Review Decision:**
- **Accepted:** Test set and core tag UI wiring.
- **Edited manually:** Follow-up prompts for Clear tag filter and modal Save-button visibility after usability issues were observed.
- **Rejected:** Backend/API redesign during frontend work (explicitly forbidden in prompts).


# Weak Prompt vs Strong Prompt Example

## Original weak prompt

```text
fix my Business-rules file to include due date business rule
```

## Problems with the weak prompt

- **Vague goal:** Does not define what “due date business rule” means.
- **No scope:** Says only `business_rules.py`; does not say to wire the rule into `POST /tasks` and `PATCH /tasks/{id}`.
- **No error contract:** No validation message, no guidance to reuse existing business-rule exception/response style.
- **No constraints:** Does not forbid unrelated refactors or changes to models/storage/tests, so the AI may invent structure or touch the wrong files.

## Improved prompt approach

The full strong prompt is recorded in `docs/prompts.md` (Due Date Not In Past — business rule + wire into create/update). It:

- States the rule explicitly: due date must be **today or future**; **earlier than today** is invalid; `None` is allowed.
- Names the function shape (`validate_due_date_not_in_past`), message (`"Due date cannot be earlier than today"`), and where to call it (create always; update only when `due_date` is provided).
- Limits edits to `app/business_rules.py` and `app/main.py`, keeps endpoints thin (call rule → storage → response), and lists hard constraints (no models/storage/DB/ORM/auth/logging/services).

## Result improvement

With the vague prompt, the AI could invent an incomplete or inconsistent due-date rule—or add a helper that never gets called from create/update. The improved prompt produced a clear validator (`today` / future / `None` allowed, past rejected with a fixed message), wired it into both endpoints in the existing error style, and kept changes limited to `business_rules.py` and `main.py`.
