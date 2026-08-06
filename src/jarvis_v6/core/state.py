class StateManager:

    def __init__(self, logger, event_bus):

        self.logger = logger
        self.event_bus = event_bus

        self._is_speaking = False
        self._is_listening = False
        self._is_thinking = False

    @property
    def is_speaking(self):
        return self._is_speaking

    def set_speaking(self, value: bool):
        if self._is_speaking == value:
            return

        self._is_speaking = value

        self.logger.info(f"Speaking: {value}")

        self.event_bus.publish(
            "state.speaking.changed",
            {"value": value}
        )

    @property
    def is_listening(self):

        return self._is_listening

    def set_listening(self, value: bool):

        if self._is_listening == value:
            return

        self.is_listening = value

        self.logger.info(f"Listening: {value}")

        self.event_bus.publish(
            "state.listening.changed",
            {"value": value}
        )


    @property
    def is_thinking(self):

        return self._is_thinking

    def set_thinking(self, value: bool):

        if self.is_thinking == value:
            return

        self.is_thinking = value

        self.logger.info(f"Thinking: {value}")

        self.event_bus.publish(
            "state.thinking.changed",
            {"value": value}
        )