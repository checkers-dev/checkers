from typing import Optional
import datetime as dt
from enum import Enum
from pydantic import BaseModel


# I think let's make the values here `pass`, `warn`, `error`, etc
class CheckResultStatus(Enum):
    passing = "PASS"
    warning = "WARN"
    failure = "FAIL"
    error = "ERROR"
    skipped = "SKIP"


class CheckResult(BaseModel):
    check_name: str
    checked_at: dt.datetime
    status: CheckResultStatus
    node_name: str
    node_type: str
    node_id: str
    message: Optional[str] = None

    @classmethod
    def from_node(
        cls,
        check_name: str,
        node: "Model",
        message: Optional[str],
        status: CheckResultStatus,
    ) -> "CheckResult":
        return cls(
            check_name=check_name,
            checked_at=dt.datetime.utcnow(),
            status=status,
            message=message,
            node_name=node.name,
            node_id=node.unique_id,
            node_type=node.resource_type,
        )


class Model(BaseModel):
    """
    Represents a model in a dbt project
    """

    name: str
    """
    The name of the model
    """

    unique_id: str
    """
    The unique id of the model
    """

    resource_type: str
    """
    The resource type. Always `model`.
    """
