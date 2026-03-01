"""
weltenfw - WeltenHub Client Framework

Typed REST client and Pydantic schemas for the WeltenHub Story Universe API.

Invariante: 1 WeltenClient = 1 Token = 1 Tenant.
"""

__version__ = "0.1.0"

from weltenfw.client import WeltenClient
from weltenfw.exceptions import (
    AuthError,
    NotFoundError,
    PaginationError,
    RateLimitError,
    ServerError,
    ValidationError,
    WeltenError,
)
from weltenfw.schema.base import BaseInput, BaseSchema

__all__ = [
    "__version__",
    "WeltenClient",
    "WeltenError",
    "NotFoundError",
    "AuthError",
    "RateLimitError",
    "ValidationError",
    "ServerError",
    "PaginationError",
    "BaseSchema",
    "BaseInput",
]
