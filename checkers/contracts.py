from typing import Optional, Dict, List, Any
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


class Manifest(BaseModel):
    nodes: Dict[str, Dict]
    """
    Dictionary mapping node_id's to node details.
    """

    parent_map: Dict[str, List[str]]
    """
    Dictionary mapping node_id's to nodes directly upstream
    """

    child_map: Dict[str, List[str]]
    """
    Dictionary mapping node_id's to nodes directly downstream
    """

    @property
    def models(self) -> Dict[str, "Model"]:
        return {
            k: Model(**v, manifest=self)
            for k, v in self.nodes.items()
            if v["resource_type"] == "model"
        }


class Node(BaseModel):
    unique_id: str
    """
    The unique id of the model
    """

    resource_type: str
    """
    The resource type. Can be `model`, `test`, `seed`, etc.
    """

    manifest: Manifest
    """
    The Manifest object. Useful for querying the node's parents, children, etc.
    """

    @property
    def child_map(self):
        return self.manifest.child_map[self.unique_id]

    @property
    def parent_map(self):
        return self.manifest.parent_map[self.unique_id]


class Column(BaseModel):
    name: str
    description: Optional[str] = None
    meta: dict
    data_type: Optional[str]
    constraints: List
    quote: Optional[bool]
    tags: List[str]


class Test(Node):
    __test__ = False  # Don't break pytest

    manifest: Manifest
    """
    The Manifest object. Useful for querying the node's parents, children, etc.
    """

    column_name: Optional[str] = None
    """
    The name of the column this test is defined on, if it's a column-level test
    """

    test_metadata: Dict[str, Any] = dict()
    """
    Additional data about the test, such as its name, namespace, and arguments specified
    """

    @property
    def test_name(self):
        """
        The name of the test, eg `unique`, `not_null`, etc
        """

        return self.test_metadata.get("name")


class Model(Node):
    """
    Represents a model in a dbt project
    """

    name: str
    """
    The name of the model
    """

    description: Optional[str] = None
    """
    The model's description
    """

    columns: Dict[str, Column]
    """
    Dictionary containing details about each column defined in the model's yaml file
    """

    original_file_path: str
    """
    The path to the model
    """

    fqn: List[str]
    """
    An array containing the fully qualified database name of the model
    """

    meta: Dict[str, Any]
    """
    The meta config property of the model
    """

    tags: List[str]
    """
    The tags of the model
    """

    @property
    def tests(self) -> List[Test]:
        results = []
        for c in self.child_map:
            if self.manifest.nodes[c]["resource_type"] == "test":
                d = self.manifest.nodes[c]
                results.append(Test(**d, manifest=self.manifest))
        return results
