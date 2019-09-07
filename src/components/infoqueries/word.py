# note :: this query could be used as an extension of an autocorrelation...
from components.kankeiforms.transforms import two_list_transform


def get_word_info(tx, value):
    result = tx.run(
        f"""
        MATCH (w1:Word{{writing: $value}})
        OPTIONAL MATCH p=(w1)-[:IsComposedOf]->(w2:Word)
        WITH [w1] + collect(DISTINCT w2)  AS wtot, collect(nodes(p)) as c_nodes, collect(relationships(p)) as c_links
        UNWIND wtot AS w
        OPTIONAL MATCH mp=(w)-[:HasDefinition]->(d:Definition)-[:HasMeaning]->(:Meaning:English)
        OPTIONAL MATCH rp=(w)-[:HasReading]->(:Reading:Japanese)
        WITH
            collect(nodes(mp))
            + collect(nodes(rp))
            + c_nodes as nds,
            collect(relationships(mp))
            + collect(relationships(rp))
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
