import base64
import os
from time import sleep
import pytest

from betamax import Betamax
from betamax.decorator import use_cassette

from tests.custom_betamax import CustomURIMatcher, CustomQueryMatcher


APIKEY = os.getenv("POLYGON_SCAN_API_KEY", "APIKEY")
SLEEP_BETWEEN_TESTS = int(os.getenv("SLEEP_BETWEEN_TESTS", 0))
BETAMAX_RECORD_MODE = os.getenv("BETAMAX_RECORD_MODE")


Betamax.register_request_matcher(CustomQueryMatcher)
Betamax.register_request_matcher(CustomURIMatcher)

with Betamax.configure() as config:
    config.cassette_library_dir = "tests/fixtures/cassettes"
    config.define_cassette_placeholder(
        "B64APIKEY", base64.b64encode(APIKEY.encode("utf-8")).decode("utf-8")
    )
    config.define_cassette_placeholder("APIKEY", APIKEY)

    record_mode = "once"
    if BETAMAX_RECORD_MODE and BETAMAX_RECORD_MODE in (
        "once",
        "new_episodes",
        "all",
        "none",
    ):
        record_mode = BETAMAX_RECORD_MODE
    config.default_cassette_options["record_mode"] = record_mode

    # custom matcher
    config.default_cassette_options["match_requests_on"] = ["method", "custom_uri"]


@pytest.fixture(autouse=SLEEP_BETWEEN_TESTS)
def slow_down_api_tests():
    if SLEEP_BETWEEN_TESTS:
        sleep(SLEEP_BETWEEN_TESTS)
