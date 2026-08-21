"""
weltenfw.resources.items - Item Resource
"""

from __future__ import annotations

from weltenfw.resources.base import BaseResource
from weltenfw.schema.item import ItemSchema


class ItemResource(BaseResource[ItemSchema]):
    """Resource fuer /api/v1/items/."""
