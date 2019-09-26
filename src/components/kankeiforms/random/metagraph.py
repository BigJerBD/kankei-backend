from collections import OrderedDict

from components.kankeiforms.graph_util import ALL_NODES, ALL_RELATIONSHIPS
from components.kankeiforms.kankeiform import KankeiForm
from components.kankeiforms.shown_properties import (
    DEFAULT_SHOWN_PROPERTIES,
    make_shown_properties,
)
from components.kankeiforms.transforms import two_list_transform

EXCLUDE_NODES = [
    # Meaning
    "French",
    "English",
    "Spanish",
    "Portugese",
    # Reading
    "Korean",
    "Japanese",
    "Chinese",
    # Writing
    "Kanji",
    "Component",
    "Radical",
    # Other
    "Computed",
    "WordInfo",
]


def exclude_descriptive_label(records):
    return {
        "nodes": {
            k: node
            for k, node in records["nodes"].items()
            if node["data"]["name"] not in EXCLUDE_NODES
        },
        "relationships": {k: rel for k, rel in records["relationships"].items()},
    }


def _transform_output(records):
    return exclude_descriptive_label(two_list_transform(records))


class MetagraphForm(KankeiForm):
    group = "Random"
    name = "Get the metagraph"
    tooltip = ""
    coloring_types = [
        "Meaning",
        "Character",
        "Reading",
        "Word",
        "Definition",
        "PartOfSpeech",
        "Domain",
        "Usage",
        "Dialect",
        "Stroke",
    ]
    fields = []
    transform_output = _transform_output
    shown_properties = make_shown_properties(
        {
            "nodes": OrderedDict([(v, "name") for v in ALL_NODES]),
            "relationships": OrderedDict([(v, "__self__") for v in ALL_RELATIONSHIPS]),
        }
    )

    @classmethod
    def get_query(cls, **kwargs):
        return (
            """
            CALL db.schema()
            """,
            {},
        )
