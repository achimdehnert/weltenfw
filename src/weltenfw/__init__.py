"""
weltenfw - WeltenHub Client Framework

Typed REST client and Pydantic schemas for the WeltenHub Story Universe API.
"""

__version__ = "0.1.0"

from weltenfw.exceptions import (
    AuthError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    WeltenError,
)
from weltenfw.schema.base import BaseInput, BaseSchema

__all__ = [
    "__version__",
    "WeltenError",
    "NotFoundError",
    "AuthError",
    "RateLimitError",
    "ValidationError",
    "BaseSchema",
    "BaseInput",
]
