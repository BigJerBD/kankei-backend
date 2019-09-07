import logging

import tools.japanese as jp
from components.searchqueries.utils import run_transaction, cleanup_string, strip_tag

log = logging.getLogger(__name__)


def make_search_selector(
    *,
    driver,
    kanji_callback,
    word_callback,
    meaning_callback,
    hiragana_callback,
    katakana_callback,
    romaji_callback,
    romaji_or_meaning_callback,
):
    def selector(string):

        string = cleanup_string(string)
        string, tag = strip_tag(string)
        log.info(f"starting search for : { string }")
        if tag:
            if tag == "kanji":
                function = kanji_callback
            elif tag == "reading":
                if jp.has_hiragana(string):
                    function = hiragana_callback
                elif jp.has_katakana(string):
                    function = katakana_callback
                else:
                    function = romaji_callback
            elif tag == "word":
                function = word_callback
            elif tag == "meaning":
                function = meaning_callback
            else:
                return selector(string)
        else:
            if jp.has_kanji(string):
                if len(string) == 1:
                    function = kanji_callback
                else:
                    function = word_callback

            elif jp.has_hiragana(string):
                function = hiragana_callback
            elif jp.has_katakana(string):
                function = katakana_callback
            else:
                function = romaji_or_meaning_callback

        hits = run_transaction(driver, function, string)
        return _transform_hits_to_result(hits)

    return selector


def _transform_hits_to_result(hits):
    return [
        {
            "writing": hit["kanji"]["writing"],
            "meanings": [n["value"] for n in hit["meaning"]],
            "readings": {
                "onyomi": [n["katakana"] for n in hit["onyomi"]],
                "kunyomi": [n["hiragana"] for n in hit["kunyomi"]],
            },
        }
        for hit in (hits or [])
        # todo :: improve verification of bad query result
        if hit and hit.get("kanji")
    ]
