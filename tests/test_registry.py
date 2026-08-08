from jarvis_v6.tools.base import Tool
from jarvis_v6.tools.registry import ToolRegistry
from jarvis_v6.core.kernel import kernel

kernel.boot()
logger = kernel.container.resolve("logger")

class TestTool(Tool):
    name = "test.tool"
    description = "A test tool"
    parameters = {}

    def execute(self, **kwargs):
        return "Tool executed successfully"


registry = ToolRegistry(logger)

tool = TestTool()

registry.register(tool)

resolved_tool = registry.resolve("test.tool")

print(resolved_tool)
print(resolved_tool.name)


tools = registry.list_tools()

print(tools)

assert len(tools) == 1
assert tools[0] is tool

registry.unregister("test.tool")

assert registry.has("test.tool") is False
assert registry.list_tools() == []

print(registry._tools)

tools = kernel.container.resolve("tools")

logger.info(f"Tool registry resolved: {tools}")

assert kernel.tools is tools