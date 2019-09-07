from components.kankeiforms.transforms import nested_list_transform, two_list_transform

WORD_LIMIT = 10
PARENT_COMP_LIMIT = 100


# note :: this query could be used as an extension of an autocorrelation...


def get_kanji_info(tx, value):
    result = tx.run(
        f"""
        MATCH (k1:Kanji{{writing: $value}})
        OPTIONAL MATCH p=(k1)-[:IsComposedOf]->(k2:Component)
        WITH [k1] + collect(DISTINCT k2)  AS ktot, collect(nodes(p)) as c_nodes, collect(relationships(p)) as c_links
        UNWIND ktot AS k
        OPTIONAL MATCH mp=(k)-[:HasMeaning]->(:Meaning:English)
        OPTIONAL MATCH rp=(k)-[:HasReading]->(:Reading:Japanese)
        OPTIONAL MATCH kp=(k)-[:HasArchaism|HasAlternative]->(:Character)
        //OPTIONAL MATCH wp=(k)<-[:HasCharacter]-(:Component)
        WITH
            collect(nodes(mp))
            + collect(nodes(rp))
            + collect(nodes(kp))
            //+ collect(nodes(wp))[..{WORD_LIMIT}]
            + c_nodes as nds,
            collect(relationships(mp))
            + collect(relationships(rp))
            + collect(relationships(kp))
            //+ collect(relationships(wp))
            + c_links AS lnks
        WITH apoc.coll.flatten(nds) as nds, apoc.coll.flatten(lnks) as lnks
        UNWIND nds AS nd
        WITH collect(DISTINCT nd) AS nodes, lnks
        UNWIND lnks as lnk
        RETURN nodes, collect(DISTINCT lnk) as links
        """,
        value=value,
    )

    return two_list_transform(result)
