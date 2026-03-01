"""
weltenfw.schema.story - Story Schemas

Verifiziert aus apps/stories/serializers.py.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from weltenfw.schema.base import BaseInput, BaseSchema


class ChapterSchema(BaseSchema):
    id: UUID
    story: UUID
    title: str
    order: int = 0
    summary: str | None = None
    notes: str | None = None
    created_at: datetime


class PlotThreadSchema(BaseSchema):
    id: UUID
    story: UUID
    title: str
    description: str | None = None
    thread_type: str | None = None
    status: str | None = None
    order: int = 0
    created_at: datetime


class TimelineEventSchema(BaseSchema):
    id: UUID
    story: UUID
    title: str
    description: str | None = None
    event_type: str | None = None
    story_date: str | None = None
    order: int = 0
    created_at: datetime


class StoryListSchema(BaseSchema):
    id: UUID
    title: str
    slug: str
    world: UUID
    genre: UUID | None = None
    genre_name: str | None = None
    status: str | None = None
    is_public: bool = False
    created_at: datetime


class StorySchema(BaseSchema):
    id: UUID
    tenant: UUID
    world: UUID
    title: str
    slug: str
    subtitle: str | None = None
    genre: UUID | None = None
    genre_name: str | None = None
    logline: str | None = None
    synopsis: str | None = None
    target_audience: str | None = None
    word_count_target: int | None = None
    word_count_actual: int | None = None
    status: str | None = None
    is_public: bool = False
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class StoryCreateInput(BaseInput):
    world: UUID
    title: str
    genre: UUID | None = None
    subtitle: str | None = None
    logline: str | None = None
    synopsis: str | None = None
    target_audience: str | None = None
    word_count_target: int | None = None
    status: str | None = None
    is_public: bool = False
    notes: str | None = None


class StoryUpdateInput(BaseInput):
    title: str | None = None
    genre: UUID | None = None
    subtitle: str | None = None
    logline: str | None = None
    synopsis: str | None = None
    target_audience: str | None = None
    word_count_target: int | None = None
    word_count_actual: int | None = None
    status: str | None = None
    is_public: bool | None = None
    notes: str | None = None
