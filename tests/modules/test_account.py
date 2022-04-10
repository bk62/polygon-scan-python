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
def transaction_common_keys():
    return [
        "blockNumber",
        "blockHash",
        "timeStamp",
        "hash",
        "nonce",
        "transactionIndex",
        "from",
        "to",
        "gas",
        "gasPrice",
        "input",
        "contractAddress",
        "cumulativeGasUsed",
        "gasUsed",
        "confirmations",
    ]


@pytest.fixture
def account_normal_transaction_keys(transaction_common_keys):
    return transaction_common_keys + [
        "value",
        "txreceipt_status",
        "isError",
    ]


def test_get_account_normal_txns(
    betamax_session, test_address, account_normal_transaction_keys
):
    test_address = "0xb91dd8225Db88dE4E3CD7B7eC538677A2c1Be8Cb"

    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_account_normal_transactions(test_address)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(account_normal_transaction_keys)


@pytest.fixture
def internal_transactions_keys():
    return [
        "blockNumber",
        "timeStamp",
        "hash",
        "from",
        "to",
        "value",
        "contractAddress",
        "input",
        "type",
        "gas",
        "gasUsed",
        "traceId",
        "isError",
        "errCode",
    ]


def test_get_account_internal_transactions(betamax_session, internal_transactions_keys):
    test_address = "0x0f4240D9bD4D3CFCE7aDE7F26415780824958Bc3"

    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_account_internal_transactions(test_address)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(internal_transactions_keys)


def test_get_internal_transactions_by_transaction_hash(
    betamax_session, internal_transactions_keys
):
    txn_hash = "0x23a07d4f622ba88c8338763d7811437953a0e8fab123b4346486936646f8578d"

    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_internal_transactions_by_transaction_hash(txn_hash)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(internal_transactions_keys)


def test_get_internal_transactions_by_block_range(
    betamax_session, internal_transactions_keys
):
    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_internal_transactions_by_block_range(
        startblock=19568000, endblock=19569000
    )

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(internal_transactions_keys)


@pytest.fixture
def erc20_token_transfer_keys(transaction_common_keys):
    return transaction_common_keys + [
        "value",
        "tokenName",
        "tokenSymbol",
        "tokenDecimal",
    ]


def test_get_erc20_token_transfer_events_by_address(
    betamax_session, erc20_token_transfer_keys
):
    test_address = "0x6813ad11cca98e15ff181a257a3c2855d1eee69e"
    contract_address = "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270"

    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_erc_20_token_transfer_events_by_address(
        test_address, contractaddress=contract_address
    )

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(erc20_token_transfer_keys)


@pytest.fixture
def erc721_token_transfer_keys(transaction_common_keys):
    return transaction_common_keys + [
        "tokenID",
        "tokenName",
        "tokenSymbol",
        "tokenDecimal",
    ]


def test_get_erc721_token_transfer_events_by_address(
    betamax_session, erc721_token_transfer_keys
):
    test_address = "0x30b32e79ed9c4012a71f4235f77dcf90a6f6800f"
    contract_address = "0x7227e371540cf7b8e512544ba6871472031f3335"

    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_erc_721_token_transfer_events_by_address(
        test_address, contractaddress=contract_address
    )

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(erc721_token_transfer_keys)


@pytest.fixture
def block_keys():
    return ["blockNumber", "timeStamp", "blockReward"]


def test_get_blocks_validated_by_address(betamax_session, block_keys):
    test_address = "0xb79fad4ca981472442f53d16365fdf0305ffd8e9"

    pg_scan = PolygonScan(api_key, session=betamax_session)
    resp = pg_scan.account.get_blocks_validated_by_address(test_address)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(block_keys)
