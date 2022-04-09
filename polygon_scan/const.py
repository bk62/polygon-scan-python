import os
from .http_client.datatypes import RateLimit

__version__ = "0.1.0"

TIMEOUT = float(os.environ.get("polygon_scan_timeout", 16))


# https://docs.polygonscan.com/support/rate-limits


RATE_LIMITS = {
    "none": RateLimit(2, 5),
    "free": RateLimit(10, 1),
    "standard": RateLimit(20, 1),
    "pro": RateLimit(30, 1),
}


ENDPOINT_URLS = {
    "mainnet": "https://api.polygonscan.com/api",
    "mumbai": "https://api-testnet.polygonscan.com/api",
}
