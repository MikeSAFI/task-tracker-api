# Architecture-Document Context Strategy Comparison

## Strategy comparison

| Strategy | What it got right | What it got wrong, missed, or invented | Best suited for |
|---|---|---|---|
| A — minimal context | Produced the broadest description: task fields, validation split, transition sequence, frontend behavior, tests, ADRs, and limitations. It clearly explained the create-task flow. | It makes several highly specific claims without marking them as uncertain, including UUID and UTC timestamp generation, CORS setup, frontend reload/error behavior, and the frontend being the intended primary client. It also omits filtering behavior. | A quick, readable overview when a broad first draft matters more than strict evidence boundaries. |
| B — structured context | Best captures the project’s architectural boundaries: model validation versus stateful rules, thin route handlers, in-memory storage, derived overdue state, partial updates, and combined filtering. It also distinguishes confirmed information from unavailable details. | It is less concrete than A and C about the full task shape: it does not name the priority values or list fields such as description, assignee, timestamps, and ID behavior. Its “important fields” section is therefore incomplete as a data-model description. | A repository architecture document that needs reliable coverage across implementation, tests, conventions, and supporting documentation. |
| C — targeted anchor files | Gives a concise implementation-oriented account of the API, model, create flow, storage behavior, and core error conventions. It also explicitly labels several boundaries of what was not inspected. | It narrows the visible system too aggressively: it omits tests, ADRs, filtering behavior, and the detailed transition rules described elsewhere. It says the business-rule implementation and frontend behavior are not visible, while A and B provide specific descriptions of both. It also includes uncorroborated details such as a `/health` endpoint, local CORS origins, and empty-update timestamp behavior. | Focused work on a small set of implementation files, such as documenting a single request path or reviewing a localized change. |

## Verdict

I chose Strategy B for the final architecture document because it provides the strongest balance of coverage and restraint. Unlike A, it avoids presenting every implementation detail as certain, and unlike C, it includes the architectural context needed to explain how validation, routes, storage, filtering, tests, and ADRs fit together.

## Context-engineering rule

For the Task Tracker architecture-document task, I use structured context with `AGENTS.md` and file summaries because it covers the API, models, business rules, storage, tests, frontend, and ADRs while retaining clear uncertainty where details are unavailable.

For a bounded course implementation task such as “Due Date Not In Past — business rule + wire into create/update” or “Models + storage + API for tags,” I use targeted anchor files because they keep the context on the named files and request path without pulling in unrelated repository detail.
