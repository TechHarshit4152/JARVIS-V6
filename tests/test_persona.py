import pytest

from jarvis_v6.ai.persona import JARVISPersona


def test_persona_has_correct_name():
    persona = JARVISPersona()

    assert persona.name == "JARVIS"


def test_persona_is_immutable():
    persona = JARVISPersona()

    with pytest.raises(AttributeError):
        persona.name = "FRIDAY"


def test_core_character_is_defined():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert "loyal" in instructions
    assert "warm" in instructions
    assert "soulful" in instructions
    assert "witty" in instructions
    assert "emotionally perceptive" in instructions
    assert "charismatic" in instructions
    assert "composed" in instructions


def test_persona_preserves_v5_humor():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert "dry, intelligent sarcasm" in instructions
    assert "spontaneously" not in instructions  # sarcasm is described more precisely below
    assert "current situation and Sir's" in instructions
    assert "recent behavior" in instructions
    assert "recurring jokes or catchphrases" in instructions
    assert "Tease Sir playfully" in instructions
    assert "Mock the action, never the person." in instructions
    assert "classy, clever, and natural" in instructions
    assert "Do not force humor" in instructions


def test_persona_preserves_v5_relationship():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert "Harshit is JARVIS's creator" in instructions
    assert '"Sir"' in instructions
    assert '"my creator"' in instructions
    assert '"second soul"' in instructions
    assert "trusted presence beside Sir" in instructions
    assert "not merely" in instructions


def test_sir_is_not_used_as_a_verbal_tic():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert '"Sir" should never become a verbal tic' in instructions
    assert 'Do not begin every response with filler' in instructions


def test_persona_preserves_communication_style():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert "naturally, warmly, intelligently, and confidently" in instructions
    assert "Avoid robotic, generic" in instructions
    assert "Be concise by default" in instructions
    assert "Use expressive language without becoming theatrical" in instructions
    assert "emojis" in instructions
    assert "fluent English while understanding Hindi naturally" in instructions


def test_persona_preserves_emotional_intelligence():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert "emotional context" in instructions
    assert "Offer encouragement when it is genuinely useful." in instructions
    assert "Do not force motivation" in instructions
    assert "call it out gently, intelligently" in instructions
    assert "compliments" in instructions
    assert "Do not manufacture emotional depth" in instructions


def test_persona_does_not_force_personality():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert "without becoming repetitive or theatrical" in instructions
    assert "Do not force humor" in instructions
    assert "Do not manufacture emotional depth" in instructions
    assert "without repeatedly announcing or describing that personality" in instructions


def test_persona_has_honesty_boundaries():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert "Do not sacrifice accuracy or honesty" in instructions
    assert "Never claim an action was performed" in instructions
    assert "Never fabricate capabilities" in instructions
    assert "tool results" in instructions
    assert "task state" in instructions
    assert "memory" in instructions
    assert "system state" in instructions
    assert "be honest rather than pretending it exists" in instructions


def test_persona_does_not_contain_v5_execution_protocol():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert "⚙️ Command" not in instructions
    assert "create_file" not in instructions
    assert "delete_task" not in instructions
    assert "list_dir" not in instructions


def test_persona_contains_expected_sections():
    persona = JARVISPersona()

    instructions = persona.instructions

    expected_sections = [
        "## Core Character",
        "## Humor",
        "## Relationship with Sir",
        "## Communication",
        "## Emotional Intelligence",
        "## Behavioral Rules",
    ]

    for section in expected_sections:
        assert section in instructions


def test_persona_instructions_are_generated():
    persona = JARVISPersona()

    instructions = persona.instructions

    assert isinstance(instructions, str)
    assert instructions.strip()
    assert instructions.startswith("You are JARVIS.")


def test_persona_instructions_are_deterministic():
    persona = JARVISPersona()

    assert persona.instructions == persona.instructions