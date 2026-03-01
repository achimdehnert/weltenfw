"""
weltenfw.resources.base - Basis-Resource mit CRUD-Mixin

Alle Domain-Resources erben von BaseResource.
HTTP-Verben sind explizit:
  create()         -> POST   (alle Pflichtfelder required)
  update()         -> PUT    (alle Felder, ersetzt vollstaendig)
  partial_update() -> PATCH  (nur geaenderte Felder)
  delete()         -> DELETE

Wichtig: model_dump(mode='json') stellt sicher dass UUID/datetime-Objekte
zu JSON-serialisierbaren Typen (str) konvertiert werden, bevor sie an
httpx json= weitergegeben werden.
"""

from __future__ import annotations

from collections.abc import Generator
from typing import Any, Generic, TypeVar

from weltenfw._http import AsyncHttpTransport, HttpTransport
from weltenfw.pagination import PageResult, iter_all
from weltenfw.schema.base import BaseInput, BaseSchema

S = TypeVar("S", bound=BaseSchema)
InputT = TypeVar("InputT", bound=BaseInput)


class BaseResource(Generic[S]):
    """Basis-Resource. Kapselt CRUD fuer eine WeltenHub-Domaene.

    Args:
        http:        Synchroner Transport.
        async_http:  Asynchroner Transport.
        base_path:   API-Pfad (z.B. '/worlds').
        schema_cls:  Pydantic-Schema fuer Einzelobjekte.
        list_schema: Pydantic-Schema fuer Listenelemente (optional, default=schema_cls).
    """

    def __init__(
        self,
        http: HttpTransport,
        async_http: AsyncHttpTransport,
        base_path: str,
        schema_cls: type[S],
        list_schema_cls: type[S] | None = None,
    ) -> None:
        self._http = http
        self._async_http = async_http
        self._base_path = base_path.rstrip("/")
        self._schema_cls = schema_cls
        self._list_schema_cls = list_schema_cls or schema_cls

    def _detail_path(self, pk: Any) -> str:
        return f"{self._base_path}/{pk}"

    # --- Sync ---

    def list(self, page: int = 1, **filters: Any) -> PageResult[S]:
        """GET /{base}/ -> PageResult[S]"""
        params = {"page": page, **filters}
        data = self._http.get(self._base_path, params=params)
        return PageResult[self._list_schema_cls].model_validate(data)  # type: ignore[valid-type]

    def get(self, pk: Any) -> S:
        """GET /{base}/{pk}/ -> S"""
        data = self._http.get(self._detail_path(pk))
        return self._schema_cls.model_validate(data)

    def create(self, payload: BaseInput) -> S:
        """POST /{base}/ -> S"""
        data = self._http.post(
            self._base_path,
            json=payload.model_dump(mode="json", exclude_none=True),
        )
        return self._schema_cls.model_validate(data)

    def update(self, pk: Any, payload: BaseInput) -> S:
        """PUT /{base}/{pk}/ -> S (ersetzt vollstaendig)"""
        data = self._http.put(
            self._detail_path(pk),
            json=payload.model_dump(mode="json"),
        )
        return self._schema_cls.model_validate(data)

    def partial_update(self, pk: Any, payload: BaseInput) -> S:
        """PATCH /{base}/{pk}/ -> S (nur geaenderte Felder)"""
        data = self._http.patch(
            self._detail_path(pk),
            json=payload.model_dump(mode="json", exclude_none=True),
        )
        return self._schema_cls.model_validate(data)

    def delete(self, pk: Any) -> None:
        """DELETE /{base}/{pk}/"""
        self._http.delete(self._detail_path(pk))

    def iter_all(self, max_pages: int | None = 1000, **filters: Any) -> Generator[S, None, None]:
        """Iteriert automatisch ueber alle Seiten. Schutz vor Endlosschleifen via max_pages."""
        return iter_all(
            fetch_page=lambda page: self.list(page=page, **filters),
            max_pages=max_pages,
        )

    # --- Async ---

    async def alist(self, page: int = 1, **filters: Any) -> PageResult[S]:
        """GET /{base}/ -> PageResult[S] (async)"""
        params = {"page": page, **filters}
        data = await self._async_http.get(self._base_path, params=params)
        return PageResult[self._list_schema_cls].model_validate(data)  # type: ignore[valid-type]

    async def aget(self, pk: Any) -> S:
        """GET /{base}/{pk}/ -> S (async)"""
        data = await self._async_http.get(self._detail_path(pk))
        return self._schema_cls.model_validate(data)

    async def acreate(self, payload: BaseInput) -> S:
        """POST /{base}/ -> S (async)"""
        data = await self._async_http.post(
            self._base_path,
            json=payload.model_dump(mode="json", exclude_none=True),
        )
        return self._schema_cls.model_validate(data)

    async def aupdate(self, pk: Any, payload: BaseInput) -> S:
        """PUT /{base}/{pk}/ -> S (async)"""
        data = await self._async_http.put(
            self._detail_path(pk),
            json=payload.model_dump(mode="json"),
        )
        return self._schema_cls.model_validate(data)

    async def apartial_update(self, pk: Any, payload: BaseInput) -> S:
        """PATCH /{base}/{pk}/ -> S (async)"""
        data = await self._async_http.patch(
            self._detail_path(pk),
            json=payload.model_dump(mode="json", exclude_none=True),
        )
        return self._schema_cls.model_validate(data)

    async def adelete(self, pk: Any) -> None:
        """DELETE /{base}/{pk}/ (async)"""
        await self._async_http.delete(self._detail_path(pk))
