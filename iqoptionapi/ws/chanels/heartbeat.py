from iqoptionapi.ws.chanels.base import Base


class Heartbeat(Base):
    name = "heartbeat"

    def __call__(self, heartbeatTime):

        data = {
            "msg": {
                "heartbeatTime": int(heartbeatTime),
                "userTime": int(self.api.timesync.server_timestamp * 1000),
            }
        }
        return self.send_websocket_request(self.name, data)
