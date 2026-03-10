"""
weltenfw.backends.weltenhub — WeltenhubBackend (ADR-117)

Concrete AbstractWorldBackend that writes directly into a running
Weltenhub instance via the existing WeltenClient.

1 WeltenhubBackend = 1 token = 1 tenant (WeltenClient invariant).
Instantiate per-user after calling provision_user().

Usage:
    from weltenfw.backends.weltenhub import WeltenhubBackend

    backend = WeltenhubBackend(base_url=settings.WELTENHUB_API_URL,
                               token=user_weltenhub_token)
    result = backend.create_world(name="Mittelerde", description="...")
    # result.id  → Weltenhub UUID
    # result.backend → "weltenhub"
"""

from __future__ import annotations

import logging
from uuid import UUID

from weltenfw.backends.base import (
    CharacterPage,
    CharacterResult,
    LocationPage,
    LocationResult,
    ScenePage,
    SceneResult,
    WorldPage,
    WorldResult,
)
from weltenfw.client import WeltenClient
from weltenfw.exceptions import WeltenError
from weltenfw.schema.character import CharacterCreateInput
from weltenfw.schema.tenant import ProvisionRequest
from weltenfw.schema.world import WorldCreateInput, WorldUpdateInput

logger = logging.getLogger(__name__)

_BACKEND = "weltenhub"


