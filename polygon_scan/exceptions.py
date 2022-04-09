class BaseException(Exception):
    """Base Exception that all other exceptions derive from."""

    pass


class APIException(BaseException):
    """Exceptions involving error messages from PolygonScan API"""

    pass


class ClientException(BaseException):
    """Exceptions involving errors on the client side"""

    pass
