from .base import Base


class Account(Base):
    params = {"module": "account"}

    def get_account_balance(self, address):
        params = self.get_params(action="balance", address=address)
        return self.request(params)

    def get_multiple_accounts_balances(self, addresses):
        if type(addresses) != str:
            addresses = ",".join(addresses)
        params = self.get_params(action="balancemulti", address=addresses)
        return self.request(params)
