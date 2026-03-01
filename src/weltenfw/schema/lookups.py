"""
weltenfw.schema.lookups - Read-only Lookup-Schemas

Alle Lookup-Tabellen aus WeltenHub (DB-driven, kein Enum).
Verifiziert aus apps/lookups/urls.py und apps/lookups/views.py.
"""

from __future__ import annotations

from uuid import UUID

from weltenfw.schema.base import BaseSchema


class LookupSchema(BaseSchema):
    """Basis fuer alle Lookup-Schemas (id + name)."""

    id: UUID
    name: str
    slug: str | None = None
    order: int | None = None


class GenreSchema(LookupSchema):
    """Genre (z.B. Fantasy, Sci-Fi, Thriller)."""

    description: str | None = None


class MoodSchema(LookupSchema):
    """Mood / Stimmung einer Szene."""

    description: str | None = None


class ConflictLevelSchema(LookupSchema):
    """Konfliktstufe (z.B. Low, Medium, High)."""

    description: str | None = None


class LocationTypeSchema(LookupSchema):
    """Ortstyp (z.B. City, Forest, Cave)."""

    description: str | None = None


class SceneTypeSchema(LookupSchema):
    """Szenentyp (z.B. Action, Dialogue, Discovery)."""

    description: str | None = None


class CharacterRoleSchema(LookupSchema):
    """Charakterrolle (z.B. Protagonist, Antagonist, Mentor)."""

    description: str | None = None


class TransportTypeSchema(LookupSchema):
    """Transporttyp fuer Szenenwechsel."""

    description: str | None = None


class SceneStatusSchema(LookupSchema):
    """Szenenstatus (z.B. Draft, In Progress, Final)."""

    description: str | None = None


class BeatTypeSchema(LookupSchema):
    """Beat-Typ innerhalb einer Szene."""

    description: str | None = None
