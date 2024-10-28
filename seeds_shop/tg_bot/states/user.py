from aiogram.fsm.state import State, StatesGroup


class ClientSG(StatesGroup):
    start = State()


class LanguageSG(StatesGroup):
    select_language = State()


class LeaveReviewSG(StatesGroup):
    enter_review_text = State()


class UserProfileSG(StatesGroup):
    show_profile = State()


class CreateOrderSG(StatesGroup):
    enter_city = State()
    select_delivery_method = State()
    enter_contact_name = State()
    enter_phone = State()
    enter_address = State()
    enter_postal_code = State()
    show_delivery_message = State()
    select_payment_method = State()
    send_invoice_screenshot = State()


class UserOrdersSG(StatesGroup):
    orders_history = State()


class OrderDetailsSG(StatesGroup):
    order_details = State()
    confirm_order_payment = State()
    send_tracking_link = State()
    confirm_tracking_link = State()


class PaymentSG(StatesGroup):
    select_amount = State()
    create_payment = State()


class PromocodeSG(StatesGroup):
    enter_promocode = State()
