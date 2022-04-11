import pytest
from polygon_scan import PolygonScan
from polygon_scan.datatypes import APIResponse, AttrDict
from polygon_scan.utils import is_seq

from tests import APIKEY


def test_get_matic_total_supply(betamax_session):
    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.stats.get_matic_total_supply()

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert is_seq(resp.result)
    assert str.isnumeric(resp.result[0])


@pytest.fixture
def matic_price_keys():
    return ["maticbtc", "maticbtc_timestamp", "maticusd", "maticusd_timestamp"]


def test_get_matic_last_price(betamax_session, matic_price_keys):
    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.stats.get_matic_last_price()

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert is_seq(resp.result)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(matic_price_keys)
