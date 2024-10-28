from cashews.contrib.fastapi import CacheDeleteMiddleware, CacheEtagMiddleware, CacheRequestControlMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from seeds_shop.core.config import ApiConfig

from .verify_key import verify_key


def setup_middlewares(app: FastAPI, config: ApiConfig) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=verify_key)
    app.add_middleware(CacheDeleteMiddleware)
    app.add_middleware(CacheEtagMiddleware)
    app.add_middleware(CacheRequestControlMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.allowed_hosts)
