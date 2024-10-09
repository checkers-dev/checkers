from typing import Dict
from checkers.contracts import Model


def check_model_has_description(model: Model, params: Dict):
    assert model.description not in ("", None), "Missing model description"
    assert (
        len(model.description) >= params["minimum_description_length"]
    ), "Model description not long enough"
    assert (
        len(model.description.split()) >= params["minimum_description_words"]
    ), f"Model description is too few words"


check_model_has_description.params = {
    "minimum_description_length": 10,
    "minimum_description_words": 4,
}


def check_something_else(model: Model):
    assert True


check_something_else.params = {
    'enabled': False
}
