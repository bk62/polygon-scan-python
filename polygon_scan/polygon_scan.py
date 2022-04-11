"""Module containing the main PolygonScan class."""
import logging, os
from .http_client import Client, RateLimit
from .http_client.exceptions import InvalidRequest
from .modules import Account, Contract, Transaction, Block, Logs, Token
from .exceptions import APIException, ClientException
from .datatypes import AttrDict, APIResponse
from .const import TIMEOUT, RATE_LIMITS, __version__, ENDPOINT_URLS


ENV_API_KEY = os.environ.get("POLYGON_SCAN_API_KEY", None)


logger = logging.getLogger("polygon_scan")


class PolygonScan:
    """Main PolygonScan class.

    Attributes
    ----------
    network: str
        Polygon network, mainnet or testnet (mumbai)
    endpoint_url: str
        API Endpoint URL
    rate_limit: polygon_scan.datatypes.RateLimit
        Rate limit used by this PolygonScan API client instance
    http_client: polygon_scan.http_client.Client
        Http Client instance used by this PolygonScan API client instance

    account: polygon_scan.modules.Account
        Account helper container for all account API calls

    Methods
    -------
    request(params, **kwargs)
        Return data from endpoint with url parameters `params`.

    """

    def __init__(
        self,
        api_key=ENV_API_KEY,
        network=None,
        tag="latest",
        api_tier="none",
        http_client=None,
        **http_client_kwargs,
    ):
        """
        Parameters
        ----------
        api_key: str, optional, default `os.env.get("ENV_API_KEY", None)`
            Polygon Scan API key
        network: str, optional, default `mainnet`
            `mainnet` or `testnet` (or `mumbai`)
        tag: str, optional, default `latest`
            API tag
        api_tier: str or polygon_scan.http_client.RateLimit, optional, default `none`
            API tier (`free`, `standard`, `pro`) or a RateLimit instance to specify a custom rate limit. Used to set API rate limits.
        http_client: polygon_scan.http_client.Client, optional
            Client instance
        http_client_kwargs: kwargs, optional
            Extra kwargs to send to http client.
        """

        self._api_key = api_key
        self._api_tier = api_tier

        if self._api_key is None:
            self._api_tier = "free"
            logger.warn(f"API key not set. Rate limit set to {RATE_LIMITS['none']}")
        if api_tier not in RATE_LIMITS.keys():
            if isinstance(api_tier, RateLimit):
                self._api_tier = "custom"
                self._rate_limit = api_tier
            else:
                self._api_tier = "none"
                self._rate_limit = RATE_LIMITS[api_tier]
                logger.warn(
                    f"Invalid API tier {api_tier}. Set to unauthenticated tier with rate limit {RATE_LIMITS['none']}"
                )
        else:
            self._rate_limit = RATE_LIMITS[api_tier]
        self._network = network or "mainnet"
        if self._network == "mainnet":
            self._endpoint_url = ENDPOINT_URLS["mainnet"]
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
        if http_client:
            http_client.session.params.update(self._get_params())
        self._http_client = http_client or Client(**http_client_kwargs)

        self.account = Account(self)
        self.contract = Contract(self)
        self.transaction = Transaction(self)
        self.block = Block(self)
        self.logs = Logs(self)
        self.token = Token(self)

    @property
    def network(self):
        return self._network

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @property
    def rate_limit(self):
        return self._rate_limit

    @property
    def http_client(self):
        return self._http_client

    def _get_params(self):
        return {"apikey": self._api_key, "tag": self._tag}

    def request(self, params=None, **kwargs) -> APIResponse:
        """Request the API endpoint url using `params` and return the parsed JSON."""
        params = params or {}
        kwargs.update(params=params)
        # TODO parse_json=False or test is json here, b/c api returns html sometimes (? check)
        # return and store request and response metadata for debugging
        response = self._http_client.request(self._endpoint_url, **kwargs)
        if response.response_dict["status"] == "0":
            raise APIException(response)
        response = APIResponse(response)
        return response
