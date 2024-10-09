import toml
from pathlib import Path
from checkers.config import Config
from checkers.generators import (
    generate_linter_template,
    generate_config_file,
    linter_template,
)
from checkers.collectors import CheckCollector


def test_generate_linter_template(tmp_path: Path):
    target = tmp_path / "linter.py"
    generate_linter_template(target)
    out = target.read_text()
    assert linter_template in out


def test_generate_config_file(tmp_path: Path, config: Config):
    target = tmp_path / "linter.toml"
    generate_config_file(target, config)
    saved = toml.load(target.open())
    assert "dbt_project_dir" in saved


def test_generate_config_file_with_checkers(tmp_path: Path, config: Config):
    target = tmp_path / "linter.toml"
    collector = CheckCollector(config)
    checkers = collector.collect()
    generate_config_file(target, config, checkers)
    saved = toml.load(target.open())
    assert "dbt_project_dir" in saved
    assert "checks" in saved
    assert len(saved["checks"]) > 0
    for checker in checkers:
        assert checker.check.__name__ in saved["checks"], saved["checks"]
        assert checker.params == saved["checks"][checker.check.__name__]
