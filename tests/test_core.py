from checkers.core import Checker
from checkers.contracts import CheckResultStatus


def test_checker_with_passing_check(passing_check, model, config):
    checker = Checker(check=passing_check, config=config)
    res = checker.run(model)
    assert res.status == CheckResultStatus.passing


def test_checker_with_failing_check(failing_check, model, config):
    checker = Checker(check=failing_check, config=config)
    res = checker.run(model)
    assert res.status == CheckResultStatus.failure
    assert "failed" in res.message


def test_checker_with_error_check(error_check, model, config):
    checker = Checker(check=error_check, config=config)
    res = checker.run(model)
    assert res.status == CheckResultStatus.error
    assert "division by zero" in res.message
