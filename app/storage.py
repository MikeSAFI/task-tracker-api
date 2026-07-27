from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def _is_overdue(task: TaskResponse) -> bool:
    if task.due_date is None:
        return False
    return task.due_date < date.today()


def _with_overdue(task: TaskResponse) -> TaskResponse:
    return task.model_copy(update={"overdue": _is_overdue(task)})


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task.

    Generates a new UUID id and sets ``created_at``/``updated_at`` to the
    current UTC time.

    Args:
        payload: The validated task-creation data.

    Returns:
        TaskResponse: The stored task, with ``overdue`` computed relative to
        today's date.
    """
    now = datetime.now(timezone.utc)
    task_id = str(uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        overdue=False,
        tags=payload.tags or [],
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return _with_overdue(task)


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    """List stored tasks, optionally filtered.

    Filters are applied cumulatively (logical AND) when more than one is
    given.

    Args:
        status: Only include tasks with this status.
        priority: Only include tasks with this priority.
        overdue: Only include tasks whose derived overdue state (due date
            earlier than today) matches this value.
        tag: Only include tasks that contain this exact tag.

    Returns:
        list[TaskResponse]: The matching tasks, each with ``overdue``
        freshly computed.
    """
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if overdue is not None:
        tasks = [task for task in tasks if _is_overdue(task) == overdue]
    if tag is not None:
        tasks = [task for task in tasks if tag in task.tags]
    return [_with_overdue(task) for task in tasks]


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Fetch a single task by id.

    Args:
        task_id: The id of the task to fetch.

    Returns:
        Optional[TaskResponse]: The task with ``overdue`` freshly computed,
        or ``None`` if no task with ``task_id`` exists.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None
    return _with_overdue(task)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to a stored task.

    Only fields explicitly set on ``payload`` (per
    ``model_dump(exclude_unset=True)``) are applied; unset fields keep their
    existing value. [VERIFY] Because ``exclude_unset`` only checks whether a
    field was provided in the request (not whether its value differs), an
    explicit ``null`` for an optional field (e.g. ``assignee``) will
    overwrite the existing value with ``None``. If no fields were set, the
    task is returned unchanged and ``updated_at`` is not bumped.

    Args:
        task_id: The id of the task to update.
        payload: The partial set of fields to apply.

    Returns:
        Optional[TaskResponse]: The updated task with ``overdue`` freshly
        computed, or ``None`` if no task with ``task_id`` exists.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return _with_overdue(task)

    now = datetime.now(timezone.utc)
    updated_task = task.model_copy(update={**updates, "updated_at": now, "overdue": False})
    _tasks[task_id] = updated_task
    return _with_overdue(updated_task)


def delete_task(task_id: str) -> bool:
    """Delete a task by id.

    Args:
        task_id: The id of the task to delete.

    Returns:
        bool: ``True`` if a task was deleted, ``False`` if no task with
        ``task_id`` existed.
    """
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()
