"""
An immutable, hashable Python mapping object.
Supports Python 2.7 and 3.4.

Inspired by:
* https://github.com/slezica/python-frozendict
* http://www.cs.toronto.edu/~tijmen/programming/immutableDictionaries.html
"""
from functools import reduce
from operator import xor


class FrozenDict(dict):

    def __init__(self, *args, **kwargs):
        super(FrozenDict, self).__init__(*args, **kwargs)
        self.__hash = None

    def __setitem__(self, key, value):
        raise TypeError('%r object does not support item assignment' % self.__class__.__name__)

    def __hash__(self):
        if self.__hash is None:
            self.__hash = reduce(xor, map(hash, self.items()), 0)

        return self.__hash

    def __repr__(self):
        return '<frozendict {}>'.format(super(FrozenDict, self).__repr__())

    def copy(self):
        return FrozenDict(super(FrozenDict, self).copy())


frozendict = FrozenDict
