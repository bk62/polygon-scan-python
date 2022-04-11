import pytest
from polygon_scan import PolygonScan
from polygon_scan.datatypes import APIResponse, AttrDict

from tests import APIKEY


@pytest.fixture
def txn_receipt_keys():
    return ["status"]


def test_check_transaction_receipt_status(betamax_session, txn_receipt_keys):
    test_txn_hash = "0x591ca00bf6b404e24e21732023abc0416673beff9586f37e61fb0f07ca560940"

    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.transaction.check_transaction_receipt_status(test_txn_hash)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(txn_receipt_keys)
