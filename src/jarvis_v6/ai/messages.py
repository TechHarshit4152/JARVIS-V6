from dataclasses import dataclass
from enum import Enum
from typing import Any

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

@dataclass(frozen=True)
class Message:
    role: MessageRole
    content: str
    metadata: dict[str, Any] | None=None