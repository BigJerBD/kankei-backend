from components.kankeiforms.graph_util import (
    ALL_NODES,
    ALL_RELATIONSHIPS,
    ALL_NODES_MAIN,
)
from components.kankeiforms.kankeiform import KankeiForm
from components.kankeiforms.shown_properties import DEFAULT_SHOWN_PROPERTIES
from components.kankeiforms.transforms import two_list_transform
from tools.queryform.field_types import ChoiceSubField
from tools.queryform.fields import IntField


class RandomEdgeForm(KankeiForm):
    group = "Random"
    name = "Get random edges"
    tooltip = ""
    coloring_types = ALL_NODES_MAIN
    fields = [
        IntField(
            name="Number of edges",
            template_name="edge_max",
            description="Maximum number of node",
            default=5,
            validate=lambda x: 0 <= x <= 500,
            validate_error_message='"component depth" must be between 0 and 5',
        ),
        ChoiceSubField(
            name="Direction",
            template_name="direction",
            choices={"Undirected": [], "1->2": [], "1<-2": []},
            description="first node type",
        ),
        ChoiceSubField(
            name="Node 1 type",
            template_name="node1_type",
            choices={"Any": [], **{node: [] for node in ALL_NODES}},
            description="first node type",
        ),
        ChoiceSubField(
            name="Node 2 type",
            template_name="node2_type",
            choices={"Any": [], **{node: [] for node in ALL_NODES}},
            description="second node type",
        ),
        ChoiceSubField(
            name="Edge type",
            template_name="edge_type",
            choices={node: [] for node in ALL_RELATIONSHIPS},
            description="The type of edge that should be shown",
        ),
    ]
    transform_output = two_list_transform
    shown_properties = DEFAULT_SHOWN_PROPERTIES

    @classmethod
    def get_query(cls, **kwargs):
        direction = kwargs["direction"].value[0]
        if direction == "Undirected":
            link_left, link_right = "-", "-"
        elif direction == "1->2":
            link_left, link_right = "-", "->"
        else:
            link_left, link_right = "<-", "-"

        node1 = kwargs["node1_type"].value[0]
        node1 = (":" + node1) if node1 != "Any" else ""
        node2 = kwargs["node2_type"].value[0]
        node2 = (":" + node2) if node2 != "Any" else ""
        edge = kwargs["edge_type"].value[0]

        return (
            f"""
            MATCH p=({node1}){link_left}[:{edge}]{link_right}({node2})
            WITH p ORDER BY rand() LIMIT {kwargs["edge_max"].value}
            WITH collect(nodes(p)) AS nds, collect(relationships(p)) AS lnks
            WITH apoc.coll.flatten(nds) AS nds, apoc.coll.flatten(lnks) AS lnks
            UNWIND nds AS nd
            WITH collect(DISTINCT nd) AS nodes, lnks
            UNWIND lnks AS lnk
            RETURN nodes, collect(DISTINCT lnk) AS links;
            """,
            {},
        )
