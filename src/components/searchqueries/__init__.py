from components.searchqueries import kanji_search as sk
from components.searchqueries import word_search as sw
from components.searchqueries import kanji_search_handling, word_search_handling


def get_kanji_search_handler(driver):
    return kanji_search_handling.make_search_selector(
        driver=driver,
        kanji_callback=sk.kanji_search,
        word_callback=sk.word_search,
        meaning_callback=sk.meaning_search,
        hiragana_callback=sk.reading_hira_search,
        katakana_callback=sk.reading_kata_search,
        romaji_callback=sk.romaji_search,
        romaji_or_meaning_callback=sk.romaji_or_meaning_callback,
    )


def get_word_search_handler(driver):
    return word_search_handling.make_search_selector(
        driver=driver,
        word_callback=sw.word_search,
        meaning_callback=sw.meaning_search,
        hiragana_callback=sw.reading_hira_search,
        katakana_callback=sw.reading_kata_search,
        romaji_callback=sw.romaji_search,
        romaji_or_meaning_callback=sw.romaji_or_meaning_callback,
    )
