class BaseException(Exception):
    """Base Exception that all other exceptions derive from."""

    pass


class APIException(BaseException):
    """Exceptions involving error messages from PolygonScan API"""

    def __init__(self, response_dict):
        self.response_dict = response_dict
        super().__init__(
            f'API Error: ({response_dict["status"]} {response_dict["message"]}) {response_dict["result"]}'
        )


class ClientException(BaseException):
    """Exceptions involving errors on the client side"""

    pass
