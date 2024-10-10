import sys
import os
import json
from pathlib import Path
from typing import List, Callable
from types import ModuleType
from checkers import checks
from .core import Checker
from .contracts import Model, Manifest, Source
from .config import Config


class CheckCollector:
    def __init__(self, config: Config):
        self.config = config

    def collect_all_checks(self) -> List[Checker]:
        builtin_checks = self.collect_builtin_checks()
        builtin_checks.extend(self.collect_custom_lint_checks())
        return [Checker(check=c, config=self.config) for c in builtin_checks]

    def collect(self, include_disabled=False) -> List[Checker]:
        all_checks = self.collect_all_checks()
        if include_disabled:
            return all_checks
        else:
            return list(filter(lambda c: c.enabled, all_checks))

    def collect_custom_lint_checks(self) -> List[Callable]:
        if "linter.py" in os.listdir(self.config.dbt_project_dir):
            sys.path.append(self.config.dbt_project_dir)
            import linter

            return self.collect_checks_from_module(linter)
        else:
            return list()

    def collect_checks_from_module(self, module: ModuleType) -> List[Callable]:
        results = list()
        for k, v in vars(module).items():
            if k.startswith("check") and callable(v):
                results.append(v)
        return results

    def collect_builtin_checks(self) -> List[Callable]:
        return self.collect_checks_from_module(checks)


class NodeCollector:
    def __init__(self, config: Config):
        self.config = config

    def load_manifest(self, path: str) -> Manifest:
        with open(path) as fh:
            data = json.load(fh)
            manifest = Manifest(**data, raw=data)
        return manifest

    def collect_all_nodes(self) -> List[Model]:
        manifest = self.load_manifest(self.config.manifest_path)
        results = list()
        for _, v in manifest.nodes.items():
            if v["resource_type"] == "model":
                results.append(Model(**v, manifest=manifest))
        results.extend(manifest.sources.values())
        return results

    def match_path(self, path: Path, others: List[Path]):
        """
        Check if `path` is either contained in `others`, or whether
        `other` contains a directory that contains `path`
        """

        for p in others:
            if path == p:
                return True
            if p.is_dir():
                if p in path.parents:
                    return True
        else:
            return False

    def collect(self, *paths: List[Path]) -> List[Model]:
        all_models = self.collect_all_nodes()
        if not paths:
            return all_models
        else:
            return list(
                filter(
                    lambda p: self.match_path(Path(p.original_file_path), paths),
                    all_models,
                )
            )
