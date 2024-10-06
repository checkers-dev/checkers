import sys
import os
import json
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
        builtin_checks.extend(self.collect_custom_lint_checks())
        return [Checker(check=c) for c in builtin_checks]

    def collect_custom_lint_checks(self):
        if "linter.py" in os.listdir(self.config.dbt_project_dir):
            sys.path.append(self.config.dbt_project_dir)
            import linter

            return self.collect_checks_from_module(linter)
        else:
            return list()

    def collect_checks_from_module(self, module: ModuleType):
        results = list()
        for k, v in vars(module).items():
            if k.startswith("check") and callable(v):
                results.append(v)
        return results

    def collect_builtin_checks(self):
        return self.collect_checks_from_module(checks)


class ModelCollector:
    def __init__(self, config: Config):
        self.config = config

    def load_manifest(self, path: str) -> dict:
        with open(path) as fh:
            data = json.load(fh)
        return data

    def collect(self) -> List[Model]:
        manifest = self.load_manifest(self.config.manifest_path)
        results = list()
        for _, v in manifest["nodes"].items():
            if v["resource_type"] == "model":
                results.append(Model(**v))
        return results
