"""Module for IQ Option websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class Changebalance(Base):
    """Class for IQ option buy websocket chanel."""

    # pylint: disable=too-few-public-methods

    name = "api_profile_changebalance"

    def __call__(self, balance_id):
        """Method to change balance.

        :param balance_id: Id of balance.
        """

        data = {"balance_id": balance_id}

        return self.send_websocket_request(self.name, data)