class WeltenhubBackend:
    """Storage backend that persists worlds and characters in Weltenhub.

    Implements AbstractWorldBackend via structural subtyping (Protocol).

    Args:
        base_url: Weltenhub API base URL (e.g. 'https://weltenforger.com/api/v1').
        token:    DRF auth token for this tenant.
        timeout:  HTTP timeout in seconds (default: 30).
    """

    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 30.0,
    ) -> None:
        self._base_url = base_url
        self._token = token
        self._timeout = timeout

    def _client(self) -> WeltenClient:
        return WeltenClient(
            base_url=self._base_url,
            token=self._token,
            timeout=self._timeout,
        )

    # ------------------------------------------------------------------
    # User provisioning
    # ------------------------------------------------------------------

    @classmethod
    def provision_user(
        cls,
        username: str,
        email: str,
        *,
        base_url: str,
        service_token: str,
        timeout: float = 30.0,
    ) -> str | None:
        """Provision a Weltenhub user/tenant and return their auth token.

        Idempotent — safe to call on every project creation or login.
        Returns the per-user token, or None on failure.

        This is a classmethod so it can be called before a per-user
        WeltenhubBackend is constructed.
        """
        try:
            client = WeltenClient(
                base_url=base_url,
                token=service_token,
                timeout=timeout,
            )
            with client:
                resp = client.tenants.provision(
                    ProvisionRequest(username=username, email=email)
                )
            logger.info(
                "weltenhub_user_provisioned",
                extra={"username": username, "created": resp.created},
            )
            return resp.token
        except WeltenError as exc:
            logger.warning(
                "weltenhub_provision_failed",
                extra={"username": username, "error": str(exc)},
            )
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
        try:
            with self._client() as client:
                existing = client.worlds.list(search=name)
                for w in existing.results:
                    if w.name.lower() == name.lower():
                        logger.info(
                            "weltenhub_world_found",
                            extra={"world_id": str(w.id), "name": name},
                        )
                        return WorldResult(
                            id=str(w.id),
                            name=w.name,
                            description=w.description or "",
                            setting_era=w.setting_era or "",
                            genre_name=w.genre_name or "",
                            backend=_BACKEND,
                        )
                world = client.worlds.create(
                    WorldCreateInput(
                        name=name,
                        description=description or None,
                        setting_era=setting_era or None,
                    )
                )
            logger.info(
                "weltenhub_world_created",
                extra={"world_id": str(world.id), "name": name},
            )
            return WorldResult(
                id=str(world.id),
                name=world.name,
                description=world.description or "",
                setting_era=world.setting_era or "",
                genre_name=world.genre_name or "",
                backend=_BACKEND,
            )
        except WeltenError as exc:
            logger.warning(
                "weltenhub_world_create_failed",
                extra={"name": name, "error": str(exc)},
            )
            return WorldResult(id="", name=name, backend=_BACKEND, error=str(exc))

    def get_world(self, world_id: str) -> WorldResult:
        try:
            with self._client() as client:
                world = client.worlds.get(UUID(world_id))
            return WorldResult(
                id=str(world.id),
                name=world.name,
                description=world.description or "",
                setting_era=world.setting_era or "",
                genre_name=world.genre_name or "",
                backend=_BACKEND,
            )
        except WeltenError as exc:
            return WorldResult(
                id=world_id, name="", backend=_BACKEND, error=str(exc)
            )

    def list_worlds(self, search: str = "", page: int = 1) -> WorldPage:
        try:
            with self._client() as client:
                page_result = client.worlds.list(page=page, search=search)
            return WorldPage(
                results=[
                    WorldResult(
                        id=str(w.id),
                        name=w.name,
                        genre_name=w.genre_name or "",
                        backend=_BACKEND,
                    )
                    for w in page_result.results
                ],
                count=page_result.count,
            )
        except WeltenError as exc:
            logger.warning("weltenhub_list_worlds_failed", extra={"error": str(exc)})
            return WorldPage()

    def update_world(self, world_id: str, **fields: object) -> WorldResult:
        try:
            with self._client() as client:
                world = client.worlds.partial_update(
                    UUID(world_id),
                    WorldUpdateInput(**{k: v for k, v in fields.items() if v is not None}),
                )
            return WorldResult(
                id=str(world.id),
                name=world.name,
                description=world.description or "",
                backend=_BACKEND,
            )
        except WeltenError as exc:
            return WorldResult(
                id=world_id, name="", backend=_BACKEND, error=str(exc)
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
        try:
            with self._client() as client:
                existing = client.characters.list(world=world_id, search=name)
                for c in existing.results:
                    if c.name.lower() == name.lower():
                        logger.info(
                            "weltenhub_character_found",
                            extra={"char_id": str(c.id), "name": name},
                        )
                        return CharacterResult(
                            id=str(c.id),
                            name=c.name,
                            world_id=world_id,
                            role_name=c.role_name or "",
                            backend=_BACKEND,
                        )
                char = client.characters.create(
                    CharacterCreateInput(
                        world=UUID(world_id),
                        name=name,
                        personality=personality or None,
                        backstory=backstory or None,
                        is_protagonist=is_protagonist,
                    )
                )
            logger.info(
                "weltenhub_character_created",
                extra={"char_id": str(char.id), "name": name},
            )
            return CharacterResult(
                id=str(char.id),
                name=char.name,
                world_id=world_id,
                personality=char.personality or "",
                backend=_BACKEND,
            )
        except WeltenError as exc:
            logger.warning(
                "weltenhub_character_create_failed",
                extra={"name": name, "error": str(exc)},
            )
            return CharacterResult(
                id="", name=name, world_id=world_id, backend=_BACKEND, error=str(exc)
            )

    def get_character(self, character_id: str) -> CharacterResult:
        try:
            with self._client() as client:
                char = client.characters.get(UUID(character_id))
            return CharacterResult(
                id=str(char.id),
                name=char.name,
                world_id=str(char.world),
                personality=char.personality or "",
                backend=_BACKEND,
            )
        except WeltenError as exc:
            return CharacterResult(
                id=character_id, name="", backend=_BACKEND, error=str(exc)
            )

    def list_characters(self, world_id: str, page: int = 1) -> CharacterPage:
        try:
            with self._client() as client:
                page_result = client.characters.list(page=page, world=world_id)
            return CharacterPage(
                results=[
                    CharacterResult(
                        id=str(c.id),
                        name=c.name,
                        world_id=world_id,
                        role_name=c.role_name or "",
                        backend=_BACKEND,
                    )
                    for c in page_result.results
                ],
                count=page_result.count,
            )
        except WeltenError as exc:
            logger.warning(
                "weltenhub_list_characters_failed",
                extra={"world_id": world_id, "error": str(exc)},
            )
            return CharacterPage()

    # ------------------------------------------------------------------
    # Location operations
    # ------------------------------------------------------------------

    def list_locations(
        self, world_id: str, page: int = 1, page_size: int = 100
    ) -> LocationPage:
        try:
            with self._client() as client:
                page_result = client.locations.list(
                    page=page, world=world_id, page_size=page_size
                )
            return LocationPage(
                results=[
                    LocationResult(
                        id=str(loc.id),
                        name=loc.name,
                        world_id=world_id,
                        parent_id=str(loc.parent) if loc.parent else None,
                        location_type_name=loc.location_type_name or "",
                        full_path=loc.full_path or "",
                        backend=_BACKEND,
                    )
                    for loc in page_result.results
                ],
                count=page_result.count,
            )
        except WeltenError as exc:
            logger.warning(
                "weltenhub_list_locations_failed",
                extra={"world_id": world_id, "error": str(exc)},
            )
            return LocationPage()

    # ------------------------------------------------------------------
    # Scene operations
    # ------------------------------------------------------------------

    def list_scenes(
        self, story_id: str, page: int = 1, page_size: int = 100
    ) -> ScenePage:
        try:
            with self._client() as client:
                page_result = client.scenes.list(
                    page=page, story=story_id, page_size=page_size
                )
            return ScenePage(
                results=[
                    SceneResult(
                        id=str(s.id),
                        title=s.title,
                        story_id=story_id,
                        location_name=s.location_name or "",
                        order=s.order,
                        backend=_BACKEND,
                    )
                    for s in page_result.results
                ],
                count=page_result.count,
            )
        except WeltenError as exc:
            logger.warning(
                "weltenhub_list_scenes_failed",
                extra={"story_id": story_id, "error": str(exc)},
            )
            return ScenePage()
