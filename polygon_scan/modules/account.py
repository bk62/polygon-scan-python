from .base import Base


class Account(Base):
    """Helper class containing all account module methods."""

    params = {"module": "account"}

    def get_account_balance(self, address):
        params = self.get_params(action="balance", address=address)
        return self.request(params)

    def get_multiple_accounts_balances(self, addresses):
        addresses = self.prep_addresses_arg(addresses)
        params = self.get_params(action="balancemulti", address=addresses)
        return self.request(params)

    def get_account_balance_history_by_block_no(self, addresses, blockno):
        # TODO
        # specific rate limit for this endpint 2/sec
        # only 20 addrs max
        # pro tier only
        addresses = self.prep_addresses_arg(addresses)
        params = self.get_params(
            action="balancehistory", address=addresses, blockno=blockno
        )
        return self.request(params)

    def get_account_normal_transactions(
        self, address, startblock=0, endblock=None, page=1, offset=0, sort="asc"
    ):
        params = self.get_params(
            action="txlist",
            address=address,
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        return self.request(params)

    def get_account_internal_transactions(
        self, address, startblock=0, endblock=99999999, page=1, offset=0, sort="asc"
    ):
        # max 10k records
        params = self.get_params(
            action="txlistinternal",
            address=address,
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        return self.request(params)

    def get_internal_transactions_by_transaction_hash(self, txhash):
        params = self.get_params(action="txlistinternal", txhash=txhash)
        return self.request(params)

    def get_internal_transactions_by_block_range(
        self, startblock=0, endblock=99999999, page=1, offset=0, sort="asc"
    ):
        # max 10k records
        params = self.get_params(
            action="txlistinternal",
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        return self.request(params)

    def get_erc_20_token_transfer_events_by_address(
        self,
        address,
        contractaddress,
        startblock=0,
        endblock=99999999,
        page=1,
        offset=0,
        sort="asc",
    ):
        params = self.get_params(
            action="tokentx",
            address=address,
            contractaddress=contractaddress,
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        return self.request(params)

    def get_erc_721_token_transfer_events_by_address(
        self,
        address,
        contractaddress,
        startblock=0,
        endblock=99999999,
        page=1,
        offset=0,
        sort="asc",
    ):
        params = self.get_params(
            action="tokennfttx",
            address=address,
            contractaddress=contractaddress,
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        return self.request(params)

    def _get_erc_token_transfer_events_by_address(
        self,
        action,
        address,
        contractaddress,
        startblock=0,
        endblock=99999999,
        page=1,
        offset=0,
        sort="asc",
    ):
        assert action in (
            "tokentx",
            "tokennfttx",
        ), 'Action has to be one of ("tokentx", "tokennfttx")'
        params = self.get_params(
            action=action,
            address=address,
            contractaddress=contractaddress,
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        return self.request(params)

    def get_blocks_validated_by_address(
        self, address, blocktype="blocks", page=1, offset=0
    ):
        params = self.get_params(
            action="getminedblocks",
            address=address,
            blocktype=blocktype,
            page=page,
            offset=offset,
        )
        return self.request(params)
