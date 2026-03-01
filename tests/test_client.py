"""
Tests fuer weltenfw.client - WeltenClient
"""

from __future__ import annotations

import pytest
import httpx
import respx
from uuid import uuid4
from datetime import datetime, timezone

from weltenfw.client import WeltenClient
from weltenfw.cache import MemoryCache, NullCache
from weltenfw.schema.world import WorldSchema
from weltenfw.schema.tenant import ProvisionResponse


BASE_URL = "https://test.weltenforger.com/api/v1"
NOW = datetime(2026, 3, 1, 12, 0, 0, tzinfo=timezone.utc).isoformat()


def _world_data(name: str = "Arandur") -> dict:
    return {
        "id": str(uuid4()),
        "tenant": str(uuid4()),
        "name": name,
        "slug": name.lower(),
        "is_public": False,
        "created_at": NOW,
        "updated_at": NOW,
    }


@respx.mock
def test_should_client_list_worlds() -> None:
    world = _world_data()
    respx.get(f"{BASE_URL}/worlds/").mock(
        return_value=httpx.Response(200, json={"count": 1, "next": None, "results": [world]})
    )
    with WeltenClient(base_url=BASE_URL, token="tok") as client:
        result = client.worlds.list()
    assert result.count == 1
    assert result.results[0].name == "Arandur"


@respx.mock
def test_should_client_get_world() -> None:
    world = _world_data("Midgard")
    pk = world["id"]
    respx.get(f"{BASE_URL}/worlds/{pk}/").mock(
        return_value=httpx.Response(200, json=world)
    )
    with WeltenClient(base_url=BASE_URL, token="tok") as client:
        w = client.worlds.get(pk)
    assert w.name == "Midgard"
    assert isinstance(w, WorldSchema)


@respx.mock
def test_should_client_iter_all_worlds() -> None:
    world1 = _world_data("W1")
    world2 = _world_data("W2")
    respx.get(f"{BASE_URL}/worlds/").mock(
        side_effect=[
            httpx.Response(200, json={"count": 2, "next": f"{BASE_URL}/worlds/?page=2", "results": [world1]}),
            httpx.Response(200, json={"count": 2, "next": None, "results": [world2]}),
        ]
    )
    with WeltenClient(base_url=BASE_URL, token="tok") as client:
        worlds = list(client.worlds.iter_all())
    assert len(worlds) == 2
    assert worlds[0].name == "W1"
    assert worlds[1].name == "W2"


@respx.mock
def test_should_client_provision_tenant() -> None:
    tenant_id = str(uuid4())
    respx.post(f"{BASE_URL}/tenants/provision/user/").mock(
        return_value=httpx.Response(201, json={
            "token": "newtoken123",
            "user_id": 99,
            "tenant_id": tenant_id,
            "tenant_slug": "dt-max",
            "created": True,
        })
    )
    from weltenfw.schema.tenant import ProvisionRequest
    with WeltenClient(base_url=BASE_URL, token="servicetoken") as client:
        resp = client.tenants.provision(ProvisionRequest(username="max", email="max@example.com"))
    assert resp.token == "newtoken123"
    assert resp.created is True


def test_should_client_use_null_cache_by_default() -> None:
    client = WeltenClient(base_url=BASE_URL, token="tok")
    assert isinstance(client.lookups._cache, NullCache)
    client.close()


def test_should_client_accept_memory_cache() -> None:
    cache = MemoryCache(ttl=60)
    client = WeltenClient(base_url=BASE_URL, token="tok", lookup_cache=cache)
    assert client.lookups._cache is cache
    client.close()


@respx.mock
def test_should_client_cache_lookup_on_second_call() -> None:
    respx.get(f"{BASE_URL}/lookups/genres/").mock(
        return_value=httpx.Response(200, json=[
            {"id": str(uuid4()), "name": "Fantasy", "slug": "fantasy"}
        ])
    )
    cache = MemoryCache(ttl=3600)
    with WeltenClient(base_url=BASE_URL, token="tok", lookup_cache=cache) as client:
        genres1 = client.lookups.genres()
        genres2 = client.lookups.genres()  # aus Cache
    assert len(genres1) == 1
    assert genres1[0].name == genres2[0].name
    # Nur 1 HTTP-Call trotz 2 Aufrufen
    assert respx.calls.call_count == 1
