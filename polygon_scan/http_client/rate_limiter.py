import logging
from sqlite3 import Timestamp
import time

from polygon_scan.http_client.datatypes import RateLimit


logger = logging.getLogger(__package__)


class SimpleRateLimiter:
    def __init__(self, rate_limit=None):
        self.rate_limit = rate_limit or RateLimit(2, 5)  # 2 reqs/ 5s

        self._remaining = self.rate_limit.limit
        self._reset_timestamp = None
        self._new_interval = True

    def __call__(self, request_function, *args, **kwargs):
        # use requests response hook for accurate timestamps:
        def update_timestamp_hook(response, *argg, **kwargs):
            now = time.time()
            if self._new_interval:
                # just completed first req in new interval post delay
                self._reset_timestamp = now + self.rate_limit.limit_time_interval
                self._new_interval = False
            self._remaining -= 1

        if "hooks" in kwargs:
            if "response" in kwargs["hooks"]:
                kwargs["hooks"]["response"].append(update_timestamp_hook)
            else:
                kwargs["hooks"]["response"] = [update_timestamp_hook]
        else:
            kwargs["hooks"] = {"response": [update_timestamp_hook]}

        if self._remaining <= 0:
            # used up all requests in curent interval, delay then reset count
            self._delay()
            self._remaining = self.rate_limit.limit
            self._new_interval = True

        resp = request_function(*args, **kwargs)
        return resp

    def _delay(self):
        if self._reset_timestamp is None:
            return
        sleep_seconds = self._reset_timestamp - time.time()
        if sleep_seconds <= 0:
            return
        msg = f"Sleeping: {sleep_seconds:0.2f} seconds"
        logger.debug(msg)
        time.sleep(sleep_seconds)
