from .exceptions import ClientException


class AttrDict:
    def __init__(self, dictionary, **kwargs):
        self.__dict__ = dict(dictionary)
        self.__dict__.update(**kwargs)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()

    def __repr__(self):
        return self.__class__.__name__ + f"({self.__dict__!r})"


class APIResponse:
    def __init__(self, response) -> None:
        self.response = response
        response_dict = response.response_dict

        if response_dict:
            status = response_dict["status"]
            message = response_dict["message"]
            result = response_dict["result"]

        self.status = status
        self.message = message
        self._set_result(result)

    def _set_result(self, result):
        if type(result) == dict:
            self._result = [AttrDict(result)]
        elif type(result) == list:
            self._result = [AttrDict(r) for r in result]
        elif type(result) == str:
            self._result = [result]
        else:
            raise ClientException("Unknown API result type/format", result)

    @property
    def result(self):
        return self._result

    def __len__(self):
        return len(self._result)

    def __getitem__(self, ix):
        return self._result[ix]

    def __repr__(self):
        return (
            self.__class__.__name__
            + f"(status={self.status}, message={self.message}, result={self.result!r}, request_url={self.request_url}, request_kwargs={self.request_kwargs!r})"
        )
