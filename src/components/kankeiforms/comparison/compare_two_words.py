from components.kankeiforms.kankeiform import KankeiForm
from components.kankeiforms.shown_properties import DEFAULT_SHOWN_PROPERTIES
from components.kankeiforms.transforms import two_list_transform
from tools.queryform.fields import IntField, StringField


class CompareTwoWords(KankeiForm):
    group = "Comparison"
    name = "Compare two words"
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
        StringField(name="word 1", template_name="word1", description="first word"),
        StringField(name="word 2", template_name="word2", description="second word"),
        IntField(
            name="meaning depth",
            template_name="meaning_depth",
            description="how deep a meaning path can go",
            default=2,
            validate=lambda x: 0 <= x <= 4,
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
            name="max reading path",
            template_name="reading_max",
            description="maximum number of reading path",
            default=20,
            validate=lambda x: 0 <= x <= 50,
            validate_error_message='"max reading path" must be between 0 and 50',
            hidden=True,
        ),
        IntField(
            name="max character path",
            template_name="char_max",
            description="maximum number of word path",
            default=20,
            validate=lambda x: 0 <= x <= 25,
            validate_error_message='"max word path" must be between 0 and 25',
            hidden=True,
        ),
        IntField(
            name="max word info path",
            template_name="winfo_max",
            description="maximum number of word info path",
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
            f"""MATCH p1= (
              (read1:Reading:Japanese)<-[:HasReading]-
              (word1:Word {{writing: $word1}})-[:HasDefinition]->()-[:HasMeaning]->(mean1:Meaning:English)
            )
            MATCH p2= (
              (read2:Reading:Japanese)<-[:HasReading]-
              (word2:Word {{writing: $word2}})-[:HasDefinition]->()-[:HasMeaning]->(mean2:Meaning:English)
            )
            OPTIONAL MATCH char_path= (
            (word1)-[:HasCharacter]->(:Character)<-[:HasCharacter]->(word2)
            )
            OPTIONAL MATCH meaning_path = allShortestPaths(
            (mean1)
            -[:IsAntonym|IsSynonym|IsComposedOf|IsHypernym|IsMeronym|IsFrequentWith*1..{kwargs["meaning_depth"].value}]
            -(mean2)
            )
            OPTIONAL MATCH read_path = allShortestPaths(
              (read1)-[:HasSimilarSound*1..{kwargs['reading_depth'].value}]-(read2)
            )
            OPTIONAL MATCH read_path2 = (read1)-[:IsComposedOf]->()<-[:IsComposedOf]-(read2)
            OPTIONAL MATCH winfo_path = (
                (word1)-[:HasDefinition]->()-[:HasInfo]->(:WordInfo)<-[:HasInfo]-()-[:HasDefinition]-(word2)
            )
            WITH
              collect(char_path)[..{kwargs['char_max'].value}]
              + collect(meaning_path)[..{kwargs['meaning_max'].value}]
              + collect(read_path)[..{kwargs['reading_max'].value}]
              + collect(read_path2)[..{kwargs['reading_max'].value}]
              + collect(winfo_path)[..{kwargs['winfo_max'].value}]
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
            {"word1": kwargs["word1"].value, "word2": kwargs["word2"].value},
        )
