import ast as _ast
import functools as _functools
import collections as _collections

from .exceptions import PoloniexCommandException


class AutoCastDict(_collections.Mapping):

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
        items = ('{!r}: {!r}'.format(*it) for it in self.iteritems())
        return '{{{}}}'.format(', '.join(items))

    __repr__ = __str__

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)


def raise_on_error(fn):
    """decorator that raises PoloniexCommandException if there is an error."""

    @_functools.wraps(fn)
    def _fn(*args, **kwargs):
        response = fn(*args, **kwargs)
        if 'error' in response:
            raise PoloniexCommandException(response['error'])
        return response

    return _fn
