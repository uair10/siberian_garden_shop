### Base messages ###
confirm-btn = ✅ Confirm
back-btn = ⬅️ Back
cancel-btn = ✖️ Cancel
main-menu-btn = ↪️ Main menu
skip-btn = Skip
continue-btn = Continue
yes-btn = Yes
no-btn = No

### DB errors ###
unknown-server-error = ❗️ An error occurred on the server
user-not-exists-msg = User doesn't exist
user-already-exists-msg = This user already exists
order-already-exists-msg = This order already exists
order-not-exists-msg = The order doesn't exist
insufficient-stock-msg = ❗️The number of available items has changed. Re-assemble your order
insufficient-bonuses = ❗ You do not have enough bonuses on your account to pay for the order


### Validation Errors ###
wrong-input-msg = ❗ Incorrect photo. Try again
wrong-photo-extension = ❗ Supported photo extensions: .jpeg, .png


### Menu ###
welcome =
    Hello, { $user }!
    Select option to start.
verify-btn = Confirm
catalog-btn = 🛒 Catalog
orders-btn = 🛍️ My orders
admin-btn = ⚙️ Admin panel
help-btn = ❓ Help
change-lang-btn = 🌍 Сменить язык
select-lang-msg = Select language
verify-age-to-use-bot = You have to confirm your age to use bot
age-verified-msg = Your age is verified!
go-to-shopping-btn = Go to shopping
bot-disabled-until-morning-msg = Delivery will be available tomorrow from 09:00 am (Bangkok). You can create an order, but we will only deliver it tomorrow morning.
bot-disabled-msg = The bot only works for pre-orders. We will let you know as soon as the service becomes available

### Support ###
ticket-sent-msg = Expect a manager to contact you shortly


### Cart ###
cart-review-msg = Your cart:{"\u000A"}{"\u000A"}
cart-total-summ =
    {"\u000A"}Total: { $cart_total }{ $currency_symbol }
    Bonuses used: { $bonuses_amount }
select-delivery-type =
    {"\u000A"}
    How would you like to receive your order?
delivery-btn = Delivery
change-cart-btn = Change cart


### Orders ###
orders-history-msg = Your orders:
unconfirmed-orders-msg = Orders for payment confirmation:
orders-for-shipping-msg = Orders for shipping:
enter-city-msg = In order to determine the possible methods of delivery, as well as their cost - enter the city in which it is convenient for you to receive the order
city-is-not-supported-yet = We are not shipping to this city yet
select-delivery-method = Select delivery method:
enter-address-msg =
    📍 Enter delivery address
    Example: Moscow, Pushkin St., Kolotushkin's house
enter-postal-code-msg = Enter postal code. Example: 186339
enter-phone-msg = 📞 Put your phone number
enter-name-msg = Put your name
select-payment-method-msg = Select payment method:
rub = 🇷🇺 Card - RUB
usdt = 💲 Crypto - USDT
btc = 💰 Crypto - BTC
ton = 💎 Crypto - TON
cash = 💵 Cash
photo-processing-msg = Hold on, the photo is being processed
send-invoice-screenshot-msg =
    Transfer the amount { $summ } { $currency } to account ⬇️

    <code>{ $payment_address }</code>

    Delivery summ: { $delivery_cost } { $currency }

    To confirm payment, <b>send a screenshot</b> of the receipt by return message.
    Time for payment - 1 hour{"\u000A"}
after-payment-msg = 🙏 <b>Thank you for your payment</b>. As soon as payment is confirmed (within 15 minutes), you will be notified
order-collecting-msg = ✅ Payment for your order has been <b>confirmed</b>. Your order is being collected from the warehouse
order-in-transit-msg =
    🚚 Your order is <b>on its way!</b>

    To contact the courier - <b>follow this link</b>
    { $tracking_link }

    Have a nice day!
order-closed-msg = Your order №{ $order_id } was closed
order-cancelled-msg = Your order №{ $order_id } was cancelled
payment-time-expiring-msg = The remaining time for payment is 10 minutes, after which the order will be canceled
payment-time-expired-msg = Time for payment has expired
request-new-address-btn = Request new details
contact-support-btn = Contact support
prepaid-delivery-order = <b>🚚 PREPAID DELIVERY ORDER</b>{"\u000A"}
order-id = <b>Order №:</b> { $order_id }
order-status = <b>Payment status:</b> { $status }
order-payment-method = <b>Payment method:</b> { $currency }
order-delivery-method = <b>Delivery method:</b> { $delivery_method }
order-delivery-duration = <b>Delivery duration:</b> { $delivery_duration } day(s)
order-products =
    {"\u000A"}Products:
    { $order_products }
