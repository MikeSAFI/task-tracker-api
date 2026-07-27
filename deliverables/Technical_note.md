# Technical Decision Note — Module 4 Task Tracker

**Topic:** Dockerfile design  
**Scope:** `Dockerfile`, `.dockerignore`, and how these choices support the learning-focused Task Tracker API described in `README.md`  
**Status:** Accepted

---

## 1. Context

The Task Tracker API is a learning project built with FastAPI and Pydantic. The application uses in-memory storage, does not include authentication or a database, and is not intended to be deployed as a production system.

Module 4 introduces Docker support so the application can be built and run locally inside a container using the same project structure. The API provides JSON endpoints and also serves the static frontend through the application.

The runtime requirements are simple:

- Python dependencies from `requirements.txt`
- The backend application code under `app/`
- The frontend files required by the application

Development files such as tests, documentation, environment files, and course-related artifacts are not required when running the application, so they are excluded from the Docker image using `.dockerignore`.

The Docker setup uses a multi-stage Dockerfile based on Python 3.11. The final image contains only the required runtime dependencies and application files. The container runs the application using Uvicorn without development options such as `--reload`.

---

## 2. Decision

I decided to use a multi-stage Dockerfile to separate dependency installation from the final runtime image.

The Docker build process:

- Uses a builder stage to install Python dependencies.
- Creates a smaller runtime image containing only the installed dependencies, backend code, and frontend files.
- Runs the application using:  
  `uvicorn app.main:app --host 0.0.0.0 --port 8000`

I also chose to run the container using a dedicated non-root user (`app`). This was not required by the project rubric, but I selected it as a good practice because the application does not require administrator permissions.

The `.dockerignore` file excludes files that are not needed inside the runtime image, including:

- tests
- documentation
- deliverables
- environment files
- GitHub configuration files
- Python caches
- virtual environments

The Docker image is treated as a local execution option for the project, not as a production deployment configuration.

---

## 3. Alternatives Considered

| Alternative | Why it was not chosen |
|---|---|
| Single-stage Docker image | A single-stage image would be simpler, but the final image would contain build-related layers and would provide less separation between building and running the application. |
| Copy the entire repository into the image | This could include unnecessary files such as tests, documentation, and potentially sensitive files like environment configurations. Keeping only runtime files makes the image cleaner. |
| Running the container as root | This is common in simple tutorials, but I preferred using a dedicated `app` user as a safer default practice. |
| Running Uvicorn with `--reload` | This is useful during development, but the Docker container is intended to represent a stable application run rather than a development environment. |
| Adding Docker build steps to CI | This could provide additional validation, but it was outside the current project workflow scope, so I kept CI unchanged. |

---

## 4. Trade-offs

In practice I develop with a local venv and `uvicorn --reload`. Docker is for verifying that the packaged image builds and serves the API + frontend on port 8000 — not for day-to-day editing.

The main trade-offs are:

**Smaller runtime image vs Dockerfile complexity**  
Multi-stage builds are slightly harder to read than a one-file tutorial Dockerfile, but they keep dependency install separate from the runtime copy of `app/` and `frontend/`, which matches how I actually use the image (rebuild when packaging changes, not on every code tweak).

**Non-root user vs convenience**  
Running as `app` was my choice (not a rubric requirement). It is better default hygiene for a container demo; I do not need root inside the container because the app only holds tasks in memory.

**Strict `.dockerignore` vs including everything**  
Excluding tests, docs, and deliverables keeps the image to runtime files only. That means I cannot run `pytest` inside this image — tests stay on the host / in CI, which is how I already run them.

**Python 3.11 in Docker/CI vs Python 3.13 locally**  
The image pins 3.11 to match CI. My local environment uses 3.13. I have not done a side-by-side compatibility check between those two versions for this project.

**No `--reload` vs development convenience**  
Omitting `--reload` keeps the container as a stable run path. Automatic refresh stays in the local venv workflow; changing app code for Docker always means a rebuild.

I chose to keep Docker focused on running the packaged application rather than turning it into a second development environment.

---

## 5. Consequences

The Docker setup provides a consistent way to run the application locally:

```bash
docker build -t task-tracker-api .
docker run --rm -p 8000:8000 task-tracker-api
```

The application can then be accessed through the same port used when running it directly with Uvicorn.

Other consequences:

- Changes to application files require rebuilding the Docker image.
- The Docker image does not include project documentation, tests, or development-only files because they are excluded through `.dockerignore`.
- CI still only runs `pytest`; a broken Dockerfile can merge while tests stay green.
- Docker does not add persistence because the application still uses in-memory storage. Restarting the container will reset all tasks.
- The Docker setup does not introduce authentication, database support, or production-level configuration.

---


