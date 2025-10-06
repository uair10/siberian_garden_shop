from typing import Awaitable, Callable

import structlog
from starlette.requests import Request
from starlette.responses import Response


async def structlog_bind_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Passing request_id to all logs during the request"""

    with structlog.contextvars.bound_contextvars(request_id=str(request.state.request_id)):
        return await call_next(request)
