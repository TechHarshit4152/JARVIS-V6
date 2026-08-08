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


kernel.boot()
logger = kernel.container.resolve("logger")

registry = kernel.container.resolve("tools")
tool = TestTool()

registry.register(tool)
registry.register(FailingTool())

executor = ToolExecutor(registry=registry, logger=logger)

result1 = executor.execute("test.tool")



result2 = executor.execute("failing.tool")

print(result2)

assert result2.success is False
assert result2.error == "Something went wrong"

result = executor.execute("does.not.exist")

print(result)

assert result.success is False
assert result.error == "Tool not registered: does.not.exist"

