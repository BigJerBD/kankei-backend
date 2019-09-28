import logging
from json import loads as jsonloads
from sanic import response

from components import kankeiforms as kankeiforms_module, neo4j_database, infoqueries
from components.kankeiforms.coloring_types import DEFAULT_COLORING_TYPES
from components.kankeiforms.shown_properties import DEFAULT_SHOWN_PROPERTIES
from components.searchqueries import get_kanji_search_handler, get_word_search_handler


# todo :: replace with blueprints for more a more standard Sanic/Flask Application :)


def inject_endpoints(app, config):  # noqa: C901
    kankeiforms = kankeiforms_module.get_kankeiforms(config)
    kankeiforms_info = kankeiforms_module.get_kankeiforms_dict(config)

    db_driver = neo4j_database.get_db_driver(config)
    kanji_search = get_kanji_search_handler(db_driver)
    word_search = get_word_search_handler(db_driver)

    @app.route("/api/queries_info")
    async def get_all_queries(request):
        return response.json(kankeiforms_info)

    @app.route("/api/graph_info")
    async def get_default_info(request):
        return response.json(
            {
                "shown_properties": DEFAULT_SHOWN_PROPERTIES,
                "coloring_types": DEFAULT_COLORING_TYPES,
            }
        )

    @app.route("/api/run_query/<group>/<name>", methods=["POST"])
    async def run_query(request, group, name):
        logging.info("executing query")

        # get query
        logging.debug(f"running query with {request.body}")
        grp = kankeiforms.get(group, None)

        if not grp:
            return response.json("Group does not exist", status=400)
        query = grp.get(name, None)
        if not query:
            return response.json("Group does not exist in this group", status=400)

        logging.debug(f"query fetched : {query}")
        try:
            result = query.run_query(db_driver, **jsonloads(request.body))
            return response.json(result)
        except ValueError as e:
            return response.json(str(e), status=422)

    @app.route("/api/search/word")
    async def search_word(request):
        if "value" in request.args:
            results = word_search(request.args.get("value"))
            return response.json(results)
        else:
            return response.json("value need to be in the query arguments")

    @app.route("/api/search/kanji")
    async def search_kanji(request):
        if "value" in request.args:
            results = kanji_search(request.args.get("value"))
            return response.json(results)
        else:
            return response.json("value need to be in the query arguments")

    @app.route("/api/info/kanji")
    async def info_kanji(request):
        if "value" in request.args:

            with db_driver.session() as session:
                result = session.read_transaction(
                    infoqueries.get_kanji_info, value=request.args.get("value")
                )

            return response.json(result)
        else:
            return response.json("value need to be in the query arguments")

    @app.route("/api/info/word")
    async def info_word(request):
        if "value" in request.args:
            with db_driver.session() as session:
                result = session.read_transaction(
                    infoqueries.get_word_info, value=request.args.get("value")
                )
            return response.json(result)

        else:
            return response.json("value need to be in the query arguments")
