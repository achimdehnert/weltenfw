"""
weltenfw.resources.lookups - Lookup Resource (read-only, gecacht)

Alle Lookups sind read-only. Werden via CacheBackend gecacht.
Cache-Key = Lookup-Name (z.B. 'genres', 'moods').
"""

from __future__ import annotations

from typing import Any

from weltenfw.cache import CacheBackend, NullCache
from weltenfw.schema.lookups import (
    BeatTypeSchema,
    CharacterRoleSchema,
    ConflictLevelSchema,
    GenreSchema,
    LocationTypeSchema,
    LookupSchema,
    MoodSchema,
    SceneStatusSchema,
    SceneTypeSchema,
    TransportTypeSchema,
)


class LookupResource:
    """Read-only Resource fuer alle Lookup-Tabellen.

    Erbt nicht von BaseResource da nur GET (keine CRUD).
    Cache ist immer explizit konfiguriert (kein stilles Fallback).

    Args:
        http:    Synchroner Transport.
        cache:   CacheBackend (default: NullCache).
        ttl:     Cache-TTL in Sekunden (default: 3600).
    """

    def __init__(self, http: Any, cache: CacheBackend | None = None, ttl: int = 3600) -> None:
        self._http = http
        self._cache: CacheBackend = cache or NullCache()
        self._ttl = ttl

    def _fetch(self, path: str, key: str, schema_cls: type[LookupSchema]) -> list:
        cached = self._cache.get(key)
        if cached is not None:
            return [schema_cls.model_validate(item) for item in cached]
        data = self._http.get(path)
        results = data.get("results", data) if isinstance(data, dict) else data
        self._cache.set(key, results, ttl=self._ttl)
        if hasattr(self._cache, "register_key"):
            self._cache.register_key(key)  # type: ignore[attr-defined]
        return [schema_cls.model_validate(item) for item in results]

    def genres(self) -> list[GenreSchema]:
        return self._fetch("/lookups/genres", "genres", GenreSchema)  # type: ignore[return-value]

    def moods(self) -> list[MoodSchema]:
        return self._fetch("/lookups/moods", "moods", MoodSchema)  # type: ignore[return-value]

    def conflict_levels(self) -> list[ConflictLevelSchema]:
        return self._fetch("/lookups/conflict-levels", "conflict_levels", ConflictLevelSchema)  # type: ignore[return-value]

    def location_types(self) -> list[LocationTypeSchema]:
        return self._fetch("/lookups/location-types", "location_types", LocationTypeSchema)  # type: ignore[return-value]

    def scene_types(self) -> list[SceneTypeSchema]:
        return self._fetch("/lookups/scene-types", "scene_types", SceneTypeSchema)  # type: ignore[return-value]

    def character_roles(self) -> list[CharacterRoleSchema]:
        return self._fetch("/lookups/character-roles", "character_roles", CharacterRoleSchema)  # type: ignore[return-value]

    def transport_types(self) -> list[TransportTypeSchema]:
        return self._fetch("/lookups/transport-types", "transport_types", TransportTypeSchema)  # type: ignore[return-value]

    def scene_statuses(self) -> list[SceneStatusSchema]:
        return self._fetch("/lookups/scene-statuses", "scene_statuses", SceneStatusSchema)  # type: ignore[return-value]

    def beat_types(self) -> list[BeatTypeSchema]:
        return self._fetch("/lookups/beat-types", "beat_types", BeatTypeSchema)  # type: ignore[return-value]
