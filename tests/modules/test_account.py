import pytest
from polygon_scan import PolygonScan
from tests import api_key


@pytest.fixture
def test_address():
    return "0x5A534988535cf27a70e74dFfe299D06486f185B7"


@pytest.fixture
def response_keys():
    return ["status", "message", "result"]


def test_get_account_balance(betamax_session, test_address, response_keys):
    """Test get account balance API call"""
    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_account_balance(test_address)

    assert isinstance(resp, dict)
    assert set(response_keys).issubset(resp.keys())
    assert resp["status"] == "1"
    assert resp["message"] == "OK"
    assert str.isnumeric(resp["result"])


@pytest.fixture
def test_addresses():
    return [
        "0x5A534988535cf27a70e74dFfe299D06486f185B7",
        "0x54bA15efe1b6D886bA4Cd5C5837240675BD0D43a",
        "0x39842a0Fe638cc956b76A49E918c30d818708BA0",
    ]


@pytest.fixture
def account_balance_keys():
    return ["account", "balance"]


def test_get_multi_accounts_balances(
    betamax_session, test_addresses, response_keys, account_balance_keys
):

    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_multiple_accounts_balances(test_addresses)

    assert isinstance(resp, dict)
    assert set(response_keys).issubset(resp.keys())
    assert resp["status"] == "1"
    assert resp["message"] == "OK"
    assert isinstance(resp["result"], list)
    assert isinstance(resp["result"][0], dict)
    assert set(resp["result"][0].keys()).issubset(account_balance_keys)
    assert resp["result"][0]["account"] == test_addresses[0]
    assert str.isnumeric(resp["result"][0]["balance"])