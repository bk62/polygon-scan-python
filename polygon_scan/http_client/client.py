"""HTTP API Client implementation WIP."""

import logging

import requests
from requests.exceptions import ChunkedEncodingError, ConnectionError, ReadTimeout
from requests.status_codes import codes

from .retry import FiniteRetryStrategy
from .const import TIMEOUT
from .rate_limiter import SimpleRateLimiter
from .datatypes import ClientResponse
from .exceptions import (
    InvalidJSON,
    InvalidRequest,
    InvalidArguments,
    NotFound,
    Redirect,
    RequestException,
    ServerError,
    Conflict,
    Forbidden,
    MediaTypeError,
    TooLarge,
    TooManyRequests,
    URITooLong,
    UnavailableForLegalReasons,
)

logger = logging.getLogger(__package__)


RETRY_EXCEPTIONS = (ChunkedEncodingError, ConnectionError, ReadTimeout)
RETRY_STATUSES = {
    520,
    522,
    codes["bad_gateway"],
    codes["gateway_timeout"],
    codes["internal_server_error"],
    codes["request_timeout"],
    codes["service_unavailable"],
}
STATUS_EXCEPTIONS = {
    codes["bad_gateway"]: ServerError,
    codes["bad_request"]: InvalidRequest,
    codes["conflict"]: Conflict,
    codes["found"]: Redirect,
    codes["forbidden"]: Forbidden,
    codes["gateway_timeout"]: ServerError,
    codes["internal_server_error"]: ServerError,
    codes["media_type"]: MediaTypeError,
    codes["moved_permanently"]: Redirect,
    codes["not_found"]: NotFound,
    codes["request_entity_too_large"]: TooLarge,
    codes["request_uri_too_large"]: URITooLong,
    codes["service_unavailable"]: ServerError,
    codes["too_many_requests"]: TooManyRequests,
    codes["unauthorized"]: Forbidden,
    codes[
        "unavailable_for_legal_reasons"
    ]: UnavailableForLegalReasons,  # Cloudflare status (not named in requests)
    520: ServerError,
    522: ServerError,
}
SUCCESS_STATUSES = {codes["accepted"], codes["created"], codes["ok"]}


class Client:
    """HTTP API Client class"""

    @staticmethod
    def _log_request(url, kwargs):
        logger.debug(f"Requesting: {url}")
        logger.debug(f"Kwargs: {kwargs}")

    def __init__(
        self,
        rate_limiter=None,
        retry_strategy=None,
        timeout=TIMEOUT,
        rate_limit=None,
        session=None,
        **session_kwargs,
    ):
        # TODO option to disable rate limiting
        self._rate_limiter = rate_limiter or SimpleRateLimiter(rate_limit)
        self._retry_strategy = retry_strategy or FiniteRetryStrategy()
        self._timeout = timeout

        self.session = session or requests.Session()
        for key in ("params", "headers", "hooks", "proxies"):
            if key in session_kwargs:
                self.session.params.update(session_kwargs[key])

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def request(self, url, method="GET", **kwargs):
        kwargs.update(method=method)
        return self._request_with_retries(url, **kwargs)

    def _request_with_retries(self, url, parse_json=True, **kwargs):
        self._retry_strategy.sleep()
        self._log_request(url, kwargs)
        response, exception = self._make_request(url, **kwargs)

        retry = False
        if self._retry_strategy.retry_on_failure() and (
            retry or response is None or response.status_code in RETRY_STATUSES
        ):
            self._retry_request(url, response, exception, **kwargs)
        elif response.status_code in STATUS_EXCEPTIONS:
            raise STATUS_EXCEPTIONS[response.status_code](response)
        elif response.status_code == codes["no_content"]:
            return {}
        assert (
            response.status_code in SUCCESS_STATUSES
        ), f"Unexpected status code: {response.status_code}"
        if response.headers.get("content-length") == "0":
            return {}

        client_response = ClientResponse(response)
        if parse_json:
            try:
                client_response.response_dict = response.json()
            except ValueError:
                raise InvalidJSON(response)
        return client_response

    def _retry_request(self, url, response, exception, **kwargs):
        if exception:
            status = repr(exception)
        else:
            status = response.status_code
        logger.warning(f"retrying due to {status}: {url}")
        self._retry_strategy.consume_retry()
        return self._request_with_retries(url, **kwargs)

    def _make_request(self, url, **kwargs):
        try:
            response = self._rate_limiter(self._request, url, **kwargs)
            logger.debug(
                f"{url} {response.status_code} ({response.headers.get('content-length')} bytes)"
            )
            return response, None
        except RequestException as exc:
            if not self._retry_strategy.retry_on_failure() or not isinstance(
                exc.original_exception, RETRY_EXCEPTIONS
            ):
                raise
            return None, exc.original_exception

    def _request(self, *args, timeout=None, **kwargs):
        logger.debug("client request", args, kwargs)
        method = kwargs["method"]
        del kwargs["method"]  # requests expects method in args
        try:
            return self.session.request(
                method, *args, timeout=timeout or self._timeout, **kwargs
            )
        except Exception as exc:
            raise RequestException(exc, args, kwargs)

    def close(self):
        self.session.close()
