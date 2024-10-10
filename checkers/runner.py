from pathlib import Path
from typing import Iterable, List
from .contracts import CheckResult
from .collectors import CheckCollector, NodeCollector
from .printer import Printer, CheckResultRenderable
from .config import Config


class Runner:
    def __init__(
        self,
        check_collector: CheckCollector,
        model_collector: NodeCollector,
        printer: Printer,
        config: Config,
    ):
        self.check_collector = check_collector
        self.model_collector = model_collector
        self.printer = printer
        self.config = config
        self.results: List[CheckResult] = list()

    def run(self, *paths: List[Path]) -> Iterable[CheckResult]:
        for model in self.model_collector.collect(*paths):
            for check in self.check_collector.collect():
                if check.resource_type != model.resource_type:
                    continue
                res = check.run(model)
                self.results.append(res)
                self.printer.print(CheckResultRenderable(res))
                yield res
