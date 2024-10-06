import os
from pydantic import BaseModel


class Config(BaseModel):
    dbt_project_dir: str

    @property
    def manifest_path(self):
        return os.path.join(self.dbt_project_dir, "target", "manifest.json")
