from checkers.runner import Runner
from checkers.contracts import CheckResult


def test_runner_runs(runner: Runner):
    results = list(runner.run())
    assert len(results) > 0
    assert len(runner.results) > 0
    assert isinstance(results[0], CheckResult)
