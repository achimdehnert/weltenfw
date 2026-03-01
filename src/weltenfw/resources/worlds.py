"""
weltenfw.resources.worlds - World Resource
"""

from __future__ import annotations

from typing import Any

from weltenfw.resources.base import BaseResource
from weltenfw.schema.world import (
    WorldListSchema,
    WorldRuleSchema,
    WorldSchema,
)


class WorldResource(BaseResource[WorldSchema]):
    """Resource fuer /api/v1/worlds/."""

    def rules(self, world_pk: Any) -> list[WorldRuleSchema]:
        """GET /worlds/{pk}/rules/ -> list[WorldRuleSchema]"""
        data = self._http.get(f"{self._base_path}/{world_pk}/rules")
        results = data.get("results", data) if isinstance(data, dict) else data
        return [WorldRuleSchema.model_validate(r) for r in results]

    async def arules(self, world_pk: Any) -> list[WorldRuleSchema]:
        """GET /worlds/{pk}/rules/ -> list[WorldRuleSchema] (async)"""
        data = await self._async_http.get(f"{self._base_path}/{world_pk}/rules")
        results = data.get("results", data) if isinstance(data, dict) else data
        return [WorldRuleSchema.model_validate(r) for r in results]
