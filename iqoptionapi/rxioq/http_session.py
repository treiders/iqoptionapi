from asyncio import Future, get_event_loop
from dataclasses import dataclass, field

from requests import Response, Session


@dataclass
class HTTPSession:
    username: str = field(repr=True)
    password: str = field(repr=False)
    method: str = field(default="POST")
    headers: dict = field(default_factory=dict)
    proxies: dict = field(default_factory=dict)
    session: Session = field(default_factory=Session)
    url: str = field(default="https://auth.iqoption.com/api/v2/login")
    login_response: Future[Response] = field(default_factory=Future, repr=False)

    def __post_init__(self):
        if not self.login_response.done():
            self.login_response = _login_response(self)

    @property
    async def session_id(self) -> str:
        login_response = await self.login_response
        login_response.raise_for_status()
        return login_response.cookies["ssid"]

    async def send(self, url: str, method="POST", **request_args) -> Response:
        await self.login_response
        return await _request(self.session, method=method, **request_args)


def _request(session: Session, **request_args):
    return get_event_loop().run_in_executor(
        None, lambda: session.request(**request_args))


async def _login_response(http_session: HTTPSession) -> Response:
    auth = {
        "identifier": http_session.username,
        "password": http_session.password
    }
    return await _request(
        http_session.session,
        data=auth, url=http_session.url,
        method=http_session.method, headers=http_session.headers)
