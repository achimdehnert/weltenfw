"""
weltenfw.pagination - Pagination-Unterstuetzung

Macht DRF-Pagination explizit sichtbar. Kein stilles Abschneiden nach Seite 1.
iter_all() und aiter_all() paginieren automatisch mit Schutz vor Endlosschleifen.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, Callable, Generator
from typing import Generic, TypeVar

from pydantic import ConfigDict

from weltenfw.exceptions import PaginationError
from weltenfw.schema.base import BaseSchema

T = TypeVar("T")


class PageResult(BaseSchema, Generic[T]):
    """Paginiertes API-Response (DRF-Standard-Format).

    Macht Pagination explizit sichtbar.
    Fuer automatische Iteration: iter_all() oder aiter_all() nutzen.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    count: int
    next: str | None = None
    previous: str | None = None
    results: list[T]

    @property
    def has_next(self) -> bool:
        return self.next is not None

    @property
    def has_previous(self) -> bool:
        return self.previous is not None


def iter_all(
    fetch_page: Callable[[int], PageResult[T]],
    max_pages: int | None = 1000,
) -> Generator[T, None, None]:
    """Iteriert automatisch ueber alle Seiten eines paginierten Endpunkts.

    Args:
        fetch_page: Callable das eine Seitennummer entgegennimmt.
        max_pages:  Maximale Seiten als Schutz vor Endlosschleifen.
                    None = unbegrenzt.

    Raises:
        PaginationError: Wenn max_pages ueberschritten wird.

    Yields:
        Einzelne Ergebnis-Objekte ueber alle Seiten.
    """
    page = 1
    fetched = 0
    while True:
        result = fetch_page(page)
        yield from result.results
        fetched += 1
        if not result.has_next:
            break
        if max_pages is not None and fetched >= max_pages:
            raise PaginationError(max_pages)
        page += 1


async def aiter_all(
    fetch_page: Callable[[int], object],
    max_pages: int | None = 1000,
) -> AsyncGenerator[T, None]:
    """Async-Variante von iter_all()."""
    page = 1
    fetched = 0
    while True:
        result = await fetch_page(page)  # type: ignore[misc]
        for item in result.results:
            yield item
        fetched += 1
        if not result.has_next:
            break
        if max_pages is not None and fetched >= max_pages:
            raise PaginationError(max_pages)
        page += 1
