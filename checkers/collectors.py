from typing import List
from types import ModuleType
from checkers import checks
from .core import Checker
from .contracts import Model
from .config import Config


class CheckCollector:

    def __init__(self, config: Config):
        self.config = config

    def collect(self) -> List[Checker]:
        builtin_checks = self.collect_builtin_checks()
        return [Checker(check=c) for c in builtin_checks]
    
    def collect_checks_from_module(self, module: ModuleType):
        results = list()
        for k, v in vars(module).items():
            if k.startswith('check') and callable(v):
                results.append(v)
        return results

    def collect_builtin_checks(self):
        return self.collect_checks_from_module(checks)

class ModelCollector:

    def __init__(self, config: Config):
        self.config = config

    def collect(self) -> List[Model]:
        return [Model(name="temp", unique_id="temp", resource_type="model")]
