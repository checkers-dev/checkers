from typing import Callable
from .contracts import CheckResult, CheckResultStatus, Model


class Checker:
    def __init__(self, check: Callable):
        self.check = check

    def __repr__(self):
        return f"<Checker {self.check.__name__}>"

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
