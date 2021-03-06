from asyncio import Future, get_event_loop
from dataclasses import dataclass, field

from requests import Response, Session


@dataclass
class HTTPSession:
    username: str = field(repr=True)
    password: str = field(repr=False)
    method: str = field(default='POST')
    headers: dict = field(default_factory=dict)
    url: str = field(default='https://auth.iqoption.com/api/v2/login')
    login_response: Future[Response] = field(default_factory=Future, repr=False)
    session_id: Future[str] = field(default_factory=Future, repr=False)

    def __post_init__(self):
        if not self.login_response.done():
            self.login_response = get_event_loop().run_in_executor(
                None, lambda: _login_response(self))

        if not self.session_id.done():
            self.session_id = _session_id(self.login_response)


def _login_response(http_session: HTTPSession) -> Response:
    auth = {"identifier": http_session.username, "password": http_session.password}
    return Session().request(
        data=auth, url=http_session.url,
        method=http_session.method, headers=http_session.headers,
    )


async def _session_id(future_login_response: Future[Response]) -> str:
    login_response = await future_login_response
    print(login_response)
    login_response.raise_for_status()
    return login_response.cookies["ssid"]
