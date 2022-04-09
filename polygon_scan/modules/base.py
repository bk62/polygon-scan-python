class Base:
    params = {}

    def __init__(self, polygon_scan):
        self._polygon_scan = polygon_scan

    def get_params(self, **kwargs):
        return {**self.params, **kwargs}

    def request(self, params, **kwargs):
        return self._polygon_scan.request(params=params, **kwargs)
