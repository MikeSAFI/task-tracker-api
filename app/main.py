from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app import storage
from app.business_rules import validate_due_date_not_in_past, validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

app = FastAPI(
    title="Task Tracker API",
    description="A learning-focused Task Tracker REST API built with FastAPI.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://localhost:5501",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


@app.get("/", include_in_schema=False)
def serve_frontend() -> FileResponse:
    """Serve the static Task Tracker frontend.

    Returns the pre-built ``frontend/index.html`` file so that navigating to
    the API root in a browser loads the task board UI directly.

    Returns:
        FileResponse: The frontend's ``index.html`` file.
    """
    frontend_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
    return FileResponse(frontend_path)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Report service liveness.

    Returns:
        dict: A payload with ``status`` set to ``"ok"`` and ``timestamp``
        set to the current UTC time in ISO 8601 format.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
    tag: str | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status, priority, overdue state, and/or tag.

    Filters are combinable; when more than one is supplied, tasks must match
    all of them (logical AND).

    Args:
        status: Only return tasks with this status.
        priority: Only return tasks with this priority.
        overdue: Only return tasks whose derived overdue state matches this value.
        tag: Only return tasks that contain this exact tag.

    Returns:
        list[TaskResponse]: The matching tasks, each with ``overdue`` freshly
        computed relative to today's date.

    Example:
        GET /tasks?status=ToDo&priority=High&tag=backend
    """
    return storage.get_all_tasks(
        status=status,
        priority=priority,
        overdue=overdue,
        tag=tag,
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by id.

    Args:
        task_id: The id of the task to fetch.

    Returns:
        TaskResponse: The requested task.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        GET /tasks/{task_id}
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: The task fields to create. Field-level validation (title,
            tags) is enforced by ``TaskCreate`` before this handler runs.

    Returns:
        TaskResponse: The newly created task, with ``overdue`` computed.

    Raises:
        HTTPException: 422 if ``due_date`` is set and earlier than today.

    Example:
        POST /tasks
        {"title": "Write docs", "priority": "High"}
    """
    validate_due_date_not_in_past(payload.due_date)
    return storage.add_task(payload)


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task.

    Only fields explicitly present in the request body are applied; omitted
    fields are left unchanged. ``due_date`` is only re-validated against
    today's date when it is present in the request AND differs from the
    task's current ``due_date`` — patching other fields on a task that
    already has a past due date is allowed. ``status`` changes are checked
    against the allowed transition graph in
    ``business_rules.VALID_TRANSITIONS``.

    Args:
        task_id: The id of the task to update.
        payload: The partial set of fields to update.

    Returns:
        TaskResponse: The updated task.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.
        HTTPException: 422 if the new ``due_date`` is earlier than today, or
            if ``status`` is not a valid transition from the current status.

    Example:
        PATCH /tasks/{task_id}
        {"status": "InProgress"}
    """
    due_date_in_request = "due_date" in payload.model_fields_set
    needs_existing = due_date_in_request or payload.status is not None

    existing = storage.get_task_by_id(task_id) if needs_existing else None
    if needs_existing and existing is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    # Only validate when due_date is present and actually changing.
    # Unchanged past due dates must not block other field updates.
    if due_date_in_request and payload.due_date != existing.due_date:
        validate_due_date_not_in_past(payload.due_date)

    if payload.status is not None:
        validate_status_transition(existing.status, payload.status)

    updated = storage.update_task(task_id, payload)
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task.

    Args:
        task_id: The id of the task to delete.

    Returns:
        None: Responds with 204 No Content on success.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        DELETE /tasks/{task_id}
    """
    if storage.delete_task(task_id):
        return
    raise HTTPException(
        status_code=404,
        detail=f"Task with id {task_id} not found",
    )
