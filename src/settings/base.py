# util function for prettier config
import logging
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Logging
LOGGING_LEVEL = logging.DEBUG

# SANIC
SANIC_DEBUG = True
KEEP_ALIVE_TIMEOUT = 10
WORKER_COUNT = 5

# DB AND QUERIES
DB_URI = "bolt://localhost:7687"
DB_USER = "neo4j"
DB_PASSWORD = "relation"
DB_TIMEOUT_SEC = 30

# STATIC CONTENT
STATIC_FOLDER = "../dist/static"
STATIC_PATH = "/static"

# ROUTING
BACKEND_URL = "localhost:5000"
ALLOW_CORS = False
