# Module 4 review log

**Diff reviewed:** `mid-course-project...main` (+ unstaged `Dockerfile` notes)  
**Reviewer:** Auto  
**Date:** 2026-07-27

| # | Location | Severity | Category | Issue | Verdict | Notes |
|---|----------|----------|----------|-------|---------|-------|
| 1 | `README.md` §9 (~243–245) | medium | docs | README implies CORS for `127.0.0.1:5173`; code only allows `localhost:5173` for that port. | Useful | The README should accurately reflect the configured CORS origins. If 127.0.0.1:5173 isn't allowed, the documentation is misleading. |
| 2 | `README.md` overview / §9 (~19–20, 230–231) | medium | docs | Status transition graph is stated as a global rule; it is enforced only on PATCH, not on create. | Useful | If the status transition rule is enforced only during updates (PATCH) and not on task creation, the documentation overstates the behaviour. |
| 3 | `docs/prompts.md` (~85–86) | medium | docs | ADR prompt placeholder corrupted to `the user stories >>>`. | Useful | A corrupted placeholder in a prompt is a documentation quality issue that should be fixed. |
| 4 | `docs/prompts.md` (file-level) | medium | scope | ~1.6k lines of earlier course prompts removed while README still lists the file as a deliverable. | Noise | If the earlier course prompts were intentionally removed and the remaining prompts satisfy the assignment requirements, this is not a defect. It only matters if the README explicitly promises the removed content. |
| 5 | `README.md` §9 (~220–223) | low | docs | Claims handlers have “no business logic”; PATCH still gates due-date re-validation. | Useful | The PATCH handler still contains business-rule validation, so saying handlers have "no business logic" is not strictly accurate. |
| 6 | `app/main.py` GET/PATCH/DELETE docstrings | low | docs | Docstrings claim 404; OpenAPI/`/docs` omit 404 without explicit `responses`. | Useful | The API documentation should match the actual responses. If the endpoint can return 404 but OpenAPI doesn't document it, that's a valid documentation improvement. |
| 7 | `app/storage.py` `update_task` docstring | low | docs | `[VERIFY]` left after `claim-vs-reality.md` already confirmed the behavior. | Noise | Leaving a [VERIFY] comment in a docstring is a minor cleanup item rather than a functional or documentation defect. |

**Quick mark sheet:**

```
1: Useful
2: Useful
3: Useful
4: Noise
5: Useful
6: Useful
7: Noise
```

---

## Triage summary

| Comment summary | Bucket | Evidence needed or evidence found | Action |
|---|---|---|---|
| README CORS implies `127.0.0.1:5173` | **Useful** | Found: README §9 groups `localhost`/`127.0.0.1` on `5500`/`5501`/`5173`; `app/main.py` has `localhost:5173` only (no `127.0.0.1:5173`). | Fix README to list the six origins, or add the missing origin if intended. |
| Status transitions stated as global rule | **Useful** | Found: README overview/§9 state the graph without PATCH-only scope; `create_task` never calls `validate_status_transition`. | Scope the README claim to PATCH; note create may set any `TaskStatus`. |
| `prompts.md` placeholder corrupted | **Useful** | Found: lines 85–86 are `<<<` / `the user stories >>>` (broken placeholder). | Restore a clear `<<<` … `>>>` placeholder (or paste real stories). |
| Large prompt history deleted vs deliverable listing | **Noise** | Found: README lists `docs/prompts.md` as a curriculum artifact; it does not promise the deleted Module 2/3 prompt bodies. | None |
| “No business logic” in handlers | **Useful** | Found: README §9 says handlers have no business logic; `update_task` still gates due-date re-validation before calling storage. | Soften README wording (handlers orchestrate; rules live in `business_rules.py`). |
| Docstrings claim 404; OpenAPI omits it | **Useful** | Found: GET/PATCH/DELETE docstrings claim 404; routes lack `responses={404:...}`; `claim-vs-reality.md` already records OpenAPI missing 404. | Add explicit 404 responses on those routes, or note that raised `HTTPException`s aren’t auto-documented. |
| Leftover `[VERIFY]` in `storage.update_task` | **Noise** | Found: docstring still has `[VERIFY]`; `claim-vs-reality.md` already confirmed null-clearing — cleanup only, not a defect. | None |
