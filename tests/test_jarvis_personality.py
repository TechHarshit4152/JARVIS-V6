from jarvis_v6.ai.messages import Message, MessageRole
from jarvis_v6.ai.system_prompt import SystemPromptBuilder
from jarvis_v6.ai.providers.webscout import WebscoutProvider


def test_real_jarvis_personality():
    system_prompt = SystemPromptBuilder().build()

    provider = WebscoutProvider(
        model="@cf/meta/llama-3.1-70b-instruct",
        system_prompt=system_prompt,
    )

    prompts = [
        "Hello JARVIS. I'm finally back to working on you.",
        "Bro, I spent way too much time procrastinating today instead of working.",
        "I just finished something difficult and I'm pretty proud of it.",
        "I'm frustrated with how slowly I'm progressing today.",
        "What do you think makes you different from a generic assistant?",
    ]

    for prompt in prompts:
        print("\n" + "=" * 70)
        print(f"USER: {prompt}")
        print("=" * 70)
        print("JARVIS: ", end="", flush=True)

        messages = [
            Message(
                role=MessageRole.USER,
                content=prompt,
            )
        ]

        full_response = ""

        for chunk in provider.stream(messages):
            print(chunk.content, end="", flush=True)
            full_response += chunk.content

        print("\n")
        assert full_response.strip()