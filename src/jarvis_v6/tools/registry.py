from typing import Any
from jarvis_v6.tools.base import Tool

class ToolRegistry:


    def __init__(self, logger):

        self.logger = logger
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

        self.logger.info(f"Tool registered: {tool.name}")

    def resolve(self, name:str) -> Tool:

        if name not in self._tools:
            raise ValueError(
                f"Tool not registered: {name}"
            )

        return self._tools[name]

    def has(self, name:str) -> bool:

        return name in self._tools

    def list_tools(self) -> list[Tool]:

        return list(self._tools.values())

    def unregister(self, name:str) -> None:

        if name not in self._tools:

            raise ValueError(
                f"Tool not registered: {name}"
            )

        del self._tools[name]

        self.logger.info(f"Tool unregistered: {name}")