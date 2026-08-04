# Repo-Grounded Comments Feature Plan

Comments on Tasks — feature plan grounded in this repository’s files and conventions. Saved for Module 5 comparison; not implemented here.

## 1. Data Model

Add the comment schemas to `app/models.py`, alongside `TaskCreate`, `TaskUpdate`, and `TaskResponse`.

Recommended shapes:

- **CommentCreate** — `author: str`, `body: str`, `extra="forbid"`, matching every existing Pydantic request model.
- **CommentResponse** — `id: str`, `task_id: str`, `author: str`, `body: str`, `created_at: datetime`

Follow the existing model-validation pattern:

- Add shared helpers such as author/body validators near `_validate_title` and `_validate_tag`.
- Strip leading/trailing whitespace before checking length.
- Reject blank values after stripping.
- Enforce author length of 1–100 and body length of 1–2,000.
- Keep `id`, `task_id`, and `created_at` out of `CommentCreate`, so they are server-controlled or path-derived. This mirrors the current task creation shape, where generated fields are absent from `TaskCreate` and unknown fields are rejected.
- `task_id` should appear in `CommentResponse`, despite being supplied by the route path, so a returned comment is self-describing.
- No comment-related cross-field or state-transition rule is currently evident, so comment field validation belongs in `app/models.py`; task existence should be checked by route/storage coordination, as GET, PATCH, and DELETE `/tasks/{task_id}` do today.

## 2. API Routes

Add nested routes in `app/main.py`, keeping its established flow: handler checks required state, then delegates persistence to `app.storage`.

| Method and path | Request body | Success response | Error cases |
| --- | --- | --- | --- |
| `POST /tasks/{task_id}/comments` | author, body | 201 Created with `CommentResponse` | 404 with the repository’s existing task-not-found detail if `task_id` is absent; 422 for missing, blank, overlong, malformed, or extra fields |
| `GET /tasks/{task_id}/comments` | None | 200 OK with `list[CommentResponse]` | 404 if the task does not exist; 200 `[]` for an existing task with no comments |

The create handler should first confirm the parent task exists, then ask storage to generate the UUID and UTC timestamp. This matches the current `storage.add_task()` responsibility for IDs and timestamps.

For consistency with the established error text, use:

`Task with id {task_id} not found`

Comments should not be added to existing `TaskResponse` payloads in the initial version. Current task list and detail routes return a stable, flat task shape; a nested collection would expand every task response and require loading comments even when the UI does not need them. The nested comments endpoint provides a narrower addition.

Recommended initial ordering for `GET /tasks/{task_id}/comments`: oldest first, in creation order. Document this as part of the route contract and test it.

## 3. Tests

Extend `tests/test_tasks.py`, which already uses descriptive `test_<action>_<condition>_returns_<result>` names and creates normal setup data through the API. Reuse `created_task` from `tests/conftest.py`.

### Happy path

- `test_create_comment_valid_returns_201_with_full_body`
- `test_create_comment_generates_uuid_and_utc_created_at_returns_201`
- `test_list_comments_for_task_returns_200_and_comments`
- `test_list_comments_for_task_without_comments_returns_200_and_empty_list`
- `test_list_comments_returns_comments_in_creation_order`
- `test_list_comments_for_task_returns_only_its_comments`

### Validation

- `test_create_comment_missing_author_returns_422`
- `test_create_comment_blank_author_returns_422`
- `test_create_comment_author_over_100_characters_returns_422`
- `test_create_comment_missing_body_returns_422`
- `test_create_comment_blank_body_returns_422`
- `test_create_comment_body_over_2000_characters_returns_422`
- `test_create_comment_unknown_field_returns_422`
- `test_create_comment_client_supplied_id_returns_422`
- `test_create_comment_client_supplied_task_id_returns_422`
- `test_create_comment_client_supplied_created_at_returns_422`

The generated-field tests should follow the existing API-level style: assert status code and returned JSON fields rather than relying only on direct storage access.

### Edge cases

