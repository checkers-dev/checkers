from checkers.contracts import Model


def check_custom_check(model: Model):
    pass


def check_model_has_owner(model: Model):
    assert 'owner' in model.meta, "Model must specify an `owner` field in its `meta` block"
