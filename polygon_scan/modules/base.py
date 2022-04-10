from polygon_scan.utils import is_seq


class Base:
    """Base helper class for Polygon Scan's API Modules e.g. Account, Block etc."""

    params = {}

    def __init__(self, polygon_scan):
        self._polygon_scan = polygon_scan

    def get_params(self, params=None, **kwargs):
        params = params or {}
        return {**self.params, **params, **kwargs}

    def request(self, params, **kwargs):
        return self._polygon_scan.request(params=params, **kwargs)

    def prep_addresses_arg(self, addresses):
        if type(addresses) == str:
            # single addr or addrs sep by ,
            return addresses
        else:
            # is sequence
            assert is_seq(addresses), "addresses must be a string or a sequence"
            addresses = ",".join(addresses)
        return addresses
