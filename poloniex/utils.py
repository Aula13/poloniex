import json as _json
import collections as _collections


class AutoCastDict(_collections.Mapping):

    """Dictionary that automatically cast strings."""

    def __init__(self, *args, **kwargs):
        self.__dict = dict(*args, **kwargs)

    def __getitem__(self, key):
        value = self.__dict[key]
        try: return _json.loads(value)
        except ValueError: return value

    def __str__(self):
        items = ('{!r}: {!r}'.format(*it) for it in self.iteritems())
        return '{{{}}}'.format(', '.join(items))

    __repr__ = __str__
    __iter__ = lambda self: iter(self.__dict)
    __len__ = lambda self: len(self.__dict)
