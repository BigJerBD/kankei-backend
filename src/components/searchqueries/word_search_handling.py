import logging

from components.searchqueries.utils import cleanup_string, strip_tag, run_transaction
from tools import japanese as jp

log = logging.getLogger(__name__)


def make_search_selector(
    *,
    driver,
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
        log.info(f"starting search for : {string}")
        if tag:
            if tag == "reading":
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
            # note :: it is mandatory to have kanji first in this if
            if jp.has_kanji(string):
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
            "writing": hit["word"]["writing"],
            "meanings": [n["value"] for n in hit["meaning"]],
            "readings": [n["value"] for n in hit["reading"]],
        }
        for hit in (hits or [])
        # todo :: improve verification of bad query result
        if hit and hit.get("word")
    ]
