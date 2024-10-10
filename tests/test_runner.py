from unittest.mock import MagicMock
from checkers.core import Checker
from checkers.runner import Runner
from checkers.contracts import CheckResult
from checkers.collectors import NodeCollector, CheckCollector
from checkers.printer import Printer


def test_runner_runs(runner: Runner):
    results = list(runner.run())
    assert len(results) > 0
    assert len(runner.results) > 0
    assert isinstance(results[0], CheckResult)


def test_runner_runs_multiple_resource_types(config, source_check, model_check):
    node_collector = NodeCollector(config=config)
    printer = Printer(config=config)
    check_collector = CheckCollector(config=config)
    check_collector.collect = MagicMock()
    check_collector.collect.return_value = [
        Checker(check=source_check, config=config),
        Checker(check=model_check, config=config),
    ]
    runner = Runner(
        config=config,
        check_collector=check_collector,
        model_collector=node_collector,
        printer=printer,
    )
    checked_resource_types = set([r.node_type for r in runner.run()])
    assert "model" in checked_resource_types
    assert "source" in checked_resource_types
