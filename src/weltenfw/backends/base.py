"""
weltenfw.backends.base — AbstractWorldBackend Protocol + Result types (ADR-117)

All concrete backends implement this Protocol. Callers type-hint against
AbstractWorldBackend so the backend is swappable without changing call sites.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class WorldResult:
    """Returned by AbstractWorldBackend.create_world / get_world."""

    id: str
    name: str
    description: str = ""
    setting_era: str = ""
    genre_name: str = ""
    backend: str = "unknown"
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class CharacterResult:
    """Returned by AbstractWorldBackend.create_character / get_character."""

    id: str
    name: str
    world_id: str = ""
    role_name: str = ""
    description: str = ""
    personality: str = ""
    backend: str = "unknown"
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class LocationResult:
    """Returned by AbstractWorldBackend.list_locations / get_location."""

    id: str
    name: str
    world_id: str = ""
    parent_id: str | None = None
    location_type_name: str = ""
    description: str = ""
    full_path: str = ""
    backend: str = "unknown"
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class SceneResult:
    """Returned by AbstractWorldBackend.list_scenes / get_scene."""

    id: str
    title: str
    story_id: str = ""
    summary: str = ""
    location_name: str = ""
    order: int = 0
    backend: str = "unknown"
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class WorldPage:
    """Paginated list of worlds."""

    results: list[WorldResult] = field(default_factory=list)
    count: int = 0


@dataclass(frozen=True)
class CharacterPage:
    """Paginated list of characters."""

    results: list[CharacterResult] = field(default_factory=list)
    count: int = 0


@dataclass(frozen=True)
class LocationPage:
    """Paginated list of locations."""

    results: list[LocationResult] = field(default_factory=list)
    count: int = 0


@dataclass(frozen=True)
class ScenePage:
    """Paginated list of scenes."""

    results: list[SceneResult] = field(default_factory=list)
    count: int = 0


@runtime_checkable
class AbstractWorldBackend(Protocol):
    """Protocol every storage backend must satisfy.

    Implementations:
        WeltenhubBackend  — writes to Weltenhub via REST API (Premium mode)
        LocalWorldBackend — no-op stub; caller manages local DB (Basic mode)
    """

    # ------------------------------------------------------------------
    # World operations
    # ------------------------------------------------------------------

    def create_world(
        self,
        name: str,
        description: str = "",
        setting_era: str = "",
        **kwargs: object,
    ) -> WorldResult:
        """Create a world and return its canonical ID."""
        ...

    def get_world(self, world_id: str) -> WorldResult:
        """Fetch a world by its canonical ID."""
        ...

    def list_worlds(self, search: str = "", page: int = 1) -> WorldPage:
        """List worlds visible to the current tenant."""
        ...

    def update_world(
        self,
        world_id: str,
        **fields: object,
    ) -> WorldResult:
        """Partial-update a world."""
        ...

    # ------------------------------------------------------------------
    # Character operations
    # ------------------------------------------------------------------

    def create_character(
        self,
        world_id: str,
        name: str,
        personality: str = "",
        backstory: str = "",
        is_protagonist: bool = False,
        **kwargs: object,
    ) -> CharacterResult:
        """Create a character in the given world."""
        ...

    def get_character(self, character_id: str) -> CharacterResult:
        """Fetch a character by its canonical ID."""
        ...

    def list_characters(self, world_id: str, page: int = 1) -> CharacterPage:
        """List characters belonging to the given world."""
        ...

    # ------------------------------------------------------------------
    # User provisioning (idempotent)
    # ------------------------------------------------------------------

    def provision_user(self, username: str, email: str) -> str | None:
        """Provision a user/tenant in the backend and return an auth token.

        Returns None if not applicable (e.g. LocalWorldBackend).
        """
        ...
