from typing import Optional
from rich.console import Console, RenderableType


class Printer:
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()

    def print(self, renderable: RenderableType):
        self.console.print(renderable)
