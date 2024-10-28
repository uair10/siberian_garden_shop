import enum


class Currency(enum.Enum):
    rub = "rub"
    usdt = "usdt"
    btc = "btc"
    ton = "ton"


class CurrencySymbol(enum.Enum):
    rub = "₽"
    usdt = "USDT"
    btc = "BTC"
    ton = "TON"
