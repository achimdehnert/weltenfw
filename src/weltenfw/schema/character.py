"""
weltenfw.schema.character - Character Schemas

Verifiziert aus apps/characters/serializers.py.
"""

from __future__ import annotations

from uuid import UUID
from datetime import date, datetime

from weltenfw.schema.base import BaseInput, BaseSchema


class CharacterListSchema(BaseSchema):
    """Character in Listenansicht."""

    id: UUID
    name: str
    slug: str
    world: UUID
    role: UUID | None = None
    role_name: str | None = None
    age: int | None = None
    gender: str | None = None
    is_protagonist: bool = False
    created_at: datetime


class CharacterSchema(BaseSchema):
    """Character Detailansicht (alle Felder)."""

    id: UUID
    tenant: UUID
    world: UUID
    name: str
    slug: str
    title: str | None = None
    role: UUID | None = None
    role_name: str | None = None
    nickname: str | None = None
    age: int | None = None
    gender: str | None = None
    description: str | None = None
    personality: str | None = None
    backstory: str | None = None
    motivation: str | None = None
    goals: str | None = None
    flaws: str | None = None
    strengths: str | None = None
    voice: str | None = None
    home_location: UUID | None = None
    current_location: UUID | None = None
    portrait: str | None = None
    is_protagonist: bool = False
    is_public: bool = False
    tags: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class CharacterArcSchema(BaseSchema):
    """Character Arc (Charakterentwicklung in einer Story)."""

    id: UUID
    character: UUID
    story: UUID
    arc_type: str | None = None
    starting_state: str | None = None
    ending_state: str | None = None
    key_moments: str | None = None
    internal_conflict: str | None = None
    external_conflict: str | None = None
    lesson_learned: str | None = None
    notes: str | None = None
    created_at: datetime


class CharacterRelationshipSchema(BaseSchema):
    """Beziehung zwischen zwei Charakteren."""

    id: UUID
    character_a: UUID
    character_a_name: str
    character_b: UUID
    character_b_name: str
    relationship_type: str | None = None
    description: str | None = None
    strength: int | None = None
    is_mutual: bool = False
    started_at: date | None = None
    notes: str | None = None
    created_at: datetime


class CharacterCreateInput(BaseInput):
    """Input fuer POST /characters/ (Pflichtfelder required)."""

    world: UUID
    name: str
    role: UUID | None = None
    title: str | None = None
    nickname: str | None = None
    age: int | None = None
    gender: str | None = None
    description: str | None = None
    personality: str | None = None
    backstory: str | None = None
    motivation: str | None = None
    goals: str | None = None
    flaws: str | None = None
    strengths: str | None = None
    voice: str | None = None
    home_location: UUID | None = None
    current_location: UUID | None = None
    is_protagonist: bool = False
    is_public: bool = False
    tags: str | None = None
    notes: str | None = None


class CharacterUpdateInput(BaseInput):
    """Input fuer PATCH /characters/{id}/ (alle Felder optional)."""

    name: str | None = None
    role: UUID | None = None
    title: str | None = None
    nickname: str | None = None
    age: int | None = None
    gender: str | None = None
    description: str | None = None
    personality: str | None = None
    backstory: str | None = None
    motivation: str | None = None
    goals: str | None = None
    flaws: str | None = None
    strengths: str | None = None
    voice: str | None = None
    home_location: UUID | None = None
    current_location: UUID | None = None
    is_protagonist: bool | None = None
    is_public: bool | None = None
    tags: str | None = None
    notes: str | None = None
