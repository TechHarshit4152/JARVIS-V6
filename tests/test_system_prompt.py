from jarvis_v6.ai.persona import JARVISPersona
from jarvis_v6.ai.system_prompt import SystemPromptBuilder


def test_system_prompt_is_generated():
    prompt = SystemPromptBuilder().build()

    assert isinstance(prompt, str)
    assert prompt.strip()


def test_system_prompt_contains_identity():
    prompt = SystemPromptBuilder().build()

    assert "You are JARVIS" in prompt
    assert "built by Harshit" in prompt
    assert "Harshit is your creator" in prompt
    assert "Assist Sir" in prompt


def test_system_prompt_contains_persona():
    persona = JARVISPersona()
    prompt = SystemPromptBuilder().build()

    assert persona.instructions in prompt


def test_system_prompt_contains_persona_sections():
    prompt = SystemPromptBuilder().build()

    expected_sections = [
        "## Core Character",
        "## Humor",
        "## Relationship with Sir",
        "## Communication",
        "## Emotional Intelligence",
        "## Behavioral Rules",
    ]

    for section in expected_sections:
        assert section in prompt


def test_system_prompt_does_not_contain_v5_execution_protocol():
    prompt = SystemPromptBuilder().build()

    assert "⚙️ Command" not in prompt
    assert "create_file" not in prompt
    assert "delete_task" not in prompt
    assert "list_dir" not in prompt


def test_system_prompt_is_deterministic():
    builder = SystemPromptBuilder()

    first = builder.build()
    second = builder.build()

    assert first == second


def test_system_prompt_can_use_custom_persona():
    persona = JARVISPersona(
        name="TEST-JARVIS",
    )

    prompt = SystemPromptBuilder(
        persona=persona,
    ).build()

    assert "You are TEST-JARVIS." in prompt