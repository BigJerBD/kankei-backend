from components.kankeiforms.graph_util import (
    MEANING_SUBPATHS_PARTIAL,
    READING_SUB_PATH,
    get_reading_key,
)
from components.kankeiforms.kankeiform import KankeiForm
from components.kankeiforms.shown_properties import DEFAULT_SHOWN_PROPERTIES
from components.kankeiforms.transforms import nested_list_transform
from tools.queryform.field_types import ChoiceSubField
from tools.queryform.fields import IntField, StringField
from tools.queryform.form import QueryForm


class KanjiLinkedToReading(KankeiForm):
    group = "Exploration"
    name = "Get kanji around reading"
    tooltip = ""
    coloring_types = ["Meaning", "Character", "Reading"]
    fields = [
        StringField(
            name="Reading", template_name="reading", description="central meaning"
        ),
        ChoiceSubField(
            name="Search kanji with",
            template_name="kanji_search",
            choices={
                "Radical": [StringField(name="Radical", template_name="radical")],
                "Subcomponent": [
                    StringField(name="Component", template_name="comp"),
                    IntField(
                        name="component depth",
                        template_name="component_depth",
                        description="how deep a component path can go",
                        default=2,
                        validate=lambda x: 0 <= x <= 5,
                        validate_error_message='"component depth" must be between 0 and 5',
                    ),
                ],
            },
            description="method to find the kanji related to meaning",
        ),
        IntField(
            name="max paths",
            template_name="max_paths",
            description="maximum number of path",
            default=100,
            validate=lambda x: 0 <= x <= 250,
            validate_error_message='"max paths" must be between 0 and 250',
            hidden=True,
        ),
        IntField(
            name="random number",
            template_name="randomizer",
            description="field skip",
            default=0,
            validate=lambda x: 0 <= x <= 1000,
            validate_error_message='"random number" must be between 0 and 1000',
            hidden=True,
        ),
        IntField(
            name="reading depth",
            template_name="reading_depth",
            description="how deep a reading path can go",
            default=2,
            validate=lambda x: 0 <= x <= 5,
            validate_error_message='"reading depth" must be between 0 and 5',
            hidden=True,
        ),
    ]
    transform_output = nested_list_transform
    shown_properties = DEFAULT_SHOWN_PROPERTIES

    @classmethod
    def get_query(cls, **kwargs):
        kanji_search = kwargs["kanji_search"]
        read_type = get_reading_key(kwargs["reading"].value)
        if kanji_search.choice == "Radical":

            return (
                f"""
            MATCH (r:Reading:Japanese {{{read_type}: $reading}})
            MATCH(comp:Character {{writing: $radical}})
            MATCH p = (
            (r)-[{READING_SUB_PATH}*0..{kwargs["reading_depth"].value}]->(:Reading:Japanese)
              <-[:HasReading]-(k:Kanji)-[:HasRadical]->(comp)
            )
            WITH p AS path
              SKIP $randomizer
              LIMIT $max_paths
            RETURN collect(tail(reverse(nodes(path)))),
                   collect(tail(reverse(relationships(path))))
            """,
                {
                    "reading": kwargs["reading"].value,
                    "radical": kanji_search.fields["radical"],
                    "max_paths": kwargs["max_paths"].value,
                    "randomizer": kwargs["randomizer"].value,
                },
            )
        elif kanji_search.choice == "Subcomponent":
            return (
                f"""
            MATCH (r:Reading:Japanese {{{read_type}: $reading}})
            MATCH(comp:Character {{writing: $comp}})
            MATCH p = (
            (r)-[{READING_SUB_PATH}*0..{kwargs["reading_depth"].value}]->(:Reading:Japanese)
              <-[:HasReading]-(k:Kanji)-[:IsComposedOf*0..{kanji_search.fields["component_depth"]}]->(comp)
            )
            WITH p AS path
              SKIP $randomizer
              LIMIT $max_paths
            RETURN collect(tail(reverse(nodes(path)))),
                   collect(tail(reverse(relationships(path))))
            """,
                {
                    "reading": kwargs["reading"].value,
                    "comp": kanji_search.fields["comp"],
                    "max_paths": kwargs["max_paths"].value,
                    "randomizer": kwargs["randomizer"].value,
                },
            )
