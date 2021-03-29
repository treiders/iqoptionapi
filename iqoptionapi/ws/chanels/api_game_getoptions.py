# python
"""Module for IQ option candles websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class Get_options(Base):

    name = "api_game_getoptions"

    def __call__(self, limit, balance_id):

        data = {
            "limit": int(limit),
            "user_balance_id": int(balance_id)
        }

        return self.send_websocket_request(self.name, data)


class Get_options_v2(Base):
    name = "sendMessage"

    def __call__(self, limit, instrument_type, balance_id):
        data = {
            "name": "get-options",
            "body": {
                "limit": limit,
                "instrument_type": instrument_type,
                "user_balance_id": int(balance_id),
            },
        }
        return self.send_websocket_request(self.name, data)
