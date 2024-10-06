from typing import Iterable
from .contracts import CheckResult
from .collectors import CheckCollector, ModelCollector


class Runner:
    def __init__(self, check_collector: CheckCollector, model_collector: ModelCollector):
        self.check_collector = check_collector
        self.model_collector = model_collector

    def run(self) -> Iterable[CheckResult]:
        for model in self.model_collector.collect():
            for check in self.check_collector.collect():
                yield check.run(model)
