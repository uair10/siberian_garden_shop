### Base messages ###
confirm-btn = ✅ Подтвердить
back-btn = ⬅️ Назад
cancel-btn = ✖️ Отменить
main-menu-btn = ↪️ В главное меню
skip-btn = Пропустить
continue-btn = Продолжить
yes-btn = Да
no-btn = Нет

### DB errors ###
unknown-server-error = ❗️ Произошла ошибка на сервере
user-not-exists-msg = Пользователь не существует
user-already-exists-msg = Такой пользователь уже существует
order-already-exists-msg = Такой заказ уже существует
order-not-exists-msg = Заказ не существует
insufficient-stock-msg = ❗️ Количество доступных товаров изменилось. Соберите заказ еще раз
insufficient-bonuses = ❗ У вас на счету недостаточно бонусов для оплаты заказа


### Validation Errors ###
wrong-input-msg = ❗ Некорректное фото. Попробуйте еще раз
wrong-photo-extension = ❗ Поддерживаемые расширения фото: .jpeg, .png


### Menu ###
welcome =
    Здравствуйте, { $user }!
    Чтобы начать, просто выберите нужную вам опцию.
catalog-btn = 🛒 Каталог
orders-btn = 🛍️ Мои заказы
admin-btn = ⚙️ Администрирование
help-btn = ❓ Помощь
change-lang-btn = 🌍 Change language
select-lang-msg = Выберите язык
verify-age-to-use-bot = Для использования бота нужно подтвердить свой возраст
age-verified-msg = Ваш возраст подтвержден!
go-to-shopping-btn = Перейти к покупкам
bot-disabled-until-morning-msg = Доставка станет доступна завтра с 09:00 утра (Бангкок). Вы можете создать заказ, однако доставим его только завтра утром.
bot-disabled-msg = Бот работает только на предзаказы. Сообщим вам, как только сервис станет доступным

### Support ###
ticket-sent-msg = Ожидайте, в ближайшее время с вами свяжется менеджер


### Cart ###
cart-review-msg = Ваша корзина:{"\u000A"}{"\u000A"}
cart-total-summ =
    {"\u000A"}Итого: { $cart_total }{ $currency_symbol }
    Использовано бонусов: { $bonuses_amount }
select-delivery-type =
    {"\u000A"}
    Как вам удобно получить заказ?
delivery-btn = Доставка
change-cart-btn = Пересобрать корзину


### Orders ###
orders-history-msg = Ваши заказы:
unconfirmed-orders-msg = Заказы для подтверждения оплаты:
orders-for-shipping-msg = Заказы для отгрузки:
enter-city-msg = Для того, чтобы определить возможные способы доставки, а также их стоимость - введите город, в котором вам удобно получить заказ
city-is-not-supported-yet = Мы пока не осуществляем доставку в этот город
select-delivery-method = Выберите метод доставки:
enter-address-msg =
    📍 Введите адрес доставки
    Пример: Г. Москва, ул. Пушкина, д. Колотушкина
enter-postal-code-msg = Введите почтовый код. Пример: 186339
enter-phone-msg = 📞 Введите ваш номер телефона
enter-name-msg = Введите ваше имя
select-payment-method-msg = Выберите удобный для вас способ оплаты заказа:
rub = 🇷🇺 Карта - RUB
usdt = 💲 Крипто - USDT
btc = 💰 Крипто - BTC
ton = 💎 Крипто - TON
photo-processing-msg = Подождите, фотография обрабатывается
send-invoice-screenshot-msg =
    Переведите сумму { $summ } { $currency } на счет ⬇️

    <code>{ $payment_address }</code>

    Сумма доставки: { $delivery_cost } { $currency }

    Для того чтобы подтвердить оплату, <b>отправьте скриншот</b> квитанции ответным сообщением.
    Время на оплату - 1 час{"\u000A"}
after-payment-msg = 🙏 <b>Благодарим за оплату</b>. Как только оплата будет подтверждена (в течение 15-ти минут), вы получите уведомление
order-collecting-msg = ✅ Оплата заказа <b>подтверждена</b>. Ваш заказ собирается на складе
order-in-transit-msg =
    🚚 Ваш заказ <b>в пути</b>

    Для связи с курьером - <b>перейдите по ссылке</b>
    { $tracking_link }

    Хорошего дня!
order-closed-msg = Ваш заказ №{ $order_id } был закрыт
order-cancelled-msg = Ваш заказ №{ $order_id } был отменен
payment-time-expiring-msg = Оставшееся время на оплату - 10 минут, после чего заказ будет аннулирован
payment-time-expired-msg = Время на оплату истекло
request-new-address-btn = Запросить новые реквизиты
contact-support-btn = Связаться с менеджером
prepaid-delivery-order = <b>🚚 PREPAID DELIVERY ORDER</b>{"\u000A"}
order-id = <b>Номер заказа</b>: { $order_id }
order-status = <b>Статус платежа:</b> { $status }
order-payment-method = <b>Метод оплаты:</b> { $currency }
order-delivery-method = <b>Метод доставки:</b> { $delivery_method }
order-delivery-duration = <b>Срок доставки в днях:</b> { $delivery_duration }
order-products =
    {"\u000A"}Товары в заказе:
    { $order_products }
