from jarvis_v6.tools.registry import ToolRegistry
from jarvis_v6.tools.results import ToolResult

class ToolExecutor:

    def __init__(self,logger, registry: ToolRegistry, event_bus):
        self.registry = registry
        self.logger = logger
        self.event_bus = event_bus

    def execute(self, name:str, **kwargs) -> ToolResult:


        try:
            tool = self.registry.resolve(name)

        except Exception as e:

            self.logger.error(
                f"Tool resolution failed: {name} - {e}"
            )

            return ToolResult(
                success=False,
                error=str(e),
            )
        

        self.event_bus.publish(
            "tool.execution.started",
            {
                "tool": name
            }
        )
        try:

            result = tool.execute(**kwargs)

            self.event_bus.publish(
                "tool.execution.completed",
                {
                    "tool": name,
                    "success": True
                }
            )

            self.logger.info(f"Tool executed: {name}")

            return ToolResult(
                success=True,
                output=result,
            )

        except Exception as e:

            self.event_bus.publish(
                "tool.execution.failed",
                {
                    "tool": name,
                    "error": str(e)
                }
            )

            self.logger.error(
                f"Tool execution failed: {name} - {e}"
            )
            return ToolResult(
                success=False,
                error=str(e),
            )