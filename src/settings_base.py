# util function for prettier config
import logging
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# LOGGING
LOGGING_LEVEL = logging.INFO

# SANIC
SANIC_DEBUG = False
CORS_AUTOMATIC_OPTIONS = True
KEEP_ALIVE_TIMEOUT = os.environ.get("KANKEI__SANIC__KEEP_ALIVE_TIMEOUT", 10)
WORKER_COUNT = os.environ.get("KANKEI__SANIC__WORKER_COUNT", 8)
PROXIES_COUNT = os.environ.get("KANKEI__SANIC__PROXIES_COUNT", 1)

# DATABASE
DB_URI = os.environ.get("KANKEI__DB__URI", "bolt://localhost:7687")
DB_USER = os.environ.get("KANKEI__DB__USER", "neo4j")
DB_PASSWORD = os.environ.get("KANKEI__DB__PASSWORD", "neo4j")
DB_TIMEOUT_SEC = os.environ.get("KANKEI__DB__TIMEOUT_SEC", 30)
DB_ALLOW_NONE = False

# STATIC
STATIC_FOLDER = "../dist/static"
STATIC_PATH = "/static"

# BACKEND
BACKEND_URL = os.environ.get("KANKEI__BACKEND__URL", "0.0.0.0:5000")