order-summ = <b>Сумма заказа:</b> { $summ } { $currency_symbol }
order-shipping-address = <b>Адрес доставки:</b> <code>{ $shipping_address }</code>
order-user-phone = <b>Контактный телефон:</b> <code>{ $user_phone }</code>
order-contact-name = <b>Имя клиента:</b> { $contact_name }
order-tracking-link = <b>Ссылка для отслеживания:</b> { $tracking_link }
order-comment = <b>Комментарий:</b> { $comment }
was-created = <b>Дата создания:</b> { $was_created }
bonuses-credited-for-order =
    Вам начислено { $bonuses_amount } бонусов за заказ!
    { $days_before_using_bonuses ->
        [0] Вы можете использовать их при следующем заказе
        *[other] Вы сможете использовать их через { $days_before_using_bonuses } день(ей) с момента начисления
    }
bonuses-used = <b>Использовано бонусов:</b> { $bonuses_amount }

## Order statuses ##
created = Создан
payment_not_confirmed = Оплата не подтверждена
payment_confirmed = Оплата подтверждена
collecting = В сборке
in_transit = В пути
closed = Закрыт
cancelled = Отменен
payment_canceled = Оплата отменена
on_dispute = Решается администратором

### Promocodes ###
wrong-promocode = Промокод недействителен. Проверьте правильность набора
promocode-already-used = Промокод уже был использован вами
promocode-usage-limit-reached = Промокод был использован максимальное количество раз
promocode-activated = ✅ Промокод активирован! Ваша скидка { $discount_percent}%

### Ticket ###
take-ticket-btn = Взять тикет
tickets-history-msg = Ваши тикеты:
ticket-taken-msg = ✅ Тикет взят в работу
ticket-already-taken = Тикет уже взят админом { $admin_id }
ticket-overview = <b>Информация о тикете</b>{"\u000A"}
ticket-id = ID: { $ticket_id }
ticket-status = Статус тикета: { $status }
ticket-order-id = ID заказа: { $order_id }
ticket-user-id = ID клиента: { $user_id }
ticket-user-username = Ник клиента: @{ $username }
close-order-btn = Закрыть заказ
cancel-order-btn = Отменить заказ
close-ticket-btn = Закрыть тикет
confirm-closing-ticket-msg = Вы подтверждаете закрытие тикета?
confirm-closing-order-msg = Вы подтверждаете закрытие заказа?
confirm-canceling-order-msg = Вы подтверждаете отмену заказа?
ticket-closed-msg = ✅ Тикет закрыт
ticket-order-closed-msg = ✅ Заказ закрыт
ticket-order-cancelled-msg = ✅ Заказ отменен

## Ticket statuses ##
opened = Открыт
closed = Закрыт

### Reviews ###
leave-review-btn = Оставить отзыв
enter-review-text-msg = Введите ваш отзыв
thanks-for-review-msg = Спасибо за отзыв!


### Admin messages ###
select-option-msg = Выберите нужную опцию:
send-mailing-btn = Отправить рассылку
unconfirmed-orders-btn = Заказы для подтверждения оплаты
orders-for-shipping-btn = Заказы для отгрузки
tickets-btn = Открытые тикеты
bot-status-btn = Статус бота

new-order-msg =
    🛒 Новый заказ №{ $order_id }
    Магазин: { $shop_id }
    Сумма: { $order_summ }{ $currency_symbol }
order-status-changed-msg = Изменен статус заказа №{ $order_id }. Новый статус: { $status }
order-automatically-closed-msg = Заказ №{ $order_id } был автоматически закрыт
order-automatically-cancelled-msg = Заказ №{ $order_id } был автоматически отменен
new-order-for-payment-confirmation-msg = Новый заказ для подтверждения оплаты. ID: { $order_id }
new-ticket-msg = Новый тикет №{ $ticket_id } от пользователя { $user_id } в магазине { $shop_id }
ticket-assigned-by-admin-msg = Тикет №{ $ticket_id } взят в работу админом { $admin_id }
ticket-was-closed-msg = Тикет №{ $ticket_id } был закрыт админом { $admin_id }

go-to-order-btn = Перейти в заказ
confirm-order-payment-btn = Подтвердить оплату заказа
confirm-order-payment-msg = Подтвердить оплату?
order-payment-confirmed-msg = ✅ Оплата заказа подтверждена

## Mailing ##
enter-mailing-text-msg = Введите текст рассылки
select-mailing-date-msg = Выберите дату рассылки
select-mailing-time-msg = Введите время рассылки в формате 23:59:59
current-time-msg = Текущее время: <code>{ $current_time }</code>
wrong-time-format-msg = Время не в том формате
confirm-mailing-msg = Подтвердить рассылку?
yes-btn = Да
no-btn = Нет
mailing-planned-msg = Рассылка запланирована
mailing-cancelled-msg = Рассылка отменена
bot-status = Статус бота:
disable-bot-btn = Выключить бота
bot-disabled-until = Бот отключен до: { $bot_disabled_until }
enable-bot-btn = Включить бота
select-bot-disable-type = Насколько отключить бота?
until-enabled-btn = До следующего включения
until-morning-btn = До завтра


### Stuff messages ###
send-tracking-link-btn = Отправить ссылку для отслеживания
new-order-for-shipping-msg =
    Новый заказ. Номер заказа: { $order_id }
hold-off-btn = Отложить на 5 минут
waiting-tracking-link-msg = Отправьте ссылку на службу доставки
tracking-link-confirmation-msg =
    Вы уверены, что введенная ссылка корректна?
    { $tracking_link }
order-tracking-link-changed-msg = ✅ Ссылка обновлена