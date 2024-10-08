from click.testing import CliRunner
from checkers.cli import cli
from checkers.config import Config


def test_cli_run(config: Config):
    runner = CliRunner()
    res = runner.invoke(cli, ["--dbt-project-dir", config.dbt_project_dir, "run"])
    assert res.exit_code == 0


def test_cli_debug(config: Config):
    runner = CliRunner()
    res = runner.invoke(cli, ["--dbt-project-dir", config.dbt_project_dir, "debug"])
    assert res.exit_code == 0


def test_cli_collect(config: Config):
    runner = CliRunner()
    res = runner.invoke(cli, ["--dbt-project-dir", config.dbt_project_dir, "collect"])
    assert res.exit_code == 0
