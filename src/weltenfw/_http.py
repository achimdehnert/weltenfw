"""
weltenfw._http - Interner HTTP-Transport

Kapselt httpx fuer sync und async Requests.
Normalisiert URLs (trailing slash), mapped HTTP-Fehler auf WeltenError-Subklassen.

Django APPEND_SLASH=True: Requests ohne trailing slash -> 301 Redirect.
Bei POST geht dabei die HTTP-Methode verloren (301 -> GET). Daher:
Alle Pfade werden vor dem Request mit trailing slash normalisiert.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import httpx

from weltenfw.auth import TokenAuth
from weltenfw.exceptions import (
    AuthError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    WeltenError,
)


class HttpTransport:
    """Synchroner HTTP-Transport auf Basis von httpx.

    Args:
        base_url: Basis-URL der WeltenHub-API (z.B. 'https://weltenforger.com/api/v1').
        token:    DRF-Auth-Token.
        timeout:  Request-Timeout in Sekunden (default: 30.0).
    """

    def __init__(self, base_url: str, token: str, timeout: float = 30.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            auth=TokenAuth(token),
            timeout=timeout,
            follow_redirects=False,
        )

    def _url(self, path: str) -> str:
        """Normalisiert Pfad: fuegt trailing slash hinzu, verbindet mit base_url."""
        if not path.startswith("/"):
            path = "/" + path
        if not path.endswith("/"):
            path = path + "/"
        return urljoin(self._base_url + "/", path.lstrip("/"))

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Mapped HTTP-Fehlercodes auf WeltenError-Subklassen."""
        code = response.status_code
        if code < 400:
            return
        try:
            detail = response.json()
        except Exception:
            detail = {"raw": response.text}
        if code in (401, 403):
            raise AuthError(str(detail))
        if code == 404:
            raise NotFoundError(str(detail))
        if code == 429:
            raise RateLimitError(str(detail))
        if code in (400, 422):
            raise ValidationError(
                str(detail), detail=detail if isinstance(detail, dict) else {}
            )
        if code >= 500:
            raise ServerError(str(detail), status_code=code)
        raise WeltenError(str(detail), status_code=code)

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = self._client.get(self._url(path), params=params)
        self._raise_for_status(response)
        return response.json()

    def post(self, path: str, json: Any) -> Any:
        response = self._client.post(self._url(path), json=json)
        self._raise_for_status(response)
        return response.json()

    def put(self, path: str, json: Any) -> Any:
        response = self._client.put(self._url(path), json=json)
        self._raise_for_status(response)
        return response.json()

    def patch(self, path: str, json: Any) -> Any:
        response = self._client.patch(self._url(path), json=json)
        self._raise_for_status(response)
        return response.json()

    def delete(self, path: str) -> None:
        response = self._client.delete(self._url(path))
        self._raise_for_status(response)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> HttpTransport:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncHttpTransport:
    """Asynchroner HTTP-Transport auf Basis von httpx.AsyncClient."""

    def __init__(self, base_url: str, token: str, timeout: float = 30.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            auth=TokenAuth(token),
            timeout=timeout,
            follow_redirects=False,
        )

    def _url(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        if not path.endswith("/"):
            path = path + "/"
        return urljoin(self._base_url + "/", path.lstrip("/"))

    def _raise_for_status(self, response: httpx.Response) -> None:
        code = response.status_code
        if code < 400:
            return
        try:
            detail = response.json()
        except Exception:
            detail = {"raw": response.text}
        if code in (401, 403):
            raise AuthError(str(detail))
        if code == 404:
            raise NotFoundError(str(detail))
        if code == 429:
            raise RateLimitError(str(detail))
        if code in (400, 422):
            raise ValidationError(
                str(detail), detail=detail if isinstance(detail, dict) else {}
            )
        if code >= 500:
            raise ServerError(str(detail), status_code=code)
        raise WeltenError(str(detail), status_code=code)

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = await self._client.get(self._url(path), params=params)
        self._raise_for_status(response)
        return response.json()

    async def post(self, path: str, json: Any) -> Any:
        response = await self._client.post(self._url(path), json=json)
        self._raise_for_status(response)
        return response.json()

    async def put(self, path: str, json: Any) -> Any:
        response = await self._client.put(self._url(path), json=json)
        self._raise_for_status(response)
        return response.json()

    async def patch(self, path: str, json: Any) -> Any:
        response = await self._client.patch(self._url(path), json=json)
        self._raise_for_status(response)
        return response.json()

    async def delete(self, path: str) -> None:
        response = await self._client.delete(self._url(path))
        self._raise_for_status(response)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncHttpTransport:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()
