from tools.japanese import has_hiragana, has_katakana

ALL_NODES = [
    "Character",
    "Component",
    "Radical",
    "Stroke",
    "Meaning",
    "Reading",
    "Japanese",
    "Definition",
    "WordInfo",
    "Word",
    "Chinese",
    "Korean",
    "English",
    "French",
    "Spanish",
    "Portugese",
    "Kanji",
    "PartOfSpeech",
    "Domain",
    "Usage",
    "Dialect",
    "Computed",
]

ALL_NODES_MAIN = [
    "Character",
    "Kanji",
    "Component",
    "Radical",
    "Reading",
    "Stroke",
    "Word",
    "PartOfSpeech",
    "Domain",
    "Usage",
    "Dialect",
    "Usage",
    "Definition",
    "Meaning",
]

ALL_RELATIONSHIPS = [
    "HasMeaning",
    "HasReading",
    "IsComposedOf",
    "HasStroke",
    "HasDefinition",
    "HasInfo",
    "HasRadical",
    "HasCharacter",
    "HasSimilarSound",
    "IsAntonym",
    "IsSynonym",
    "HasArchaism",
    "HasAlternative",
    "IsHypernym",
    "IsHyponym",
    "IsHolonym",
    "IsMeronym",
    "IsFrequentWith",
]

MEANING_SUBPATHS_PARTIAL = ":%s" % "|".join(
    [
        "IsAntonym",
        "IsSynonym",
        "IsHypernym",
        "IsHyponym",
        "IsMeronym",
        "IsHolonym",
        "IsComposedOf",
        "IsFrequentWith",
    ]
)
MEANING_SUBPATHS_FULL = ":%s" % "|".join(
    ["IsSynonym", "IsHypernym", "IsHyponym", "IsMeronym", "IsHolonym", "IsComposedOf"]
)
READING_SUB_PATH = ":%s" % "|".join(["HasSimilarSound", "IsComposedOf"])
KANJI_SUBSYMBOLS = ":%s" % "|".join(["IsComposedOf", "HasRadical"])
KANJI_SIBLINGS = ":%s" % "|".join(["HasArchaism", "HasAlternative"])


def get_reading_key(value):
    return (
        "hiragana"
        if has_hiragana(value)
        else "katakana"
        if has_katakana(value)
        else "romaji"
    )
