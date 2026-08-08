from jarvis_v6.tools.registry import ToolRegistry
from jarvis_v6.tools.results import ToolResult

class ToolExecutor:

    def __init__(self,logger, registry: ToolRegistry):
        self.registry = registry
        self.logger = logger

    def execute(self, name:str, **kwargs) -> ToolResult:


        try:
            tool = self.registry.resolve(name)
            result = tool.execute(**kwargs)

            self.logger.info(f"Tool executed: {name}")

            return ToolResult(
                success=True,
                output=result,
            )

        except Exception as e:

            self.logger.error(
                f"Tool execution failed: {name} - {e}"
            )
            return ToolResult(
                success=False,
                error=str(e),
            )