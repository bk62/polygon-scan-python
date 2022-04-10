from time import sleep
import pytest, os
from polygon_scan import PolygonScan
from polygon_scan.datatypes import APIResponse, AttrDict
from polygon_scan.utils import is_seq
from polygon_scan.exceptions import APIException
from tests import api_key


@pytest.fixture(autouse=os.environ.get("SLOW_DOWN_API_TESTS"))
def slow_down_api_tests():
    sleep(2)


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

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert is_seq(resp.result)
    assert str.isnumeric(resp.result[0])


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

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(account_balance_keys)
    assert resp.result[0]["account"] == test_addresses[0]
    assert str.isnumeric(resp.result[0]["balance"])


# TODO
# fails currently -- requires PRO?
# add another test that succeeds
def test_get_historical_account_balance_by_blockno__raises_api_exc(
    betamax_session, response_keys
):
    """Test get account balance API call"""
    test_address = "0x23eA5Ec7Ea2d4282012313c9899Cdc07bd45243d"
    blockno = 18798641

    pg_scan = PolygonScan(api_key, session=betamax_session)

    with pytest.raises(APIException):
        resp = pg_scan.account.get_account_balance_history_by_block_no(
            test_address, blockno
        )

    # sucess:
    # assert isinstance(resp, APIResponse)
    # assert resp.status == "1"
    # assert resp.message == "OK"
    # assert is_seq(resp.result)
    # assert str.isnumeric(resp.result[0])


@pytest.fixture
def account_normal_transaction_keys():
    return [
        "blockNumber",
        "blockHash",
        "timeStamp",
        "hash",
        "nonce",
        "transactionIndex",
        "from",
        "to",
        "value",
        "gas",
        "gasPrice",
        "input",
        "contractAddress",
        "cumulativeGasUsed",
        "txreceipt_status",
        "gasUsed",
        "confirmations",
        "isError",
    ]


def test_get_account_normal_txns(
    betamax_session, test_address, response_keys, account_normal_transaction_keys
):
    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_account_normal_transactions(test_address)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(account_normal_transaction_keys)
