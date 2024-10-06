from typing import Callable, List
from pytest import fixture
from rich.console import Console
from checkers.summarizer import Summarizer
from checkers.contracts import Model
from checkers.collectors import ModelCollector, CheckCollector
from checkers.runner import Runner
from checkers.core import Checker
from checkers.printer import Printer
from checkers.config import Config


@fixture
def failing_check() -> Callable:
    def check(node):
        assert False, "This failed"

    return check


@fixture
def passing_check() -> Callable:
    def check(node):
        return

    return check


@fixture
def error_check() -> Callable:
    def check(node):
        return 1 / 0

    return check


@fixture
def model():
    return Model(name="test", unique_id="test", resource_type="model")


@fixture
def config():
    return Config()


@fixture
def model_collector(model, config):
    class MockModelCollector(ModelCollector):
        def collect(self) -> List[Model]:
            return [model]

    return MockModelCollector(config=config)


@fixture
def check_collector(passing_check, config):
    checker = Checker(check=passing_check)

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
def check_result_passing(passing_check, model):
    checker = Checker(check=passing_check)
    res = checker.run(model)
    return res


@fixture
def check_result_failure(failing_check, model):
    checker = Checker(check=failing_check)
    res = checker.run(model)
    return res


@fixture
def check_result_error(error_check, model):
    checker = Checker(check=error_check)
    res = checker.run(model)
    return res
