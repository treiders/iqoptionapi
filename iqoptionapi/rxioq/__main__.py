from .connection import WSConnection
from .http_session import HTTPSession


if __name__ == "__main__":
    import sys
    import asyncio
    import requests
    import time
    import json
    from websockets.client import connect as _connect

    _, username, password = sys.argv

    async def ainput(string: str) -> str:
        await asyncio.get_event_loop().run_in_executor(
                None, lambda s=string: sys.stdout.write(s+' '))
        content = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline)
        return content.strip()

    async def echonnect(pid: int):
        client = await _connect('wss://iqoption.com/echo/websocket')
        connection = WSConnection(client=client)
        def print_msg(msg):
            if 'heartbeat' not in msg and 'timeSync' not in msg:
                print(f'\n`{msg}`')

        connection.subscribe(on_next=print_msg)

        ssid = await HTTPSession(username=username, password=password).session_id

        request_id = int(str(time.time()).split(".")[1])
        data = json.dumps(dict(name="ssid", msg=ssid, request_id=request_id))
        connection.send(data)

        while True:
            name = await ainput('Command?:\n')
            if not name.strip() or name.strip() == 'help':
                print(
                    "IQOptions Commands:\n"
                    "exit\n\n"
                    "subscribeMessage\n"
                )
                continue

            if 'exit' == name:
                print('exiting...')
                break

            msg = await ainput('Param?:\n')
            if not msg or msg == 'help':
                print(
                    f"""IQOptions Params for {name}:\n"""
                    "exit\n\n"
                    '{"name":"candle-generated","params":{"routingFilters":{"active_id":1,"size":1}}}\n'
                )
                continue

            if 'exit' == msg:
                print('exiting...')
                break


            request_id = int(str(time.time()).split(".")[1])
            data = json.dumps(dict(name=name, msg=json.loads(msg), request_id=request_id))
            print(f"sending... {data}")
            connection.send(data)

    asyncio.run(echonnect(3))