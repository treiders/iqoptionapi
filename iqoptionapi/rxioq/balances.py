from enum import Enum, unique


@unique
class BalanceTypes(Enum):
    REAL = 1
    TOURNAMENT = 2
    PRATICE = 4
    CRYPTO = 5


@unique
class BalanceOrderChanged(Enum):
    CFD = "cfd"
    FOREX = "forex"
    CRYPTO = "crypto"
    DIGITAL_OPTION = "digital-option"
    TURBO_OPTION = "turbo"
    BINARY_OPTION = "binary"


@unique
class BalancePositionChanged(Enum):
    CFD = "cfd"
    CRYPTO = "crypto"
    FOREX = "forex"
    DIGITAL_OPTION = "digital-option"
    BINARY_OPTION = "binary-option"
    TURBO_OPTION = "turbo-option"