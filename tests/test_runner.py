from checkers.runner import Runner

def test_runner_runs(runner: Runner):
    results = list(runner.run())
    assert len(results) > 0