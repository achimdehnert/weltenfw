"""
weltenfw.schema.world - World + WorldRule Schemas

Verifiziert aus apps/worlds/serializers.py.
"""

from __future__ import annotations

from uuid import UUID
from datetime import datetime

from weltenfw.schema.base import BaseInput, BaseSchema


class WorldRuleSchema(BaseSchema):
    """Weltenbau-Regel (read-only)."""

    id: UUID
    world: UUID
    rule_type: str
    title: str
    description: str
    is_absolute: bool = False
    order: int = 0
    created_at: datetime


class WorldListSchema(BaseSchema):
    """World in Listenansicht (reduzierte Felder)."""

    id: UUID
    name: str
    slug: str
    tenant: UUID
    genre: UUID | None = None
    genre_name: str | None = None
    is_public: bool = False
    created_at: datetime


class WorldSchema(BaseSchema):
    """World Detailansicht (alle Felder)."""

    id: UUID
    tenant: UUID
    name: str
    slug: str
    subtitle: str | None = None
    genre: UUID | None = None
    genre_name: str | None = None
    description: str | None = None
    history: str | None = None
    geography: str | None = None
    climate: str | None = None
    magic_system: str | None = None
    technology_level: str | None = None
    setting_era: str | None = None
    is_public: bool = False
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class WorldCreateInput(BaseInput):
    """Input fuer POST /worlds/ (alle Pflichtfelder required)."""

    name: str
    genre: UUID | None = None
    subtitle: str | None = None
    description: str | None = None
    history: str | None = None
    geography: str | None = None
    climate: str | None = None
    magic_system: str | None = None
    technology_level: str | None = None
    setting_era: str | None = None
    is_public: bool = False
    notes: str | None = None


class WorldUpdateInput(BaseInput):
    """Input fuer PATCH /worlds/{id}/ (alle Felder optional)."""

    name: str | None = None
    genre: UUID | None = None
    subtitle: str | None = None
    description: str | None = None
    history: str | None = None
    geography: str | None = None
    climate: str | None = None
    magic_system: str | None = None
    technology_level: str | None = None
    setting_era: str | None = None
    is_public: bool | None = None
    notes: str | None = None
