import os
from typing import List
from pathlib import Path
from click import group, pass_obj, pass_context, option, argument, Argument
from rich import print
from .runner import Runner
from .collectors import CheckCollector, NodeCollector
from .summarizer import Summarizer
from .printer import Printer, CheckerRenderable
from .generators import generate_config_file, generate_linter_template
from .config import Config, load_config


@group()
@pass_context
@option(
    "--config-path",
    default=os.path.join(os.getcwd(), "linter.toml"),
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

    if not os.path.exists(config_path):
        config_path = None
    ctx.obj = load_config(path=config_path, dbt_project_dir=dbt_project_dir)


@cli.command()
@argument("paths", nargs=-1, type=Path)
@pass_obj
def run(obj: Config, paths: List[Path]):
    """
    Run the checks.

    Paths supplied can be either full paths to a model, or directories containing models. The following are all valid ways to use this command.

    $ checkers run models/model1.sql models/model2.sql\n
    $ checkers run models/marts models/shared/user.sql

    """

    check_collector = CheckCollector(config=obj)
    model_collector = NodeCollector(config=obj)
    printer = Printer(config=obj)
    runner = Runner(
        check_collector=check_collector,
        model_collector=model_collector,
        printer=printer,
        config=obj,
    )
    for _ in runner.run(*paths):
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
@option(
    "--include-disabled", default=False, is_flag=True, help="Include disabled checks"
)
def collect(obj: Config, include_disabled):
    """
    Print the names of collected checks
    """

    collector = CheckCollector(config=obj)
    printer = Printer(config=obj)
    for check in collector.collect(include_disabled=include_disabled):
        printer.print(CheckerRenderable(check))


@cli.command()
@option(
    "--path",
    "-p",
    type=Path,
    help="Directory to place the file. Defaults to current working directory.",
    default=os.getcwd(),
)
@pass_obj
def init(obj: Config, path: Path):
    """
    Create default `linter.toml` file
    """

    collector = CheckCollector(config=obj)
    checkers = collector.collect()
    generate_config_file(path / "linter.toml", config=obj, checkers=checkers)
    print("Created", path / "linter.toml")
    generate_linter_template(path / "linter.py")
    print("Created", path / "linter.py")
