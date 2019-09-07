import logging
import os

from sanic import Sanic
from sanic_cors import CORS

from endpoints import inject_endpoints
from exception_responses import inject_exceptions_responses


def set_static(app, config):
    app.static(config.STATIC_PATH, config.STATIC_FOLDER)


def set_logging(config):
    logging.basicConfig(level=config.LOGGING_LEVEL)


def get_app():
    app = Sanic(__name__)
    if "KANKEI_WEB_SETTINGS" in os.environ:
        app.config.from_envvar("KANKEI_WEB_SETTINGS")
    else:
        app.config.from_object("settings_default")
    return app


def start_server():
    app = get_app()
    config = app.config
    set_logging(config)
    set_static(app, config)

    inject_endpoints(app=app, config=config)
    inject_exceptions_responses(app=app, config=config)

    if config.ALLOW_CORS:
        # todo :: allow cors for static file?
        CORS(app, resources={r"/api/*": {"origins": "*"}})

    *host, port = app.config.BACKEND_URL.split(":")
    app.run(
        host="".join(host),
        port=int(port),
        workers=config.WORKER_COUNT,
        debug=config.SANIC_DEBUG,
    )


if __name__ == "__main__":
    start_server()
