# Personal AI Usage Rules

| Rule category | Revised rule |
|---|---|
| What I will never paste | I will never paste real customer data, production logs, credentials, or third-party PII into an AI prompt. |
| What I will always verify before accepting | Before I accept an AI-generated change, I will review its diff against the current requirement and decide whether I understand the changed code path; if the product rule is unclear or I do not own the path, I will keep it for follow-up or backlog it instead of shipping a one-line fix. |
| How I will record AI contributions | For each AI-generated contribution I keep or defer, I will record the generated item, course module, whether I understand it line by line, and its action: keep, follow-up, backlog, accept as a course-scope limit, or drop as noise. |

## Rule Scenario Checks

| Revised rule | Future scenario based on my notes | Clear yes/no decision? | Result |
|---|---|---|---|
| Never paste real customer data, production logs, credentials, or third-party PII. | An AI prompt would include a production log containing real customer data. | Yes | No — do not paste it. |
| Review the diff against the requirement; if unclear or not owned, defer/backlog it rather than ship a one-line fix. | AI proposes a one-line create-status change, but the project has not decided whether new tasks must start as `ToDo`. | Yes | No — do not accept it; backlog it until the product rule is confirmed. |
| Record generated item, module, understanding level, and action. | I keep AI-generated frontend board logic but only partially understand its `innerHTML` paths. | Yes | Yes, if recorded as: frontend board logic, Module 3, partially understood, keep with follow-up/security backlog. |
