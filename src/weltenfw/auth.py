"""
weltenfw.auth - Authentifizierung

DRF Token-Authentifizierung: Authorization: Token <key>
"""

from __future__ import annotations

import httpx


class TokenAuth(httpx.Auth):
    """DRF Token-Auth fuer httpx.

    Injiziert 'Authorization: Token <token>' in jeden Request.
    """

    def __init__(self, token: str) -> None:
        if not token:
            raise ValueError("token must not be empty")
        self._token = token

    def auth_flow(self, request: httpx.Request) -> object:
        request.headers["Authorization"] = f"Token {self._token}"
        yield request
