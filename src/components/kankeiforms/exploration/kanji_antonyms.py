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


class KanjiAntonym(KankeiForm):
    group = "Exploration"
    name = "Get antonym (kanji)"
    tooltip = ""
    coloring_types = ["Meaning", "Character", "Reading"]
    fields = [
        StringField(
            name="Kanji", template_name="kanji", description="kanji to search around"
        ),
        ChoiceSubField(
            name="English meaning Search",
            template_name="english_meaning_search",
            choices={"Yes": [], "No": []},
            description="Search with the use of english meaning",
        ),
        ChoiceSubField(
            name="Japanese meaning Search",
            template_name="japanese_meaning_search",
            choices={"Yes": [], "No": []},
            description="Search with the use of japanese meaning",
        ),
    ]
    transform_output = two_list_transform
    shown_properties = DEFAULT_SHOWN_PROPERTIES

    @classmethod
    def get_query(cls, **kwargs):
        base_query = f"MATCH (k:Character {{writing: '{kwargs['kanji'].value}'}})"
        to_collect = []

        if kwargs["english_meaning_search"].choice == "Yes":
            base_query += "OPTIONAL MATCH p0=(k)-[:HasMeaning]-(:English)-[:IsAntonym]-(:Meaning)<-[:HasMeaning]-(:Character) "
            to_collect.append("p0")

        if kwargs["japanese_meaning_search"].choice == "Yes":
            base_query += "OPTIONAL MATCH p1=(k)-[:HasMeaning]-(:Japanese)-[:IsAntonym]->(:Kanji) "
            base_query += "OPTIONAL MATCH p2=(k)-[:IsAntonym]-(:Japanese)<-[:HasMeaning]-(:Kanji) "
            to_collect.append("p1")
            to_collect.append("p2")

        to_collect = [f"collect({p})" for p in to_collect]
        base_query += f"WITH {' + '.join(to_collect)} AS paths "
        base_query += (
            f"UNWIND paths as path "
            f"WITH collect(nodes(path)) AS nds, collect(relationships(path)) AS lnks "
            f"WITH apoc.coll.flatten(nds) AS nds, apoc.coll.flatten(lnks) AS lnks "
            f"UNWIND nds AS nd WITH collect(DISTINCT nd) AS nodes, lnks UNWIND lnks AS lnk "
            f"RETURN nodes, collect(DISTINCT lnk) AS links;"
        )

        return (base_query, {})
