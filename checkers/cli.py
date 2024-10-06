from click import group
from .runner import Runner
from .collectors import CheckCollector, ModelCollector


@group
def cli():
    """
    An extensible dbt linter
    """


@cli.command()
def run():
    check_collector = CheckCollector()
    model_collector = ModelCollector()
    runner = Runner(check_collector=check_collector, model_collector=model_collector)
    for res in runner.run():
        print(res)
