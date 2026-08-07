from jarvis_v6.core.kernel import kernel

kernel.boot()

container = kernel.container

state = container.resolve("state")
memory = container.resolve("memory")
memory2 = container.resolve("memory")
logger = container.resolve("logger")

state.set_speaking(True)
state.set_speaking(True)
state.set_speaking(True)
state.set_listening(True)
state.set_thinking(True)

logger.info(f"Stored Events: {memory.count}")

events = memory.get_recent_events()

for event in events:
    logger.info(event)

assert memory is memory2