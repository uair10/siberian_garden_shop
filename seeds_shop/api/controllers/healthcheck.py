from fastapi import APIRouter, status

from seeds_shop.api.controllers.responses.base_responses import OkResponse

healthcheck_router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
)


@healthcheck_router.get("/", status_code=status.HTTP_200_OK)
async def get_status() -> OkResponse:
    return OkResponse()
