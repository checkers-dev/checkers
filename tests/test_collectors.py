from checkers.checks import check_model_has_description
from checkers.config import Config
from checkers.collectors import CheckCollector, ModelCollector
from checkers.core import Checker


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


def test_check_collector_filters_disabled_checks(config: Config):
    def check_one(model):
        pass

    def check_two(model):
        pass

    check_one.params = {'enabled': False}
    check_two.params = {'enabled': True}

    check1 = Checker(check=check_one, config=config)
    check2 = Checker(check=check_two, config=config)

    collector = CheckCollector(config=config)
    collector.collect_all_checks = lambda: [check1, check2]
    assert collector.collect() == [check2]
    assert collector.collect(include_disabled=True) == [check1, check2]


def test_model_collector(config: Config):
    collector = ModelCollector(config=config)
    models = collector.collect()
    assert len(models) > 0
