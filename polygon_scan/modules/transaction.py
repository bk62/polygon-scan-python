from .base import Base


class Transaction(Base):
    """Helper class containing all transaction module methods."""

    params = {"module": "transaction"}

    def check_transaction_receipt_status(self, txhash):
        params = self.get_params(action="gettxreceiptstatus", txhash=txhash)
        return self.request(params)
