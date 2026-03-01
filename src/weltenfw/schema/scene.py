"""
weltenfw.schema.scene - Scene Schemas

Verifiziert aus apps/scenes/serializers.py.
"""

from __future__ import annotations

from uuid import UUID
from datetime import datetime

from weltenfw.schema.base import BaseInput, BaseSchema


class SceneBeatSchema(BaseSchema):
    """Beat innerhalb einer Szene."""

    id: UUID
    scene: UUID
    beat_type: UUID | None = None
    description: str
    order: int = 0
    notes: str | None = None
    created_at: datetime


class SceneConnectionSchema(BaseSchema):
    """Verbindung zwischen zwei Szenen."""

    id: UUID
    from_scene: UUID
    from_scene_title: str
    to_scene: UUID
    to_scene_title: str
    connection_type: str | None = None
    description: str | None = None
    created_at: datetime


class SceneListSchema(BaseSchema):
    """Scene in Listenansicht."""

    id: UUID
    title: str
    story: UUID
    chapter: UUID | None = None
    location: UUID | None = None
    location_name: str | None = None
    order: int = 0
    status: UUID | None = None
    status_name: str | None = None
    is_auto_generated: bool = False
    created_at: datetime


class SceneSchema(BaseSchema):
    """Scene Detailansicht (alle Felder inkl. Beats)."""

    id: UUID
    tenant: UUID
    story: UUID
    chapter: UUID | None = None
    template: UUID | None = None
    title: str
    summary: str | None = None
    content: str | None = None
    from_location: UUID | None = None
    to_location: UUID | None = None
    location: UUID | None = None
    pov_character: UUID | None = None
    mood: UUID | None = None
    conflict_level: UUID | None = None
    story_datetime: datetime | None = None
    story_date_description: str | None = None
    goal: str | None = None
    disaster: str | None = None
    order: int = 0
    word_count_target: int | None = None
    word_count_actual: int | None = None
    status: UUID | None = None
    is_auto_generated: bool = False
    notes: str | None = None
    beats: list[SceneBeatSchema] = []
    created_at: datetime
    updated_at: datetime


class SceneCreateInput(BaseInput):
    """Input fuer POST /scenes/ (Pflichtfelder required)."""

    story: UUID
    title: str
    chapter: UUID | None = None
    template: UUID | None = None
    summary: str | None = None
    content: str | None = None
    from_location: UUID | None = None
    to_location: UUID | None = None
    location: UUID | None = None
    pov_character: UUID | None = None
    mood: UUID | None = None
    conflict_level: UUID | None = None
    story_datetime: datetime | None = None
    story_date_description: str | None = None
    goal: str | None = None
    disaster: str | None = None
    order: int = 0
    word_count_target: int | None = None
    status: UUID | None = None
    notes: str | None = None


class SceneUpdateInput(BaseInput):
    """Input fuer PATCH /scenes/{id}/ (alle Felder optional)."""

    title: str | None = None
    chapter: UUID | None = None
    template: UUID | None = None
    summary: str | None = None
    content: str | None = None
    from_location: UUID | None = None
    to_location: UUID | None = None
    location: UUID | None = None
    pov_character: UUID | None = None
    mood: UUID | None = None
    conflict_level: UUID | None = None
    story_datetime: datetime | None = None
    story_date_description: str | None = None
    goal: str | None = None
    disaster: str | None = None
    order: int | None = None
    word_count_target: int | None = None
    word_count_actual: int | None = None
    status: UUID | None = None
    notes: str | None = None
