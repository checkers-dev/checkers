from typing import Dict
from checkers.contracts import Model, Source


def check_model_has_description(model: Model, params: Dict):
    """
    Validate the model has a description
    """

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


def check_model_has_primary_key_test(model: Model, params: Dict):
    """
    Validate the model has at least one column with a unique and not_null test
    """

    column_test_maps = {c: [] for c in model.columns}
    for test in model.tests:
        if test.column_name in column_test_maps:
            column_test_maps[test.column_name].append(test.test_name)
    for column_name, column_tests in column_test_maps.items():
        if "unique" in column_tests and "not_null" in column_tests:
            break
    else:
        raise AssertionError(
            "Missing a column that defined both a unique and not_null test"
        )


def check_multiple_sources(model: Model):
    """
    Validate that a model can depend on only a single source.
    """

    assert (
        len(model.sources) <= 1
    ), f"Model can only depend on a single source, currently uses: {len(model.sources)}"
