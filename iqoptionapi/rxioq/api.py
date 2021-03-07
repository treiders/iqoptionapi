"""
Interface expected by ..ws.chanels and ..http
"""

from asyncio import ensure_future
from dataclasses import dataclass, field
from typing import Awaitable

from rx import operators as ops

from .connection import WSConnection
from .http_session import HTTPSession
from .time_sync import TimeSync


def url_of(endpoint) -> str:
    return f"https://iqoption.com/api/{endpoint}"


async def set_session_id(websocket: WSConnection, future_session_id: Awaitable[str]):
    session_id = await future_session_id
    websocket.send(name="ssid", msg=session_id)


@dataclass
class Api:
    http: HTTPSession
    websocket: WSConnection
    timesync: TimeSync = field(init=False)

    def __post_init__(self):
        time_source = self.websocket.inbox.pipe(
            ops.filter(lambda message: message.name == 'timeSync'),
            ops.map(lambda message: int(message.msg))
        )
        self.timesync = TimeSync(source=time_source)

        future_session_id = ensure_future(self.http.session_id)
        loop = future_session_id.get_loop()
        loop.create_task(set_session_id(self.websocket, future_session_id))

    async def send(self, name, msg, request_id=0):
        return self.websocket.send(name, msg, request_id)

    async def send_websocket_request(self, name, msg, request_id=0):
        return self.send(name, msg, request_id)

    async def request(self, url: str, method="POST", **request_args):
        return self.http.send(url, method=method, **request_args)

    async def send_http_request(self, resource, method,
                                data=None, params=None, headers=None,
                                proxies=None):
        return self.request(url_of(resource.url), method=method, data=data,
                            params=params, headers=headers, proxies=proxies)

    async def send_http_request_v2(self, url, method,
                                   data=None, params=None, headers=None,
                                   proxies=None):
        return self.request(url, method=method, data=data,
                            params=params, headers=headers, proxies=proxies)
