from iqoptionapi.ws.chanels.base import Base


class GetDeferredOrders(Base):

    name = "sendMessage"

    def __call__(self, instrument_type, balance_id):

        data = {
            "name": "get-deferred-orders",
            "version": "1.0",
            "body": {
                "user_balance_id": int(balance_id),
                "instrument_type": instrument_type,
            },
        }

        return self.send_websocket_request(self.name, data)
