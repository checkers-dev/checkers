import os
from click.testing import CliRunner
from checkers.cli import cli
from checkers.config import Config


def default_params(config: Config):
    mock_config_path = os.path.join(config.dbt_project_dir, "linter.toml")
    return [
        "--dbt-project-dir",
        config.dbt_project_dir,
        "--config-path",
        mock_config_path,
    ]


def test_cli_run(config: Config):
    runner = CliRunner()
    params = default_params(config)
    params.extend(["run", "models/example/my_first_dbt_model.sql"])
    res = runner.invoke(cli, params)
    assert res.exit_code == 0, res.output


def test_cli_run_with_paths(config: Config):
    runner = CliRunner()
    params = default_params(config)
    params.extend(["run", "models/example/my_first_dbt_model.sql"])
    res = runner.invoke(cli, params)
    assert res.exit_code == 0, res.output


def test_cli_debug(config: Config):
    runner = CliRunner()
    params = default_params(config)
    params.extend(["debug"])
    res = runner.invoke(cli, params)
    assert res.exit_code == 0


def test_cli_collect(config: Config):
    runner = CliRunner()
    params = default_params(config)
    params.extend(["collect"])
    res = runner.invoke(cli, params)
    assert res.exit_code == 0
    assert "enabled=False" not in res.output


def test_cli_collect_disabled(config: Config):
    runner = CliRunner()
    params = default_params(config)
    params.extend(["collect", "--include-disabled"])
    res = runner.invoke(cli, params)
    assert res.exit_code == 0
    assert "enabled=True" in res.output
    assert "enabled=False" not in res.output


def test_cli_collect_disabled(config: Config):
    runner = CliRunner()
    params = default_params(config)
    params.extend(["collect", "--include-disabled"])
    res = runner.invoke(cli, params)
    assert res.exit_code == 0
    assert "enabled=True" in res.output


def test_cli_init(tmpdir):
    runner = CliRunner()
    res = runner.invoke(cli, ["init", "--path", tmpdir])
    assert res.exit_code == 0
    assert "linter.py" in os.listdir(tmpdir)
    assert "linter.toml" in os.listdir(tmpdir)
