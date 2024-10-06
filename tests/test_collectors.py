from checkers.checks import check_temp
from checkers.config import Config
from checkers.collectors import CheckCollector


def test_check_collector_collects_builtin_checks(config: Config):
    collector = CheckCollector(config=config)
    checks = collector.collect_builtin_checks()
    assert check_temp in checks
