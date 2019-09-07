import logging

import neobolt.exceptions
from neo4j import GraphDatabase

log = logging.getLogger(__name__)


def get_db_driver(config):

    db_driver = GraphDatabase.driver(
        config.DB_URI, auth=(config.DB_USER, config.DB_PASSWORD)
    )
    return db_driver
