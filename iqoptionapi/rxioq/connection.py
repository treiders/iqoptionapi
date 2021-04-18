from dataclasses import asdict, dataclass, field
from json import dumps, loads
from logging import WARNING, getLogger
from time import time
from typing import Any, Dict

from rx import typing
from rx.scheduler.eventloop import AsyncIOScheduler
from rx.subject import Subject
from websockets.client import WebSocketClientProtocol
from websockets.client import connect as _connect

logger = getLogger(__file__)
logger.setLevel(WARNING)


def new_request_id() -> int:
    return int(str(time()).split(".")[1])


@dataclass
class WSSent:
    name: str
    msg: Any
    request_id: int = field(default_factory=new_request_id)


@dataclass
class WSReceived:
    name: str = field(init=False)
    msg: Any = field(init=False)
    raw: Dict[str, Any] = field(repr=False, hash=False, compare=False)

    def __post_init__(self):
        self.name = self.raw.get('name')
        self.msg = self.raw.get('msg')


def _wire_inbox(client) -> Subject:
    inbox = Subject()
    loop = client.loop

    async def async_emiter():
        try:
            async for message in client:
                if 'timeSync' not in message and 'heartbeat' not in message:
                    logger.debug(message)
                inbox.on_next(WSReceived(raw=loads(message)))
        except Exception as error:
            inbox.on_error(error)

    loop.create_task(async_emiter())
    return inbox


def _wire_outbox(client) -> Subject:
    outbox = Subject()

    async def send(message):
        await client.send(dumps(asdict(message)))

    outbox.subscribe(
        on_next=lambda message: client.loop.create_task(send(message)),
        scheduler=AsyncIOScheduler(loop=client.loop)
    )
    return outbox


@dataclass
class WSConnection:
    client: WebSocketClientProtocol
    inbox: typing.Observable[WSReceived] = field(init=False)
    outbox: typing.Observer[WSSent] = field(init=False)

    def __post_init__(self):
        self.outbox = _wire_outbox(self.client)
        self.inbox = _wire_inbox(self.client)

    def send(self, name, msg, request_id=0):
        return self.outbox.on_next(
            WSSent(
                name=name,
                msg=msg,
                request_id=request_id or new_request_id()
            )
        )

    def subscribe(self, on_next=None, on_error=None, on_completed=None):
        return self.inbox.subscribe(
            on_next=on_next,
            on_error=on_error,
            on_completed=on_completed,
        )


if __name__ == "__main__":
    from asyncio import Queue, gather, run, sleep

    async def echonnect(pid: int):
        client = await _connect("wss://echo.websocket.org/")
        connection = WSConnection(client=client)

        calls: Queue[int] = Queue()
        connection.subscribe(on_next=lambda _: calls.get_nowait())

        connection.subscribe(
            on_next=lambda event: print(f"bad pun received `{event.msg}`"))

        for call_id in range(pid):
            await calls.put(call_id)
            calls.empty()
            print(f"{pid}: sendind pun {call_id + 1}")
            connection.send(
                name="pun", msg=f"{pid}: here comes your mean {call_id + 1}")

        # usually we should wait forever
        # but for this example we will wait
        # only until receive N events
        while not calls.empty():
            await sleep(0.01)

        print(f"{pid} I'm done")

    async def main():
        await gather(
            echonnect(1),
            echonnect(2),
            echonnect(3))

    run(main())
