"""
weltenfw.schema.location - Location Schemas

Location ist hierarchisch: parent FK auf sich selbst.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from weltenfw.schema.base import BaseInput, BaseSchema


class LocationListSchema(BaseSchema):
    id: UUID
    world: UUID
    name: str
    parent: UUID | None = None
    location_type: UUID | None = None
    location_type_name: str | None = None
    full_path: str | None = None
    is_public: bool = False
    created_at: datetime


class LocationSchema(BaseSchema):
    id: UUID
    tenant: UUID
    world: UUID
    name: str
    parent: UUID | None = None
    location_type: UUID | None = None
    location_type_name: str | None = None
    description: str | None = None
    atmosphere: str | None = None
    significance: str | None = None
    coordinates: str | None = None
    real_world_reference: str | None = None
    full_path: str | None = None
    is_public: bool = False
    order: int = 0
    created_at: datetime
    updated_at: datetime


class LocationCreateInput(BaseInput):
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
