import enum


class OrderStatus(enum.Enum):
    created = "Создан"
    payment_not_confirmed = "Оплата не подтверждена"
    payment_confirmed = "Оплата подтверждена"
    collecting = "В сборке"
    in_transit = "В пути"
    closed = "Закрыт"
    cancelled = "Отменен"
    payment_canceled = "Оплата отменена"
    on_dispute = "Решается администратором"
