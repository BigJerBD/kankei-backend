from tools.japanese import has_hiragana, has_katakana

meaning_broad_subpathing = ":%s" % "|".join(
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

meaning_limited_subpathing = ":%s" % "|".join(
    ["IsSynonym", "IsHypernym", "IsHyponym", "IsMeronym", "IsHolonym", "IsComposedOf"]
)

reading_subpathing = ":%s" % "|".join(["HasSimilarSound", "IsComposedOf"])


kanji_subwriting = ":%s" % "|".join(["IsComposedOf", "HasRadical"])

kanji_siblings = ":%s" % "|".join(["HasArchaism", "HasAlternative"])


def get_reading_key(value):
    return (
        "hiragana"
        if has_hiragana(value)
        else "katakana"
        if has_katakana(value)
        else "romaji"
    )
