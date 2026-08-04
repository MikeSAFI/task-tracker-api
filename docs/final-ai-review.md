# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log

**File reviewed:** `app/main.py` (`update_task` / PATCH due-date gating, lines ~142–186)

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Call `validate_due_date_not_in_past` whenever `due_date` appears in the PATCH body (`model_fields_set`). | Wrong | The edit form resubmits the existing past due date when saving other fields. Validating on presence alone blocks legitimate updates of overdue tasks. | Corrected to: validate only when `due_date` is present **and** `payload.due_date != existing.due_date` (see handler comment and `docs/prompt-log.md` Prompt 4 / `docs/ai-playbook.md`). |
| Keep status changes behind `validate_status_transition` so PATCH cannot skip states (e.g. ToDo→Done). | Useful | Matches `VALID_TRANSITIONS` and existing pytest cases for invalid transitions. | Kept; still called only when `payload.status is not None`. |
| Persist an `overdue` boolean on the task so list filters do not recompute it. | Noise | Duplicates data already derived from `due_date` vs today; Mini-ADR-001 rejected storing overdue. | Rejected; overdue stays computed in `storage._with_overdue()` / `_is_overdue()`. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| SEC-01: Task fields rendered via unescaped `innerHTML` (stored XSS risk). | `frontend/index.html` (~991–1005) | Valid | Title/description/assignee/tags are interpolated into HTML without escaping; length limits do not remove XSS risk. | Backlog: escape before `innerHTML` (small frontend refactor, not a one-line ship). |
| SEC-03: No authentication on task routes. | `app/main.py` (public `/tasks` routes); README “no authentication” | Valid | Any caller can CRUD tasks; intentional course scope, but a real deployment blocker. | Accept as course-scope limit; do not deploy with real data. |
| SEC-05: Unpinned base image / no dependency scan hashes in Docker/CI. | `Dockerfile`; `.github/workflows/ci.yml` | Noise | Facts may be true, but no specific vulnerable package or compromised action was shown; generic supply-chain hardening, not a demonstrated defect in this learning image. | Drop for final grade; optional later hardening note only. |

## Manual security check

I manually confirmed SEC-06: create can set any status because `create_task` never calls `validate_status_transition`. Live check: `POST /tasks` with `{"title":"x","status":"Done"}` returned **201** and `status: "Done"`. The create form also offers Done (`frontend/index.html`). I did not accept a one-line “force ToDo” fix—product rule is still undecided—so this stays on the backlog (`docs/security-review.md`).

## One AI output I rejected or corrected

AI’s first PATCH gating idea treated “`due_date` present in the body” as enough to re-run past-due validation. That broke editing other fields on already-overdue tasks when the UI resubmitted the same past date. I rejected that as-is and tightened the condition to compare against the stored value (`payload.due_date != existing.due_date`). Separately, Mini-ADR-001 rejected AI’s suggestion to **store** an `overdue` flag instead of deriving it.

## Three AI usage rules
1. Never paste: real customer data, production logs, credentials, tokens, or third-party personal information into AI prompts or the repo.
2. Always verify: review the diff against the requirement/ADR, run tests (or a live check), and only keep changes whose path I can explain; if the product rule is unclear, backlog instead of shipping a one-liner.
3. Record AI contributions by: item, module, whether I understand it line by line, and action (keep / follow-up / backlog / course-scope limit / drop as noise)—as in the governance worksheet and security grade tables.

## Ownership statement

I am comfortable submitting this repo as my work because every decisions is reviewed and accepted, not pasted and left unverified. AI drafted models, tests, frontend, CI, and Docker, but I ran the py tests and the manuel tests myself, i reviewed every chunck of code before submitting. I graded Module 5 findings with file evidence instead of accepting every AI severity. I backlog items that I am not fully sure of (XSS escaping, create-status policy) rather than pretend they are fixed. The final evidence files document what I verified, what I rejected, and what remains out of scope for this learning app.

