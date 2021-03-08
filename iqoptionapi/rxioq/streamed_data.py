from asyncio import Future
from json import dumps
from typing import Callable, Generic, TypeVar

from rx import operators as ops
from rx.core.observable import Observable

from .connection import WSReceived

T = TypeVar('T')


class From(Generic[T]):

    def __init__(self, source: Observable,
                 fn_filter: Callable[[WSReceived], bool] = lambda _: True,
                 fn_map: Callable[[WSReceived], T] = lambda event: event.msg):

        self._last_event = None
        self.state_ready = Future()

        self._source = source.pipe(
            ops.filter(fn_filter), ops.map(fn_map))

        def update_me(message):
            self._last_event = message
            if not self.state_ready.done():
                self.state_ready.set_result(self)

        self.subscribe = self._source.subscribe
        self._source.subscribe(on_next=update_me)

    def __str__(self) -> str:
        return dumps(self._last_event.__str__())

    def __repr__(self) -> str:
        return self._last_event.__repr__()

    def __pos__(self):
        return self._last_event.__pos__()

    def __neg__(self):
        return self._last_event.__neg__()

    def __invert__(self):
        return self._last_event.__invert__()

    def __cmp__(self, other):
        return self._last_event.__cmp__(other)

    def __eq__(self, other):
        return self._last_event.__eq__(other)

    def __ne__(self, other):
        return self._last_event.__ne__(other)

    def __lt__(self, other):
        return self._last_event.__lt__(other)

    def __gt__(self, other):
        return self._last_event.__gt__(other)

    def __le__(self, other):
        return self._last_event.__le__(other)

    def __ge__(self, other):
        return self._last_event.__ge__(other)

    def __add__(self, other):
        return self._last_event.__add__(other)

    def __sub__(self, other):
        return self._last_event.__sub__(other)

    def __mul__(self, other):
        return self._last_event.__mul__(other)

    def __floordiv__(self, other):
        return self._last_event.__floordiv__(other)

    def __div__(self, other):
        return self._last_event.__div__(other)

    def __truediv__(self, other):
        return self._last_event.__truediv__(other)

    def __mod__(self, other):
        return self._last_event.__mod__(other)

    def __divmod__(self, other):
        return self._last_event.__divmod__(other)

    def __pow__(self, other):
        return self._last_event.__pow__(other)

    def __lshift__(self, other):
        return self._last_event.__lshift__(other)

    def __rshift__(self, other):
        return self._last_event.__rshift__(other)

    def __radd__(self, other):
        return self._last_event.__rshift__(other)

    def __rsub__(self, other):
        return self._last_event.__sub__(other)

    def __rmul__(self, other):
        return self._last_event.__mul__(other)

    def __rfloordiv__(self, other):
        return self._last_event.__floordiv__(other)

    def __rdiv__(self, other):
        return self._last_event.__div__(other)

    def __rtruediv__(self, other):
        return self._last_event.__truediv__(other)

    def __rmod__(self, other):
        return self._last_event.__mod__(other)

    def __rdivmod__(self, other):
        return self._last_event.__divmod__(other)

    def __rpow__(self, other):
        return self._last_event.__pow__(other)

    def __rlshift__(self, other):
        return self._last_event.__lshift__(other)

    def __rrshift__(self, other):
        return self._last_event.__rshift__(other)

    def __rand__(self, other):
        return self._last_event.__and__(other)

    def __ror__(self, other):
        return self._last_event.__or__(other)

    def __rxor__(self, other):
        return self._last_event.__xor__(other)

    def __and__(self, other):
        return self._last_event.__and__(other)

    def __or__(self, other):
        return self._last_event.__or__(other)

    def __xor__(self, other):
        return self._last_event.__xor__(other)

    def __index__(self):
        return self._last_event.__index__()

    def __bool__(self):
        return self._last_event.__bool__()

    def __int__(self):
        return self._last_event.__int__()

    def __float__(self):
        return self._last_event.__float__()

    def __getattribute__(self, name):
        if name in ('_source', '_last_event', 'state_ready', 'subscribe'):
            return super().__getattribute__(name)
        try:
            return self._last_event[name]
        except:
            return self._last_event.__getattribute__(name)

    def __getitem__(self, key):
        return self._last_event.__getitem__(key)

    def __iter__(self):
        return self._last_event.__iter__()
