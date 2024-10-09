import os
from click.testing import CliRunner
from checkers.cli import cli
from checkers.config import Config


def default_params(config: Config):
    mock_config_path = os.path.join(config.dbt_project_dir, 'linter.toml')
    return ["--dbt-project-dir", config.dbt_project_dir, "--config-path", mock_config_path]


def test_cli_run(config: Config):
    runner = CliRunner()
    params = default_params(config)
    params.extend(['run'])
    res = runner.invoke(cli, params)
    assert res.exit_code == 0


def test_cli_debug(config: Config):
    runner = CliRunner()
    params = default_params(config)
    params.extend(['debug'])
    res = runner.invoke(cli, params)
    assert res.exit_code == 0


def test_cli_collect(config: Config):
    runner = CliRunner()
    params = default_params(config)
    params.extend(['collect'])
    res = runner.invoke(cli, params)
    assert res.exit_code == 0


def test_cli_init(tmpdir):
    runner = CliRunner()
    res = runner.invoke(cli, ["init", "--path", tmpdir])
    assert res.exit_code == 0
