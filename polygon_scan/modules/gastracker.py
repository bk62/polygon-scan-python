from .base import Base


class GasTracker(Base):
    """Helper class containing all gas tracker module methods."""

    params = {"module": "gastracker"}

    def get_gas_oracle(self):
        return self.request(self.get_params(action="gasoracle"))

    # TODO pro tier endpoints
