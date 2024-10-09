from typing import Callable, Dict
from .contracts import CheckResult, CheckResultStatus, Model
from .config import Config


class Checker:
    def __init__(self, check: Callable, config: Config):
        self.check = check
        self.config = config
        self._params = dict()

    def __repr__(self):
        return f"<Checker {self.check.__name__}>"

    def build_params(self):
        params = {"enabled": True}
        default_params = getattr(self.check, "params", dict())
        override_params = self.config.checks.get(self.check.__name__, dict())
        params.update(default_params)
        params.update(override_params)
        self._params = params
        return self._params

    @property
    def params(self) -> Dict:
        if not self._params:
            self.build_params()
        return self._params

    def run(self, node: Model) -> CheckResult:
        try:
            self.check(node)
            status = CheckResultStatus.passing
            message = None
        except AssertionError as err:
            status = CheckResultStatus.failure
            message = str(err)
        except Exception as err:
            status = CheckResultStatus.error
            message = str(err)

        return CheckResult.from_node(
            check_name=self.check.__name__, node=node, status=status, message=message
        )
