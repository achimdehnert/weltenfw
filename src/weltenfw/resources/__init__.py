"""
weltenfw.resources - Resource-Klassen fuer alle WeltenHub-Domaenen
"""

from weltenfw.resources.characters import CharacterResource
from weltenfw.resources.locations import LocationResource
from weltenfw.resources.lookups import LookupResource
from weltenfw.resources.scenes import SceneResource
from weltenfw.resources.stories import StoryResource
from weltenfw.resources.tenants import TenantResource
from weltenfw.resources.worlds import WorldResource

__all__ = [
    "WorldResource",
    "CharacterResource",
    "SceneResource",
    "StoryResource",
    "LocationResource",
    "LookupResource",
    "TenantResource",
]
