from dataclasses import dataclass
from datetime import datetime
from collections import deque
from typing import Any

@dataclass(slots=True)
class MemoryEvent:

    timestamp: datetime
    event_name: str
    payload: dict[str, Any]

class MemoryManager:

    def __init__(self, logger, max_event:int = 1000):
        self.logger = logger
        self._events = deque(maxlen=max_event)


    def record(self, event_name:str, payload: dict[str, Any]):

        event = MemoryEvent(
            timestamp = datetime.now(),
            event_name=event_name,
            payload = payload
        )

        self._events.append(event)

        self.logger.info(f"Memory recorded: {event_name}")

    def get_recent_events(self, limit:int = 10) -> list[MemoryEvent]:

        return list(self._events)[-limit:]

    def clear(self):
        self._events.clear()

        self.logger.info("Runtime memory cleared.")

    @property
    def count(self) -> int:

        return len(self._events)
