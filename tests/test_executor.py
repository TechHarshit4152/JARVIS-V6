from jarvis_v6.core.kernel import kernel
from jarvis_v6.tools.base import Tool
from jarvis_v6.tools.executor import ToolExecutor


class TestTool(Tool):
    name = "test.tool"
    description = "A test tool"
    parameters = {}

    def execute(self, **kwargs):
        return "Tool executed successfully"

class FailingTool(Tool):
    name = "failing.tool"
    description = "A tool that fails."
    parameters = {}

    def execute(self, **kwargs):
        raise RuntimeError("Something went wrong")

events=[]

kernel.boot()
logger = kernel.container.resolve("logger")
event_bus = kernel.container.resolve("event_bus")

registry = kernel.container.resolve("tools")
tool = TestTool()

registry.register(tool)
registry.register(FailingTool())

executor = ToolExecutor(registry=registry, logger=logger, event_bus=event_bus)

event_bus.subscribe(
    "tool.execution.started",
    lambda payload: events.append(
        ("started", payload)
    )
)

event_bus.subscribe(
    "tool.execution.completed",
    lambda payload: events.append(
        ("completed", payload)
    )
)

event_bus.subscribe(
    "tool.execution.failed",
    lambda payload: events.append(
        ("failed", payload)
    )
)


result1 = executor.execute("test.tool")



result2 = executor.execute("failing.tool")

print(result2)

assert result2.success is False
assert result2.error == "Something went wrong"

result = executor.execute("does.not.exist")

print(result)

assert result.success is False
assert result.error == "Tool not registered: does.not.exist"

assert events == [
    ("started", {"tool": "test.tool"}),
    ("completed", {"tool": "test.tool", "success": True}),
    ("started", {"tool": "failing.tool"}),
    ("failed", {
        "tool": "failing.tool",
        "error": "Something went wrong"
    }),
]

assert not any(
    event[1]["tool"] == "does.not.exist"
    for event in events
)

