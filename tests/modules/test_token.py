import pytest
from polygon_scan import PolygonScan
from polygon_scan.datatypes import APIResponse, AttrDict
from polygon_scan.modules import contract
from polygon_scan.utils import is_seq


from tests import APIKEY


def test_get_token_total_supply_by_contract_address(betamax_session):
    contract_address = "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619"

    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.token.get_token_total_supply_by_contract_address(contract_address)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert is_seq(resp.result)
    assert str.isnumeric(resp.result[0])


def test_get_token_account_balance_by_contract_address(betamax_session):
    contract_address = "0x8a953cfe442c5e8855cc6c61b1293fa648bae472"
    address = "0xe04c9c8b5939fb0bb2ce58573fa4fa0411093506"

    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.token.get_token_account_balance_by_contract_address(
        contractaddress=contract_address, address=address
    )

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert is_seq(resp.result)
    assert str.isnumeric(resp.result[0])
