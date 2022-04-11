from .base import Base


class Stats(Base):
    """Helper class containing stats methods."""

    params = {"module": "stats"}

    def get_matic_total_supply(self):
        return self.request(self.get_params(action="maticsupply"))

    def get_matic_last_price(self):
        return self.request(self.get_params(action="maticprice"))

    # TODO pro tier calls
