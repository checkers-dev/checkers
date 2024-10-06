from typing import Callable
from pytest import fixture
from checkers.contracts import Model


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