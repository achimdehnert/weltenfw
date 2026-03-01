"""
weltenfw.resources.stories - Story Resource
"""

from __future__ import annotations

from weltenfw.resources.base import BaseResource
from weltenfw.schema.story import StoryListSchema, StorySchema


class StoryResource(BaseResource[StorySchema]):
    """Resource fuer /api/v1/stories/."""
