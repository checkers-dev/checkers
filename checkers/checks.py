from typing import Dict
from checkers.contracts import Model


def check_model_has_description(model: Model, params: Dict):
    assert model.description not in ("", None)


check_model_has_description.params = {
    'minimum_description_length': 10,
    'minimum_description_words': 4
}

def check_something_else(model: Model):
    assert True
