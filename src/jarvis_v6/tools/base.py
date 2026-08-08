from abc import ABC, abstractmethod
from typing import Any

class Tool(ABC):

    name: str
    description: str
    parameters: dict[str, Any]

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:

        raise NotImplementedError