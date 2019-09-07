from collections import OrderedDict


def make_shown_properties(props):
    return {
        "nodes": list(props["nodes"].items()),
        "relationships": list(props["relationships"].items()),
    }


DEFAULT_SHOWN_PROPERTIES = make_shown_properties(
    {
        "nodes": OrderedDict(
            # symbols
            [
                ("Character", "writing"),
                ("Kanji", "writing"),
                ("Component", "writing"),
                ("Radical", "writing"),
                # reading
                ("Reading", "value"),
                ("Japanese", "value"),
                ("Chinese", "value"),
                ("Korean", "value"),
                # Words
                ("Word", "writing"),
                ("WordInfo", "value"),
                ("Definition", ""),
                ("Usage", "value"),
                ("Meaning", "value"),
            ]
        ),
        "relationships": OrderedDict(
            [
                ("HasCharacter", ""),
                ("HasDefinition", "__self__"),
                ("HasInfo", "__self__"),
                ("HasMeaning", "__self__"),
                ("HasRadical", "__self__"),
                ("HasReading", "__self__"),
                ("HasStroke", "__self__"),
                ("IsComposedOf", ""),
                #
                ("IsAntonym", "__self__"),
                ("IsSynonym", "__self__"),
                ("IsFrequentWith", "__self__"),
                ("IsHypernym", "__self__"),
                ("IsHyponym", "__self__"),
                ("IsHolonym", "__self__"),
                ("IsMeronym", "__self__"),
                ("HasArchaism", "__self__"),
                ("HasAlternative", "__self__"),
            ]
        ),
    }
)
