from checkers.contracts import Model


def check_model_has_description(model: Model):
    assert model.description not in ("", None)


def check_something_else(model: Model):
    assert True
