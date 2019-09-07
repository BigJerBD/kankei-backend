# noinspection PyUnresolvedReferences
import logging

from settings.base import dir_path

# Logging
LOGGING_LEVEL = logging.INFO
SANIC_DEBUG = False

STATIC_FOLDER = f"{dir_path}/../../../dist/static"
FRONTEND_LOCATION = "TEMPLATE"
FRONTEND_PATH = f"{dir_path}/../../../dist"

BACKEND_URL = "0.0.0.0:5000"
DB_URI = "bolt://kankeidb:7687"
