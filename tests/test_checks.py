from checkers import checks, Model
from checkers.core import Checker
from checkers.contracts import CheckResultStatus
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
