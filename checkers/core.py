import inspect
from typing import Callable, Dict
from .contracts import CheckResult, CheckResultStatus, Node
from .config import Config, CheckConfig
from .exceptions import SkipException, WarnException, InvalidCheckException


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
        self.check_config = self.build_check_config()

    def __repr__(self):
        return f"<Checker {self.check.__name__} [{self.resource_type}]>"

    def build_check_config(self) -> CheckConfig:
        builtin_params = getattr(self.check, "params", dict())
        override_params = self.config.checks.get(self.check.__name__, dict())
        builtin_params.update(override_params)
        config = CheckConfig(**builtin_params)
        return config

    def signature(self):
        sig = inspect.signature(self.check).parameters
        return sig

    def build_args(self, node: Node):
        args = {node.resource_type: node}
        if "params" in self.signature():
            args.update(params=self.params)
        return args

    @property
    def resource_type(self):
        try:
            first_param = list(self.signature().keys())[0]
            return first_param
        except IndexError:
            raise InvalidCheckException(
                "Check function specified no arguments. The first argument of a check function must specify the resource type to check"
            )

    @property
    def params(self) -> Dict:
        return self.check_config.model_dump()

    @property
    def enabled(self) -> bool:
        return self.params["enabled"] is True

    def skip(self, node: Node) -> None:
        """
        Raises a `SkipException` if the node should be skipped per its CheckConfig
        """

        for exclude_path in self.check_config.exclude_paths:
            if str(node.original_file_path).startswith(str(exclude_path)):
                raise SkipException(f"Excluding path {exclude_path}")

        if not self.check_config.include_paths:
            return

        for include_path in self.check_config.include_paths:
            if str(node.original_file_path).startswith(str(include_path)):
                break
        else:
            raise SkipException("Path did not match any included paths")

    def run(self, node: Node) -> CheckResult:
        try:
            self.skip(node)  # Raises a SkipException if the model should be skipped
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
