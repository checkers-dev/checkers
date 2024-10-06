from click import group, pass_obj, pass_context
from .runner import Runner
from .collectors import CheckCollector, ModelCollector
from .printer import Printer
from .config import Config


@group
@pass_context
def cli(ctx):
    """
    An extensible dbt linter
    """

    ctx.obj = Config()


@cli.command()
@pass_obj
def run(obj: Config):
    check_collector = CheckCollector(config=obj)
    model_collector = ModelCollector(config=obj)
    printer = Printer(config=obj)
    runner = Runner(
        check_collector=check_collector,
        model_collector=model_collector,
        printer=printer,
        config=obj,
    )
    for res in runner.run():
        runner.printer.print(res)
