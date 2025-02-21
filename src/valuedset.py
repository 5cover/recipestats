from typing import TypeVar
from collections.abc import Mapping

_KT = TypeVar('_KT')


class ValuedSet(Mapping[_KT, float]):
    _data: dict[_KT, float]
    _hash: int | None = None

    def __init__(self, initial_data: Mapping[_KT, float] | None = None):
        self._data = {} if initial_data is None else dict({k: v for k, v in initial_data.items() if v != 0})

    def copy(self):
        return ValuedSet(self._data)

    def single(self):
        if len(self._data) != 1:
            raise ValueError('Not 1 item in ValuedSet')
        return next(iter(self._data.items()))

    def __repr__(self):
        return f'ValuedSet({dict(self._data)})'

    def __hash__(self):
        'Calculates the hash if all values are hashable, otherwise raises a TypeError.'
        if self._hash is None:
            self._hash = hash(frozenset(self.items()))
        return self._hash

    def __getitem__(self, key: _KT):
        return self._data.__getitem__(key)

    def __iter__(self):
        return self._data.__iter__()

    def __len__(self):
        return self._data.__len__()

    def __add__(self, other: Mapping[_KT, float]):
        result = self.copy()
        result += other
        return result

    def __iadd__(self, other: Mapping[_KT, float]):
        for k, v in other.items():
            if k not in self._data:
                self._data[k] = v
            elif self._data[k] == -v:
                del self._data[k]
            else:
                self._data[k] += v
        return self

    def __sub__(self, other: Mapping[_KT, float]):
        result = self.copy()
        result -= other
        return result

    def __isub__(self, other: Mapping[_KT, float]):
        for k, v in other.items():
            if k not in self._data:
                self._data[k] = -v
            elif self._data[k] == v:
                del self._data[k]
            else:
                self._data[k] -= v
        return self

    def __mul__(self, other: float):
        result = self.copy()
        result *= other
        return result

    def __imul__(self, other: float):
        for k in self._data:
            self._data[k] *= other
        return self

    def __and__(self, other: Mapping[_KT, float]):
        return ValuedSet({k: self._data[k] for k in self._data.keys() & other.keys()})

    def delta(self, other: Mapping[_KT, float]):
        return ValuedSet({k: self._data[k] - other[k] for k in self._data.keys() & other.keys() if self._data[k] != other[k]})
    
    def exclude(self, other: Mapping[_KT, float]):
        return ValuedSet({k: self._data[k] for k in self._data.keys() - other.keys()})
