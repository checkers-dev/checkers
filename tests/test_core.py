from pytest import raises
from checkers.core import Checker, skip, warn
from checkers.contracts import CheckResultStatus
from checkers.config import Config
from checkers.exceptions import SkipException, WarnException


def test_skip():
    with raises(SkipException) as err:
        skip("some message")
    assert "some message" in str(err)


def test_warn():
    with raises(WarnException) as err:
        warn("some message")
    assert "some message" in str(err)


def test_checker_with_passing_check(passing_check, model, config):
    checker = Checker(check=passing_check, config=config)
    res = checker.run(model)
    assert res.status == CheckResultStatus.passing, res.message


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


def test_checker_with_warning_check(warning_check, model, config):
    checker = Checker(check=warning_check, config=config)
    res = checker.run(model)
    assert res.status == CheckResultStatus.warning
    assert "Warning" in res.message


def test_checker_with_skipped_check(skipped_check, model, config):
    checker = Checker(check=skipped_check, config=config)
    res = checker.run(model)
    assert res.status == CheckResultStatus.skipped
    assert "Skipped" in res.message


def test_checker_with_default_params(config):
    def check_something(model):
        pass

    checker = Checker(config=config, check=check_something)
    assert checker.params["enabled"] is True
    assert len(checker.params) == 1


def test_checker_with_base_params(config):
    def check_something(model):
        pass

    check_something.params = {"enabled": False, "p1": 1}

    checker = Checker(config=config, check=check_something)
    assert checker.params["p1"] is 1
    assert checker.params["enabled"] is False
    assert len(checker.params) == 2


def test_checker_with_override_params(config: Config):
    def check_something(model):
        pass

    check_something.params = {"enabled": False, "p1": 1}
    config.checks[check_something.__name__] = {"enabled": True, "p1": 2, "p2": 3}
    checker = Checker(config=config, check=check_something)
    assert checker.params["enabled"] is True
    assert checker.params["p1"] is 2
    assert checker.params["p2"] is 3
    assert len(checker.params) == 3


def test_checker_build_args_with_default_args(config: Config, model):
    def check_something(model):
        pass

    checker = Checker(config=config, check=check_something)
    args = checker.build_args(node=model)
    assert args["model"] == model


def test_checker_build_args_with_params(config: Config, model):
    def check_something(model, params):
        pass

    check_something.params = {"p1": "testing"}
    checker = Checker(config=config, check=check_something)
    args = checker.build_args(node=model)
    assert args["model"] == model
    assert args["params"]["p1"] == "testing"


def test_checker_run_with_no_params(config: Config, model):
    def check_something(model):
        pass

    check_something.params = {"p1": "testing"}
    checker = Checker(config=config, check=check_something)
    res = checker.run(node=model)
    assert res.status == CheckResultStatus.passing


def test_checker_run_with_custom_params(config: Config, model):
    def check_something(model, params):
        assert 'p1' in params

    check_something.params = {"p1": "testing"}
    checker = Checker(config=config, check=check_something)
    res = checker.run(node=model)
    assert res.status == CheckResultStatus.passing
