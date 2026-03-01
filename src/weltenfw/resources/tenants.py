"""
weltenfw.resources.tenants - Tenant Resource + S2S Provisioning
"""

from __future__ import annotations

from weltenfw.resources.base import BaseResource
from weltenfw.schema.tenant import ProvisionRequest, ProvisionResponse, TenantSchema


class TenantResource(BaseResource[TenantSchema]):
    """Resource fuer /api/v1/tenants/.

    Zusaetzlich: S2S Provisioning via POST /api/v1/tenants/provision/user/
    """

    def provision(self, request: ProvisionRequest) -> ProvisionResponse:
        """POST /tenants/provision/user/ -> ProvisionResponse

        Idempotent: existierender User wird nicht doppelt angelegt.
        Nach Provisioning: neuen WeltenClient mit response.token erstellen.
        """
        data = self._http.post(
            "/tenants/provision/user",
            json=request.model_dump(exclude_none=True),
        )
        return ProvisionResponse.model_validate(data)

    async def aprovision(self, request: ProvisionRequest) -> ProvisionResponse:
        """POST /tenants/provision/user/ -> ProvisionResponse (async)"""
        data = await self._async_http.post(
            "/tenants/provision/user",
            json=request.model_dump(exclude_none=True),
        )
        return ProvisionResponse.model_validate(data)
