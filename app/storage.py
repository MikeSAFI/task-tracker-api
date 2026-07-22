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
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return _with_overdue(task)


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if overdue is not None:
        tasks = [task for task in tasks if _is_overdue(task) == overdue]
    return [_with_overdue(task) for task in tasks]


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None
    return _with_overdue(task)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
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
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()
