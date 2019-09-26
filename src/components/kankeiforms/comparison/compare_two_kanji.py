from components.kankeiforms.kankeiform import KankeiForm
from components.kankeiforms.shown_properties import DEFAULT_SHOWN_PROPERTIES
from components.kankeiforms.transforms import two_list_transform
from tools.queryform.fields import IntField, StringField


class CompareTwoKanji(KankeiForm):
    group = "Comparison"
    name = "Compare two kanji"
    tooltip = ""
    coloring_types = ["Meaning", "Character", "Reading", "Word"]
    fields = [
        StringField(name="kanji 1", template_name="kanji1", description="first kanji"),
        StringField(name="kanji 2", template_name="kanji2", description="second kanji"),
        IntField(
            name="meaning depth",
            template_name="meaning_depth",
            description="how deep a meaning path can go",
            default=2,
            validate=lambda x: 0 <= x <= 2,
            validate_error_message='"meaning depth" must be between 0 and 2',
            hidden=True,
        ),
        IntField(
            name="reading depth",
            template_name="reading_depth",
            description="how deep a meaning path can go",
            default=2,
            validate=lambda x: 0 <= x <= 2,
            validate_error_message='"meaning depth" must be between 0 and 2',
            hidden=True,
        ),
        IntField(
            name="writing depth",
            template_name="writing_depth",
            description="how deep a writing path can go",
            default=2,
            validate=lambda x: 0 <= x <= 2,
            validate_error_message='"writing depth" must be between 0 and 2',
            hidden=True,
        ),
        # maximums and skips
        IntField(
            name="max meaning path",
            template_name="meaning_max",
            description="maximum number of meaning path",
            default=25,
            validate=lambda x: 0 <= x <= 50,
            validate_error_message='"max meaning path" must be between 0 and 100',
            hidden=True,
        ),
        IntField(
            name="max writing path",
            template_name="writing_max",
            description="maximum number of writing path",
            default=20,
            validate=lambda x: 0 <= x <= 50,
            validate_error_message='"max writing path" must be between 0 and 50',
            hidden=True,
        ),
        IntField(
            name="max reading path",
            template_name="reading_max",
            description="maximum number of reading path",
            default=20,
            validate=lambda x: 0 <= x <= 50,
            validate_error_message='"max reading path" must be between 0 and 50',
            hidden=True,
        ),
        IntField(
            name="max word path",
            template_name="word_max",
            description="maximum number of word path",
            default=20,
            validate=lambda x: 0 <= x <= 25,
            validate_error_message='"max word path" must be between 0 and 25',
            hidden=True,
        ),
    ]
    transform_output = two_list_transform
    shown_properties = DEFAULT_SHOWN_PROPERTIES

    @classmethod
    def get_query(cls, **kwargs):
        return (
            f"""
            MATCH p1= (
              (read1:Reading:Japanese)<-[:HasReading]-
              (kanji1:Kanji {{writing: $kanji1}})-[:HasMeaning]->(mean1:Meaning:English)
            )
            MATCH p2= (
              (read2:Reading:Japanese)<-[:HasReading]-
              (kanji2:Kanji {{writing: $kanji2}})-[:HasMeaning]->(mean2:Meaning:English)
            )
            OPTIONAL MATCH word_path = (
            (kanji1)<-[:HasCharacter]-(:Word)-[:HasCharacter]->(kanji2)
            )
            OPTIONAL MATCH meaning_path = allShortestPaths(
            (mean1)
            -[:IsAntonym|IsSynonym|IsComposedOf|IsHypernym|IsMeronym|IsFrequentWith*1..{kwargs["meaning_depth"].value}]
            -(mean2)
            )
            OPTIONAL MATCH comp_path = (
            (kanji1)-[:HasAlternative|HasArchaism|IsComposedOf*0..4]->(:Component)
              <-[:HasAlternative|HasArchaism|IsComposedOf*0..4]-(kanji2))
            OPTIONAL MATCH read_path = allShortestPaths(
              (read1)-[:HasSimilarSound*1..{kwargs['reading_depth'].value}]-(read2)
            )
            OPTIONAL MAtCH read_path2 = (read1)-[:IsComposedOf]->()<-[:IsComposedOf]-(read2)
            WITH
              collect(word_path)[..{kwargs['word_max'].value}]
              + collect(meaning_path)[..{kwargs['meaning_max'].value}]
              + collect(comp_path)[..{kwargs['writing_max'].value}]
              + collect(read_path)[..{kwargs['reading_max'].value}]
              + collect(read_path2)[..{kwargs['reading_max'].value}]
              + collect(p1)
              + collect(p2)
              AS paths
            UNWIND paths as path
            WITH collect(nodes(path)) AS nds, collect(relationships(path)) AS lnks
            WITH apoc.coll.flatten(nds) AS nds, apoc.coll.flatten(lnks) AS lnks
            UNWIND nds AS nd
            WITH collect(DISTINCT nd) AS nodes, lnks
            UNWIND lnks AS lnk
            RETURN nodes, collect(DISTINCT lnk) AS links;
        """,
            {"kanji1": kwargs["kanji1"].value, "kanji2": kwargs["kanji2"].value},
        )
