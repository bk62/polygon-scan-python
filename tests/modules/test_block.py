import pytest
from polygon_scan import PolygonScan
from polygon_scan.datatypes import APIResponse, AttrDict

from tests import APIKEY


@pytest.fixture
def block_reward_keys():
    return [
        "blockNumber",
        "timeStamp",
        "blockMiner",
        "blockReward",
        "uncles",
        "uncleInclusionReward",
    ]


def test_get_block_rewards_by_block_number(betamax_session, block_reward_keys):
    test_blockno = 2170000

    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.block.get_block_rewards_by_block_number(test_blockno)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(block_reward_keys)


@pytest.fixture
def block_countdown_keys():
    return ["CurrentBlock", "CountdownBlock", "RemainingBlock", "EstimateTimeInSec"]


def test_get_estimated_block_countdown(betamax_session, block_countdown_keys):
    test_blockno = 24926850

    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.block.get_estimated_block_countdown(test_blockno)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert resp.result is not None
    assert isinstance(resp.result, list)
    assert isinstance(resp.result[0], AttrDict)
    assert set(resp.result[0].keys()).issubset(block_countdown_keys)


def test_get_block_number_by_timestamp(betamax_session):
    timestamp = "1601510400"

    pg_scan = PolygonScan(APIKEY, session=betamax_session)
    resp = pg_scan.block.get_block_number_by_timestamp(timestamp)

    assert isinstance(resp, APIResponse)
    assert resp.status == "1"
    assert resp.message == "OK"
    assert isinstance(resp.result, list)
    assert str.isnumeric(resp.result[0])
