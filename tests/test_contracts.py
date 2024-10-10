from checkers.contracts import Model, Test, Manifest


def test_manifest_finds_models(manifest: Manifest):
    assert len(manifest.models) > 0


def test_model_has_tests(manifest: Manifest):
    model = manifest.models["model.mock.my_first_dbt_model"]
    assert len(model.tests) > 0
