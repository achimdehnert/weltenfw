# weltenfw — v0.4.1

**WeltenHub Client Framework** — typed REST client, Pydantic v2 schemas,
and a pluggable storage-backend pattern for the
[WeltenHub](https://weltenforger.com) Story Universe API.

[![CI](https://github.com/achimdehnert/weltenfw/actions/workflows/ci.yml/badge.svg)](https://github.com/achimdehnert/weltenfw/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/iil-weltenfw)](https://pypi.org/project/iil-weltenfw/)
[![Python](https://img.shields.io/pypi/pyversions/iil-weltenfw)](https://pypi.org/project/iil-weltenfw/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Installation

```bash
pip install iil-weltenfw                  # core (httpx + pydantic)
pip install iil-weltenfw[django]          # + Django AppConfig + DjangoCache
```

## Quick Start — Low-Level Client

```python
from weltenfw import WeltenClient

with WeltenClient(
    base_url="https://weltenforger.com/api/v1",
    token="your-token",
) as client:
    world = client.worlds.create(WorldCreateInput(
        name="Aldoria", setting_era="medieval",
    ))
    chars = client.characters.list(world=str(world.id))
    locs  = client.locations.list(world=str(world.id))
    stories = client.stories.list(world=str(world.id))
    scenes  = client.scenes.list(story=str(stories.results[0].id))
```

## Async

```python
async with WeltenClient(base_url=..., token=...) as client:
    world = await client.worlds.aget(world_id)
    locs  = await client.locations.alist(world=world_id)
```

## Django Integration

```python
# settings.py
INSTALLED_APPS  = [..., "weltenfw.django"]
WELTENHUB_URL   = "https://weltenforger.com/api/v1"
WELTENHUB_TOKEN = env("WELTENHUB_TOKEN")

# services.py
from weltenfw.django import get_client
client = get_client()   # lazy singleton, one per worker
```

---

## Storage Backend Pattern (ADR-117)

`weltenfw` ships `WeltenhubBackend` — a **higher-level write/read facade**
on top of `WeltenClient`. Consumer apps (bfagent, travel-beat, …) use this
to keep Weltenhub as the single source of truth without duplicating data.

### Two Scenarios — same API

```python
from weltenfw.backends import WeltenhubBackend

backend = WeltenhubBackend(
    base_url="https://weltenforger.com/api/v1",
    token=token,   # user token (A) or service token (B)
)
```

**Scenario A — user has Weltenhub account:**
`token = user.weltenhub_token` → data visible in Weltenhub UI immediately.

**Scenario B — user not yet linked:**
`token = WELTENHUB_API_KEY` (service token) → data stored, UUID returned,
UI locked until user links their account. No duplication; consumer stores only UUID.

---

## Backend API Reference

### Worlds

| Method | Signature | Returns |
|---|---|---|
| `create_world` | `(name, description, setting_era, **kw)` | `WorldResult` |
| `get_world` | `(world_id)` | `WorldResult` |
| `list_worlds` | `(search, page)` | `WorldPage` |
| `update_world` | `(world_id, **fields)` | `WorldResult` |

```python
result = backend.create_world(name="Aldoria", description="Kingdom of runes")
result.id       # Weltenhub UUID
result.ok       # True on success
result.error    # str | None
result.backend  # "weltenhub"
```

### Characters

| Method | Signature | Returns |
|---|---|---|
| `create_character` | `(world_id, name, personality, backstory, is_protagonist, **kw)` | `CharacterResult` |
| `get_character` | `(character_id)` | `CharacterResult` |
| `list_characters` | `(world_id, page)` | `CharacterPage` |

```python
chars = backend.list_characters(world_id="<uuid>")
for c in chars.results:
    print(c.name, c.role_name)
```

### Locations

| Method | Signature | Returns |
|---|---|---|
| `create_location` | `(world_id, name, description, parent_id, **kw)` | `LocationResult` |
| `list_locations` | `(world_id, page, page_size)` | `LocationPage` |

```python
locs = backend.list_locations(world_id="<uuid>")
for loc in locs.results:
    print(loc.name, loc.location_type_name, loc.full_path)

new_loc = backend.create_location(
    world_id="<uuid>", name="Eisenhain",
    description="A fortress city in the northern mountains.",
)
```

### Stories

| Method | Signature | Returns |
|---|---|---|
| `create_story` | `(world_id, title, synopsis, **kw)` | `StoryResult` |
| `list_stories` | `(world_id, page, page_size)` | `StoryPage` |

```python
stories = backend.list_stories(world_id="<uuid>")
for s in stories.results:
    print(s.title, s.status)

story = backend.create_story(world_id="<uuid>", title="Der Ruf der Runen")
```

### Scenes

| Method | Signature | Returns |
|---|---|---|
| `create_scene` | `(story_id, title, summary, order, **kw)` | `SceneResult` |
| `list_scenes` | `(story_id, page, page_size)` | `ScenePage` |

```python
scenes = backend.list_scenes(story_id="<uuid>")
for s in scenes.results:
    print(s.title, s.location_name, s.order)
```

### Result Types

All result types are **frozen dataclasses** with an `.ok` property:

| Type | Key fields |
|---|---|
| `WorldResult` | `id, name, description, setting_era, genre_name` |
| `CharacterResult` | `id, name, world_id, role_name, description, personality` |
| `LocationResult` | `id, name, world_id, parent_id, location_type_name, description, full_path` |
| `SceneResult` | `id, title, story_id, summary, location_name, order` |
| `StoryResult` | `id, title, world_id, genre_name, status, synopsis` |

All `*Page` types have `.results: list[*Result]` and `.count: int`.

---

## User Provisioning (S2S, idempotent)

```python
token = WeltenhubBackend.provision_user(
    username="bf_hugo",
    email="hugo@example.com",
    base_url="https://weltenforger.com/api/v1",
    service_token=WELTENHUB_API_KEY,
)
# Returns per-user token (Scenario A) or None on failure
```

---

## LocalWorldBackend (tests / offline)

```python
from weltenfw.backends.local import LocalWorldBackend

backend = LocalWorldBackend()
result = backend.create_world(name="Test")
# result.id = "" — caller manages local DB
# result.backend = "local"
```

---

## Custom Backend (Protocol)

Implement `AbstractWorldBackend` without inheriting — structural subtyping:

```python
from weltenfw.backends.base import AbstractWorldBackend, WorldResult

class MyBackend:
    def create_world(self, name: str, **kw) -> WorldResult: ...
    def get_world(self, world_id: str) -> WorldResult: ...
    def list_worlds(self, search: str = "", page: int = 1): ...
    def update_world(self, world_id: str, **fields): ...
    def create_character(self, world_id, name, **kw): ...
    def get_character(self, character_id): ...
    def list_characters(self, world_id, page=1): ...
    def list_locations(self, world_id, page=1, page_size=100): ...
    def create_location(self, world_id, name, **kw): ...
    def list_stories(self, world_id, page=1, page_size=100): ...
    def create_story(self, world_id, title, **kw): ...
    def list_scenes(self, story_id, page=1, page_size=100): ...
    def create_scene(self, story_id, title, **kw): ...
```

---

## Architecture

- **1 Client = 1 Token = 1 Tenant** — no global singleton; multi-tenant callers
  instantiate one client per token.
- **Pydantic v2** — all API responses validated into typed, frozen schemas.
- **Separate Input schemas** — `*CreateInput` (POST) / `*UpdateInput` (PATCH).
- **Lookup cache** — pluggable `CacheBackend` (NullCache → MemoryCache → DjangoCache).
- **Storage Backend Pattern** — Weltenhub-DB is SSoT; consumer apps store UUID only.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Links

- [WeltenHub API Docs](https://weltenforger.com/api/docs/)
- [ADR-117 — Shared World Layer](https://github.com/achimdehnert/platform/blob/main/docs/adr/ADR-117-shared-world-layer-worldfw.md)
