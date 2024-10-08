import os
from click import group, pass_obj, pass_context, option
from rich import print
from .runner import Runner
from .collectors import CheckCollector, ModelCollector
from .summarizer import Summarizer
from .printer import Printer
from .config import Config, load_config


@group()
@pass_context
@option(
    "--config-path",
    default=None,
    envvar="CHECKERS_CONFIG_PATH",
    help="Path to a checkers configuration file. If not supplied, will use `linter.toml` in the current working directory.",
)
@option(
    "--dbt-project-dir",
    default=os.getcwd(),
    envvar="DBT_PROJECT_DIR",
    help="Path to a dbt project. If not supplied, will use the current working directly.",
)
def cli(ctx, config_path, dbt_project_dir: str):
    """
    An extensible dbt linter
    """

    ctx.obj = load_config(path=config_path, dbt_project_dir=dbt_project_dir)


@cli.command()
@pass_obj
def run(obj: Config):
    """
    Run the checks
    """

    check_collector = CheckCollector(config=obj)
    model_collector = ModelCollector(config=obj)
    printer = Printer(config=obj)
    runner = Runner(
        check_collector=check_collector,
        model_collector=model_collector,
        printer=printer,
        config=obj,
    )
    for _ in runner.run():
        pass
    summary = Summarizer(runner)
    exit(summary.exit_code())


@cli.command()
@pass_obj
def debug(obj: Config):
    """
    Print config details
    """

    print(obj)


@cli.command()
@pass_obj
def collect(obj: Config):
    """
    Print the names of collected checks
    """

    collector = CheckCollector(config=obj)
    printer = Printer(config=obj)
    for check in collector.collect():
        printer.print(check)


@cli.command()
@option(
    "--path",
    "-p",
    help="Directory to place the file. Defaults to current working directory.",
    default=os.getcwd(),
)
@pass_obj
def init(obj: Config, path: str):
    """
    Create default `linter.toml` file
    """

    obj.dump(os.path.join(path, "linter.toml"))
