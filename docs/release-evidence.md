# Release Evidence

## Baseline
- Branch: `final-project`
- Date: 2026-08-04
- Local app run command: `.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000` (use the Python 3.13 `venv`, not `.venv` / Python 3.14)
- /health result: `{"status":"ok","timestamp":"2026-08-04T16:11:58.762224+00:00"}` (HTTP 200 from running container on port 8000)
- Frontend check: `GET /` returned HTTP 200 from the Docker image (`task-tracker-api` serving `frontend/index.html`)
- Test command: `.\venv\Scripts\python.exe -m pytest -q` (also `.\venv\Scripts\python.exe -m pytest tests/test_tasks.py -q`)
- Test result: **47 passed** in 0.56s

## CI evidence
- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: Actions at https://github.com/MikeSAFI/task-tracker-api/actions (`gh` CLI not installed locally; workflow runs on `push` / `pull_request`)
- Test command used by CI: `pytest -v` (after `pip install -r requirements.txt` on Python 3.11)
- Shortcut check: no continue-on-error / no || true / pytest is not skipped. Confirmed — workflow has a single hard-fail `Run tests` step with `pytest -v` only.

## Docker evidence
- Build command: `docker build -t task-tracker-api .`
- Run command: `docker run --rm -p 8000:8000 task-tracker-api`
- /health check: `Invoke-RestMethod http://localhost:8000/health` → `{"status":"ok","timestamp":"..."}` (also verified on a second container at port 8001)
- Non-root check, if implemented: `docker exec <container> whoami` → `app`; `id` → `uid=999(app) gid=999(app)` (matches `USER app` in Dockerfile)
- No-baked-secrets check: `.dockerignore` excludes `.env`, `.env.example`, `venv/`, `.venv/`, `tests/`, `docs/`; Dockerfile copies only `requirements.txt`, `app/`, and `frontend/` — no secrets copied into the image

## Documentation claim-vs-reality log
| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `pytest` runs from PATH on Windows | Ran `pytest tests/test_tasks.py -q` in PowerShell | Fail — `pytest` not recognized | Use `.\venv\Scripts\python.exe -m pytest -q` (or activate `venv`) |
| Project `.venv` is usable for tests | `.\.venv\Scripts\python.exe -m pytest` | Fail — Python 3.14; `ModuleNotFoundError: pydantic_core._pydantic_core`; force-reinstall also failed (no wheel / no MSVC linker) | Use Python 3.13 `venv` instead of `.venv` |
| `requirements.txt` is missing a package | Compared imports vs pinned deps; Docker/local install of `pydantic` pulls `pydantic-core` | Pass — nothing required missing; duplicate `pytest`/`httpx` lines were cleaned earlier | None required for release |
| Docker Desktop must be running to build | `docker build -t task-tracker-api .` | Fail initially — daemon pipe `dockerDesktopLinuxEngine` missing | Started Docker Desktop; rebuild succeeded |
| Docker build installs deps cleanly | First build log: `No matching distribution found for pydantic-core==2.27.1 (from versions: none)` | Transient PyPI miss; rebuild succeeded (`Successfully installed ... pydantic-core-2.27.1`) | Retry `docker build -t task-tracker-api .` |
| Image serves API + frontend non-root | `docker run` + `/health` + `GET /` + `whoami`/`id` | Pass — health ok, frontend 200, process user `app` | None |
