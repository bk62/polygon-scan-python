from .base import Base


class Token(Base):
    """Helper class for all token module methods."""

    # different module for different methods
    params = {}

    def get_token_total_supply_by_contract_address(self, contractaddress):
        params = self.get_params(
            module="stats", action="tokensupply", contractaddress=contractaddress
        )
        return self.request(params)

    def get_token_account_balance_by_contract_address(self, contractaddress, address):
        params = self.get_params(
            module="account",
            action="tokenbalance",
            contractaddress=contractaddress,
            address=address,
        )
        return self.request(params)
