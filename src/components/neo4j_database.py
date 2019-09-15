import logging

import neobolt.exceptions
from neo4j import GraphDatabase

log = logging.getLogger(__name__)


def get_db_driver(config):
    try:
        db_driver = GraphDatabase.driver(
            config.DB_URI, auth=(config.DB_USER, config.DB_PASSWORD)
        )
    except neobolt.exceptions.ServiceUnavailable as e:

        if config.DB_ALLOW_NONE:
            log.error("Could not connect to the database")
            db_driver = None
        else:
            raise e

    return db_driver
