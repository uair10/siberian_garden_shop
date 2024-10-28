import logging
from collections.abc import Awaitable, Callable
from functools import partial

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request

from seeds_shop.api.controllers.responses.base_responses import ErrorResponse
from seeds_shop.core.exceptions.common import AppException
from seeds_shop.core.exceptions.order import InsufficientStock
from seeds_shop.core.exceptions.user import UserNameNotExist, UserTgIdNotExist

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, error_handler(status.HTTP_500_INTERNAL_SERVER_ERROR))
    app.add_exception_handler(UserTgIdNotExist, error_handler(status.HTTP_404_NOT_FOUND))
    app.add_exception_handler(UserNameNotExist, error_handler(status.HTTP_404_NOT_FOUND))
    app.add_exception_handler(InsufficientStock, error_handler(status.HTTP_409_CONFLICT))
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: status) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(handle_error, status_code=status_code)


async def unknown_exception_handler(_, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(message="Unknown server error has occurred", data=err),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(request: Request, err: AppException, status_code: int) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(message=err.message, data=err.__class__.__name__),
        status_code=status_code,
    )
