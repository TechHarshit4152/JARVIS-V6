from jarvis_v6.config.settings import settings
from jarvis_v6.core.container import container
from jarvis_v6.core.event_bus import event_bus
from jarvis_v6.core.logger import logger
from jarvis_v6.core.state import StateManager

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

    def boot(self):
        self.logger.info("🚀 Booting JARVIS V6...")

        self.container.register("settings", self.settings)
        self.container.register("logger", self.logger)
        self.container.register("event_bus", self.event_bus)
        self.container.register("state", self.state)

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