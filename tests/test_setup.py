import os


def test_mock_project_setup(mock_dbt_project):
    assert "dbt_project.yml" in os.listdir(mock_dbt_project)
    assert os.getcwd() == str(mock_dbt_project)
