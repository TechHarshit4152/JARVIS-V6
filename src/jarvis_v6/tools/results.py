from dataclasses import dataclass, field
from typing import Any

@dataclass
class ToolResult:

    success:bool
    output: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)