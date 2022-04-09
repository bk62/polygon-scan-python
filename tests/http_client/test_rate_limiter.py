import itertools
import pytest, time
from polygon_scan.http_client.rate_limiter import SimpleRateLimiter
from polygon_scan.http_client import RateLimit


@pytest.fixture
def mock_time_sleep(mocker):
    mocker.patch("time.time")
    mocker.patch("time.sleep")


def test_simple_rate_limiter_delay(mock_time_sleep):
    time.time.return_value = 1
    rate_limit = SimpleRateLimiter(RateLimit(2, 5))
    rate_limit._reset_timestamp = 100

    rate_limit._delay()

    assert time.time.called
    assert time.sleep.called
    time.sleep.assert_called_with(99)


def test_simple_rate_limiter_delay_not_called_when_time_is_past(mock_time_sleep):
    time.time.return_value = 101
    rate_limit = SimpleRateLimiter(RateLimit(2, 5))
    rate_limit._reset_timestamp = 100

    rate_limit._delay()

    assert time.time.called
    assert not time.sleep.called


def test_simple_rate_limiter_delay_not_called_when_time_not_set(mock_time_sleep):
    time.time.return_value = 101
    rate_limit = SimpleRateLimiter(RateLimit(2, 5))
    rate_limit._reset_timestamp = None

    rate_limit._delay()

    assert not time.sleep.called


def test_simple_rate_limiter_delay_not_called_when_time_matches(mock_time_sleep):
    time.time.return_value = 101
    rate_limit = SimpleRateLimiter(RateLimit(2, 5))
    rate_limit._reset_timestamp = 101

    rate_limit._delay()

    assert time.time.called
    assert not time.sleep.called


def test_simple_rate_limiter_delay_full_time_with_zero_remaining(mock_time_sleep):
    time.time.return_value = 0
    rate_limit = SimpleRateLimiter(RateLimit(2, 5))
    rate_limit._reset_timestamp = 50
    rate_limit._remaining = 0

    rate_limit._delay()

    assert time.sleep.called
    time.sleep.assert_called_with(50)


def test_simple_rate_limiter_delay_full_time_with_negative_remaining(mock_time_sleep):
    time.time.return_value = 0
    rate_limit = SimpleRateLimiter(RateLimit(2, 5))
    rate_limit._reset_timestamp = 50
    rate_limit._remaining = -1

    rate_limit._delay()

    assert time.sleep.called
    time.sleep.assert_called_with(50)


def test_simple_rate_limiter__integration(mock_time_sleep):
    request_count = 0

    def test_request(*args, **kwargs):
        nonlocal request_count
        request_count += 1
        kwargs["hooks"]["response"][0](None)

    # initial
    rate_limit = SimpleRateLimiter(RateLimit(2, 5))

    assert not time.time.called
    assert not time.sleep.called

    # 1 req / 2
    time.time.side_effect = [0, 1]  # first request completed at t=0
    rate_limit(test_request)

    assert request_count == 1
    assert time.time.call_count == 1
    assert not time.sleep.called

    # 2 req / 2
    rate_limit(test_request)

    assert request_count == 2
    assert time.time.call_count == 2
    assert not time.sleep.called

    # 3 req / 2
    # 3rd request attempated at t = 2, 3rd request completes at t=6
    time.time.side_effect = [2, 6]
    rate_limit(test_request)

    assert request_count == 3
    assert time.time.call_count == 4  # once in call, once in delay to calc sleep time
    time.sleep.assert_called_with(5 - 2)
    assert time.sleep.call_count == 1

    # 4 req / 2
    time.time.side_effect = [7]
    rate_limit(test_request)

    assert request_count == 4
    assert time.time.call_count == 5
    assert time.sleep.call_count == 1

    # 5 req / 2
    # 5th request attempated at t = 7, completes at t=9
    time.time.side_effect = [7, 11]
    rate_limit(test_request)

    assert request_count == 5
    assert time.time.call_count == 7
    time.sleep.assert_called_with(11 - 7)
    assert time.sleep.call_count == 2
