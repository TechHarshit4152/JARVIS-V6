from dataclasses import FrozenInstanceError

import pytest

from jarvis_v6.ai.messages import Message, MessageRole
from jarvis_v6.ai.models import AIChunk, AIResponse
from jarvis_v6.ai.runtime import AIRuntime


def test_message_creation():
    message = Message(
        role=MessageRole.USER,
        content="Hello JARVIS",
    )

    assert message.role == MessageRole.USER
    assert message.content == "Hello JARVIS"


def test_all_message_roles():
    roles = [
        MessageRole.SYSTEM,
        MessageRole.USER,
        MessageRole.ASSISTANT,
        MessageRole.TOOL,
    ]

    for role in roles:
        message = Message(
            role=role,
            content="test",
        )

        assert message.role == role


def test_message_is_immutable():
    message = Message(
        role=MessageRole.USER,
        content="Hello",
    )

    with pytest.raises(FrozenInstanceError):
        message.content = "Changed"


def test_message_metadata():
    message = Message(
        role=MessageRole.USER,
        content="Hello",
        metadata={"source": "test"},
    )

    assert message.metadata == {
        "source": "test"
    }


def test_ai_response_creation():
    response = AIResponse(
        content="Hello, sir."
    )

    assert response.content == "Hello, sir."


def test_ai_response_metadata():
    response = AIResponse(
        content="Hello",
        metadata={"model": "test-model"},
    )

    assert response.metadata == {
        "model": "test-model"
    }


class FakeRuntime(AIRuntime):

    def generate(
        self,
        messages: list[Message],
    ) -> AIResponse:

        return AIResponse(
            content="Fake response"
        )

    def stream(
        self,
        messages: list[Message],
    ):
        yield AIChunk(content="Fake ")
        yield AIChunk(content="response")


def test_ai_runtime_stream():
    runtime = FakeRuntime()

    chunks = list(
        runtime.stream([
            Message(
                role=MessageRole.USER,
                content="Hello",
            )
        ])
    )

    assert chunks == [
        AIChunk(content="Fake "),
        AIChunk(content="response"),
    ]

    assert "".join(
        chunk.content for chunk in chunks
    ) == "Fake response"


def test_ai_runtime_implementation():
    runtime = FakeRuntime()

    response = runtime.generate([
        Message(
            role=MessageRole.USER,
            content="Hello",
        )
    ])

    assert isinstance(response, AIResponse)
    assert response.content == "Fake response"


def test_ai_runtime_receives_messages():

    class RecordingRuntime(AIRuntime):

        def __init__(self):
            self.received_messages = None

        def generate(
            self,
            messages: list[Message],
        ) -> AIResponse:

            self.received_messages = messages

            return AIResponse(
                content="Recorded"
            )

        def stream(
            self,
            messages: list[Message],
        ):
            self.received_messages = messages

            yield AIChunk(
                content="Recorded"
            )

    runtime = RecordingRuntime()

    messages = [
        Message(
            role=MessageRole.SYSTEM,
            content="You are JARVIS.",
        ),
        Message(
            role=MessageRole.USER,
            content="Hello.",
        ),
    ]

    response = runtime.generate(messages)

    assert response.content == "Recorded"
    assert runtime.received_messages == messages


def test_ai_runtime_is_abstract():
    with pytest.raises(TypeError):
        AIRuntime()