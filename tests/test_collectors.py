from checkers.checks import check_model_has_description
from checkers.config import Config
from checkers.collectors import CheckCollector, ModelCollector


def test_check_collector_collects_builtin_checks(config: Config):
    collector = CheckCollector(config=config)
    checks = collector.collect_builtin_checks()
    assert check_model_has_description in checks


def test_check_collector_collects_linter_checks(config: Config):
    collector = CheckCollector(config=config)
    checks = collector.collect_custom_lint_checks()
    assert len(checks) > 0


def test_check_collector_collects(config: Config):
    collector = CheckCollector(config=config)
    all_checks = collector.collect()
    assert len(all_checks) > 0


def test_model_collector(config: Config):
    collector = ModelCollector(config=config)
    models = collector.collect()
    assert len(models) > 0
