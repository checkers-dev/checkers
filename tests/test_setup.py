import os
from checkers.config import Config


def test_mock_project_setup(mock_dbt_project):
    assert "dbt_project.yml" in os.listdir(mock_dbt_project)
    assert os.getcwd() == str(mock_dbt_project)


def test_config_setup(config: Config):
    assert os.path.exists(config.manifest_path)
