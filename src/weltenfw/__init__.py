"""
weltenfw - WeltenHub Client Framework

Typed REST client and Pydantic schemas for the WeltenHub Story Universe API.

Invariante: 1 WeltenClient = 1 Token = 1 Tenant.
"""

__version__ = "0.2.0"

from weltenfw.backends.base import (
    AbstractWorldBackend,
    CharacterPage,
    CharacterResult,
    WorldPage,
    WorldResult,
)
from weltenfw.backends.local import LocalWorldBackend
from weltenfw.backends.weltenhub import WeltenhubBackend
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
    # Client
    "WeltenClient",
    # Backends (ADR-117)
    "AbstractWorldBackend",
    "WeltenhubBackend",
    "LocalWorldBackend",
    "WorldResult",
    "CharacterResult",
    "WorldPage",
    "CharacterPage",
    # Exceptions
    "WeltenError",
    "NotFoundError",
    "AuthError",
    "RateLimitError",
    "ValidationError",
    "ServerError",
    "PaginationError",
    # Schema bases
    "BaseSchema",
    "BaseInput",
]
