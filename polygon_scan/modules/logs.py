from .base import Base


class Logs(Base):
    """Helper class containing alll logs module methods."""

    params = {"module": "logs"}

    def get_logs(self, filter_params, **filter_params_kwargs):
        """Please refer to https://docs.polygonscan.com/api-endpoints/logs for a list of filter params."""

        params = self.get_params(
            action="getLogs", **filter_params, **filter_params_kwargs
        )
        return self.request(params)
