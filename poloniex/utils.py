import ast as _ast
import six as _six

try:
    import collections.abc as _collections_abc       # only works on python 3.3+
except ImportError:
    import collections as _collections_abc


class AutoCastDict(_collections_abc.Mapping):

    """Dictionary that automatically cast strings."""

    def __init__(self, *args, **kwargs):
        self.__dict = dict(*args, **kwargs)

    def __getitem__(self, key):
        value = self.__dict[key]
        try:
            return _ast.literal_eval(value)
        except (ValueError, SyntaxError, TypeError):
            return value

    def __str__(self):
        items = ('{!r}: {!r}'.format(*it) for it in _six.iteritems(self))
        return '{{{}}}'.format(', '.join(items))

    __repr__ = __str__

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)
