from collections.abc import Awaitable, Callable
from datetime import datetime

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from seeds_shop.core.config import ApiConfig
from seeds_shop.infrastructure.config_loader import load_config


async def verify_key(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
):
    if request.method == "OPTIONS":
        return await call_next(request)

    received_key = request.headers.get("X-Key", "")

    if load_config(ApiConfig, "api").debug:
        return await call_next(request)

    try:
        timestamp, random_value = map(int, received_key.split("-"))
    except (ValueError, TypeError):
        return JSONResponse(content={"detail": "Missing or invalid key"}, status_code=status.HTTP_401_UNAUTHORIZED)

    cur_date = datetime.utcnow()
    # Timestamp должен быть не старше двух минут
    if (cur_date - datetime.utcfromtimestamp(timestamp / 1000)).total_seconds() < 2 * 60:
        return await call_next(request)

    return JSONResponse(content={"detail": "Wrong key"}, status_code=status.HTTP_401_UNAUTHORIZED)
