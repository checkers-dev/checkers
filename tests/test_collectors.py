from pathlib import Path
from unittest.mock import MagicMock
from checkers import Model
from unittest.mock import MagicMock
from checkers.checks import check_model_has_description
from checkers.config import Config
from checkers.collectors import CheckCollector, NodeCollector
from checkers.core import Checker


def test_check_collector_collects_builtin_checks(config: Config):
    collector = CheckCollector(config=config)
    checks = collector.collect_builtin_checks()
    assert check_model_has_description in checks


def test_check_collector_collects_linter_checks(config: Config):
    collector = CheckCollector(config=config)
    checks = collector.collect_custom_lint_checks()
    assert len(checks) > 0


def test_check_collector_collects(config: Config):
    collector = CheckCollector(config=config)
    all_checks = collector.collect()
    assert len(all_checks) > 0


def test_check_collector_filters_disabled_checks(config: Config):
    def check_one(model):
        pass

    def check_two(model):
        pass

    check_one.params = {"enabled": False}
    check_two.params = {"enabled": True}

    check1 = Checker(check=check_one, config=config)
    check2 = Checker(check=check_two, config=config)

    collector = CheckCollector(config=config)
    collector.collect_all_checks = MagicMock()
    collector.collect_all_checks.return_value = [check1, check2]
    assert collector.collect() == [check2]
    assert collector.collect(include_disabled=True) == [check1, check2]
    collector.collect_all_checks.assert_called()


def test_node_collector_collects_multiple_resource_types(config: Config):
    collector = NodeCollector(config=config)
    resource_types = set([n.resource_type for n in collector.collect()])
    assert len(resource_types) >= 2
    assert "model" in resource_types
    assert "source" in resource_types


def test_node_collector(config: Config):
    collector = NodeCollector(config=config)
    models = collector.collect()
    assert len(models) > 0


# Note that the directories used in the paths here need to actually exist on the filesystem.
# Otherwise the match_path will not identify the checked paths as potentially being directories.
def test_node_collector_match_subpath(config):
    collector = NodeCollector(config=config)
    assert collector.match_path(Path("models/test.sql"), [Path("models/test.sql")])
    assert collector.match_path(Path("models/test.sql"), [Path("models/")])
    assert not collector.match_path(Path("models/test.sql"), [Path("models/other")])
    assert not collector.match_path(Path("models/test.sql"), [Path("models/other.sql")])
    assert collector.match_path(
        Path("models/example/test.sql"), [Path("models/example/test.sql")]
    )
    assert collector.match_path(
        Path("models/example/test.sql"), [Path("models/example/")]
    )


def test_node_collector_with_filepaths(config: Config, model: Model):
    collector = NodeCollector(config=config)
    m1 = model.model_copy(update={"original_file_path": "models/example/model1.sql"})
    m2 = model.model_copy(update={"original_file_path": "models/example/model2.sql"})
    m3 = model.model_copy(update={"original_file_path": "models/model3.sql"})
    m4 = model.model_copy(update={"original_file_path": "models/model4.sql"})
    collector.collect_all_nodes = MagicMock()
    collector.collect_all_nodes.return_value = [m1, m2, m3, m4]
    assert collector.collect() == [m1, m2, m3, m4]
    assert collector.collect(Path("models")) == [m1, m2, m3, m4]
    assert collector.collect(Path("models/example")) == [m1, m2]
    assert collector.collect(Path("models/example"), Path(m3.original_file_path)) == [
        m1,
        m2,
        m3,
    ]
    assert collector.collect(
        Path(m4.original_file_path), Path(m3.original_file_path)
    ) == [m3, m4]
