import logging, time

logger = logging.getLogger(__package__)


class BaseRetryStrategy:
    def sleep(self):
        secs = self.sleep_duration
        if secs is not None:
            msg = f"Sleeping: {secs:0.2f}s before retrying"
            logger.debug(msg)
            time.sleep(secs)


class FiniteRetryStrategy(BaseRetryStrategy):
    def __init__(self, retries=3, sleep_duration=2):
        self.retries = retries
        self._sleep_duration = sleep_duration

    @property
    def sleep_duration(self):
        if self.retries < 3:
            return self._sleep_duration
        return None

    def consume_retry(self):
        self.retries -= 1
        return self.retries

    def retry_on_failure(self):
        return self.retries > 1
