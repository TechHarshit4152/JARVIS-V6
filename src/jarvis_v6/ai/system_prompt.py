from jarvis_v6.ai.persona import JARVISPersona


class SystemPromptBuilder:
    def __init__(
        self,
        persona: JARVISPersona | None = None,
    ):
        self.persona = persona or JARVISPersona()

    def build(self) -> str:
        return self.persona.instructions