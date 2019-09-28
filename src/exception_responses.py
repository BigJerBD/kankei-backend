#
# for exc in default_exceptions:
#     app.register_error_handler(exc, handle_interal_error)
import logging
import traceback


from neobolt.exceptions import ClientError
from sanic import response
from sanic.handlers import ErrorHandler


class CustomErrorHandler(ErrorHandler):
    def default(self, request, e):
        return default_response(request, e)


def default_response(request, e):
    code = 500
    logging.error(f"Internal Error :: {e}")
    logging.error(traceback.format_exc())
    return response.json("Internal Server Error", status=code)


def inject_exceptions_responses(app, config):
    app.error_handler = CustomErrorHandler()

    @app.exception(ClientError)
    async def handle_client_errors(request, e):
        if e.code == "Neo.ClientError.Transaction.TransactionTimedOut":
            return response.json(
                f"Query Timeout : The query took over {config.DB_TIMEOUT_SEC} second",
                status=408,
            )
        else:
            return default_response(request, e)
