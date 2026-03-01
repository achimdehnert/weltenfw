"""
weltenfw.schema.location - Location Schemas

Verifiziert aus apps/locations/serializers.py.
Location ist hierarchisch: parent FK auf sich selbst.
"""

from __future__ import annotations

from uuid import UUID
from datetime import datetime

from weltenfw.schema.base import BaseInput, BaseSchema


class LocationListSchema(BaseSchema):
    """Location in Listenansicht."""

    id: UUID
    name: str
    slug: str
    world: UUID
    parent: UUID | None = None
    parent_name: str | None = None
    location_type: UUID | None = None
    location_type_name: str | None = None
    created_at: datetime


class LocationSchema(BaseSchema):
    """Location Detailansicht (alle Felder)."""

    id: UUID
    tenant: UUID
    world: UUID
    parent: UUID | None = None
    name: str
    slug: str
    location_type: UUID | None = None
    location_type_name: str | None = None
    description: str | None = None
    atmosphere: str | None = None
    significance: str | None = None
    coordinates: str | None = None
    real_world_reference: str | None = None
    image: str | None = None
    is_public: bool = False
    order: int = 0
    full_path: str | None = None
    depth: int = 0
    research_data: dict | None = None
    research_status: UUID | None = None
    research_status_code: str = "none"
    researched_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class LocationCreateInput(BaseInput):
    """Input fuer POST /locations/ (Pflichtfelder required)."""

    world: UUID
    name: str
    parent: UUID | None = None
    location_type: UUID | None = None
    description: str | None = None
    atmosphere: str | None = None
    significance: str | None = None
    coordinates: str | None = None
    real_world_reference: str | None = None
    is_public: bool = False
    order: int = 0


class LocationUpdateInput(BaseInput):
    """Input fuer PATCH /locations/{id}/ (alle Felder optional)."""

    name: str | None = None
    parent: UUID | None = None
    location_type: UUID | None = None
    description: str | None = None
    atmosphere: str | None = None
    significance: str | None = None
    coordinates: str | None = None
    real_world_reference: str | None = None
    is_public: bool | None = None
    order: int | None = None
