# noinspection PyUnresolvedReferences
from settings.base import *
import logging

# todo :: put prod level setting configurable from env-variable
# Logging
LOGGING_LEVEL = logging.INFO
SANIC_DEBUG = False

BACKEND_URL = "0.0.0.0:5000"
DB_URI = "bolt://kankei-db:7687"
