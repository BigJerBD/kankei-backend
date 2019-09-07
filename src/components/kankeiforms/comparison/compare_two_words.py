from components.kankeiforms.kankeiform import KankeiForm
from components.kankeiforms.shown_properties import DEFAULT_SHOWN_PROPERTIES
from components.kankeiforms.transforms import double_nested_list_transform
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
    transform_output = double_nested_list_transform
    shown_properties = DEFAULT_SHOWN_PROPERTIES

    @classmethod
    def get_query(cls, **kwargs):
        return (
            f"""
        MATCH(word1:Word {{writing: $word1}})
        MATCH(word2:Word {{writing: $word2}})
        MATCH mp = (
        (word1)-[:HasDefinition]->(:Definition)-[:HasMeaning]->(:Meaning:English)
          -[:IsAntonym|IsSynonym|IsComposedOf|IsHypernym|IsMeronym|IsFrequentWith*0..{kwargs["meaning_depth"].value}]-
        (:Meaning:English)<-[:HasMeaning]-(:Definition)<-[:HasDefinition]-(word2)
        )
        WITH mp AS path
          SKIP 0
          LIMIT $meaning_max
        RETURN collect(nodes(path)), collect(relationships(path))
        UNION
        MATCH(word1:Word {{writing: $word1}})
        MATCH(word2:Word {{writing: $word2}})
        MATCH mp = (
        (word1)-[:HasDefinition]->(:Definition)-[:HasInfo]->(:WordInfo)<-[:HasInfo]-(:Definition)<-[:HasDefinition]-(word2)
        )
        WITH mp AS path
          SKIP 0
          LIMIT $winfo_max
        RETURN collect(nodes(path)), collect(relationships(path))
        UNION
        MATCH(word1:Word {{writing: $word1}})
        MATCH(word2:Word {{writing: $word2}})
        MATCH cp = ((word1)-[:HasReading]->(:Reading)
          -[:IsComposedOf|HasSimilarSound*0..{kwargs[
            "writing_depth"].value}]->(:Reading)<-[:IsComposedOf|HasSimilarSound*0..{kwargs["reading_depth"].value}]-
        (:Reading)<-[:HasReading]-(word2)
        )
        WITH cp AS path
          SKIP 0
          LIMIT $reading_max
        RETURN collect(nodes(path)), collect(relationships(path))
        UNION
        MATCH(word1:Word {{writing: $word1}})
        MATCH(word2:Word {{writing: $word2}})
        MATCH p = ((word1)-[:HasCharacter]->(:Character)<-[:HasCharacter]-(word2)
        )
        WITH p AS path
          SKIP 0
          LIMIT $char_max
        RETURN collect(nodes(path)), collect(relationships(path));
        """,
            {
                "word1": kwargs["word1"].value,
                "word2": kwargs["word2"].value,
                "reading_max": kwargs["reading_max"].value,
                "meaning_max": kwargs["meaning_max"].value,
                "winfo_max": kwargs["winfo_max"].value,
                "char_max": kwargs["char_max"].value,
                "writing_max": kwargs["writing_max"].value,
            },
        )
