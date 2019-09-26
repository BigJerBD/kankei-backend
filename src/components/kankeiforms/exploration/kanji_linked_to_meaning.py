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


class KanjiLinkedToMeaning(KankeiForm):
    group = "Exploration"
    name = "Get kanji around meaning"
    tooltip = ""
    coloring_types = ["Meaning", "Character", "Reading"]
    fields = [
        StringField(
            name="Meaning", template_name="meaning", description="central meaning"
        ),
        ChoiceSubField(
            name="Search kanji with",
            template_name="kanji_search",
            choices={
                "Radical": [StringField(name="Radical", template_name="radical")],
                "Subcomponent": [
                    StringField(name="Component", template_name="comp"),
                    IntField(
                        name="component_depth",
                        template_name="component_depth",
                        description="how deep a component path can go",
                        default=2,
                        validate=lambda x: 0 <= x <= 5,
                        validate_error_message='"component depth" must be between 0 and 5',
                    ),
                ],
                "Reading": [
                    StringField(name="Reading", template_name="read"),
                    IntField(
                        name="reading depth",
                        template_name="reading_depth",
                        description="how deep a reading path can go",
                        default=2,
                        validate=lambda x: 0 <= x <= 3,
                        validate_error_message='"reading depth" must be between 0 and 3',
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
            name="meaning depth",
            template_name="meaning_depth",
            description="how deep a meaning path can go",
            default=2,
            validate=lambda x: 1 <= x <= 5,
            validate_error_message='"meaning depth" must be between 0 and 5',
            hidden=True,
        ),
    ]
    transform_output = nested_list_transform
    shown_properties = DEFAULT_SHOWN_PROPERTIES

    @classmethod
    def get_query(cls, **kwargs):
        kanji_search = kwargs["kanji_search"]

        if kanji_search.choice == "Radical":

            return (
                f"""
            MATCH (m:Meaning:English {{value: $meaning}})
            MATCH(comp:Character {{writing: $radical}})
            MATCH p = (
            (m)-[{MEANING_SUBPATHS_PARTIAL}*1..{kwargs["meaning_depth"].value}]-(n:Meaning:English)
              <-[:HasMeaning]-(k:Kanji)-[:HasRadical]->(comp)
            )
            WITH p AS path
              SKIP $randomizer
              LIMIT $max_paths
            RETURN collect(tail(reverse(nodes(path)))),
                   collect(tail(reverse(relationships(path))))
            """,
                {
                    "meaning": kwargs["meaning"].value,
                    "radical": kanji_search.fields["radical"],
                    "max_paths": kwargs["max_paths"].value,
                    "randomizer": kwargs["randomizer"].value,
                },
            )
        elif kanji_search.choice == "Subcomponent":
            return (
                f"""
            MATCH (m:Meaning:English {{value: $meaning}})
            MATCH(comp:Character {{writing: $comp}})
            MATCH p = (
            (m)-[{MEANING_SUBPATHS_PARTIAL}*1..{kwargs["meaning_depth"].value}]-(n:Meaning:English)
              <-[:HasMeaning]-(k:Kanji)-[:IsComposedOf*0..{kanji_search.fields["component_depth"]}]->(comp)
            )
            WITH p AS path
              SKIP $randomizer
              LIMIT $max_paths
            RETURN collect(tail(reverse(nodes(path)))),
                   collect(tail(reverse(relationships(path))))
            """,
                {
                    "meaning": kwargs["meaning"].value,
                    "comp": kanji_search.fields["comp"],
                    "max_paths": kwargs["max_paths"].value,
                    "randomizer": kwargs["randomizer"].value,
                },
            )

        elif kanji_search.choice == "Reading":
            return (
                f"""
            MATCH (m:Meaning:English {{value: $meaning}})
            MATCH(read:Reading:Japanese {{{get_reading_key(kanji_search.fields["read"])}: $read}})
            MATCH p = (
            (m)-[{MEANING_SUBPATHS_PARTIAL}*0..{kwargs["meaning_depth"].value}]-(n:Meaning:English)
            <-[:HasMeaning]-(k:Kanji)-[{READING_SUB_PATH}|HasReading*0..{kanji_search.fields[
                "reading_depth"]}]->(read)
            )
            WITH p AS path
              SKIP $randomizer
              LIMIT $max_paths
            RETURN collect(tail(reverse(nodes(path)))),
                   collect(tail(reverse(relationships(path))))
            """,
                {
                    "meaning": kwargs["meaning"].value,
                    "read": kanji_search.fields["read"],
                    "max_paths": kwargs["max_paths"].value,
                    "randomizer": kwargs["randomizer"].value,
                },
            )
