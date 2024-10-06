from click.testing import CliRunner
from checkers.cli import cli


def test_cli_run():
    runner = CliRunner()
    res = runner.invoke(cli, ["run"])
    assert res.exit_code == 0
