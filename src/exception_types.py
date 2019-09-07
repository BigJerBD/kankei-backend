# todo :: adding status code and message is making the design heavier
#  do it more simply


class BaseSendableException(Exception):
    """
    base exception that can be sent through rest
    """

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


class QueryDoesNotExist(BaseSendableException):
    status_code = 404


class InvalidArgumentError(BaseSendableException):
    status_code = 422
