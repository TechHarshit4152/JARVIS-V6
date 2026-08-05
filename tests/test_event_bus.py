from jarvis_v6.core.event_bus import event_bus
from jarvis_v6.core.logger import logger

def browser_listener(payload):
    logger.info(f"Browser opened: {payload['url']}")

event_bus.subscribe("browser.opened", browser_listener)

event_bus.publish("browser.opened", {"url": "https://github.com"})