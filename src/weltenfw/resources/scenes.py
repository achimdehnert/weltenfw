"""
weltenfw.resources.scenes - Scene Resource
"""

from __future__ import annotations

from typing import Any

from weltenfw.resources.base import BaseResource
from weltenfw.schema.scene import SceneBeatSchema, SceneListSchema, SceneSchema


class SceneResource(BaseResource[SceneSchema]):
    """Resource fuer /api/v1/scenes/."""

    def beats(self, scene_pk: Any) -> list[SceneBeatSchema]:
        """GET /scenes/{pk}/beats/ -> list[SceneBeatSchema]"""
        data = self._http.get(f"{self._base_path}/{scene_pk}/beats")
        results = data.get("results", data) if isinstance(data, dict) else data
        return [SceneBeatSchema.model_validate(r) for r in results]

    async def abeats(self, scene_pk: Any) -> list[SceneBeatSchema]:
        data = await self._async_http.get(f"{self._base_path}/{scene_pk}/beats")
        results = data.get("results", data) if isinstance(data, dict) else data
        return [SceneBeatSchema.model_validate(r) for r in results]
