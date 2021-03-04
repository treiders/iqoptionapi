# python

from random import randint

import iqoptionapi.global_value as global_value
from iqoptionapi.ws.chanels.base import Base

# work for forex digit cfd(stock)


class Digital_options_place_digital_option(Base):
    name = "sendMessage"

    def __call__(self, instrument_id, amount, user_balance_id=None):
        if not user_balance_id:
            user_balance_id = int(self.api.profile.balance_id)

        data = {
            "name": "digital-options.place-digital-option",
            "version": "1.0",
            "body": {
                "user_balance_id": int(global_value.balance_id),
                "instrument_id": str(instrument_id),
                "amount": str(amount),
            },
        }
        request_id = str(randint(0, 100000))
        self.send_websocket_request(self.name, data, request_id)
        return request_id


class Digital_options_close_position(Base):
    name = "sendMessage"

    def __call__(self, position_id):
        data = {
            "name": "digital-options.close-position",
            "version": "1.0",
            "body": {
                "position_id": int(position_id)
            },
        }
        self.send_websocket_request(self.name, data)
