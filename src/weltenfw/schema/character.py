"""
weltenfw.schema.character - Character Schemas

Verifiziert aus apps/characters/serializers.py.
"""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from weltenfw.schema.base import BaseInput, BaseSchema


class CharacterArcSchema(BaseSchema):
    id: UUID
    character: UUID
    arc_type: str
    title: str
    description: str | None = None
    start_state: str | None = None
    end_state: str | None = None
    catalyst: str | None = None
    created_at: datetime


class CharacterRelationshipSchema(BaseSchema):
    id: UUID
    from_character: UUID
    from_character_name: str
    to_character: UUID
    to_character_name: str
    relationship_type: str
    description: str | None = None
    strength: int = 5
    is_mutual: bool = False
    created_at: datetime


class CharacterListSchema(BaseSchema):
    id: UUID
    world: UUID
    name: str
    role: UUID | None = None
    role_name: str | None = None
    is_protagonist: bool = False
    is_active: bool = True
    created_at: datetime


class CharacterSchema(BaseSchema):
    id: UUID
    tenant: UUID
    world: UUID
    name: str
    role: UUID | None = None
    role_name: str | None = None
    title: str | None = None
    age: int | None = None
    birth_date: date | None = None
    nationality: str | None = None
    occupation: str | None = None
    personality: str | None = None
    backstory: str | None = None
    goals: str | None = None
    fears: str | None = None
    strengths: str | None = None
    weaknesses: str | None = None
    appearance: str | None = None
    is_protagonist: bool = False
    is_active: bool = True
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class CharacterCreateInput(BaseInput):
    world: UUID
    name: str
    role: UUID | None = None
    title: str | None = None
    age: int | None = None
    birth_date: date | None = None
    nationality: str | None = None
    occupation: str | None = None
    personality: str | None = None
    backstory: str | None = None
    goals: str | None = None
    fears: str | None = None
    strengths: str | None = None
    weaknesses: str | None = None
    appearance: str | None = None
    is_protagonist: bool = False
    is_active: bool = True
    notes: str | None = None


class CharacterUpdateInput(BaseInput):
    name: str | None = None
    role: UUID | None = None
    title: str | None = None
    age: int | None = None
    birth_date: date | None = None
    nationality: str | None = None
    occupation: str | None = None
    personality: str | None = None
    backstory: str | None = None
    goals: str | None = None
    fears: str | None = None
    strengths: str | None = None
    weaknesses: str | None = None
    appearance: str | None = None
    is_protagonist: bool | None = None
    is_active: bool | None = None
    notes: str | None = None
