"""
weltenfw.resources.locations - Location Resource
"""

from __future__ import annotations

from weltenfw.resources.base import BaseResource
from weltenfw.schema.location import LocationListSchema, LocationSchema


class LocationResource(BaseResource[LocationSchema]):
    """Resource fuer /api/v1/locations/."""
