import pytest
from polygon_scan import PolygonScan
from polygon_scan.datatypes import APIResponse, AttrDict

from tests import APIKEY


@pytest.fixture
def test_contract_address():
    return "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"


@pytest.fixture
def abi_keys():
    return []


def test_get_contract_abi(betamax_session, test_contract_address):

    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.contract.get_contract_abi(test_contract_address)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], str)
    # assert set(resp.result[0].keys()).issubset(abi_keys)


@pytest.fixture
def source_keys():
    return [
        "SourceCode",
        "ABI",
        "ContractName",
        "CompilerVersion",
        "OptimizationUsed",
        "Runs",
        "ConstructorArguments",
        "EVMVersion",
        "Library",
        "LicenseType",
        "Proxy",
        "Implementation",
        "SwarmSource",
    ]


def test_get_contract_source(betamax_session, test_contract_address, source_keys):
    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.contract.get_contract_source(test_contract_address)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(source_keys)
