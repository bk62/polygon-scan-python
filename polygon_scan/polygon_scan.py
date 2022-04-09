import logging
import requests
from .http_client import Client, RateLimit
from .http_client.exceptions import InvalidRequest
from .modules import Account
from .exceptions import APIException, ClientException
from .datatypes import AttrDict
from .const import TIMEOUT, RATE_LIMITS, __version__, ENDPOINT_URLS


logger = logging.getLogger("polygon_scan")


class PolygonScan:
    def __init__(
        self,
        api_key=None,
        network=None,
        tag="latest",
        api_tier="free",
        http_client=None,
        **http_client_kwargs,
    ):
        self._api_key = api_key
        self._api_tier = api_tier

        if self._api_key is None:
            self._api_tier = "free"
            logger.warn(f"API key not set. Rate limit set to {RATE_LIMITS['none']}")
        if api_tier not in RATE_LIMITS.keys():
            if isinstance(api_tier, RateLimit):
                self._api_tier = "custom"
                self._api_tier = api_tier
            logger.warn(
                f"Invalid API tier {api_tier}. Set to Free tier with rate limit {RATE_LIMITS['free']}"
            )
        else:
            self._rate_limit = RATE_LIMITS[api_tier]
        self._network = network or "mainnet"
        if network == "mainnet":
            self._endpoint_url = ENDPOINT_URLS[network]
        else:
            self._endpoint_url = ENDPOINT_URLS["mumbai"]
        self._tag = tag

        if "params" in http_client_kwargs:
            http_client_kwargs["params"] = {
                **http_client_kwargs["params"],
                **self._get_params(),
            }
        else:
            http_client_kwargs["params"] = self._get_params()
        http_client_kwargs["rate_limit"] = (
            http_client_kwargs.get("rate_limit", None) or self._rate_limit
        )
        self._http_client = http_client or Client(**http_client_kwargs)

        self.account = Account(self)

    def _get_params(self):
        return {"api_key": self._api_key, "tag": self._tag}

    def request(self, params=None, **kwargs):
        params = params or {}
        kwargs.update(params=params)
        # TODO parse_json=False or test is json here, b/c api returns html sometimes (? check)
        return self._http_client.request(self._endpoint_url, **kwargs)
