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

## Storage Backend Pattern (v0.2.0, ADR-117)

`weltenfw` ships a **configurable storage backend** so any app (bfagent,
travel-beat, …) can write worlds and characters directly into Weltenhub-DB
without duplicating data or building a sync pipeline.

### Two scenarios — same code

```python
from weltenfw import WeltenhubBackend

backend = WeltenhubBackend(
    base_url="https://weltenforger.com/api/v1",
    token=token,          # user token (Scenario A) or service token (Scenario B)
)

result = backend.create_world(name="Aldoria", description="Kingdom of runes")
# result.id      → Weltenhub UUID (stored locally as FK reference only)
# result.ok      → True on success
# result.backend → "weltenhub"
```

**Scenario A — user has a Weltenhub account:**
`token = user.weltenhub_token` → world visible in Weltenhub UI immediately.

**Scenario B — user not yet linked ("data without UI"):**
`token = WELTENHUB_API_KEY` (service token) → world stored in Weltenhub-DB,
UUID available, but Weltenhub UI features locked until the user links their account.
No data duplication. The consumer app stores only the UUID.

### User provisioning (S2S, idempotent)

```python
token = WeltenhubBackend.provision_user(
    username="bf_hugo",
    email="hugo@example.com",
    base_url="https://weltenforger.com/api/v1",
    service_token=WELTENHUB_API_KEY,
)
# Returns per-user token for Scenario A
```

### Characters

```python
char = backend.create_character(
    world_id=str(world.id),
    name="Elara",
    personality="Curious and fearless",
    is_protagonist=True,
)
chars = backend.list_characters(world_id=str(world.id))
```

### LocalWorldBackend (for tests / offline)

```python
from weltenfw import LocalWorldBackend

backend = LocalWorldBackend()   # no-op, returns empty results
result = backend.create_world(name="Test")
# result.id = ""  — caller manages local DB
# result.backend = "local"
```

### Backend Protocol

All backends implement `AbstractWorldBackend` (structural subtyping via
`Protocol`). You can write your own backend (e.g. `ObsidianBackend`) without
changing any call sites:

```python
from weltenfw.backends.base import AbstractWorldBackend, WorldResult

class MyBackend:
    def create_world(self, name: str, **kw) -> WorldResult:
        ...
    # implement remaining protocol methods
```

See [`src/weltenfw/backends/`](src/weltenfw/backends/) for full source.

## Architecture

- **1 Client = 1 Token = 1 Tenant** — Multi-tenant consumers instantiate
  one client per tenant token.
- **Pydantic v2** — all responses validated into typed schemas (`frozen=True`).
- **Separate Input schemas** — `*CreateInput` for POST, `*UpdateInput` for PATCH.
- **Lookup cache** — pluggable `CacheBackend` (NullCache default, MemoryCache,
  DjangoCache for Redis).
- **Trailing-slash normalization** — prevents silent `POST→GET` method loss
  on Django's 301 redirect.
- **Storage Backend Pattern** — swappable write channel (ADR-117). Weltenhub-DB
  is the single source of truth; consumer apps store only the UUID reference.

## Links

- [WeltenHub API Docs](https://weltenforger.com/api/docs/)
- [ADR-032](https://github.com/achimdehnert/weltenhub/blob/main/docs/adr/ADR-032-weltenfw-pypi-client-package.md) — weltenfw package decision
- [ADR-117](https://github.com/achimdehnert/platform/blob/main/docs/adr/ADR-117-shared-world-layer-worldfw.md) — Shared World Layer / Storage Backend Pattern
- [backends/ README](src/weltenfw/backends/README.md)
- [Changelog](CHANGELOG.md)
