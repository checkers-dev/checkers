from click import group
from .runner import Runner
from .collectors import CheckCollector, ModelCollector
from .printer import Printer


@group
def cli():
    """
    An extensible dbt linter
    """


@cli.command()
def run():
    check_collector = CheckCollector()
    model_collector = ModelCollector()
    printer = Printer()
    runner = Runner(check_collector=check_collector, model_collector=model_collector, printer=printer)
    for res in runner.run():
        runner.printer.print(res)
