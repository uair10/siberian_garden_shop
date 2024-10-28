from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login import current_user

from seeds_shop.admin_panel.app import db
from seeds_shop.admin_panel.app.constants import media_path
from seeds_shop.admin_panel.app.views import (
    AdminUserBaseModelview,
    BonusModelView,
    CategoryModelView,
    DeliveryCityModelView,
    DeliveryMethodModelView,
    DeliveryZoneModelView,
    DiscountModelView,
    MyAdminIndexView,
    MyFileAdmin,
    OrderLineModelView,
    OrderModelView,
    PaymentDetailsModelView,
    ProductFeaturesModelView,
    ProductImageModelView,
    ProductModelView,
    PromocodeModelView,
    ReviewModelView,
    SettingsModelView,
    ShopModelView,
    StockModelView,
    TicketModelView,
    UserModelView,
)
from seeds_shop.infrastructure.database.models import (
    AdminUser,
    BonusOperation,
    BotSettings,
    Category,
    DeliveryCity,
    DeliveryMethod,
    DeliveryZone,
    Discount,
    Feeling,
    Genetics,
    Order,
    OrderLine,
    PaymentDetails,
    Product,
    ProductImage,
    Promocode,
    Review,
    Shop,
    Stock,
    Ticket,
    User,
)


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated


def init_admin_panel(app):
    admin = Admin(
        app,
        name="Admin Dashboard",
        base_template="myadmin3/my_master.html",
        template_mode="bootstrap4",
        index_view=MyAdminIndexView(url="/"),
    )

    admin.add_view(
        UserModelView(
            User,
            db.session,
            name="Пользователи",
            menu_icon_type="fas",
            menu_icon_value="fa-user",
            endpoint="users",
        ),
    )
    admin.add_view(
        OrderModelView(
            Order,
            db.session,
            name="Заказы",
            menu_icon_type="fas",
            menu_icon_value="fa-shopping-cart",
            endpoint="orders",
        ),
    )
    admin.add_view(
        OrderLineModelView(
            OrderLine,
            db.session,
            name="Товары в заказах",
            menu_icon_type="fas",
            menu_icon_value="fa-shopping-cart",
            endpoint="orders-lines",
        ),
    )
    admin.add_view(
        CategoryModelView(
            Category,
            db.session,
            name="Категории",
            menu_icon_type="fas",
            menu_icon_value="fa-list",
            endpoint="categories",
        ),
    )
    admin.add_view(
        ProductModelView(
            Product,
            db.session,
            name="Товары",
            menu_icon_type="fas",
            menu_icon_value="fa-cubes",
            endpoint="products",
        ),
    )
    admin.add_view(
        ProductImageModelView(
            ProductImage,
            db.session,
            name="Фото товаров",
            menu_icon_type="fas",
            menu_icon_value="fa-image",
            endpoint="product-images",
        ),
    )
    admin.add_category("Характеристики товаров")
    admin.add_view(
        ProductFeaturesModelView(
            Genetics,
            db.session,
            name="Genetics",
            endpoint="genetics",
            category="Характеристики товаров",
        ),
    )
    admin.add_view(
        ProductFeaturesModelView(
            Feeling,
            db.session,
            name="Feelings",
            endpoint="feelings",
            category="Характеристики товаров",
        ),
    )
    admin.add_view(
        ShopModelView(
            Shop,
            db.session,
            name="Магазины",
            menu_icon_type="fas",
            menu_icon_value="fa-address-card",
            endpoint="shops",
        ),
    )
    admin.add_category("Остатки в магазинах")
    for shop in db.session.query(Shop).all():
        admin.add_view(
            StockModelView(
                model=Stock,
                session=db.session,
                shop_id=shop.id,
                name=shop.title,
                endpoint=f"stocks-{shop.id}",
                category="Остатки в магазинах",
            ),
        )
    admin.add_view(
        DeliveryZoneModelView(
            DeliveryZone,
            db.session,
            name="Зоны доставки",
            menu_icon_type="fas",
            menu_icon_value="fa-map-marker",
            endpoint="delivery_zone",
        ),
    )
    admin.add_view(
        DeliveryMethodModelView(DeliveryMethod, db.session, name="Методы доставки", endpoint="delivery_method")
    )
    admin.add_view(DeliveryCityModelView(DeliveryCity, db.session, name="Города доставки", endpoint="delivery_city"))
    admin.add_view(
        DiscountModelView(
            Discount,
            db.session,
            name="Скидки",
            menu_icon_type="fas",
            menu_icon_value="fa-credit-card",
            endpoint="discounts",
        ),
    )
    admin.add_view(
        BonusModelView(
            BonusOperation,
            db.session,
            name="Бонусы",
            menu_icon_type="fas",
            menu_icon_value="fa-gift",
            endpoint="bonuses",
        ),
    )
    admin.add_view(
        PromocodeModelView(
            Promocode,
            db.session,
            name="Промокоды",
            menu_icon_type="fas",
            menu_icon_value="fa-percent",
            endpoint="promocodes",
        ),
    )
    admin.add_view(
        PaymentDetailsModelView(
            PaymentDetails,
            db.session,
            name="Данные для платежей",
            menu_icon_type="fas",
            menu_icon_value="fa-credit-card",
            endpoint="payment_details",
        ),
    )
    admin.add_view(
        TicketModelView(
            Ticket,
            db.session,
            name="Тикеты",
            menu_icon_type="fas",
            menu_icon_value="fa-question",
            endpoint="tickets",
        ),
    )
    admin.add_view(
        ReviewModelView(
            Review,
            db.session,
            name="Отзывы",
            menu_icon_type="fas",
            menu_icon_value="fa-comments",
            endpoint="reviews",
        ),
    )
    admin.add_view(
        AdminUserBaseModelview(
            AdminUser,
            db.session,
            name="Администраторы",
            menu_icon_type="fas",
            menu_icon_value="fa-users",
            endpoint="admin-user",
        ),
    )
    admin.add_view(
        SettingsModelView(
            BotSettings,
            db.session,
            name="Настройки",
            menu_icon_type="fas",
            menu_icon_value="fa-gears",
            endpoint="settings",
        ),
    )

    admin.add_view(
        MyFileAdmin(
            media_path,
            name="Загруженные файлы",
            menu_icon_type="fas",
            menu_icon_value="fa-copy",
        ),
    )
