from jarvis_v6.core.kernel import kernel


kernel.boot()

state = kernel.container.resolve("state")
event_bus = kernel.container.resolve("event_bus")
logger = kernel.container.resolve("logger")


def on_speaking_changed(payload):
    logger.info(f"Listener received: {payload}")


event_bus.subscribe(
    "state.speaking.changed",
    on_speaking_changed
)


state.set_speaking(True)