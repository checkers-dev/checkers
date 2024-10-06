from typing import Optional
from rich.console import Console, RenderableType
from .config import Config


class Printer:
    def __init__(self, config: Config, console: Optional[Console] = None):
        self.console = console or Console()
        self.config = config

    def print(self, renderable: RenderableType):
        self.console.print(renderable)
