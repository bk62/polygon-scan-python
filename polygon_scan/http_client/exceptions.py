class HTTPClientException(Exception):
    """Base exception"""

    pass


class InvalidArguments(HTTPClientException):
    pass


class RequestException(HTTPClientException):
    """Incomplete HTTP request related exception."""

    def __init__(self, original_exception, request_args, request_kwargs):
        self.original_exception = original_exception
        self.request_args = request_args
        self.request_kwargs = request_kwargs
        super().__init__(f"error with request {original_exception}")


class ResponseException(HTTPClientException):
    """Completed HTTP response related exception"""

    def __init__(self, response):
        self.response = response
        super().__init__(f"received {response.status_code} HTTP response")


class Forbidden(ResponseException):
    """Not authenticated or authorized"""


class InvalidJSON(ResponseException):
    """Response contained invalid JSON"""


class InvalidRequest(ResponseException):
    """Invalid request parameters"""


class NotFound(ResponseException):
    """URL not found"""


class Conflict(ResponseException):
    pass


class InvalidToken(ResponseException):
    pass


class Redirect(ResponseException):
    pass


class ServerError(ResponseException):
    pass


class MediaTypeError(ResponseException):
    pass


class TooLarge(ResponseException):
    pass


class TooManyRequests(ResponseException):
    pass


class UnavailableForLegalReasons(ResponseException):
    pass


class URITooLong(ResponseException):
    pass
