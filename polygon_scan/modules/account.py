from .base import Base


class Account(Base):
    """Helper class containing all account module methods."""

    params = {"module": "account"}

    def get_account_balance(self, address):
        params = self.get_params(action="balance", address=address)
        return self.request(params)

    def get_multiple_accounts_balances(self, addresses):
        if type(addresses) != str:
            addresses = ",".join(addresses)
        params = self.get_params(action="balancemulti", address=addresses)
        return self.request(params)

    def get_account_balance_history(self):
        # TODO
        # specific rate limit for this endpint 2/sec
        pass

    def get_account_normal_transactions(
        self, address, start_block=0, end_block=None, page=1, offset=0, sort="asc"
    ):
        params = self.get_params(
            action="txlist",
            address=address,
            start_block=start_block,
            end_block=end_block,
            page=page,
            offset=offset,
            sort=sort,
        )
        return self.request(params)

    def get_account_internal_transactions(self):
        pass

    def get_internal_transactions_by_transaction_hash(self):
        pass

    def get_interal_transactions_by_block_range(self):
        pass

    def get_erc_20_token_transfer_events_by_address(self):
        pass

    def get_erc_721_token_transfer_events_by_address(self):
        pass

    def get_blocks_validated_by_address(self):
        pass
