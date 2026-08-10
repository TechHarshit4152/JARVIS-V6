from threading import RLock
from typing import Any

from jarvis_v6.tasks.models import Task


class TaskManager:

    def __init__(self, logger, event_bus):
        self.logger = logger
        self.event_bus = event_bus

        self._tasks: dict[str, Task] = {}
        self._lock = RLock()

    def create(
        self,
        objective: str,
        owner_id: str = "user",
        worker_type: str | None = None,
        parent_task_id: str | None = None,
    ) -> Task:

        if not objective.strip():
            raise ValueError("Task objective cannot be empty.")

        task = Task(
            objective=objective,
            owner_id=owner_id,
            worker_type=worker_type,
            parent_task_id=parent_task_id,
        )

        with self._lock:
            self._tasks[task.task_id] = task

        self.logger.info(
            f"Task created: {task.task_id} - {task.objective}"
        )

        self.event_bus.publish(
            "task.created",
            task.to_dict(),
        )

        return task

    def get(self, task_id: str) -> Task:
        with self._lock:
            try:
                return self._tasks[task_id]
            except KeyError:
                raise ValueError(
                    f"Task '{task_id}' was not found."
                )

    def list(self) -> list[Task]:
        with self._lock:
            return list(self._tasks.values())

    def start(self, task_id: str) -> Task:
        task = self.get(task_id)

        with self._lock:
            task.start()

        self.logger.info(
            f"Task started: {task.task_id}"
        )

        self.event_bus.publish(
            "task.started",
            task.to_dict(),
        )

        return task

    def update_progress(
        self,
        task_id: str,
        progress: float | None = None,
        message: str | None = None,
    ) -> Task:

        task = self.get(task_id)

        with self._lock:
            task.update_progress(
                progress=progress,
                message=message,
            )

        self.event_bus.publish(
            "task.progress",
            task.to_dict(),
        )

        return task

    def complete(
        self,
        task_id: str,
        result: Any = None,
    ) -> Task:

        task = self.get(task_id)

        with self._lock:
            task.complete(result)

        self.logger.info(
            f"Task completed: {task.task_id}"
        )

        self.event_bus.publish(
            "task.completed",
            task.to_dict(),
        )

        return task

    def fail(
        self,
        task_id: str,
        error: str,
    ) -> Task:

        task = self.get(task_id)

        with self._lock:
            task.fail(error)

        self.logger.error(
            f"Task failed: {task.task_id} - {error}"
        )

        self.event_bus.publish(
            "task.failed",
            task.to_dict(),
        )

        return task

    def cancel(self, task_id: str) -> Task:
        task = self.get(task_id)

        with self._lock:
            task.cancel()

        self.logger.info(
            f"Task cancelled: {task.task_id}"
        )

        self.event_bus.publish(
            "task.cancelled",
            task.to_dict(),
        )

        return task