- `test_create_comment_for_missing_task_returns_404_with_detail`
- `test_list_comments_for_missing_task_returns_404_with_detail`
- `test_delete_task_with_comments_removes_associated_comments` — if cascade deletion is selected.
- `test_create_comment_with_author_at_100_characters_returns_201`
- `test_create_comment_with_body_at_2000_characters_returns_201`

Update the autouse reset in `tests/conftest.py` indirectly by ensuring `storage._reset()` clears both task and comment state. No new test cleanup fixture should be needed.

## 4. Frontend Changes

Change `frontend/index.html`, the single static HTML/CSS/JavaScript frontend served from `/` by `app.main`.

The current UI is a three-column task board. Cards are rendered by `renderTaskCard`, and the existing edit modal is opened by the Edit button. The lowest-risk interaction design is to show comments within the existing Edit Task modal only:

- When editing an existing task, show a comments section below the task fields.
- Load comments from `GET /tasks/{task_id}/comments` when that modal opens.
- Display author, body, and a locally formatted `created_at`.
- Show a visible empty state such as “No comments yet.”
- Add an author input and body textarea with a submit button.
- Submit to `POST /tasks/{task_id}/comments`, then reload or append the returned comment.
- Provide distinct loading and error states for comments so a comment request failure does not prevent task editing.
- Hide or disable the comments section when creating a new task, because no task ID exists until the task is created.

Add CSS in the same file for the comment list, entry form, compact metadata, empty state, and validation/error messages. Match the current modal, field-group, field-error, and button conventions.

The frontend currently renders task values through template-string `innerHTML`. The implementation should ensure comment author/body text is safely rendered as text rather than interpolated as raw HTML; comments are a new free-form text surface.

## 5. Migration Notes

There is no database migration required: `app/storage.py` stores tasks in the in-memory `_tasks: dict[str, TaskResponse]`, and the README confirms data is lost on server restart.

Add separate in-memory comment storage rather than embedding comment arrays into the existing `TaskResponse` values. A practical shape is a mapping keyed by task ID, preserving efficient retrieval for the proposed nested routes. Storage functions should mirror the current task CRUD naming and keep UUID/timestamp generation in storage.

Task deletion needs an explicit decision. If cascade deletion is chosen, `delete_task()` should remove the associated comment collection as part of the same in-memory operation. The reset helper must clear comment state as well as `_tasks`.

Existing task objects and existing task endpoint response shapes need not change. Existing tasks will naturally return no comments until comments are created.

Record this decision in `docs/mini-adr.md`, whose existing ADRs document why due dates and tags use their current data shapes.

## 6. Open Questions

- Should deleting a task cascade-delete its comments, or should deletion be blocked when comments exist? For this in-memory learning app, cascade deletion is the simplest behavior, but it is still a product decision.
- Is author intentionally user-entered text? The README states that this project has no authentication, so there is currently no authenticated identity to derive it from.
- Should comments be immutable in the first release, or should edit/delete endpoints be included? The requested fields do not include `updated_at`, which favors immutable comments initially.
- Should comments display only in the edit modal, or should each board card show a comment count and a way to open the discussion?
- What ordering should the API guarantee—oldest-first for conversational reading, or newest-first for recent activity?
- Should body content be plain text only, or should markdown/rich-text support be planned? Plain text is safer and better aligned with the current single-file frontend.

## Files read

- `AGENTS.md`
- `README.md`
- `app/models.py`
- `app/main.py`
- `app/storage.py`
- `app/business_rules.py`
- `tests/conftest.py`
- `tests/test_tasks.py`
- `tests/verify_a.py`
- `frontend/index.html`
- `docs/mini-adr.md`

## Assumptions to verify

- The feature is limited to creating and listing comments; edit/delete comment behavior is not yet required.
- Comments should be removed when their parent task is deleted.
- The API should return comments oldest-first.
- The comments panel belongs in the existing task edit modal rather than a new task-detail screen.
- `created_at` should use the same timezone-aware `datetime.now(timezone.utc)` convention already used for task timestamps.
