import uuid
from typing import Awaitable, Callable

from fastapi import Request
from starlette.responses import Response


async def set_request_id_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Passing request id to request state"""

    request.state.request_id = request.headers.get("X-Request-ID", uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(request.state.request_id)

    return response
