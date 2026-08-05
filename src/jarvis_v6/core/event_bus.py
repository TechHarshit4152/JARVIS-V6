from collections import defaultdict
from jarvis_v6.core.logger import logger

class Event_bus():
    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_name: str, callback):

        self.listeners[event_name].append(callback)

    def publish(self, event_name: str, payload: dict | None = None):

        if payload is None:
            payload = {}

        for callback in self.listeners[event_name]:
            try:
                callback(payload)
            except Exception as e:
                logger.error(f"Event '{event_name}' failed: {e}")

    def unsubscribe(self, event_name: str, callback):

        if callback in self.listeners[event_name]:
            self.listeners[event_name].remove(callback)

event_bus = Event_bus()