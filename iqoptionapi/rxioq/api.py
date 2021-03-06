"""
Interface expected by ..ws.chanels and ..http
"""

from dataclasses import dataclass
from json import dumps
from time import time

from .connection import WSConnection
from .http_session import HTTPSession
from .time_sync import TimeSync


def new_request_id() -> int:
    return int(str(time()).split(".")[1])


def url_of(endpoint) -> str:
    return f"https://iqoption.com/api/{endpoint}"


@dataclass
class Api:
    timesync: TimeSync
    http_session: HTTPSession
    ws_connection: WSConnection

    async def send_websocket_request(self, name, msg, request_id=""):
        data = dumps({
            "msg": msg,
            "name": name,
            "request_id": request_id or new_request_id()
        })
        return self.ws_connection.send(data)

    async def send_http_request(self, resource, method,
                                data=None, params=None, headers=None,
                                proxies=None):
        return self.send_http_request_v2(
            url_of(resource.url), method, data, params, headers, proxies)

    async def send_http_request_v2(self, url, method,
                                   data=None, params=None, headers=None,
                                   proxies=None):
        return self.http_session.send(
            url, method, data, params, headers, proxies)
