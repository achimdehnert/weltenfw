"""
weltenfw.backends.local — LocalWorldBackend (ADR-117)

No-op backend for apps that do NOT have a Weltenhub subscription.
All methods return stub results with backend="local" and no error.

The caller (bfagent / travel-beat) is responsible for persisting the
entity in their own local database. LocalWorldBackend does not write
anything — it merely signals "no Weltenhub integration active".

Usage:
    from weltenfw.backends.local import LocalWorldBackend

    backend = LocalWorldBackend()
    result = backend.create_world(name="Mittelerde")
    # result.id     → "" (caller must assign their own PK)
    # result.backend → "local"
    # result.ok      → True (not an error — just local mode)
"""

from __future__ import annotations

from weltenfw.backends.base import (
    CharacterPage,
    CharacterResult,
    WorldPage,
    WorldResult,
)

_BACKEND = "local"


class LocalWorldBackend:
    """Storage backend for apps without a Weltenhub subscription.

    All operations are no-ops that return empty-but-ok results.
    The caller manages persistence in the local Django database.

    Implements AbstractWorldBackend via structural subtyping (Protocol).
    """

    # ------------------------------------------------------------------
    # User provisioning
    # ------------------------------------------------------------------

    def provision_user(self, username: str, email: str) -> str | None:
        """No provisioning needed in local mode."""
        return None

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
        return WorldResult(
            id="",
            name=name,
            description=description,
            setting_era=setting_era,
            backend=_BACKEND,
        )

    def get_world(self, world_id: str) -> WorldResult:
        return WorldResult(
            id=world_id,
            name="",
            backend=_BACKEND,
        )

    def list_worlds(self, search: str = "", page: int = 1) -> WorldPage:
        return WorldPage()

    def update_world(self, world_id: str, **fields: object) -> WorldResult:
        return WorldResult(
            id=world_id,
            name=str(fields.get("name", "")),
            backend=_BACKEND,
        )

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
        return CharacterResult(
            id="",
            name=name,
            world_id=world_id,
            personality=personality,
            backend=_BACKEND,
        )

    def get_character(self, character_id: str) -> CharacterResult:
        return CharacterResult(
            id=character_id,
            name="",
            backend=_BACKEND,
        )

    def list_characters(self, world_id: str, page: int = 1) -> CharacterPage:
        return CharacterPage()
