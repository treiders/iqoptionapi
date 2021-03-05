from typing import Dict, Any
from dataclasses import dataclass, field
from rx import create, Observable, from_future, operators as _op
from rx.subject import Subject
from rx.scheduler.eventloop import AsyncIOScheduler
from websockets.client import WebSocketClientProtocol, connect as _connect


def _wire_inbox(client) -> None:
    inbox = Subject()
    loop = client.loop
    async def async_emiter():
        try:
            async for message in client:
                print(message)
                inbox.on_next(message)
        except Exception as error:
            inbox.on_error(error)

    loop.create_task(async_emiter())
    return inbox


def _wire_outbox(client) -> Subject:
    outbox = Subject()
    async def send(message):
        await client.send(message)

    outbox.subscribe(
        on_next=lambda message: client.loop.create_task(send(message)),
        scheduler=AsyncIOScheduler(loop=client.loop)
    )
    return outbox


@dataclass
class WSConnection:
    client: WebSocketClientProtocol
    inbox: Subject = field(init=False)
    outbox: Subject = field(init=False)

    def __post_init__(self):
        self.outbox = _wire_outbox(self.client)
        self.inbox = _wire_inbox(self.client)
    
    def send(self, message):
        return self.outbox.on_next(message)


if __name__ == "__main__":
    import asyncio

    async def main():        
        client = await _connect('wss://echo.websocket.org/')
        connection = WSConnection(client=client)
        connection.inbox.pipe(
            _op.map(lambda message: print(f"bad pun intended `{message}`"))
        )
        while True:
            await asyncio.sleep(0.05)
            connection.send("here comes your mean")

    asyncio.run(main())