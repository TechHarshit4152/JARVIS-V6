from jarvis_v6.config.settings import settings
from jarvis_v6.core.container import container
from jarvis_v6.core.event_bus import event_bus
from jarvis_v6.core.logger import logger


container.register("settings", settings)
container.register("logger", logger)
container.register("event_bus", event_bus)


logger_service = container.resolve("logger")
settings_service = container.resolve("settings")
event_bus_service = container.resolve("event_bus")


logger_service.info("Logger resolved successfully!")

print(settings_service)

print(event_bus_service)

print(logger is logger_service)
print(settings is settings_service)
print(event_bus is event_bus_service)