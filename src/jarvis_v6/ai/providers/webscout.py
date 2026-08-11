from collections.abc import Iterator

from webscout import LLMChat

from jarvis_v6.ai.messages import Message
from jarvis_v6.ai.models import AIChunk, AIResponse
from jarvis_v6.ai.runtime import AIRuntime


class WebscoutProvider(AIRuntime):

    def __init__(
        self,
        model: str,
        system_prompt: str | None = None,
    ):
        self.model = model
        self.system_prompt = system_prompt

        self._client = LLMChat(
            model=model,
            system_prompt=system_prompt,
        )

    def generate(
        self,
        messages: list[Message],
    ) -> AIResponse:

        response = self._client.chat(
            self._convert_messages(messages),
            stream=False,
        )

        return AIResponse(
            content=response,
            metadata={
                "provider": "webscout",
                "model": self.model,
            },
        )

    def stream(
        self,
        messages: list[Message],
    ) -> Iterator[AIChunk]:

        for chunk in self._client.chat(
            self._convert_messages(messages),
            stream=True,
        ):
            if chunk:
                yield AIChunk(
                    content=chunk,
                    metadata={
                        "provider": "webscout",
                        "model": self.model,
                    },
                )

    @staticmethod
    def _convert_messages(
        messages: list[Message],
    ) -> list[dict[str, str]]:

        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in messages
        ]