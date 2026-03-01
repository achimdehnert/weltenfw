# weltenfw

**WeltenHub Client Framework** — typed REST client and Pydantic v2 schemas
for the [WeltenHub](https://weltenforger.com) Story Universe API.

[![CI](https://github.com/achimdehnert/weltenfw/actions/workflows/ci.yml/badge.svg)](https://github.com/achimdehnert/weltenfw/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/weltenfw)](https://pypi.org/project/weltenfw/)
[![Python](https://img.shields.io/pypi/pyversions/weltenfw)](https://pypi.org/project/weltenfw/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Installation

```bash
pip install weltenfw                  # core (httpx + pydantic)
pip install weltenfw[django]          # + Django AppConfig + DjangoCache
pip install weltenfw[authoring]       # + authoringfw adapter
```

## Quick Start

```python
from weltenfw import WeltenClient
from weltenfw.schema.world import WorldCreateInput

with WeltenClient(
    base_url="https://weltenforger.com/api/v1",
    token="your-token",
) as client:
    # Create a world
    world = client.worlds.create(WorldCreateInput(
        name="Aldoria",
        setting_era="medieval",
        description="A kingdom of runes and magic.",
    ))
    print(world.id, world.name)

    # List with pagination
    for w in client.worlds.iter_all():
        print(w.name)

    # Lookup cache
    genres = client.lookups.genres()   # cached after first call
```

## Async

```python
async with WeltenClient(base_url=..., token=...) as client:
    world = await client.worlds.aget(world_id)
    worlds = await client.worlds.alist()
```

## Django Integration

```python
# settings.py
INSTALLED_APPS = [..., "weltenfw.django"]
WELTENHUB_URL   = "https://weltenforger.com/api/v1"
WELTENHUB_TOKEN = env("WELTENHUB_TOKEN")

# views.py / services.py
from weltenfw.django import get_client
client = get_client()   # lazy singleton, per worker
```

## Tenant Provisioning (S2S)

```python
from weltenfw.schema.tenant import ProvisionRequest

result = client.tenants.provision(ProvisionRequest(
    username="hugo",
    email="hugo@example.com",
    display_name="Hugo",
))
# ProvisionResponse(token="...", tenant_id=UUID("..."), created=True)
```

## Architecture

- **1 Client = 1 Token = 1 Tenant** — Multi-tenant consumers instantiate
  one client per tenant token.
- **Pydantic v2** — all responses validated into typed schemas (`frozen=True`).
- **Separate Input schemas** — `*CreateInput` for POST, `*UpdateInput` for PATCH.
- **Lookup cache** — pluggable `CacheBackend` (NullCache default, MemoryCache,
  DjangoCache for Redis).
- **Trailing-slash normalization** — prevents silent `POST→GET` method loss
  on Django's 301 redirect.

## Links

- [WeltenHub API Docs](https://weltenforger.com/api/docs/)
- [ADR-032 Architecture Decision](https://github.com/achimdehnert/weltenhub/blob/main/docs/adr/ADR-032-weltenfw-pypi-client-package.md)
- [Changelog](CHANGELOG.md)
