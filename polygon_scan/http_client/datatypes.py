from dataclasses import dataclass

import requests


@dataclass(frozen=True, eq=True)
class RateLimit:
    """`limit` calls per `limit_time_interval` seconds"""

    limit: int
    limit_time_interval: int

    def __str__(self) -> str:
        return f"{self.limit} calls / {self.limit_time_interval}s"


@dataclass
class ClientResponse:
    """Wraps requests Response and parsed json for convenience."""

    response: requests.Response
    response_dict: dict = None
