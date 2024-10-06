from typing import List
from .core import Checker
from .contracts import Model
from .config import Config


class CheckCollector:

    def __init__(self, config: Config):
        self.config = config

    def collect(self) -> List[Checker]:
        def check_temp(model):
            pass

        return [Checker(check=check_temp)]


class ModelCollector:

    def __init__(self, config: Config):
        self.config = config

    def collect(self) -> List[Model]:
        return [Model(name="temp", unique_id="temp", resource_type="model")]
