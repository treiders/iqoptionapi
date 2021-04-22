from enum import Enum
from typing import Any


class MessageTypes(Enum):
    API_GAME_BETINFO_RESULT = "api_game_betinfo_result"
    API_GAME_GETOPTIONS_RESULT = "api_game_getoptions_result"
    API_OPTION_INIT_ALL_RESULT = "api_option_init_all_result"
    AUTO_MARGIN_CALL_CHANGED = "auto-margin-call-changed"
    AVAILABLE_LEVERAGES = "available-leverages"
    BALANCE_CHANGED = "balance-changed"
    BALANCES = "balances"
    BUYCOMPLETE = "buyComplete"
    CANDLES_GENERATED = "candles-generated"
    CANDLES = "candles"
    COMMISSION_CHANGED = "commission-changed"
    DEFERRED_ORDERS = "deferred-orders"
    DIGITAL_OPTION_PLACED = "digital-option-placed"
    FINANCIAL_INFORMATION = "financial-information"
    HEARTBEAT = "heartbeat"
    HISTORY_POSITIONS = "history-positions"
    INITIALIZATION_DATA = "initialization-data"
    INSTRUMENT_QUOTES_GENERATED = "instrument-quotes-generated"
    INSTRUMENTS = "instruments"
    LEADERBOARD_DEALS_CLIENT = "leaderboard-deals-client"
    LEADERBOARD_USERINFO_DEALS_CLIENT = "leaderboard-userinfo-deals-client"
    LISTINFODATA = "listInfoData"
    LIVE_DEAL_BINARY_OPTION_PLACED = "live-deal-binary-option-placed"
    LIVE_DEAL_DIGITAL_OPTION = "live-deal-digital-option"
    LIVE_DEAL = "live-deal"
    OPTION_CLOSED = "option-closed"
    OPTION_OPENED = "option-opened"
    OPTION = "option"
    OPTIONS = "options"
    ORDER = "order"
    ORDER_CANCELED = "order-canceled"
    ORDER_PLACED_TEMP = "order-placed-temp"
    OVERNIGHT_FEE = "overnight-fee"
    POSITION_CHANGED = "position-changed"
    POSITION_CLOSED = "position-closed"
    POSITION_HISTORY = "position-history"
    POSITION = "position"
    POSITIONS = "positions"
    PROFILE = "profile"
    RESULT = "result"
    SOCKET_OPTION_CLOSED = "socket-option-closed"
    SOCKET_OPTION_OPENED = "socket-option-opened"
    SOLD_OPTIONS = "sold-options"
    STRIKE_LIST = "strike-list"
    TECHNICAL_INDICATORS = "technical-indicators"
    TOP_ASSETS_UPDATED = "top-assets-updated"
    TPSL_CHANGED = "tpsl-changed"
    TRADERS_MOOD_CHANGED = "traders-mood-changed"
    TRAINING_BALANCE_RESET = "training-balance-reset"
    UNDERLYING_LIST = "underlying-list"
    USER_PROFILE_CLIENT = "user-profile-client"
    USERS_AVAILABILIT = "users-availabilit"

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        return str(self) == other or super().__eq__(other)

    def __cmp__(self, other: object) -> int:
        return str(self).__cmp__(str(other))

    def __hash__(self) -> Any:
        return str(self).__hash__()
