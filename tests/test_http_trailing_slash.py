"""
Tests fuer weltenfw._http: trailing-slash-Normalisierung

Django APPEND_SLASH=True: POST ohne trailing slash -> 301 -> GET (Methodenverlust).
_http.py normalisiert alle Pfade vor dem Request.
"""

import httpx
import pytest
import respx

from weltenfw._http import HttpTransport
from weltenfw.exceptions import AuthError, NotFoundError


@respx.mock
def test_should_add_trailing_slash_to_path() -> None:
    respx.get("https://test.example.com/api/v1/worlds/").mock(
        return_value=httpx.Response(200, json={"count": 0, "results": []})
    )
    transport = HttpTransport("https://test.example.com/api/v1", token="testtoken")
    result = transport.get("/worlds")
    assert result == {"count": 0, "results": []}
    transport.close()


@respx.mock
def test_should_not_double_trailing_slash() -> None:
    respx.get("https://test.example.com/api/v1/worlds/").mock(
        return_value=httpx.Response(200, json={"count": 0, "results": []})
    )
    transport = HttpTransport("https://test.example.com/api/v1", token="testtoken")
    result = transport.get("/worlds/")
    assert result == {"count": 0, "results": []}
    transport.close()


@respx.mock
def test_should_raise_not_found_on_404() -> None:
    respx.get("https://test.example.com/api/v1/worlds/missing/").mock(
        return_value=httpx.Response(404, json={"detail": "Not found."})
    )
    transport = HttpTransport("https://test.example.com/api/v1", token="testtoken")
    with pytest.raises(NotFoundError):
        transport.get("/worlds/missing")
    transport.close()


@respx.mock
def test_should_raise_auth_error_on_401() -> None:
    respx.get("https://test.example.com/api/v1/worlds/").mock(
        return_value=httpx.Response(401, json={"detail": "Invalid token."})
    )
    transport = HttpTransport("https://test.example.com/api/v1", token="badtoken")
    with pytest.raises(AuthError):
        transport.get("/worlds")
    transport.close()
