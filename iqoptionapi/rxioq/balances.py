from enum import Enum, IntEnum, unique


@unique
class BalanceTypes(IntEnum):
    REAL = 1
    TOURNAMENT = 2
    PRATICE = 4
    CRYPTO = 5


@unique
class BalanceOrderChanged(Enum):
    BINARY_OPTION = "binary"
    CFD = "cfd"
    CRYPTO = "crypto"
    DIGITAL_OPTION = "digital-option"
    FOREX = "forex"
    TURBO_OPTION = "turbo"


@unique
class BalancePositionChanged(Enum):
    BINARY_OPTION = "binary-option"
    CFD = "cfd"
    CRYPTO = "crypto"
    DIGITAL_OPTION = "digital-option"
    FOREX = "forex"
    TURBO_OPTION = "turbo-option"
