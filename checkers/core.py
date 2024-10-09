import inspect
from typing import Callable, Dict
from .contracts import CheckResult, CheckResultStatus, Model
from .config import Config
from .exceptions import SkipException, WarnException


# These functions are just to help beginners, who can be nervous about Exceptions. They're
# more comfortable calling functions rather than handling new keywords like `raise`,
# `try`, and `except`
def skip(message: str):
    raise SkipException(message)


def warn(message: str):
    raise WarnException(message)


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

    def build_args(self, node: Model):
        args = {"model": node}
        signature = inspect.signature(self.check)
        if "params" in signature.parameters:
            args.update(params=self.params)
        return args

    @property
    def params(self) -> Dict:
        if not self._params:
            self.build_params()
        return self._params

    @property
    def enabled(self) -> bool:
        return self.params["enabled"] is True

    def run(self, node: Model) -> CheckResult:
        try:
            args = self.build_args(node=node)
            self.check(**args)
            status = CheckResultStatus.passing
            message = None
        except AssertionError as err:
            status = CheckResultStatus.failure
            message = str(err)
        except WarnException as err:
            status = CheckResultStatus.warning
            message = str(err)
        except SkipException as err:
            status = CheckResultStatus.skipped
            message = str(err)
        except Exception as err:
            status = CheckResultStatus.error
            message = str(err)

        return CheckResult.from_node(
            check_name=self.check.__name__, node=node, status=status, message=message
        )
