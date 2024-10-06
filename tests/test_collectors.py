from checkers.checks import check_temp
from checkers.config import Config
from checkers.collectors import CheckCollector, ModelCollector


def test_check_collector_collects_builtin_checks(config: Config):
    collector = CheckCollector(config=config)
    checks = collector.collect_builtin_checks()
    assert check_temp in checks


def test_model_collector(config: Config):
    collector = ModelCollector(config=config)
    models = collector.collect()
    assert len(models) > 0
