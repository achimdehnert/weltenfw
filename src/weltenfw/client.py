"""
weltenfw.client - WeltenClient (Haupt-Einstiegspunkt)

Invariante: 1 WeltenClient = 1 Token = 1 Tenant.
Multi-Tenant-Konsumenten instanziieren mehrere Clients (einen pro Tenant-Token).

Sync + Async aus einem Client:
    client.worlds.list()          # sync
    await client.worlds.alist()   # async
"""

from __future__ import annotations

from weltenfw._http import AsyncHttpTransport, HttpTransport
from weltenfw.cache import CacheBackend, NullCache
from weltenfw.resources.characters import CharacterResource
from weltenfw.resources.locations import LocationResource
from weltenfw.resources.lookups import LookupResource
from weltenfw.resources.scenes import SceneResource
from weltenfw.resources.stories import StoryResource
from weltenfw.resources.tenants import TenantResource
from weltenfw.resources.worlds import WorldResource
from weltenfw.schema.character import CharacterListSchema, CharacterSchema
from weltenfw.schema.location import LocationListSchema, LocationSchema
from weltenfw.schema.scene import SceneListSchema, SceneSchema
from weltenfw.schema.story import StoryListSchema, StorySchema
from weltenfw.schema.tenant import TenantSchema
from weltenfw.schema.world import WorldListSchema, WorldSchema


class WeltenClient:
    """WeltenHub API Client.

    Invariante: 1 Client = 1 Token = 1 Tenant.
    Kein global geteilter Singleton fuer Multi-Tenant-Konsumenten.

    Args:
        base_url:     WeltenHub-URL (z.B. 'https://weltenforger.com/api/v1').
        token:        DRF-Auth-Token.
        lookup_cache: Cache-Backend fuer Lookups (default: NullCache).
        lookup_ttl:   Lookup-Cache-TTL in Sekunden (default: 3600).
        timeout:      HTTP-Timeout in Sekunden (default: 30.0).
    """

    def __init__(
        self,
        base_url: str,
        token: str,
        lookup_cache: CacheBackend | None = None,
        lookup_ttl: int = 3600,
        timeout: float = 30.0,
    ) -> None:
        self._http = HttpTransport(base_url=base_url, token=token, timeout=timeout)
        self._async_http = AsyncHttpTransport(base_url=base_url, token=token, timeout=timeout)

        self.worlds = WorldResource(
            http=self._http,
            async_http=self._async_http,
            base_path="/worlds",
            schema_cls=WorldSchema,
            list_schema_cls=WorldListSchema,
        )
        self.characters = CharacterResource(
            http=self._http,
            async_http=self._async_http,
            base_path="/characters",
            schema_cls=CharacterSchema,
            list_schema_cls=CharacterListSchema,
        )
        self.scenes = SceneResource(
            http=self._http,
            async_http=self._async_http,
            base_path="/scenes",
            schema_cls=SceneSchema,
            list_schema_cls=SceneListSchema,
        )
        self.stories = StoryResource(
            http=self._http,
            async_http=self._async_http,
            base_path="/stories",
            schema_cls=StorySchema,
            list_schema_cls=StoryListSchema,
        )
        self.locations = LocationResource(
            http=self._http,
            async_http=self._async_http,
            base_path="/locations",
            schema_cls=LocationSchema,
            list_schema_cls=LocationListSchema,
        )
        self.tenants = TenantResource(
            http=self._http,
            async_http=self._async_http,
            base_path="/tenants/tenants",
            schema_cls=TenantSchema,
        )
        self.lookups = LookupResource(
            http=self._http,
            cache=lookup_cache or NullCache(),
            ttl=lookup_ttl,
        )

    def close(self) -> None:
        """Schliesst httpx-Sessions. In sync-Kontexten nach Nutzung aufrufen."""
        self._http.close()

    async def aclose(self) -> None:
        """Schliesst async httpx-Sessions."""
        await self._async_http.aclose()

    def __enter__(self) -> WeltenClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    async def __aenter__(self) -> WeltenClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()
