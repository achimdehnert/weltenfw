# Changelog

All notable changes to `weltenfw` are documented here.

Format: [Semantic Versioning](https://semver.org/).

## [0.3.0] — 2026-03-10

### Added

- `backends/base.py`: `LocationResult`, `LocationPage` — typed result types for locations
- `backends/base.py`: `SceneResult`, `ScenePage` — typed result types for scenes
- `backends/base.py`: `StoryResult`, `StoryPage` — typed result types for stories
- `backends/weltenhub.py`: `list_locations(world_id, page, page_size)` — `GET /locations/?world=`
- `backends/weltenhub.py`: `create_location(world_id, name, description, parent_id)` — `POST /locations/`
- `backends/weltenhub.py`: `list_scenes(story_id, page, page_size)` — `GET /scenes/?story=`
- `backends/weltenhub.py`: `create_scene(story_id, title, summary, order)` — `POST /scenes/`
- `backends/weltenhub.py`: `list_stories(world_id, page, page_size)` — `GET /stories/?world=`
- `backends/weltenhub.py`: `create_story(world_id, title, synopsis)` — `POST /stories/`
- `backends/__init__.py`: all new types exported in `__all__`
- `README.md`: complete Backend API Reference with method tables and result type overview

### Changed

- `get_world_context()` in bfagent `WeltenhubService` now uses
  `backend.list_locations()` instead of raw HTTP — no more `_fetch_locations()` workaround

---

## [0.2.0] — 2026-03-05

### Added

- `backends/base.py`: `AbstractWorldBackend` Protocol (structural subtyping,
  `@runtime_checkable`), `WorldResult`, `WorldPage`, `CharacterResult`, `CharacterPage`
- `backends/weltenhub.py`: `WeltenhubBackend` — concrete backend writing to Weltenhub via REST:
  `provision_user()` (classmethod, S2S), `create_world()`, `get_world()`, `list_worlds()`,
  `update_world()`, `create_character()`, `get_character()`, `list_characters()`
- `backends/local.py`: `LocalWorldBackend` — no-op stub for tests / offline mode
- `backends/__init__.py`: public `__all__` export
- bfagent `WeltenhubService`: `ensure_world_registered()`, `get_world_context()`,
  `register_standalone_world()` using `WeltenhubBackend`

---

## [0.1.0] — 2026-03-01

First Alpha release. All Sprint 1–4 deliverables complete.
Pilot consumer: `travel-beat` (DriftTales).

### Added

- Sprint 1: Fundament
  - `exceptions.py`: WeltenError-Hierarchie (NotFoundError, AuthError, RateLimitError,
    ValidationError, ServerError, PaginationError)
  - `cache.py`: CacheBackend Protocol, NullCache, MemoryCache
  - `auth.py`: TokenAuth (httpx.Auth, DRF Token header)
  - `_http.py`: HttpTransport + AsyncHttpTransport (trailing-slash-fix, error-mapping)
  - `pagination.py`: PageResult[T], iter_all(max_pages=1000), aiter_all()
  - `schema/base.py`: BaseSchema (frozen=True), BaseInput (frozen=False)
  - `django/cache.py`: DjangoCache (lazy import, delete_pattern-Fallback)
  - `.github/workflows/ci.yml`: test (py3.11+3.12) + build + publish (OIDC)

- Sprint 2: Domain-Schemas
  - `schema/lookups.py`: 9 Lookup-Schemas (Genre, Mood, ConflictLevel,
    LocationType, SceneType, CharacterRole, TransportType, SceneStatus, BeatType)
  - `schema/tenant.py`: TenantSchema, ProvisionRequest, ProvisionResponse
  - `schema/world.py`: WorldSchema, WorldListSchema, WorldRuleSchema,
    WorldCreateInput, WorldUpdateInput
  - `schema/character.py`: CharacterSchema, CharacterListSchema, CharacterArcSchema,
    CharacterRelationshipSchema, CharacterCreateInput, CharacterUpdateInput
  - `schema/scene.py`: SceneSchema, SceneListSchema, SceneBeatSchema,
    SceneConnectionSchema, SceneCreateInput, SceneUpdateInput
  - `schema/story.py`: StorySchema, StoryListSchema, ChapterSchema,
    PlotThreadSchema, TimelineEventSchema, StoryCreateInput, StoryUpdateInput
  - `schema/location.py`: LocationSchema, LocationListSchema,
    LocationCreateInput, LocationUpdateInput

- Sprint 3: Resources + WeltenClient
  - `resources/base.py`: BaseResource (CRUD: list/get/create/update/partial_update/delete/iter_all
    + async equivalents). All write methods use `model_dump(mode='json')` for
    correct UUID/datetime serialization.
  - `resources/worlds.py`: WorldResource (+ rules())
  - `resources/characters.py`: CharacterResource (+ arcs(), relationships())
  - `resources/scenes.py`: SceneResource (+ beats())
  - `resources/stories.py`: StoryResource
  - `resources/locations.py`: LocationResource
  - `resources/lookups.py`: LookupResource (read-only, CacheBackend)
  - `resources/tenants.py`: TenantResource (+ provision())
  - `client.py`: WeltenClient (sync + async, context manager,
    lookup_cache + lookup_ttl params)

- Sprint 4: Django-Integration + travel-beat Pilot
  - `django/app_config.py`: WeltenfwConfig, get_client() (lazy, per Worker)
  - `django/__init__.py`: Public API (get_client, reset_client)
  - travel-beat integration: `weltenfw_adapter.py` — get_service_client,
    get_user_client, provision_user, get_or_create_world,
    get_or_create_character, get_or_create_location, create_story

### Fixed

- `resources/base.py`: `model_dump()` → `model_dump(mode='json')` in all
  write methods (create, update, partial_update and async equivalents).
  UUID and datetime objects were not serialized to strings, causing
  `TypeError: Object of type UUID is not JSON serializable` when passing
  inputs like `SceneCreateInput(story=UUID(...))` to httpx.

[0.1.0]: https://github.com/achimdehnert/weltenfw/releases/tag/v0.1.0