order-summ = <b>Order sum:</b> { $summ } { $currency_symbol }
order-shipping-address = <b>Shipping address:</b> { $shipping_address }
order-user-phone = <b>Contact phone:</b> { $user_phone }
order-contact-name = <b>Contact name:</b> { $contact_name }
order-tracking-link = <b>Tracking link:</b> { $tracking_link }
order-comment = <b>Comment:</b> { $comment }
was-created = <b>Date of creation:</b> { $was_created }
bonuses-credited-for-order =
    You have been credited { $bonuses_amount } bonuses for your order!
    { $days_before_using_bonuses ->
        [0] You can use them on your next order
        *[other] You will be able to use them { $days_before_using_bonuses } day(s) from the date of accrual
    }
bonuses-used = <b>Bonuses used:</b> { $bonuses_amount }

## Order statuses ##
created = Created
payment_not_confirmed = Payment not confirmed
payment_confirmed = Payment confirmed
collecting = Collecting
in_transit = In transit
closed = Closed
cancelled = Cancelled
payment_canceled = Payment cancelled
on_dispute = On dispute

### Promocodes ###
wrong-promocode = Promocode is invalid. Check if you typed it correctly
promocode-already-used = Promocode has already been used by you
promocode-usage-limit-reached = Promocode usage limit reached
promocode-activated = ✅ Promocode activated! Your discount is { $discount_percent}%

### Ticket ###
take-ticket-btn = Take ticket
tickets-history-msg = Your tickets:
ticket-taken-msg = ✅ Ticket taken
ticket-already-taken = Ticket taken by admin { $admin_id }
ticket-overview = <b>Ticket info</b>{"\u000A"}
ticket-id = ID: { $ticket_id }
ticket-status = Status: { $status }
ticket-order-id = Order ID: { $order_id }
ticket-user-id = User ID: { $user_id }
ticket-user-username = User username: @{ $username }
close-order-btn = Close order
cancel-order-btn = Cancel order
close-ticket-btn = Close ticket
confirm-closing-ticket-msg = Are you sure you want to close the ticket?
confirm-closing-order-msg = Are you sure you want to close the order?
confirm-canceling-order-msg = Are you sure you want to cancel the order?
ticket-closed-msg = ✅ Ticket closed
ticket-order-closed-msg = ✅ Order closed
ticket-order-cancelled-msg = ✅ Order cancelled

## Ticket statuses ##
opened = Opened
closed = Closed

### Reviews ###
leave-review-btn = Leave review
enter-review-text-msg = Enter your review
thanks-for-review-msg = Thank you for your feedback!


### Admin messages ###
select-option-msg = Select option:
send-mailing-btn = Send mailing
unconfirmed-orders-btn = Orders for payment confirmation
orders-for-shipping-btn = Orders for shipping
tickets-btn = Opened tickets
bot-status-btn = Bot status

new-order-msg =
    🛒 Новый заказ №{ $order_id }
    Магазин: { $shop_id }
    Сумма: { $order_summ }{ $currency_symbol }
order-status-changed-msg =
    Изменен статус заказа №{ $order_id }.
    Новый статус: { $status }
order-automatically-closed-msg = Заказ №{ $order_id } был автоматически закрыт
order-automatically-cancelled-msg = Заказ №{ $order_id } был автоматически отменен
new-order-for-payment-confirmation-msg = Новый заказ для подтверждения оплаты. ID: { $order_id }
new-ticket-msg = Новый тикет №{ $ticket_id } от пользователя { $user_id } в магазине { $shop_id }
ticket-assigned-by-admin-msg = Тикет №{ $ticket_id } взят в работу админом { $admin_id }
ticket-was-closed-msg = Тикет №{ $ticket_id } был закрыт админом { $admin_id }

go-to-order-btn = Go to order
confirm-order-payment-btn = Confirm order payment
confirm-order-payment-msg = Confirm payment?
order-payment-confirmed-msg = ✅ Payment confirmed

## Mailing ##
enter-mailing-text-msg = Enter mailing text
select-mailing-date-msg = Select mailing date
select-mailing-time-msg = Enter the mailing time in the format 23:59:59
current-time-msg = Current time: <code>{ $current_time }</code>
wrong-time-format-msg = Wrong time format
confirm-mailing-msg = Confirm mailing?
yes-btn = Yes
no-btn = No
mailing-planned-msg = Mailing planned
mailing-cancelled-msg = Mailing cancelled
bot-status = Bot status:
disable-bot-btn = Disable bot
bot-disabled-until = Bot disabled until: { $bot_disabled_until }
enable-bot-btn = Enable bot
select-bot-disable-type = For how long to disable the bot?
until-enabled-btn = Until enable
until-morning-btn = Until morning


### Stuff messages ###
send-tracking-link-btn = Send tracking link
new-order-for-shipping-msg =
    New order. Order №: { $order_id }
hold-off-btn = Set aside for 5 minutes
waiting-tracking-link-msg = Send a link to the delivery service
tracking-link-confirmation-msg =
    Are you sure the link you entered is correct??
    { $tracking_link }
order-tracking-link-changed-msg = ✅ Tracking link updated