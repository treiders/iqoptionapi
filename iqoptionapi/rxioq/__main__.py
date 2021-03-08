from .api import Api
from .connection import WSConnection
from .http_session import HTTPSession

if __name__ == "__main__":
    import asyncio
    import json
    import sys
    import logging
    import os

    from websockets.client import connect as _connect


    LOGLEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(level=LOGLEVEL)

    _, username, password = sys.argv

    async def ainput(string: str) -> str:
        await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s + " "))
        content = await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)
        return content.strip()

    async def echonnect(pid: int):
        client = await _connect("wss://iqoption.com/echo/websocket")
        websocket = WSConnection(client=client)

        http = HTTPSession(username=username, password=password)

        api = Api(http=http, websocket=websocket)

        while True:
            await api.profile.state_ready
            print(f'Profile ready {api.profile.address}')
            name = await ainput("Command?:\n")
            if not name.strip() or name.strip() == "help":
                print(
                    "IQOptions Commands:\n"
                    "\texit\n\n"
                    "\tsubscribeMessage\n"
                )
                continue

            if "exit" == name:
                print("exiting...")
                break

            msg = await ainput("Param?:\n")
            if not msg or msg == "help":
                print(
                    f"""IQOptions Params for {name}:\n"""
                    "\texit\n\n"
                    """\t{"name":"candle-generated","params":{"routingFilters":{"active_id":1,"size":1}}}\n"""
                )
                continue

            if "exit" == msg:
                print("exiting...")
                break

            print(f"sending... {dict(name=name, msg=json.loads(msg))}")
            await api.send(name=name, msg=json.loads(msg))

    asyncio.run(echonnect(3))
