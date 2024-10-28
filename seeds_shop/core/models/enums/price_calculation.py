import enum


class PromocodeApplyStrategy(enum.Enum):
    TO_DISCOUNTED_PRICE = "TO_DISCOUNTED_PRICE"
    TO_ORIGINAL_PRICE = "TO_ORIGINAL_PRICE"


class BonusesApplyStrategy(enum.Enum):
    TO_DISCOUNTED_PRICE = "TO_DISCOUNTED_PRICE"
    TO_ORIGINAL_PRICE = "TO_ORIGINAL_PRICE"
