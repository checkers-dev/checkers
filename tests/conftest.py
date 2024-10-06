from typing import Callable, List
from pytest import fixture
from rich.console import Console
from checkers.contracts import Model
from checkers.collectors import ModelCollector, CheckCollector
from checkers.runner import Runner
from checkers.core import Checker
from checkers.printer import Printer


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
    return Model(
        name='test', 
        unique_id='test',
        resource_type='model'
    )


@fixture
def model_collector(model):
    class MockModelCollector(ModelCollector):
        def collect(self) -> List[Model]:
            return [model]
    return MockModelCollector()


@fixture
def check_collector(passing_check):
    checker = Checker(check=passing_check)

    class MockCheckCollector(CheckCollector):
        def collect(self) -> List[Checker]:
            return [checker]
    
    return MockCheckCollector()


@fixture
def console():
    return Console()


@fixture
def printer(console):
    return Printer(console=console)


@fixture
def runner(check_collector, model_collector, printer):
    return Runner(check_collector=check_collector, model_collector=model_collector, printer=printer)
