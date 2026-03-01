# Changelog

All notable changes to `weltenfw` are documented here.

Format: [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Sprint 1: Fundament
  - `exceptions.py`: WeltenError-Hierarchie (NotFoundError, AuthError, RateLimitError,
    ValidationError, ServerError, PaginationError)
  - `cache.py`: CacheBackend Protocol, NullCache, MemoryCache
  - `auth.py`: TokenAuth (httpx.Auth, DRF Token)
  - `_http.py`: HttpTransport + AsyncHttpTransport (trailing-slash-fix, error-mapping)
  - `pagination.py`: PageResult[T], iter_all(max_pages=1000), aiter_all()
  - `schema/base.py`: BaseSchema (frozen=True), BaseInput (frozen=False)
  - `django/cache.py`: DjangoCache (lazy import, delete_pattern-Fallback)
  - `.github/workflows/ci.yml`: test (py3.11+3.12) + build + publish (OIDC)

- Sprint 2: Domain-Schemas
  - `schema/lookups.py`: 9 Lookup-Schemas (Genre, Mood, ConflictLevel, ...)
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
  - `resources/base.py`: BaseResource (CRUD: list/get/create/update/partial_update/delete/iter_all)
  - `resources/worlds.py`: WorldResource (+ rules())
  - `resources/characters.py`: CharacterResource (+ arcs(), relationships())
  - `resources/scenes.py`: SceneResource (+ beats())
  - `resources/stories.py`: StoryResource
  - `resources/locations.py`: LocationResource
  - `resources/lookups.py`: LookupResource (read-only, CacheBackend)
  - `resources/tenants.py`: TenantResource (+ provision())
  - `client.py`: WeltenClient (sync + async, context manager)

- Sprint 4: Django-Integration
  - `django/app_config.py`: WeltenfwConfig, get_client() (lazy, per Worker)
  - `django/__init__.py`: Public API (get_client, reset_client)
