import os
from pydantic import BaseModel


class Config(BaseModel):
    dbt_project_dir: str
    api_host: str = "https://www.getcheckers.com/api"

    @property
    def manifest_path(self):
        return os.path.join(self.dbt_project_dir, "target", "manifest.json")
