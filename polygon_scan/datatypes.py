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
