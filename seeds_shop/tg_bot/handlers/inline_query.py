from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from seeds_shop.core.services.delivery_method import DeliveryMethodService


async def inline_response(inline_query: InlineQuery, delivery_method_service: DeliveryMethodService):
    search_query = inline_query.query.strip()
    cities = await delivery_method_service.get_delivery_cities(city_name=search_query if search_query != "" else None)

    results = [
        InlineQueryResultArticle(
            id=str(city.id), title=city.title, input_message_content=InputTextMessageContent(message_text=city.title)
        )
        for city in cities
    ]

    await inline_query.answer(results=results, is_personal=True)
