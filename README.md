# checkers

An extensible linter for dbt


## Development

This project supports development inside a devcontainer using VSCode.

After cloning this repository, VS Code should prompt you to open the project inside the devcontainer. If not, confirm you have the devcontainers extension installed.

Once the devcontainer has started you can install the necessary development dependencies inside a virtual environment.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --editable .
```

You should now be able to run the test suite.

```
pytest
```
