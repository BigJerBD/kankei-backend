# todo move in the future into a neo4j query handling module


def two_list_transform(records):
    """
    transform that simply add the necessary value
    :param records:
    :return:
    """
    values = records.values()
    nodes, relations = values[0] if values else [[], []]
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
    """
    transform used to take a Tuple[List[List[Node]],List[List[Edge]]
    and convert it into a Tuple[List[Node],List[Edge]

    :param records:
    :return:
    """
    values = records.values()
    nodes, relations = values[0] if values else [[], []]
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
