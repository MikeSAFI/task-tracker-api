# Comments Feature Plan — Module 5 Evaluation

Grading of the **repo-grounded** comments-feature plan against the pasted plan text and verified repo context. Labels: **Right** | **Missing** | **Needs-Resequencing**.

No feature implementation was performed.

## 1. Section critique

| Section | Label | Evidence | Minimal correction |
| --- | --- | --- | --- |
| Data Model | Right | Plan places `CommentCreate` / `CommentResponse` in `app/models.py` beside `TaskCreate` / `TaskUpdate` / `TaskResponse`, with `extra="forbid"` and shared strip/length helpers near `_validate_title` / `_validate_tag`. Repo matches: `AGENTS.md` and `app/models.py` use that pattern; generated fields stay off create models. Task existence stays in routes/storage, matching how GET/PATCH/DELETE `/tasks/{task_id}` work today. | Keep as-is. |
| API Routes | Right | Nested `POST`/`GET` `/tasks/{task_id}/comments` in `app/main.py`, 201/200/404/422, and detail `Task with id {task_id} not found` match `app/main.py` (e.g. create task uses `201`, not-found text is exact). Omitting comments from `TaskResponse` and generating UUID/UTC in storage mirrors `storage.add_task()` and keeps list/detail shapes flat. Oldest-first is stated as the initial contract. | Keep as-is. |
| Tests | Needs-Resequencing | Naming (`test_<action>_<condition>_returns_<result>`), `created_task` from `tests/conftest.py`, API-level asserts, and extending `_reset()` to clear comments match repo conventions (`AGENTS.md`, `tests/test_tasks.py`, `storage._reset()` only clears `_tasks` today). But `test_delete_task_with_comments_removes_associated_comments` is gated “if cascade deletion is selected,” while **Assumptions to verify** already choose cascade. | Resolve cascade first (or treat the assumption as decided), then keep an unconditional cascade-deletion test. |
| Frontend Changes | Right | Single `frontend/index.html` board, `renderTaskCard`, shared Edit modal, and `innerHTML` template rendering are real (`frontend/index.html`; `AGENTS.md`). Comments only in edit mode, hide on create (no `task_id`), separate comment loading/error states, and safe text rendering for free-form author/body fit the existing UI and known `innerHTML` risk. | Keep as-is. |
| Migration Notes | Needs-Resequencing | Correct that there is no DB migration: in-memory `_tasks` in `app/storage.py`, data lost on restart (`README.md`, `AGENTS.md`). Separate comment map, mirror CRUD naming, and ADR in `docs/mini-adr.md` fit existing practice. Cascade is still framed as “needs an explicit decision” even though Assumptions already pick cascade. | Decide cascade (assumption already says yes), then write the storage/`_reset`/`delete_task` notes and mini-ADR as the decided behavior—not as an open fork. |
| Open Questions | Needs-Resequencing | Auth-as-author is rightly open: `README.md` states no authentication. Several other questions (cascade, create/list-only, oldest-first, edit-modal placement, plain text) are already answered in **Assumptions to verify** / earlier sections, so leaving them fully open conflicts with the plan’s own decisions. | Keep only truly unresolved product choices (e.g. board comment counts vs modal-only polish). Promote settled items to short Decisions; drop duplicates from Open Questions. |

## 2. Generic vs repo-grounded (three lines)

- **Biggest difference:** The generic plan describes a portable comments feature (DB migrations, optional pagination, PATCH/DELETE, task-detail vs list UI); the repo-grounded plan maps the same create/list idea onto this repo’s real files, in-memory storage, error text, test fixtures, and single-file edit modal.
- **Plan I would hand a teammate:** The repo-grounded plan — after closing the cascade / immutability / ordering / placement decisions — because it names concrete touch points (`models.py`, `main.py`, `storage.py`, `test_tasks.py`, `conftest.py`, `frontend/index.html`, `mini-adr.md`) and matches existing conventions.
- **When generic chat is enough:** Early scoping or product brainstorming before touching this codebase (field list, auth questions, edit/delete policy) — not for implementation sequencing in this FastAPI/in-memory/static-HTML app.
