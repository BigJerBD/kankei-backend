from tools import japanese

kanji_search_query_suffix = f"""
    OPTIONAL MATCH (k)-[:HasMeaning]->(m:Meaning:English)
    WITH k,p, collect(m) AS m
    OPTIONAL MATCH (k)-[:HasReading{{type_reading: 'kun'}}]->(kr:Reading:Japanese)
    WITH k,m,p, collect(kr) AS kr
    OPTIONAL MATCH (k)-[:HasReading{{type_reading: 'on'}}]->(oy:Reading:Japanese)
    WITH k ,m, kr, p, collect(oy) AS oy
    OPTIONAL MATCH (k)<-[:HasCharacter]-(w:Word)
    RETURN k AS kanji,
           m AS meaning,
           kr AS kunyomi,
           oy AS onyomi,
           count(w) AS w, p
   ORDER BY p ASC, w DESC
"""


def get_reading_search_body(reading_type, skip, limit):
    return f"""
    MATCH (r:Reading:Japanese {{{reading_type}: $value}})
    OPTIONAL MATCH p=(r)-[:IsComposedOf*0..5]->(:Reading:Japanese)<-[:HasReading]-(k:Kanji)
    WITH DISTINCT k, min(length(p)) AS p SKIP {skip} LIMIT {limit}
    {kanji_search_query_suffix}
    """


default_limit = 50
path_limit = 100


def reading_hira_search(tx, string, skip=0, limit=default_limit):
    return tx.run(get_reading_search_body("hiragana", skip, limit), value=string)


def reading_kata_search(tx, string, skip=0, limit=50):
    return tx.run(get_reading_search_body("katakana", skip, limit), value=string)


def romaji_search(tx, string, skip=0, limit=default_limit):
    return tx.run(get_reading_search_body("romaji", skip, limit), value=string)


def word_search(tx, string, skip=0, limit=default_limit):
    all_kanji = [c for c in string if japanese.has_kanji(c)]
    return tx.run(
        f"""
        UNWIND [{",".join(f"'{k}'" for k in all_kanji)}] AS val
        MATCH (k:Character:Kanji{{writing:val}})
        WITH DISTINCT k, 0 AS p SKIP {skip} LIMIT {limit}
        {kanji_search_query_suffix}
        """
    )


def kanji_search(tx, string, skip=0, limit=default_limit):
    return tx.run(
        f"""
        MATCH (e:Kanji{{writing: $value}})
        OPTIONAL MATCH (e)-[:HasAlternative|:HasArchaism]->(k1:Character)
        WITH k1,e
        WITH e, [{{val:e, depth:-1}}] + collect({{val:k1, depth:1}}) AS tot
        OPTIONAL MATCH p=(e)-[:IsComposedOf*0..5]->(k1:Character)
        WITH e,tot + collect({{val:k1, depth:length(p) + 10}}) AS tot2
        OPTIONAL MATCH p=(e)<-[:IsComposedOf*0..5]-(k1:Character)
        WITH e,tot2 + collect({{val:k1, depth:length(p) + 20}}) AS tot3
        UNWIND tot3 AS elems
        WITH DISTINCT elems.val  AS k, min(elems.depth) AS p SKIP {skip} LIMIT {limit}
        {kanji_search_query_suffix}
        """,
        value=string,
    )


def meaning_search(tx, string, skip=0, limit=default_limit):
    return tx.run(
        f"""
        MATCH (m:Meaning:English {{value: $value}})
        MATCH p=(m)-[:IsSynonym|IsComposedOf*0..5]-(n:Meaning:English)<-[:HasMeaning]-(k:Kanji)
        WITH DISTINCT k, p LIMIT {path_limit}
        WITH DISTINCT k, min(length(p)) AS p SKIP {skip} LIMIT {limit}
        {kanji_search_query_suffix}
        """,
        value=string,
    )


def romaji_or_meaning_callback(tx, string, skip=0, limit=default_limit):
    result1 = meaning_search(tx, string, skip, limit).data()

    remaining_limit = limit - len(result1)
    if remaining_limit > 0:
        result2 = romaji_search(tx, string, skip, remaining_limit).data()
        return result1 + result2
    else:
        return result1
