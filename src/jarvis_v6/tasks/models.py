from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    objective: str

    owner_id: str = "user"
    worker_type: str | None = None
    parent_task_id: str | None = None

    task_id: str = field(
        default_factory=lambda: f"task_{uuid4().hex}"
    )

    status: TaskStatus = TaskStatus.PENDING

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    started_at: datetime | None = None
    completed_at: datetime | None = None

    progress: float | None = None
    progress_message: str | None = None

    result: Any = None
    error: str | None = None

    def start(self) -> None:
        if self.status != TaskStatus.PENDING:
            raise ValueError(
                f"Task '{self.task_id}' cannot start "
                f"from state '{self.status.value}'."
            )

        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now(timezone.utc)

    def update_progress(
        self,
        progress: float | None = None,
        message: str | None = None,
    ) -> None:
        if self.status != TaskStatus.RUNNING:
            raise ValueError(
                f"Task '{self.task_id}' cannot update progress "
                f"from state '{self.status.value}'."
            )

        if progress is not None and not 0 <= progress <= 100:
            raise ValueError("Progress must be between 0 and 100.")

        self.progress = progress
        self.progress_message = message

    def complete(self, result: Any = None) -> None:
        if self.status != TaskStatus.RUNNING:
            raise ValueError(
                f"Task '{self.task_id}' cannot complete "
                f"from state '{self.status.value}'."
            )

        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        self.progress = 100
        self.result = result

    def fail(self, error: str) -> None:
        if self.status != TaskStatus.RUNNING:
            raise ValueError(
                f"Task '{self.task_id}' cannot fail "
                f"from state '{self.status.value}'."
            )

        if not isinstance(error, str) or not error.strip():
            raise ValueError(
                "Task failure reason cannot be empty."
            )

        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now(timezone.utc)
        self.error = error

    def cancel(self) -> None:
        if self.status not in {
            TaskStatus.PENDING,
            TaskStatus.RUNNING,
        }:
            raise ValueError(
                f"Task '{self.task_id}' cannot be cancelled "
                f"from state '{self.status.value}'."
            )

        self.status = TaskStatus.CANCELLED
        self.completed_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "objective": self.objective,
            "owner_id": self.owner_id,
            "worker_type": self.worker_type,
            "parent_task_id": self.parent_task_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": (
                self.started_at.isoformat()
                if self.started_at
                else None
            ),
            "completed_at": (
                self.completed_at.isoformat()
                if self.completed_at
                else None
            ),
            "progress": self.progress,
            "progress_message": self.progress_message,
            "result": self.result,
            "error": self.error,
        }