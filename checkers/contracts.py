from typing import Optional, Dict, List, Any
import datetime as dt
from pathlib import Path
from enum import Enum
from pydantic import BaseModel, Field


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

    raw: Dict[str, Any]
    """
    Dictionary containg the raw manifest details
    """

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
    def sources(self) -> Dict[str, "Source"]:
        return {k: Source(**v, manifest=self) for k, v in self.raw["sources"].items()}

    @property
    def models(self) -> Dict[str, "Model"]:
        return {
            k: Model(**v, manifest=self)
            for k, v in self.nodes.items()
            if v["resource_type"] == "model"
        }

    def get_model_by_name(self, name: str) -> Optional["Model"]:
        for k, v in self.models.items():
            if v.name == name:
                return v


class Node(BaseModel):
    unique_id: str
    """
    The unique id of the model
    """

    resource_type: str
    """
    The resource type. Can be `model`, `test`, `seed`, etc.
    """

    original_file_path: Path
    """
    The path to the file that defined the node, relative to the dbt_project's directory
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


class Source(Node):
    """
    Represents a source in a dbt project
    """

    database: str  # "dev"
    schema_name: str = Field(alias="schema")  # "dummy_schema"
    name: str  # "table1"
    resource_type: str  # "source"
    package_name: str  # "mock"
    path: str  # "models/staging/dummy/schema.yml"
    unique_id: str  # "source.mock.dummy.table1"
    fqn: List[str]  # ["mock","staging","dummy","dummy","table1"]
    source_name: str  # "dummy"
    source_description: Optional[str] = None  # ""
    loader: Optional[str] = None  # ""
    identifier: Optional[str] = None  # "table1"


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

    source_names: List[List[str]] = Field(alias="sources")
    """
    Array containingg tuples of the sources referenced by the model.
    """

    @property
    def sources(self) -> List[Source]:
        results = []
        for p in self.parent_map:
            if p.startswith("source"):
                results.append(self.manifest.sources[p])
        return results

    @property
    def tests(self) -> List[Test]:
        results = []
        for c in self.child_map:
            if self.manifest.nodes[c]["resource_type"] == "test":
                d = self.manifest.nodes[c]
                results.append(Test(**d, manifest=self.manifest))
        return results
