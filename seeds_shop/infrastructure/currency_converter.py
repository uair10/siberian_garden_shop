import asyncio
import logging
from decimal import ROUND_UP, Decimal

import aiohttp

from seeds_shop.core.models.enums.currency import Currency

logger = logging.getLogger(__name__)


async def get_currency_rate(currency_to: Currency) -> Decimal | None:
    url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5842.194 Safari/537.36",
    }

    if currency_to == Currency.ton:
        currency_from = "the-open-network"
    elif currency_to == Currency.btc:
        currency_from = "bitcoin"
    else:
        currency_from = "usd-coin"

    params = {"ids": currency_from, "vs_currencies": "rub"}
    async with aiohttp.ClientSession() as session, session.get(url, params=params, headers=headers) as response:
        logger.info(f"Requesting currency rate with params: {params}")
        if response.status != 200:
            resp_text = await response.text()
            print(f"Incorrect response from currency converter: {resp_text}")
            return None

        body = await response.json()
        rate = Decimal(body[currency_from]["rub"])
        return rate.quantize(Decimal("0.001"), rounding=ROUND_UP)


if __name__ == "__main__":
    print(asyncio.run(get_currency_rate(Currency.usdt)))
