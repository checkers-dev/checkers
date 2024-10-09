import toml
from typing import Optional, List
from pathlib import Path
from checkers.config import Config
from checkers.core import Checker


linter_template = """
from checkers import Model


def check_model_has_owner(model: Model):
    assert 'owner' in model.meta, "Model must define an owner in its meta block"
""".lstrip()


def generate_linter_template(path: Path):
    path.write_text(linter_template)


def generate_config_file(
    path: Path, config: Config, checkers: Optional[List[Checker]] = None
):
    data = config.model_dump()
    if checkers:
        data["checks"] = {c.check.__name__: c.params for c in checkers}
    toml.dump(data, path.open("w"))
