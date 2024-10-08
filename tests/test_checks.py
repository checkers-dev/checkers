from pytest import raises
from checkers import checks, Model


def test_check_model_has_description(model: Model):
    model.description = None
    with raises(AssertionError):
        checks.check_model_has_description(model)

    model.description = ""
    with raises(AssertionError):
        checks.check_model_has_description(model)

    model.description = "Some value"
    checks.check_model_has_description(model)
