# todo move in the future into a neo4j query handling module


def two_list_transform(records):
    nodes, relations = records.values()[0]
    return {
        "nodes": {
            int(node.id): {
                "id": int(node.id),
                "labels": list(node.labels),
                "data": node._properties,
            }
            for node in nodes
        },
        "relationships": {
            int(rel.id): {
                "id": int(rel.id),
                "from": int(rel.start),
                "to": int(rel.end),
                "type": rel.type,
                "data": rel._properties,
            }
            for rel in relations
        },
    }


def nested_list_transform(records):
    nodes, relations = records.values()[0]
    return {
        "nodes": {
            int(node.id): {
                "id": int(node.id),
                "labels": list(node.labels),
                "data": node._properties,
            }
            for nodelist in nodes
            for node in nodelist
        },
        "relationships": {
            int(rel.id): {
                "id": int(rel.id),
                "from": int(rel.start),
                "to": int(rel.end),
                "type": rel.type,
                "data": rel._properties,
            }
            for rellist in relations
            for rel in rellist
        },
    }


def double_nested_list_transform(records):
    result = {"nodes": [], "relationships": []}
    for nodes, relations in records.values()[0]:
        result["nodes"] += [
            {"id": int(node.id), "labels": list(node.labels), "data": node._properties}
            for nodelist in nodes
            for node in nodelist
        ]
        result["relationships"] += [
            {
                "id": int(rel.id),
                "from": int(rel.start),
                "to": int(rel.end),
                "type": rel.type,
                "data": rel._properties,
            }
            for rellist in relations
            for rel in rellist
        ]
    return {
        "nodes": {int(i["id"]): i for i in result["nodes"]},
        "relationships": {int(i["id"]): i for i in result["relationships"]},
    }
