"""
weltenfw.schema.item - Item Schemas

Gegenstaende, die ueber Baende tragen: eine Akte, ein Schluessel, ein Messgeraet.

Der Verbleib ist zweigeteilt und darf leer sein — eine Figur traegt den
Gegenstand ODER er liegt an einem Ort ODER keines von beidem, weil sein
Verbleib Teil der Handlung ist. Beide Felder sind deshalb optional, und keines
ersetzt das andere.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from weltenfw.schema.base import BaseInput, BaseSchema


class ItemListSchema(BaseSchema):
    id: UUID
    world: UUID
    name: str
    item_type: int | UUID | None = None
    item_type_name: str | None = None
    held_by: UUID | None = None
    held_by_name: str | None = None
    kept_at: UUID | None = None
    kept_at_name: str | None = None
    created_at: datetime


class ItemSchema(BaseSchema):
    id: UUID
    tenant: UUID | None = None
    world: UUID
    name: str
    slug: str | None = None
    item_type: int | UUID | None = None
    item_type_name: str | None = None
    description: str | None = None
    appearance: str | None = None
    significance: str | None = None
    held_by: UUID | None = None
    kept_at: UUID | None = None
    whereabouts: str | None = None
    is_unique: bool = True
    is_public: bool = False
    order: int = 0
    created_at: datetime
    updated_at: datetime | None = None


class ItemCreateInput(BaseInput):
    world: UUID
    name: str
    item_type: int | UUID | None = None
    description: str | None = None
    appearance: str | None = None
    significance: str | None = None
    held_by: UUID | None = None
    kept_at: UUID | None = None
    is_unique: bool = True
    is_public: bool = False
    order: int = 0


class ItemUpdateInput(BaseInput):
    name: str | None = None
    item_type: int | UUID | None = None
    description: str | None = None
    appearance: str | None = None
    significance: str | None = None
    held_by: UUID | None = None
    kept_at: UUID | None = None
    is_unique: bool | None = None
    is_public: bool | None = None
    order: int | None = None
