"""
weltenfw.django.cache - DjangoCache Backend

Nutzt Django's Cache-Framework (typischerweise Redis via django-redis).
Multiprocess-safe: alle Gunicorn-Worker und Celery-Worker teilen denselben Cache.

Voraussetzung: pip install weltenfw[django]

Import ist lazy um AppRegistryNotReady bei fruehzeitigem Import
in Celery-Worker-Startup zu vermeiden.
"""

from __future__ import annotations

from typing import Any


class DjangoCache:
    """Django-Cache-Backend fuer weltenfw Lookups."""

    _PREFIX = "weltenfw:"

    def __init__(self, alias: str = "default", ttl: int = 3600) -> None:
        try:
            from django.core.cache import caches as _caches  # noqa: F401
        except ImportError as exc:
            raise ImportError(
                "DjangoCache requires Django. Install with: pip install weltenfw[django]"
            ) from exc
        self._alias = alias
        self._ttl = ttl

    def _key(self, key: str) -> str:
        return f"{self._PREFIX}{key}"

    def get(self, key: str) -> list[Any] | None:
        from django.core.cache import caches

        return caches[self._alias].get(self._key(key))

    def set(self, key: str, value: list[Any], ttl: int) -> None:
        from django.core.cache import caches

        caches[self._alias].set(self._key(key), value, timeout=ttl)
        if not hasattr(self, "_registered_keys"):
            self._registered_keys: set[str] = set()
        self._registered_keys.add(key)

    def delete(self, key: str) -> None:
        from django.core.cache import caches

        caches[self._alias].delete(self._key(key))

    def clear(self) -> None:
        from django.core.cache import caches

        cache = caches[self._alias]
        if hasattr(cache, "delete_pattern"):
            cache.delete_pattern(f"{self._PREFIX}*")
        else:
            known = getattr(self, "_registered_keys", set())
            if known:
                cache.delete_many([self._key(k) for k in known])
