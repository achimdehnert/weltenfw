"""
weltenfw.schema.base - Basis-Schema-Klassen

BaseSchema: frozen=True  - fuer alle API-Response-Schemas (read-only)
BaseInput:  frozen=False - fuer alle Write-Schemas (CreateInput, UpdateInput)

Die Trennung ist bewusst und explizit:
- Jede Klasse hat ihre eigene model_config
- Kein implizites Vererbungs-Override der frozen-Einstellung
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Basis fuer alle Response-Schemas.

    frozen=True: Nach model_validate() keine Mutation erlaubt.
    populate_by_name=True: Felder koennen via alias und Python-Name gefuellt werden.
    """

    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
    )


class BaseInput(BaseModel):
    """Basis fuer alle Write-Schemas (CreateInput, UpdateInput).

    frozen=False: Felder koennen vor dem API-Call mutiert werden.
    populate_by_name=True: Konsistenz mit BaseSchema.
    """

    model_config = ConfigDict(
        frozen=False,
        populate_by_name=True,
    )
