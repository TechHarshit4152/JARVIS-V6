from jarvis_v6.config.settings import settings
from jarvis_v6.core.container import container
from jarvis_v6.core.event_bus import event_bus
from jarvis_v6.core.logger import logger
from jarvis_v6.core.state import StateManager
from jarvis_v6.memory.manager import MemoryManager
from jarvis_v6.tools.registry import ToolRegistry
from jarvis_v6.tools.executor import ToolExecutor
from jarvis_v6.tasks.manager import TaskManager
from jarvis_v6.ai.providers.webscout import WebscoutProvider
from jarvis_v6.ai.system_prompt import SystemPromptBuilder

class Kernel():
    def __init__(self):
        self.settings = settings
        self.logger = logger
        self.event_bus = event_bus
        self.container = container

        self.state = StateManager(
            logger=self.logger,
            event_bus=self.event_bus
        )

        self.memory = MemoryManager(
            logger=self.logger
        )

        self.tools = ToolRegistry(
            logger=self.logger
        )

        
        self.tool_executor = ToolExecutor(
            registry=self.tools,
            logger=self.logger,
            event_bus=self.event_bus
        )

        self.tasks = TaskManager(
            logger=self.logger,
            event_bus=self.event_bus
        )

        self.ai = WebscoutProvider(
            model="@cf/meta/llama-3.1-70b-instruct",
            system_prompt=SystemPromptBuilder().build(),
        )

    def boot(self):
        self.logger.info("🚀 Booting JARVIS V6...")

        self.container.register("settings", self.settings)
        self.container.register("logger", self.logger)
        self.container.register("event_bus", self.event_bus)
        self.container.register("state", self.state)
        self.container.register("memory", self.memory)
        self.container.register("tools", self.tools)
        self.container.register("tool_executor", self.tool_executor)
        self.container.register("tasks", self.tasks)
        self.container.register("ai", self.ai)

        MEMORY_EVENTS = [
            "state.speaking.changed",
            "state.listening.changed",
            "state.thinking.changed"
        ]

        for event_name in MEMORY_EVENTS:
            self.event_bus.subscribe(
                event_name, 
                lambda payload, event_name=event_name : self.memory.record(
                    event_name,
                    payload
                )
            )

    

        self.event_bus.publish("kernel.booted")

        self.logger.info("✅ Kernel boot completed.")

    def shutdown(self):
        """
        Shutdown the JARVIS runtime.
        """

        self.logger.info("🛑 Shutting down JARVIS V6...")

        self.event_bus.publish("kernel.shutdown")

        self.logger.info("👋 Goodbye.")

    def restart(self):
        """
        Restart the JARVIS runtime.
        """

        self.shutdown()
        self.boot()

kernel = Kernel()