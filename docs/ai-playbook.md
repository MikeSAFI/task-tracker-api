# Personal AI Coding Playbook

## 1. When I reach for AI first

- Drafting user stories, Mini ADRs, and strong constrained prompts before I touch code (ChatGPT helped me get acceptance criteria and prompt structure ready for Cursor Agent).
- Project template that must stay consistent with the existing FastAPI style adding fields, wiring query params, fixtures, and named pytest cases once the ADR and stories are done (due dates/tags: expand suite without rewriting the 19 tests baseline ended at 47).
- Planning a feature against this repo (repo grounded plans, structured architecture context with AGENTS.md) and grading security findings so I can decide keep backlog noise instead of guessing.

## 2. When I do not reach for AI

- Final product calls: what valid means: no past due dates, tags alphanumeric ≤ 255, rejecting ADR alternatives like storing an overdue flag or adding a separate Tag entity.
- Bugs that need me to own the path ex: PATCH still validating an unchanged past due date when the edit form resubmitted it, I tightened that myself after AI first approach.
- Making a fix when the product rule is unclear ex: SEC-06 create-status / ToDo only. I backlog it instead of accepting a one line change I do not stand behind.

## 3. My non-negotiables

- I never paste real customer data, production logs, credentials, or third party personal information into an AI prompt (governance: I shared only this learning Task Tracker / tests / Dockerfile no real customer data or secrets).
- Narrow prompts with hard file/scope limits, run pytest right after AI edits, treat output as a draft until stories, ADRs, and failing/passing tests agree (weak fix business rules vs strong due date prompt, past due rule 4 overdue tests failed until storage seeding).
- Before I accept a change, I review the diff against the current requirement and decide whether I understand the changed path and if not, follow up or backlog, not ship (governance: reviewed diffs before accepting, SEC-06 create-status left on backlog).

## 4. My review rules

- Check AI output against acceptance criteria and Mini ADRs, reject scope drift and out of scope extras (rejected global tag admin, Mini ADR overdue flag / Tag entity, no API redesign in frontend prompts).
- Prefer evidence: green suite, break test recovery, and live checks for security grades not AI said so (intentional validator 2 tests failed, SEC-06/SEC-07/SEC-09 confirmed with live POST/GET checks).
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
- My one rule is: AI output is a draft until the requirement, the ADR, and the tests agree and I understand the path I am shipping.
- I will re-read this playbook in 30 days, keep the rules that still match how I work, and update the parts I have learned more about.
