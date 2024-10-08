import toml
import os
from checkers.config import load_config, Config


def test_load_config_with_defaults():
    config = load_config()
    assert config


def test_load_config_with_overrides():
    default_config = load_config()
    new_config = load_config(dbt_project_dir="some/path")
    assert new_config.dbt_project_dir != default_config.dbt_project_dir


def test_load_config_from_file(checkers_root):
    default_config = load_config()
    config = load_config(path=os.path.join(checkers_root, "./tests/mock/linter.toml"))
    assert config.api_host != default_config.api_host


def test_load_config_from_file_with_overrides(checkers_root):
    path = path = os.path.join(checkers_root, "./tests/mock/linter.toml")
    config = load_config(path)
    override_config = load_config(path, api_host="somehost")
    assert config.api_host != override_config.api_host


def test_config_dumps(config: Config, tmpdir):
    out = tmpdir / "config.toml"
    config.dump(out)
    with open(out) as fh:
        res = toml.load(fh)
    assert config.api_host == res["api_host"]
    assert config.dbt_project_dir == res["dbt_project_dir"]
