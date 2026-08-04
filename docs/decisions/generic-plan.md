# Generic Comments Feature Plan

Portable / chat-style plan (not repo-specific). Saved for Module 5 comparison; not an implementation guide for this codebase.

## 1. Data Model

Add a Comment entity with:

- `id`: server-generated UUID string
- `task_id`: required task reference / foreign key
- `author`: required string, 1–100 characters
- `body`: required string, 1–2,000 characters
- `created_at`: server-generated UTC datetime

Define separate request and response shapes so clients cannot set `id` or `created_at`.

Validate trimmed author and body values; reject blank or out-of-range values.

Decide whether comment ordering is always chronological ascending, descending, or client-selectable.

## 2. API Routes

`POST /tasks/{task_id}/comments`

- Creates a comment for an existing task.
- Accepts author and body.
- Returns the created comment with generated fields.
- Returns not-found when the task does not exist.

`GET /tasks/{task_id}/comments`

- Lists comments for one task.
- Supports a documented default ordering.
- Consider pagination if tasks may accumulate many comments.

Optional future routes:

- `GET /comments/{comment_id}` for direct retrieval.
- `PATCH /comments/{comment_id}` if editing is allowed.
- `DELETE /comments/{comment_id}` if deletion or moderation is needed.

## 3. Tests

- Creation succeeds for valid author/body input.
- Creation rejects missing, blank, too-short, and too-long fields.
- Server generates a valid UUID-like ID and UTC timestamp.
- Client-supplied `id` and `created_at` are rejected or ignored, according to the API contract.
- Creating a comment for an unknown task returns not-found.
- Listing comments returns only comments belonging to the requested task.
- Listing order is verified, including multiple comments created close together.
- Comments do not alter the task’s other fields or behavior.
- If pagination is implemented, test limits, cursors/pages, and stable ordering.
- If editing/deleting is implemented, test permissions, missing comment behavior, and task-comment ownership.

## 4. Frontend Changes

- Add a comments section to the task-detail view or task card.
- Display author, body, and a user-friendly rendering of `created_at`.
- Add a comment form with author and body fields.
- Disable submission or show validation feedback for invalid input.
- Show loading, empty, success, and error states.
- Refresh or optimistically update the comment list after submission.
- Escape or safely render comment text to prevent script injection.
- Consider whether comments should be visible in task lists, only task detail, or both.

## 5. Migration or data-shape notes

- For persistent storage, add a comments table/collection keyed by `task_id`, with an index on `task_id` and likely `created_at`.
- Decide foreign-key deletion behavior:
  - cascade-delete comments with a task,
  - prevent task deletion while comments exist, or
  - retain comments in an archival form.
- Existing task payloads can remain unchanged if comments are exposed through nested routes.
- If embedding comments in task responses, define whether they are always included, optionally expanded, or summarized with a count.
- Backfill is typically unnecessary because existing tasks simply begin with zero comments.

## 6. Open Questions

- Is authentication available, and should author come from the signed-in user instead of request input?
- Can comments be edited or deleted? If so, by whom?
- Should comments support rich text, markdown, mentions, attachments, or only plain text?
- What ordering and pagination behavior is desired?
- Should deleted comments be permanently removed or soft-deleted?
- Should task deletion cascade to comments?
- Are audit history, moderation, rate limiting, or notifications required?
- Should comment counts appear in task listings?

## Assumptions this plan makes

- Assumption: Tasks already have a stable string identifier that can be referenced by comments.
- Assumption: The API uses conventional HTTP JSON endpoints and distinguishes invalid input from missing resources.
- Assumption: `created_at` is produced by the server in UTC, preferably in an unambiguous ISO 8601 representation.
- Assumption: Comment text is plain user-provided content and needs safe rendering in any browser-based interface.
- Assumption: Comments belong to exactly one task and do not need their own independent lifecycle beyond the task unless future requirements add it.
