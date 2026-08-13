from jarvis_v6.ai.messages import Message, MessageRole
from jarvis_v6.core.kernel import kernel


def test_real_jarvis_runtime():
    print("\n" + "=" * 70)
    print("REAL JARVIS RUNTIME TEST")
    print("=" * 70)

    messages = [
        Message(
            role=MessageRole.USER,
            content=(
                "Hello JARVIS. I'm back. "
                "I spent way too much time procrastinating today. "
                "Give me a short response."
            ),
        )
    ]

    response = kernel.ai.generate(messages)

    print("\nJARVIS:")
    print(response.content)

    assert response.content
    assert isinstance(response.content, str)