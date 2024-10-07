import requests
from checkers.config import Config


class Client:
    def __init__(self, config: Config):
        self.config = config

    def healthcheck(self) -> bool:
        try:
            resp = requests.get(self.config.api_host + "/healthcheck").json()
            return resp["healthy"] == True
        except Exception:
            return False
