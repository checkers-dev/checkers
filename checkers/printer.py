from typing import Optional
from rich.console import Console, RenderableType
from rich.text import Text
from .contracts import CheckResult, CheckResultStatus
from .config import Config


class CheckResultRenderable:

    colors = {
        CheckResultStatus.passing: "green",
        CheckResultStatus.warning: "dark_orange",
        CheckResultStatus.failure: "red",
        CheckResultStatus.skipped: "grey53",
        CheckResultStatus.error: "red3",
    }

    def __init__(self, check_result: CheckResult):
        self.check_result = check_result

    def __rich__(self):
        color = self.colors[self.check_result.status]
        text = f"  {self.check_result.status.value}".ljust(8)
        status = Text(
            text,
            style=f"bold bright_white on {color}",
        )
        status.append(
            " " + self.check_result.check_name, style="not bold default on default"
        )
        status.append(f" {self.check_result.node_name}", style="bold blue on default")
        return status


class Printer:
    def __init__(self, config: Config, console: Optional[Console] = None):
        self.console = console or Console()
        self.config = config

    def print(self, renderable: RenderableType):
        self.console.print(renderable)
