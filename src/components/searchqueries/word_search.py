word_search_query_suffix = f"""
    OPTIONAL MATCH (w)-[:HasDefinition]->(d:Definition)-[:HasMeaning]->(m:Meaning:English)
    WITH w,p, collect(m) AS m
    OPTIONAL MATCH (w)-[:HasReading]->(r:Reading:Japanese)
    WITH w,p,m, collect(r) AS r
    RETURN w AS word,
           m AS meaning,
           r AS reading,
           p
   ORDER BY p ASC
"""


def get_reading_search_body(reading_type, skip, limit):
    return f"""
    MATCH (r:Reading:Japanese {{{reading_type}: $value}})
    OPTIONAL MATCH p=(r)<-[:IsComposedOf*0..5]-(:Reading:Japanese)<-[:HasReading]-(w:Word)
    WHERE (w)-[:HasCharacter]->(:Kanji)
    WITH DISTINCT w, min(length(p)) AS p SKIP {skip} LIMIT {limit}
    {word_search_query_suffix}
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
    return tx.run(
        f"""
        MATCH (e:Word{{writing: $value}})
        OPTIONAL MATCH p=(e)-[:IsComposedOf]->(w1:Word)
        WITH e, [{{val:e, depth:-1}}]  + collect({{val:w1, depth: length(w1.writing) + 10}}) AS tot2
        OPTIONAL MATCH p=(e)<-[:IsComposedOf]-(w1:Word)
        WITH e,tot2 + collect({{val:w1, depth:length(w1.writing) + 10 }}) AS tot3
        UNWIND tot3 AS elems
        WITH DISTINCT elems.val  AS w, min(elems.depth) AS p SKIP {skip} LIMIT {limit}
        {word_search_query_suffix}
        """,
        value=string,
    )


def meaning_search(tx, string, skip=0, limit=default_limit):
    return tx.run(
        f"""
        MATCH (m:Meaning:English {{value: $value}})
        MATCH p=(m)-[:IsSynonym|IsComposedOf*0..5]-(n:Meaning:English)<-[:HasMeaning]
                -(d:Definition)<-[:HasDefinition]-(w:Word)
        WITH DISTINCT w, p LIMIT {path_limit}
        WITH DISTINCT w, min(length(p)) AS p SKIP {skip} LIMIT {limit}
        {word_search_query_suffix}
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
