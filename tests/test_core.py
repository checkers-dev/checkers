from unittest.mock import MagicMock
from pytest import raises
from pathlib import Path
from checkers.core import Checker, skip, warn
from checkers.contracts import CheckResultStatus, Model
from checkers.config import Config, CheckConfig
from checkers.exceptions import SkipException, WarnException, InvalidCheckException


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


def test_checker_with_base_params(config):
    def check_something(model):
        pass

    check_something.params = {"enabled": False, "p1": 1}

    checker = Checker(config=config, check=check_something)
    assert checker.params["p1"] is 1
    assert checker.params["enabled"] is False


def test_checker_with_override_params(config: Config):
    def check_something(model):
        pass

    check_something.params = {"enabled": False, "p1": 1}
    config.checks[check_something.__name__] = CheckConfig(
        **{"enabled": True, "p1": 2, "p2": 3}
    )
    checker = Checker(config=config, check=check_something)
    assert checker.params["enabled"] is True
    assert checker.params["p1"] is 2
    assert checker.params["p2"] is 3


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
        assert "p1" in params

    check_something.params = {"p1": "testing"}
    checker = Checker(config=config, check=check_something)
    res = checker.run(node=model)
    assert res.status == CheckResultStatus.passing


def test_checker_run_uses_skip(passing_check, model: Model, config: Config):
    checker = Checker(check=passing_check, config=config)
    checker.skip = MagicMock()
    res = checker.run(model)
    checker.skip.assert_called_once()
    assert res.status == CheckResultStatus.passing


def test_checker_run_handles_skip(passing_check, model: Model, config: Config):
    checker = Checker(check=passing_check, config=config)
    checker.skip = MagicMock()
    checker.skip.side_effect = SkipException
    res = checker.run(model)
    checker.skip.assert_called_once()
    assert res.status == CheckResultStatus.skipped


def test_checker_identifies_resource_type(
    config, model_check, source_check, undefined_resource_check
):
    check = Checker(check=model_check, config=config)
    assert check.resource_type == "model"

    check = Checker(check=source_check, config=config)
    assert check.resource_type == "source"

    check = Checker(check=undefined_resource_check, config=config)
    with raises(InvalidCheckException):
        check.resource_type


def test_checker_build_check_config(config):
    def check_mymodel(model):
        pass

    checker = Checker(check=check_mymodel, config=config)
    check_config = checker.build_check_config()
    assert check_config.enabled == True


def test_checker_skip(model: Model, config):
    def check_tmp(model):
        pass

    m = model.model_copy(
        update=dict(original_file_path=Path("models/testing/model.sql"))
    )
    checker = Checker(check=check_tmp, config=config)
    conf = checker.check_config

    # Expect no exception here
    checker.skip(m)

    # Add an include paths which should cause a skip exception
    checker.check_config = conf.model_copy(
        update={"include_paths": [Path("models/dne")]}
    )
    with raises(SkipException) as err:
        checker.skip(m)
        assert "did not match any included paths" in err

    # Remove the include paths but an an exclude paths, which should also have a skip exception
    checker.check_config = conf.model_copy(
        update={"include_paths": [], "exclude_paths": [Path("models/testing")]}
    )
    with raises(SkipException) as err:
        checker.skip(m)
        assert "excluding path models/testing" in err
