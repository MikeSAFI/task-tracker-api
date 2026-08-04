# Governance Retrospective - AI-Assisted Coding

## What I Shared With AI

| Item | Module | Risk Level | Reason |
|---|---|---|---|
| Task Tracker code | 2-5 | Low | Learning project with in-memory sample tasks only—no auth secrets, API keys, or real user data. Still shared course IP, so I kept prompts scoped and reviewed diffs before accepting. |
| Test output and stack traces | 2-4 | Low | Failures helped AI fix bugs faster. Paths and local env details can leak in traces, but nothing sensitive appeared in this repo’s test runs. |
| Frontend code | 3 | Low | Static HTML/JS with no credentials. Main risk is AI suggesting unsafe DOM patterns (e.g. unescaped `innerHTML`), which I later flagged in Module 5. |
| Dockerfile and CI YAML | 4 | Low | Standard packaging and `pytest` workflow; no secrets or deploy credentials in the files shared. Binding `0.0.0.0` and unpinned images are config hygiene, not secret exposure. |
| Any real external data I used by mistake | N/A | None | I did not paste real customer data, production logs, credentials, or third-party PII into prompts. |

## What I Received From AI

| Generated Thing | Module | Do I Understand It Line by Line? | Action |
|---|---|---|---|
| Backend models and validators | 2 | yes | Keep. I own the Pydantic fields and tag/title validators; I rewrote vague requirements and rejected ADR alternatives before locking the design. |
| Frontend board and drag-and-drop logic | 3 | Partially | Keep with follow-up. I can explain the board flow, but I do not yet fully own every `innerHTML` path—SEC-01/SEC-07 stay on the security backlog until escaping is implemented. |
| CI workflow | 4 | Yes | Keep. Simple install + `pytest` pipeline; I verified it matches how I run tests locally. |
| Dockerfile | 4 |  yes | Keep. Multi-stage build, non-root user, and `.dockerignore` are documented in my Module 4 technical note; I treat the image as local packaging, not production deploy. |
| Security findings and plans | 5 | Yes| Backlog high-impact items (XSS escaping, create-status policy); accept course-scope limits (no auth); drop noise (SEC-05). Do not ship one-line “fixes” until product rules are clear. |
