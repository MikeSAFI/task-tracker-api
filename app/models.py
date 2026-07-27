from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _validate_title(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("Title is required and cannot be blank")
    if len(stripped) > 200:
        raise ValueError("Title must be at most 200 characters")
    return stripped


def _validate_tag(value: str) -> str:
    if not value or not value.strip():
        raise ValueError("Tag cannot be empty or contain only whitespace")
    if len(value) > 255:
        raise ValueError("Tag must be at most 255 characters")
    if not all(
        ("A" <= char <= "Z") or ("a" <= char <= "z") or ("0" <= char <= "9")
        for char in value
    ):
        raise ValueError("Tag can contain only letters (A-Z, a-z) and numbers (0-9)")
    return value


def _validate_tags(value: Optional[list[str]]) -> Optional[list[str]]:
    if value is None:
        return value
    return [_validate_tag(tag) for tag in value]


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Validate and normalize a task title for creation.

        Delegates to ``_validate_title``.

        Args:
            value: The raw title string.

        Returns:
            str: The stripped title.

        Raises:
            ValueError: If the title is blank after stripping, or exceeds
                200 characters.
        """
        return _validate_title(value)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: Optional[list[str]]) -> Optional[list[str]]:
        """Validate every tag in the list for creation.

        Delegates to ``_validate_tags``/``_validate_tag`` for each entry.

        Args:
            value: The raw tag list, or ``None``.

        Returns:
            Optional[list[str]]: The unchanged tag list, or ``None``.

        Raises:
            ValueError: If any tag is empty/whitespace-only, exceeds 255
                characters, or contains non-alphanumeric characters.
        """
        return _validate_tags(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        """Validate and normalize a task title if one was provided.

        Args:
            value: The raw title string, or ``None`` if title is not being
                updated.

        Returns:
            Optional[str]: The stripped title, or ``None``.

        Raises:
            ValueError: If a non-``None`` title is blank after stripping, or
                exceeds 200 characters.
        """
        if value is None:
            return value
        return _validate_title(value)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: Optional[list[str]]) -> Optional[list[str]]:
        """Validate every tag in the list if any were provided.

        Delegates to ``_validate_tags``/``_validate_tag`` for each entry.

        Args:
            value: The raw tag list, or ``None``.

        Returns:
            Optional[list[str]]: The unchanged tag list, or ``None``.

        Raises:
            ValueError: If any tag is empty/whitespace-only, exceeds 255
                characters, or contains non-alphanumeric characters.
        """
        return _validate_tags(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date] = None
    overdue: bool
    tags: list[str] = []
    created_at: datetime
    updated_at: datetime
