from unittest.mock import MagicMock
from checkers import checks, Model
from checkers.core import Checker
from checkers.contracts import CheckResultStatus, Column, Test, Manifest
from checkers.config import Config


def test_check_model_has_description(model: Model, config: Config):
    model.description = None
    checker = Checker(check=checks.check_model_has_description, config=config)
    res = checker.run(model)
    assert res.status == CheckResultStatus.failure, res.message

    model.description = ""
    res = checker.run(model)
    assert checker.run(model).status == CheckResultStatus.failure, res.message

    model.description = "Some value good value of sufficient length"
    res = checker.run(model)
    assert checker.run(model).status == CheckResultStatus.passing, res.message


def test_check_model_has_primary_key_test(config: Config, manifest: Manifest):
    model = manifest.get_model_by_name("my_first_dbt_model")
    assert model is not None
    checker = Checker(check=checks.check_model_has_primary_key_test, config=config)
    assert checker.run(model).status == CheckResultStatus.passing

    model = manifest.get_model_by_name("my_second_dbt_model")
    assert model is not None
    checker = Checker(check=checks.check_model_has_primary_key_test, config=config)
    assert checker.run(model).status == CheckResultStatus.failure
