from typing import Optional, Dict, Any, List
from pathlib import Path
import os
import toml
from pydantic import BaseModel, ValidationError, ConfigDict
from .exceptions import ConfigFileNotFoundException, ConfigFileInvalid


class CheckConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool = True
    """
    This flag can be used to completely disable the check. Disabled checks are never ran.
    """

    exclude_paths: Optional[List[Path]] = list()
    """
    A set of paths that the check should skip. The paths must be relative to the dbt project directory.
    """

    include_paths: Optional[List[Path]] = list()
    """
    A set of paths that the check should target, so that any node which lives _outside_ of these paths will be skipped. The paths must be relative to the dbt project directory.
    """


class Config(BaseModel):
    dbt_project_dir: str = os.getcwd()
    api_host: str = "https://www.getcheckers.com/api"
    checks: Dict[str, CheckConfig] = dict()

    @property
    def manifest_path(self):
        return os.path.join(self.dbt_project_dir, "target", "manifest.json")

    def dump(self, out):
        with open(out, "w") as fh:
            toml.dump(self.model_dump(), fh)


def load_config(path: Optional[str] = None, **overrides) -> Config:
    if path is None:
        return Config(**overrides)
    elif not os.path.exists(path):
        raise ConfigFileNotFoundException(f"No config file found at {path}")
    else:
        raw_config = toml.load(open(path, "r"))

    raw_config.update(overrides)

    try:
        config = Config(**raw_config)
        return config
    except ValidationError as err:
        raise ConfigFileInvalid(str(err))
