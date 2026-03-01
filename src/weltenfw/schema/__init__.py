"""
weltenfw.schema - Pydantic-Schemas fuer alle WeltenHub-Entitaeten
"""

from weltenfw.schema.base import BaseInput, BaseSchema
from weltenfw.schema.character import (
    CharacterArcSchema,
    CharacterCreateInput,
    CharacterListSchema,
    CharacterRelationshipSchema,
    CharacterSchema,
    CharacterUpdateInput,
)
from weltenfw.schema.location import (
    LocationCreateInput,
    LocationListSchema,
    LocationSchema,
    LocationUpdateInput,
)
from weltenfw.schema.lookups import (
    BeatTypeSchema,
    CharacterRoleSchema,
    ConflictLevelSchema,
    GenreSchema,
    LocationTypeSchema,
    LookupSchema,
    MoodSchema,
    SceneStatusSchema,
    SceneTypeSchema,
    TransportTypeSchema,
)
from weltenfw.schema.scene import (
    SceneBeatSchema,
    SceneConnectionSchema,
    SceneCreateInput,
    SceneListSchema,
    SceneSchema,
    SceneUpdateInput,
)
from weltenfw.schema.story import (
    ChapterSchema,
    PlotThreadSchema,
    StoryCreateInput,
    StoryListSchema,
    StorySchema,
    StoryUpdateInput,
    TimelineEventSchema,
)
from weltenfw.schema.tenant import ProvisionRequest, ProvisionResponse, TenantSchema
from weltenfw.schema.world import (
    WorldCreateInput,
    WorldListSchema,
    WorldRuleSchema,
    WorldSchema,
    WorldUpdateInput,
)

__all__ = [
    "BaseSchema",
    "BaseInput",
    # Lookups
    "LookupSchema",
    "GenreSchema",
    "MoodSchema",
    "ConflictLevelSchema",
    "LocationTypeSchema",
    "SceneTypeSchema",
    "CharacterRoleSchema",
    "TransportTypeSchema",
    "SceneStatusSchema",
    "BeatTypeSchema",
    # Tenants
    "TenantSchema",
    "ProvisionRequest",
    "ProvisionResponse",
    # Worlds
    "WorldListSchema",
    "WorldSchema",
    "WorldRuleSchema",
    "WorldCreateInput",
    "WorldUpdateInput",
    # Characters
    "CharacterListSchema",
    "CharacterSchema",
    "CharacterArcSchema",
    "CharacterRelationshipSchema",
    "CharacterCreateInput",
    "CharacterUpdateInput",
    # Scenes
    "SceneListSchema",
    "SceneSchema",
    "SceneBeatSchema",
    "SceneConnectionSchema",
    "SceneCreateInput",
    "SceneUpdateInput",
    # Stories
    "StoryListSchema",
    "StorySchema",
    "ChapterSchema",
    "PlotThreadSchema",
    "TimelineEventSchema",
    "StoryCreateInput",
    "StoryUpdateInput",
    # Locations
    "LocationListSchema",
    "LocationSchema",
    "LocationCreateInput",
    "LocationUpdateInput",
]
