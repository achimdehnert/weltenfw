"""
Tests fuer weltenfw.schema — alle Domain-Schemas
"""

from __future__ import annotations

import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone

from weltenfw.schema.world import (
    WorldSchema,
    WorldListSchema,
    WorldCreateInput,
    WorldUpdateInput,
)
from weltenfw.schema.character import (
    CharacterSchema,
    CharacterCreateInput,
    CharacterUpdateInput,
)
from weltenfw.schema.scene import (
    SceneSchema,
    SceneCreateInput,
)
from weltenfw.schema.story import (
    StorySchema,
    StoryCreateInput,
)
from weltenfw.schema.location import (
    LocationSchema,
    LocationCreateInput,
)
from weltenfw.schema.tenant import (
    ProvisionRequest,
    ProvisionResponse,
    TenantSchema,
)
from weltenfw.schema.lookups import GenreSchema, MoodSchema, LookupSchema


NOW = datetime(2026, 3, 1, 12, 0, 0, tzinfo=timezone.utc)
WORLD_ID = uuid4()
TENANT_ID = uuid4()


# --- World ---

def test_should_parse_world_schema() -> None:
    data = {
        "id": str(WORLD_ID),
        "tenant": str(TENANT_ID),
        "name": "Arandur",
        "slug": "arandur",
        "is_public": False,
        "created_at": NOW.isoformat(),
        "updated_at": NOW.isoformat(),
    }
    world = WorldSchema.model_validate(data)
    assert world.name == "Arandur"
    assert world.tenant == TENANT_ID


def test_should_world_create_input_be_mutable() -> None:
    inp = WorldCreateInput(name="Test")
    inp.name = "Changed"
    assert inp.name == "Changed"


def test_should_world_update_input_all_optional() -> None:
    inp = WorldUpdateInput()
    assert inp.name is None
    assert inp.genre is None


def test_should_world_schema_be_frozen() -> None:
    data = {
        "id": str(uuid4()),
        "tenant": str(TENANT_ID),
        "name": "Frozen",
        "slug": "frozen",
        "created_at": NOW.isoformat(),
        "updated_at": NOW.isoformat(),
    }
    world = WorldSchema.model_validate(data)
    with pytest.raises(Exception):
        world.name = "mutated"  # type: ignore[misc]


# --- Character ---

def test_should_parse_character_create_input() -> None:
    inp = CharacterCreateInput(world=WORLD_ID, name="Lyra")
    assert inp.name == "Lyra"
    assert inp.world == WORLD_ID
    assert inp.is_protagonist is False


def test_should_character_update_input_all_optional() -> None:
    inp = CharacterUpdateInput()
    assert inp.name is None


# --- Scene ---

def test_should_parse_scene_create_input() -> None:
    story_id = uuid4()
    inp = SceneCreateInput(story=story_id, title="Der Aufbruch")
    assert inp.title == "Der Aufbruch"
    assert inp.story == story_id


# --- Story ---

def test_should_parse_story_create_input() -> None:
    inp = StoryCreateInput(world=WORLD_ID, title="Das erste Licht")
    assert inp.world == WORLD_ID
    assert inp.title == "Das erste Licht"
    assert inp.is_public is False


# --- Location ---

def test_should_parse_location_create_input() -> None:
    inp = LocationCreateInput(world=WORLD_ID, name="Silberwald")
    assert inp.name == "Silberwald"
    assert inp.world == WORLD_ID


# --- Tenant ---

def test_should_parse_provision_request() -> None:
    req = ProvisionRequest(username="max", email="max@example.com")
    assert req.username == "max"
    assert req.display_name is None


def test_should_parse_provision_response() -> None:
    data = {
        "token": "abc123",
        "user_id": 42,
        "tenant_id": str(uuid4()),
        "tenant_slug": "dt-max",
        "created": True,
    }
    resp = ProvisionResponse.model_validate(data)
    assert resp.token == "abc123"
    assert resp.created is True


# --- Lookups ---

def test_should_parse_genre_schema() -> None:
    data = {"id": str(uuid4()), "name": "Fantasy", "slug": "fantasy"}
    genre = GenreSchema.model_validate(data)
    assert genre.name == "Fantasy"
    assert isinstance(genre, LookupSchema)


def test_should_schema_module_exports_all_classes() -> None:
    import weltenfw.schema as s
    assert hasattr(s, "WorldSchema")
    assert hasattr(s, "CharacterSchema")
    assert hasattr(s, "SceneSchema")
    assert hasattr(s, "StorySchema")
    assert hasattr(s, "LocationSchema")
    assert hasattr(s, "ProvisionRequest")
    assert hasattr(s, "GenreSchema")
