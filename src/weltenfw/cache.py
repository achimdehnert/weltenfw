"""
weltenfw.cache - CacheBackend Protocol + Implementierungen

Kein stilles In-Memory-Fallback. Das Backend ist immer explizit konfiguriert.
Default ist NullCache (kein Cache, immer frische Daten).

Fuer Django-Konsumenten: weltenfw.django.cache.DjangoCache (Redis-backed).
"""

from __future__ import annotations

import time
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CacheBackend(Protocol):
    """Protocol fuer austauschbare Cache-Backends."""

    def get(self, key: str) -> list[Any] | None: ...
    def set(self, key: str, value: list[Any], ttl: int) -> None: ...
    def delete(self, key: str) -> None: ...
    def clear(self) -> None: ...


class NullCache:
    """Kein Cache - jeder Zugriff geht direkt an die API.

    Sicherer Default und fuer Tests: vollstaendig deterministisch,
    kein shared state zwischen Testlaeufen.
    """

    def get(self, key: str) -> None:
        return None

    def set(self, key: str, value: list[Any], ttl: int) -> None:
        pass

    def delete(self, key: str) -> None:
        pass

    def clear(self) -> None:
        pass


class MemoryCache:
    """In-process Cache mit TTL.

    WARNUNG: Nicht multiprocess-safe. Nur fuer Entwicklung und single-process
    Anwendungen. Fuer Gunicorn/Celery-Produktion: DjangoCache (Redis) verwenden.
    """

    def __init__(self, ttl: int = 3600) -> None:
        self._default_ttl = ttl
        self._store: dict[str, tuple[list[Any], float]] = {}

    def get(self, key: str) -> list[Any] | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if time.monotonic() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: list[Any], ttl: int) -> None:
        self._store[key] = (value, time.monotonic() + ttl)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()
