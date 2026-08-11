from jarvis_v6.core.kernel import kernel


def test_ai_is_registered():
    kernel.boot()

    ai = kernel.container.resolve("ai")

    assert ai is kernel.ai

    kernel.shutdown()