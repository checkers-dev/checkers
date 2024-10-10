import json
import os
from shutil import copytree
from pathlib import Path
from typing import Callable, List
from pytest import fixture, mark
from rich.console import Console
from checkers.clients.api_client import Client
from checkers.summarizer import Summarizer
from checkers.contracts import Model, Manifest
from checkers.collectors import ModelCollector, CheckCollector
from checkers.runner import Runner
from checkers.core import Checker
from checkers.printer import Printer
from checkers.config import Config
from checkers.exceptions import WarnException, SkipException
from checkers import config as config_module


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: integration tests")


def pytest_addoption(parser):
    parser.addoption(
        "--integrations",
        action="store_true",
        default=False,
        help="run integration tests",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integrations"):
        # --integration given in cli: do not skip integration tests
        return
    skip_integration = mark.skip(reason="need --integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


@fixture
def warning_check() -> Callable:
    def check(model):
        raise WarnException("Warning")

    return check


@fixture
def skipped_check() -> Callable:
    def check(model):
        raise SkipException("Skipped")

    return check


@fixture
def failing_check() -> Callable:
    def check(model):
        assert False, "This failed"

    return check


@fixture
def passing_check() -> Callable:
    def check(model):
        return

    return check


@fixture
def error_check() -> Callable:
    def check(model):
        return 1 / 0

    return check


@fixture(scope="session")
def mock_dbt_project(tmpdir_factory):
    root = tmpdir_factory.mktemp("root")
    tests_dir = Path(os.path.dirname(__file__))
    mock_dbt_project_dir = tests_dir / "mock"
    target_dir = root / "mock"
    copytree(mock_dbt_project_dir, target_dir)
    os.chdir(target_dir)
    return Path(target_dir)


@fixture
def manifest(mock_dbt_project: Path):
    manifest_path = mock_dbt_project / "target" / "manifest.json"
    data = json.loads(manifest_path.read_text())
    return Manifest(**data, raw=data)


@fixture
def model(manifest):
    return Model(
        name="test",
        unique_id="test",
        resource_type="model",
        manifest=manifest,
        original_file_path="models/test/test.sql",
        tags=list(),
        meta=dict(),
        fqn=["prod", "core", "test.sql"],
        columns=dict(),
        sources=[],
    )


@fixture
def config(mock_dbt_project):
    dbt_project_dir = str(mock_dbt_project)
    return Config(dbt_project_dir=dbt_project_dir)


@fixture
def client(config) -> Client:
    return Client(config=config)


@fixture
def checkers_root():
    return str(Path(__file__).parent.parent)


@fixture
def model_collector(model, config):
    class MockModelCollector(ModelCollector):
        def collect(self) -> List[Model]:
            return [model]

    return MockModelCollector(config=config)


@fixture
def check_collector(passing_check, config):
    checker = Checker(check=passing_check, config=config)

    class MockCheckCollector(CheckCollector):
        def collect(self) -> List[Checker]:
            return [checker]

    return MockCheckCollector(config=config)


@fixture
def console():
    return Console()


@fixture
def printer(console, config):
    return Printer(console=console, config=config)


@fixture
def runner(check_collector, model_collector, printer, config):
    return Runner(
        check_collector=check_collector,
        model_collector=model_collector,
        printer=printer,
        config=config,
    )


@fixture
def summary(runner):
    return Summarizer(runner=runner)


@fixture
def check_result_passing(passing_check, model, config):
    checker = Checker(check=passing_check, config=config)
    res = checker.run(model)
    return res


@fixture
def check_result_failure(failing_check, model, config):
    checker = Checker(check=failing_check, config=config)
    res = checker.run(model)
    return res


@fixture
def check_result_error(error_check, model, config):
    checker = Checker(check=error_check, config=config)
    res = checker.run(model)
    return res
