from typing import Any

class Container():

    def __init__(self):
        self._services: dict[str, Any] = {}

    def register(self, name: str, service:Any):
        if name in self._services:
            raise ValueError(f"Service '{name}' is already registered.")

        self._services[name] = service

    def resolve(self, name: str) -> Any:
        if name not in self._services:
            raise ValueError(f"Service '{name}' is not registered.")

        return self._services[name]

container = Container()