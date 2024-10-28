from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic.v1.generics import GenericModel

TResult = TypeVar("TResult")
TData = TypeVar("TData")


@dataclass(frozen=True)
class ErrorResponse(GenericModel, Generic[TData]):
    message: str
    data: TData


@dataclass(frozen=True)
class OkResponse:
    status: int = 200
    result: TResult | None = None
    message: str | None = None
