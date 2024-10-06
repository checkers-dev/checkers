from typing import Optional
import datetime as dt
from dataclasses import dataclass
from enum import Enum


# I think let's make the values here `pass`, `warn`, `error`, etc
class CheckResultStatus(Enum):
    passing = 0
    warning = 1
    failure = 2
    error = 3
    skipped = 4


@dataclass
class CheckResult:
    check_name: str
    checked_at: dt.datetime
    status: CheckResultStatus
    node_name: str
    node_type: str
    node_id: str
    message: Optional[str] = None

    @classmethod
    def from_node(cls, check_name: str, node: "Model", message: Optional[str], status: CheckResultStatus) -> "CheckResult":
        return cls(
            check_name=check_name,
            checked_at=dt.datetime.utcnow(),
            status=status,
            message=message,
            node_name=node.name,
            node_id=node.unique_id,
            node_type=node.resource_type,
        )


@dataclass
class Model:
    name: str
    unique_id: str
    resource_type: str
