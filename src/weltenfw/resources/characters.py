"""
weltenfw.resources.characters - Character Resource
"""

from __future__ import annotations

from typing import Any

from weltenfw.resources.base import BaseResource
from weltenfw.schema.character import (
    CharacterArcSchema,
    CharacterListSchema,
    CharacterRelationshipSchema,
    CharacterSchema,
)


class CharacterResource(BaseResource[CharacterSchema]):
    """Resource fuer /api/v1/characters/."""

    def arcs(self, character_pk: Any) -> list[CharacterArcSchema]:
        """GET /characters/{pk}/arcs/ -> list[CharacterArcSchema]"""
        data = self._http.get(f"{self._base_path}/{character_pk}/arcs")
        results = data.get("results", data) if isinstance(data, dict) else data
        return [CharacterArcSchema.model_validate(r) for r in results]

    def relationships(self, character_pk: Any) -> list[CharacterRelationshipSchema]:
        """GET /characters/{pk}/relationships/ -> list[CharacterRelationshipSchema]"""
        data = self._http.get(f"{self._base_path}/{character_pk}/relationships")
        results = data.get("results", data) if isinstance(data, dict) else data
        return [CharacterRelationshipSchema.model_validate(r) for r in results]

    async def aarcs(self, character_pk: Any) -> list[CharacterArcSchema]:
        data = await self._async_http.get(f"{self._base_path}/{character_pk}/arcs")
        results = data.get("results", data) if isinstance(data, dict) else data
        return [CharacterArcSchema.model_validate(r) for r in results]

    async def arelationships(self, character_pk: Any) -> list[CharacterRelationshipSchema]:
        data = await self._async_http.get(f"{self._base_path}/{character_pk}/relationships")
        results = data.get("results", data) if isinstance(data, dict) else data
        return [CharacterRelationshipSchema.model_validate(r) for r in results]
