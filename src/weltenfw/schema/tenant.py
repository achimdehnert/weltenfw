"""
weltenfw.schema.tenant - Tenant + S2S Provisioning Schemas

Verifiziert aus apps/tenants/views.py (ProvisionViewSet)
und apps/tenants/urls.py.

S2S Provisioning-Endpunkt: POST /api/v1/tenants/provision/user/
"""

from __future__ import annotations

from uuid import UUID

from weltenfw.schema.base import BaseInput, BaseSchema


class TenantSchema(BaseSchema):
    """Tenant-Objekt (read-only)."""

    id: UUID
    name: str
    slug: str
    tenant_id: UUID
    is_active: bool = True


class ProvisionRequest(BaseInput):
    """Input fuer S2S User-Provisioning.

    POST /api/v1/tenants/provision/user/
    Idempotent: existierender User wird nicht doppelt angelegt.
    """

    username: str
    email: str
    display_name: str | None = None


class ProvisionResponse(BaseSchema):
    """Response des S2S Provisioning-Endpunkts.

    Liefert Token fuer den provisionierten User.
    Nach Provisioning: neuen WeltenClient mit diesem Token erstellen.
    """

    token: str
    user_id: int
    tenant_id: UUID
    tenant_slug: str
    created: bool
