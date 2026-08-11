from unittest.mock import MagicMock

from jarvis_v6.ai.messages import Message, MessageRole
from jarvis_v6.ai.models import AIChunk, AIResponse
from jarvis_v6.ai.providers.webscout import WebscoutProvider


def test_provider_initializes():
    provider = WebscoutProvider(
        model="@cf/meta/llama-3.1-70b-instruct",
        system_prompt="You are JARVIS.",
    )

    assert provider.model == "@cf/meta/llama-3.1-70b-instruct"
    assert provider.system_prompt == "You are JARVIS."


def test_message_conversion():
    messages = [
        Message(
            role=MessageRole.SYSTEM,
            content="You are JARVIS.",
        ),
        Message(
            role=MessageRole.USER,
            content="Hello.",
        ),
        Message(
            role=MessageRole.ASSISTANT,
            content="Hello, sir.",
        ),
    ]

    converted = WebscoutProvider._convert_messages(messages)

    assert converted == [
        {
            "role": "system",
            "content": "You are JARVIS.",
        },
        {
            "role": "user",
            "content": "Hello.",
        },
        {
            "role": "assistant",
            "content": "Hello, sir.",
        },
    ]


def test_generate_returns_ai_response():
    provider = WebscoutProvider(
        model="@cf/meta/llama-3.1-70b-instruct",
    )

    provider._client = MagicMock()

    provider._client.chat.return_value = "Hello, sir."

    response = provider.generate([
        Message(
            role=MessageRole.USER,
            content="Hello.",
        )
    ])

    assert isinstance(response, AIResponse)
    assert response.content == "Hello, sir."

    provider._client.chat.assert_called_once()


def test_generate_passes_messages():
    provider = WebscoutProvider(
        model="@cf/meta/llama-3.1-70b-instruct",
    )

    provider._client = MagicMock()

    provider._client.chat.return_value = "Response"

    messages = [
        Message(
            role=MessageRole.USER,
            content="Hello.",
        )
    ]

    provider.generate(messages)

    provider._client.chat.assert_called_once_with(
        [
            {
                "role": "user",
                "content": "Hello.",
            }
        ],
        stream=False,
    )


def test_stream_returns_ai_chunks():
    provider = WebscoutProvider(
        model="@cf/meta/llama-3.1-70b-instruct",
    )

    provider._client = MagicMock()

    provider._client.chat.return_value = iter([
        "Hello ",
        "sir",
        ".",
    ])

    chunks = list(
        provider.stream([
            Message(
                role=MessageRole.USER,
                content="Hello.",
            )
        ])
    )

    assert chunks == [
        AIChunk(
            content="Hello ",
            metadata={
                "provider": "webscout",
                "model": "@cf/meta/llama-3.1-70b-instruct",
            },
        ),
        AIChunk(
            content="sir",
            metadata={
                "provider": "webscout",
                "model": "@cf/meta/llama-3.1-70b-instruct",
            },
        ),
        AIChunk(
            content=".",
            metadata={
                "provider": "webscout",
                "model": "@cf/meta/llama-3.1-70b-instruct",
            },
        ),
    ]


def test_stream_skips_empty_chunks():
    provider = WebscoutProvider(
        model="@cf/meta/llama-3.1-70b-instruct",
    )

    provider._client = MagicMock()

    provider._client.chat.return_value = iter([
        "Hello",
        "",
        None,
        " sir",
    ])

    chunks = list(
        provider.stream([
            Message(
                role=MessageRole.USER,
                content="Hello.",
            )
        ])
    )

    assert [chunk.content for chunk in chunks] == [
        "Hello",
        " sir",
    ]
def test_real_llama_stream():
    provider = WebscoutProvider(
        model="@cf/meta/llama-3.1-70b-instruct",
        system_prompt="You are JARVIS. Respond briefly.",
    )

    print("\nREAL JARVIS STREAM:")

    full_response = ""

    for chunk in provider.stream([
        Message(
            role=MessageRole.USER,
            content="Say hello and tell me you are online.",
        )
    ]):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content

    print()

    assert full_response.strip()