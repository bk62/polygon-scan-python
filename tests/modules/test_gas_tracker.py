import pytest
from polygon_scan import PolygonScan
from polygon_scan.datatypes import APIResponse, AttrDict
from polygon_scan.utils import is_seq

from tests import APIKEY


@pytest.fixture
def gas_oracle_keys():
    return [
        "LastBlock",
        "SafeGasPrice",
        "ProposeGasPrice",
        "FastGasPrice",
        "suggestBaseFee",
        "gasUsedRatio",
        "UsdPrice",
    ]


def test_get_gas_oracle(betamax_session, gas_oracle_keys):
    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.gas_tracker.get_gas_oracle()

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(gas_oracle_keys).issubset(resp.result[0].keys())
