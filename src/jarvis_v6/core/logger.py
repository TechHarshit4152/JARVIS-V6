import logging
from rich.console import Console
from rich.logging import RichHandler

class Logger:
    def __init__(self):
        self.console = Console()

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[
                RichHandler(
                    console=self.console,
                    rich_tracebacks=True,
                    show_time=True,
                    show_path=False,
                )
            ],
        )

        self.logger = logging.getLogger("JARVIS")

    def debug(self, message: str):
        self.logger.debug(message)
    def info(self, message: str):
        self.logger.info(message)
    def warning(self, message: str):
        self.logger.warning(message)
    def error(self, message: str):
        self.logger.error(message)
    def critical(self, message: str):
        self.logger.critical(message)


logger = Logger()