import pytest
from polygon_scan import PolygonScan
from polygon_scan.const import ENDPOINT_URLS, RATE_LIMITS
from polygon_scan.http_client.datatypes import RateLimit
from tests import api_key


def test_polygon_scan_no_api_tier_arg_sets_unauthenticated_api_tier():
    pg_scan = PolygonScan()

    assert pg_scan.rate_limit == RATE_LIMITS["none"]


def test_polygon_scan_setting_rate_limit_sets_custom_api_tier():
    r = RateLimit(14, 5)
    pg_scan = PolygonScan(api_tier=r)

    assert pg_scan.rate_limit == r
    assert pg_scan._api_tier == "custom"


def test_polygon_scan_setting_mumbai_or_testnet_works():
    pg_scan1 = PolygonScan(network="mumbai")
    pg_scan2 = PolygonScan(network="testhet")

    assert pg_scan1.endpoint_url == ENDPOINT_URLS["mumbai"]
    assert pg_scan2.endpoint_url == ENDPOINT_URLS["mumbai"]


def test_polygon_scan_params_set_in_http_client_session_params():
    pg_scan = PolygonScan(api_key="<API_KEY>", tag="<TAG")

    assert pg_scan.http_client.session.params["apikey"] == "<API_KEY>"


def test_polygon_scan_http_client_kwargs(mocker):
    session = mocker.Mock(headers={})
    pg_scan = PolygonScan(session=session)

    assert pg_scan.http_client.session is session
