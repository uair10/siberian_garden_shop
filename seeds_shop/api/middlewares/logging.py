import json
import logging
from typing import Awaitable, Callable

from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Logging request body, query and headers"""

    request_body = None
    if request.method in ("POST", "PUT", "PATCH") and "application/json" in request.headers.get("content-type", ""):
        try:
            # Читаем тело частями и собираем
            body_chunks = []
            async for chunk in request.stream():
                body_chunks.append(chunk)

            if body_chunks:
                body_bytes = b"".join(body_chunks)
                request_body = json.loads(body_bytes)

                # Восстанавливаем поток
                async def receive():
                    return {"type": "http.request", "body": body_bytes}

                request._receive = receive

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
