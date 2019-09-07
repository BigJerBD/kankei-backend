from components.kankeiforms.kankeiform import KankeiForm
from components.kankeiforms.shown_properties import DEFAULT_SHOWN_PROPERTIES
from components.kankeiforms.transforms import double_nested_list_transform
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
    transform_output = double_nested_list_transform
    shown_properties = DEFAULT_SHOWN_PROPERTIES

    @classmethod
    def get_query(cls, **kwargs):
        return (
            f"""
        MATCH(kanji1:Kanji {{writing: $kanji1}})
        MATCH(kanji2:Kanji {{writing: $kanji2}})
        MATCH mp = (
        (kanji1)-[:HasMeaning]->(m:Meaning:English)
          -[:IsAntonym|IsSynonym|IsComposedOf|IsHypernym|IsMeronym|IsFrequentWith*0..{kwargs["meaning_depth"].value}]-
        (n:Meaning:English)<-[:HasMeaning]-(kanji2)
        )
        WITH mp AS path
          SKIP 0
          LIMIT $meaning_max
        RETURN collect(nodes(path)), collect(relationships(path))
        UNION
        MATCH(kanji1:Kanji {{writing: $kanji1}})
        MATCH(kanji2:Kanji {{writing: $kanji2}})
        MATCH cp = ((kanji1)-[:HasAlternative|HasArchaism|IsComposedOf*0..{kwargs["writing_depth"].value}]->(:Component)
            <-[:HasAlternative|HasArchaism|IsComposedOf*0..{kwargs["writing_depth"].value}]-(kanji2)
            )
        WITH cp AS path
          SKIP 0
          LIMIT $writing_max
        RETURN collect(nodes(path)), collect(relationships(path))
        UNION
        MATCH(kanji1:Kanji {{writing: $kanji1}})
        MATCH(kanji2:Kanji {{writing: $kanji2}})
        MATCH cp = ((kanji1)-[:HasReading]->(:Reading)
          -[:IsComposedOf|HasSimilarSound*0..{kwargs["reading_depth"].value}]->(:Reading)
          <-[:IsComposedOf|HasSimilarSound*0..{kwargs["reading_depth"].value}]-
        (:Reading)<-[:HasReading]-(kanji2)
        )
        WITH cp AS path
          SKIP 0
          LIMIT $reading_max
        RETURN collect(nodes(path)), collect(relationships(path))
        UNION
        MATCH(kanji1:Kanji {{writing: $kanji1}})
        MATCH(kanji2:Kanji {{writing: $kanji2}})
        MATCH p = ((kanji1)<-[:HasCharacter]-(:Word)-[:HasCharacter]->(kanji2)
        )
        WITH p AS path
          SKIP 0
          LIMIT $word_max
        RETURN collect(nodes(path)), collect(relationships(path));
        """,
            {
                "kanji1": kwargs["kanji1"].value,
                "kanji2": kwargs["kanji2"].value,
                "reading_max": kwargs["reading_max"].value,
                "meaning_max": kwargs["meaning_max"].value,
                "word_max": kwargs["word_max"].value,
                "writing_max": kwargs["writing_max"].value,
            },
        )
