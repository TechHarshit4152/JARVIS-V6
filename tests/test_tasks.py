from concurrent.futures import ThreadPoolExecutor

import pytest

from jarvis_v6.core.kernel import kernel
from jarvis_v6.tasks.models import TaskStatus


def setup_module():
    kernel.boot()


def teardown_module():
    kernel.shutdown()


def test_get_returns_created_task():

    tasks = kernel.container.resolve("tasks")

    task = tasks.create("Get test")

    retrieved = tasks.get(task.task_id)

    assert retrieved is task
    assert retrieved.task_id == task.task_id


def test_get_unknown_task_rejected():

    tasks = kernel.container.resolve("tasks")

    with pytest.raises(ValueError):
        tasks.get("task_does_not_exist")


def test_get_same_task_after_lifecycle_changes():

    tasks = kernel.container.resolve("tasks")

    task = tasks.create("Lifecycle retrieval")

    tasks.start(task.task_id)

    retrieved = tasks.get(task.task_id)

    assert retrieved is task
    assert retrieved.status == TaskStatus.RUNNING

    tasks.complete(
        task.task_id,
        result="Done",
    )

    retrieved = tasks.get(task.task_id)

    assert retrieved is task
    assert retrieved.status == TaskStatus.COMPLETED
    assert retrieved.result == "Done"


def test_task_manager_does_not_duplicate_task():

    tasks = kernel.container.resolve("tasks")

    task = tasks.create("Duplicate test")

    first = tasks.get(task.task_id)
    second = tasks.get(task.task_id)

    assert first is second


def test_invalid_start_does_not_emit_started_event():

    tasks = kernel.container.resolve("tasks")
    event_bus = kernel.container.resolve("event_bus")

    events = []

    event_bus.subscribe(
        "task.started",
        lambda payload: events.append(payload),
    )

    task = tasks.create("Invalid start event test")

    tasks.start(task.task_id)

    with pytest.raises(ValueError):
        tasks.start(task.task_id)

    assert len(events) == 1
    assert events[0]["task_id"] == task.task_id


def test_invalid_completion_does_not_emit_completed_event():

    tasks = kernel.container.resolve("tasks")
    event_bus = kernel.container.resolve("event_bus")

    events = []

    event_bus.subscribe(
        "task.completed",
        lambda payload: events.append(payload),
    )

    task = tasks.create("Invalid completion event test")

    with pytest.raises(ValueError):
        tasks.complete(task.task_id)

    assert events == []


def test_progress_event_payload():

    tasks = kernel.container.resolve("tasks")
    event_bus = kernel.container.resolve("event_bus")

    events = []

    event_bus.subscribe(
        "task.progress",
        lambda payload: events.append(payload),
    )

    task = tasks.create("Progress event test")

    tasks.start(task.task_id)

    tasks.update_progress(
        task.task_id,
        progress=60,
        message="Working",
    )

    assert len(events) == 1

    payload = events[0]

    assert payload["task_id"] == task.task_id
    assert payload["progress"] == 60
    assert payload["progress_message"] == "Working"
    assert payload["status"] == "running"


def test_event_order():

    tasks = kernel.container.resolve("tasks")
    event_bus = kernel.container.resolve("event_bus")

    events = []

    for event_name in (
        "task.created",
        "task.started",
        "task.progress",
        "task.completed",
    ):
        event_bus.subscribe(
            event_name,
            lambda payload, name=event_name: events.append(name),
        )

    task = tasks.create("Event order test")

    tasks.start(task.task_id)

    tasks.update_progress(
        task.task_id,
        progress=50,
    )

    tasks.complete(
        task.task_id,
        result="Done",
    )

    assert events == [
        "task.created",
        "task.started",
        "task.progress",
        "task.completed",
    ]


def test_failed_event_payload():

    tasks = kernel.container.resolve("tasks")
    event_bus = kernel.container.resolve("event_bus")

    events = []

    event_bus.subscribe(
        "task.failed",
        lambda payload: events.append(payload),
    )

    task = tasks.create("Failure event test")

    tasks.start(task.task_id)

    tasks.fail(
        task.task_id,
        "Worker failed",
    )

    assert len(events) == 1

    payload = events[0]

    assert payload["task_id"] == task.task_id
    assert payload["status"] == "failed"
    assert payload["error"] == "Worker failed"


def test_cancelled_event_payload():

    tasks = kernel.container.resolve("tasks")
    event_bus = kernel.container.resolve("event_bus")

    events = []

    event_bus.subscribe(
        "task.cancelled",
        lambda payload: events.append(payload),
    )

    task = tasks.create("Cancellation event test")

    tasks.cancel(task.task_id)

    assert len(events) == 1

    payload = events[0]

    assert payload["task_id"] == task.task_id
    assert payload["status"] == "cancelled"


def test_invalid_progress_does_not_emit_event():

    tasks = kernel.container.resolve("tasks")
    event_bus = kernel.container.resolve("event_bus")

    events = []

    event_bus.subscribe(
        "task.progress",
        lambda payload: events.append(payload),
    )

    task = tasks.create("Invalid progress event test")

    tasks.start(task.task_id)

    with pytest.raises(ValueError):
        tasks.update_progress(
            task.task_id,
            progress=101,
        )

    assert events == []


def test_concurrent_get():

    tasks = kernel.container.resolve("tasks")

    task = tasks.create("Concurrent get test")

    def get_task(_):
        return tasks.get(task.task_id)

    with ThreadPoolExecutor(max_workers=10) as executor:
        retrieved = list(
            executor.map(get_task, range(100))
        )

    assert len(retrieved) == 100
    assert all(item is task for item in retrieved)


def test_concurrent_start_same_task():

    tasks = kernel.container.resolve("tasks")

    task = tasks.create("Concurrent start test")

    def start_task(_):
        try:
            tasks.start(task.task_id)
            return True
        except ValueError:
            return False

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(
            executor.map(start_task, range(10))
        )

    assert sum(results) == 1
    assert task.status == TaskStatus.RUNNING


def test_concurrent_complete_same_task():

    tasks = kernel.container.resolve("tasks")

    task = tasks.create("Concurrent completion test")

    tasks.start(task.task_id)

    def complete_task(_):
        try:
            tasks.complete(
                task.task_id,
                result="Done",
            )
            return True
        except ValueError:
            return False

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(
            executor.map(complete_task, range(10))
        )

    assert sum(results) == 1
    assert task.status == TaskStatus.COMPLETED