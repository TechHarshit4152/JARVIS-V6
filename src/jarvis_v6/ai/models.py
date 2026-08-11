from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AIResponse:
    content: str
    metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class AIChunk:
    content: str
    metadata: dict[str, Any] | None = None