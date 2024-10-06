from typing import Iterable
from .contracts import CheckResult
from .collectors import CheckCollector, ModelCollector
from .printer import Printer
from .config import Config


class Runner:
    def __init__(self, check_collector: CheckCollector, model_collector: ModelCollector, printer: Printer, config: Config):
        self.check_collector = check_collector
        self.model_collector = model_collector
        self.printer = printer
        self.config = config

    def run(self) -> Iterable[CheckResult]:
        for model in self.model_collector.collect():
            for check in self.check_collector.collect():
                yield check.run(model)
