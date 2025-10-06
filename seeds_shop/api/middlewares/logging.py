import logging
from typing import Awaitable, Callable

from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Logging request body, query and headers"""

    request_body = None
    if "application/json" in request.headers.get("content-type", ""):
        try:
            request_body = await request.json()
        except Exception as e:
            logger.error(f"Error reading request JSON: {e}")

    request_data = {
        "query": dict(request.query_params),
        "request_body": request_body,
        "request_headers": dict(request.headers),
    }
    if request.url.path not in ("/docs", "/openapi.json"):
        logger.info(
            f"Handling request: {request.method} {request.url.path}", extra={k: v for k, v in request_data.items() if v}
        )

    return await call_next(request)
