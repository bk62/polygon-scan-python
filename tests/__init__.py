import base64, os
from betamax import Betamax
from betamax.decorator import use_cassette

api_key = os.getenv("POLYGON_SCAN_API_KEY", "placeholder_test_api_key")

with Betamax.configure() as config:
    config.cassette_library_dir = "tests/fixtures/cassettes"
    config.define_cassette_placeholder(
        "<B64-API-KEY>", base64.b64encode(api_key.encode("utf-8")).decode("utf-8")
    )
    config.define_cassette_placeholder("<API-KEY>", api_key)
