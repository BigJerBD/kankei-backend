from components.kankeiforms.graph_util import (
    MEANING_SUBPATHS_PARTIAL,
    READING_SUB_PATH,
    get_reading_key,
)
from components.kankeiforms.kankeiform import KankeiForm
from components.kankeiforms.shown_properties import DEFAULT_SHOWN_PROPERTIES
from components.kankeiforms.transforms import nested_list_transform, two_list_transform
from tools.queryform.field_types import ChoiceSubField
from tools.queryform.fields import IntField, StringField


class WordAntonym(KankeiForm):
    group = "Exploration"
    name = "Get antonyms (word)"
    tooltip = ""
    coloring_types = [
        "Meaning",
        "Character",
        "Reading",
        "Word",
        "WordInfo",
        "Definition",
    ]
    fields = [
        StringField(
            name="Word", template_name="word", description="word to search around"
        ),
        IntField(
            name="Antonym limit",
            template_name="word_limit",
            description="maximum number of path",
            default=200,
            validate=lambda x: 0 <= x <= 1000,
            validate_error_message='"Antonym limit" must be between 0 and 250',
        ),
    ]
    transform_output = two_list_transform
    shown_properties = DEFAULT_SHOWN_PROPERTIES

    @classmethod
    def get_query(cls, **kwargs):
        base_query = f"MATCH (w:Word {{writing: '{kwargs['word'].value}'}})"
        to_collect = []

        base_query += (
            "OPTIONAL MATCH "
            "p0=(w)-[:HasDefinition]->(:Definition)-[:HasMeaning]->(:English)"
            "-[:IsAntonym]-(:Meaning)<-[:HasMeaning]-()<-[:HasDefinition]-(:Word)"
        )
        to_collect.append("p0")
        to_collect = [
            f"collect({p})[..{kwargs['word_limit'].value}]" for p in to_collect
        ]
        base_query += f"WITH {' + '.join(to_collect)} AS paths "
        base_query += (
            f"UNWIND paths as path "
            f"WITH collect(nodes(path)) AS nds, collect(relationships(path)) AS lnks "
            f"WITH apoc.coll.flatten(nds) AS nds, apoc.coll.flatten(lnks) AS lnks "
            f"UNWIND nds AS nd WITH collect(DISTINCT nd) AS nodes, lnks UNWIND lnks AS lnk "
            f"RETURN nodes, collect(DISTINCT lnk) AS links;"
        )

        return (base_query, {})
