import enum


class BillStatus(enum.Enum):
    paid = "paid"
    waiting_payment = "waiting_payment"
    payment_failed = "payment_failed"
