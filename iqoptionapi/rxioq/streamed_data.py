from asyncio import Future, Queue
from json import dumps
from typing import Callable, Generic, Optional, TypeVar

from rx import operators as ops
from rx.core.observable import Observable

from .connection import WSReceived

T = TypeVar('T')


class From(Generic[T]):

    def __init__(self, source: Observable,
                 fn_filter: Callable[[WSReceived], bool] = lambda _: True,
                 fn_map: Callable[[WSReceived], T] = lambda event: event.msg,
                 fn_reduce: Optional[Callable[[T, WSReceived], T]] = None):
        self._last_event = None
        self.state_ready = Future[T]()
        self._original_source = source
        self._source = source.pipe(
            ops.filter(fn_filter), ops.map(fn_map))

        def update_me(event):
            if fn_reduce:
                self._last_event = fn_reduce(self._last_event, event)
            else:
                self._last_event = event

            if not self.state_ready.done():
                self.state_ready.set_result(self)

        self.subscribe = self._source.subscribe
        self._source.subscribe(on_next=update_me)

    def __getattr__(self, name):
        return From(
            self._original_source,
            lambda event: event.name == name.replace('_', '-'))

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
        return float(self).__add__(other)

    def __sub__(self, other):
        return float(self).__sub__(other)

    def __mul__(self, other):
        return float(self).__mul__(other)

    def __floordiv__(self, other):
        return float(self).__floordiv__(other)

    def __div__(self, other):
        return float(self).__div__(other)

    def __truediv__(self, other):
        return float(self).__truediv__(other)

    def __mod__(self, other):
        return float(self).__mod__(other)

    def __divmod__(self, other):
        return float(self).__divmod__(other)

    def __pow__(self, other):
        return float(self).__pow__(other)

    def __radd__(self, other):
        return other.__add__(float(self))

    def __rsub__(self, other):
        return other.__sub__(float(self))

    def __rmul__(self, other):
        return other.__mul__(float(self))

    def __rfloordiv__(self, other):
        return other.__floordiv__(float(self))

    def __rdiv__(self, other):
        return other.__div__(float(self))

    def __rtruediv__(self, other):
        return other.__truediv__(float(self))

    def __rmod__(self, other):
        return other.__mod__(float(self))

    def __rdivmod__(self, other):
        return other.__divmod__(float(self))

    def __rpow__(self, other):
        return other.__pow__(float(self))

    def __rand__(self, other):
        return other and bool(self)

    def __ror__(self, other):
        return other or bool(self)

    def __index__(self):
        return self._last_event.__index__()

    def __bool__(self):
        return bool(self._last_event)

    def __int__(self):
        return int(self._last_event)

    def __float__(self):
        return float(self._last_event)

    def __getitem__(self, key):
        return self._last_event.__getitem__(key)

    def __iter__(self):
        return self._last_event.__iter__()
