from abc import ABC, abstractmethod
from collections.abc import Iterator

from jarvis_v6.ai.messages import Message
from jarvis_v6.ai.models import AIChunk, AIResponse


class AIRuntime(ABC):

    @abstractmethod
    def generate(
        self,
        messages: list[Message],
    ) -> AIResponse:
        ...

    @abstractmethod
    def stream(
        self,
        messages: list[Message],
    ) -> Iterator[AIChunk]:
        ...