import pytest
from polygon_scan import PolygonScan
from polygon_scan.datatypes import APIResponse, AttrDict


from tests import APIKEY


@pytest.fixture
def logs_keys():
    return [
        "address",
        "topics",
        "data",
        "blockNumber",
        "timeStamp",
        "gasPrice",
        "gasUsed",
        "logIndex",
        "transactionHash",
        "transactionIndex",
    ]


def test_get_logs_query1(betamax_session, logs_keys):
    filter_params = dict(
        fromBlock=5000000,
        toBlock=6000000,
        address="0x0000000000000000000000000000000000001010",
        topic0="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    )

    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.logs.get_logs(filter_params)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(logs_keys)


def test_get_logs_query2(betamax_session, logs_keys):
    filter_params = dict(
        fromBlock=5000000,
        toBlock=6000000,
        address="0x0000000000000000000000000000000000001010",
        topic0="0x4dfe1bbbcf077ddc3e01291eea2d5c70c2b422b415d95645b9adcfd678cb1d63",
        topic0_1_opr="and",
        topic1="0x0000000000000000000000000000000000000000000000000000000000001010"
    )

    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.logs.get_logs(filter_params)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(logs_keys)
