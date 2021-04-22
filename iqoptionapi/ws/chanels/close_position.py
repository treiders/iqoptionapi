from iqoptionapi.ws.chanels.base import Base


class Close_position(Base):
    name = "sendMessage"

    def __call__(self, position_id):
        data = {
            "name": "close-position",
            "version": "1.0",
            "body": {
                "position_id": position_id
            },
        }
        return self.send_websocket_request(self.name, data)
