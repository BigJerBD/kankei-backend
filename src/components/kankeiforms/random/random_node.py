import random

from components.kankeiforms.graph_util import ALL_NODES, ALL_NODES_MAIN
from components.kankeiforms.kankeiform import KankeiForm
from components.kankeiforms.shown_properties import DEFAULT_SHOWN_PROPERTIES
from components.kankeiforms.transforms import two_list_transform
from tools.queryform.field_types import ChoiceSubField
from tools.queryform.fields import IntField


class RandomNodeForm(KankeiForm):
    group = "Random"
    name = "Get random nodes"
    tooltip = ""
    coloring_types = ALL_NODES_MAIN
    fields = [
        IntField(
            name="Number of nodes",
            template_name="node_max",
            description="Maximum number of node",
            default=5,
            validate=lambda x: 0 <= x <= 500,
            validate_error_message='"component depth" must be between 0 and 5',
        ),
        ChoiceSubField(
            name="Random node type",
            template_name="node_type",
            choices={node: [] for node in ALL_NODES},
            description="The type of node that should be shown",
        ),
    ]
    transform_output = two_list_transform
    shown_properties = DEFAULT_SHOWN_PROPERTIES

    @classmethod
    def get_query(cls, **kwargs):
        return (
            f"""
            MATCH (v:{kwargs["node_type"].value[0]})
            WITH v ORDER BY rand() LIMIT {kwargs["node_max"].value}
            RETURN collect(v),[]
            """,
            {},
        )
