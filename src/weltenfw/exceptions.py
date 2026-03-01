"""
weltenfw.exceptions - Exception hierarchy

Alle Exceptions erben von WeltenError. Kein stilles Fehlverhalten:
jeder HTTP-Fehler wird auf eine konkrete Exception gemappt.
"""

from __future__ import annotations


class WeltenError(Exception):
    """Basis-Exception fuer alle weltenfw-Fehler."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status_code={self.status_code!r}, message={self.message!r})"


class NotFoundError(WeltenError):
    """HTTP 404 - Ressource nicht gefunden."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)


class AuthError(WeltenError):
    """HTTP 401/403 - Authentifizierung oder Autorisierung fehlgeschlagen."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class RateLimitError(WeltenError):
    """HTTP 429 - Rate Limit ueberschritten."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(message, status_code=429)


class ValidationError(WeltenError):
    """HTTP 400/422 - Validierungsfehler im Request-Body."""

    def __init__(self, message: str = "Validation error", detail: dict | None = None) -> None:
        super().__init__(message, status_code=400)
        self.detail = detail or {}


class ServerError(WeltenError):
    """HTTP 5xx - Server-seitiger Fehler."""

    def __init__(self, message: str = "Server error", status_code: int = 500) -> None:
        super().__init__(message, status_code=status_code)


class PaginationError(WeltenError):
    """Pagination-Limit ueberschritten (Schutz vor Endlosschleifen)."""

    def __init__(self, max_pages: int) -> None:
        super().__init__(
            f"iter_all() aborted after {max_pages} pages. Set max_pages=None or increase the limit."
        )
        self.max_pages = max_pages
