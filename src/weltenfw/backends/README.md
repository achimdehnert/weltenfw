# weltenfw — Storage Backend Pattern

## Übersicht

Das Backend-Pattern ermöglicht es jeder Consumer-App (bfagent, travel-beat, …),
Weltenbau-Entitäten (Welten, Charaktere, Orte) direkt in der **Weltenhub-DB** zu
persistieren — ohne Datenkopien, ohne Sync-Pipeline, ohne Push-Sync.

**Weltenhub-DB ist die Single Source of Truth.**
Consumer-Apps speichern nur die UUID-Referenz.

---

## Zwei Szenarien

```
┌─────────────────────────────────────────────────────────────────┐
│  Szenario A — User hat Weltenhub-Account (verknüpft)            │
│                                                                 │
│  WeltenhubBackend(token=user.weltenhub_token)                   │
│    → UUID in Weltenhub-DB                                       │
│    → Weltenhub-UI sofort verfügbar                              │
│    → Erweiterte Features: Arcs, Regeln, Locations, Szenen       │
├─────────────────────────────────────────────────────────────────┤
│  Szenario B — User noch nicht verknüpft ("Data ohne UI")        │
│                                                                 │
│  WeltenhubBackend(token=settings.WELTENHUB_API_KEY)             │
│    → UUID in Weltenhub-DB (via Service-Token)                   │
│    → Consumer-App (bfagent/travel-beat) weiterhin nutzbar       │
│    → Weltenhub-UI gesperrt bis Account verknüpft                │
│    → Nach Verknüpfung: alle Daten sofort in Weltenhub sichtbar  │
└─────────────────────────────────────────────────────────────────┘
```

**Kernprinzip:** Die UUID existiert ab dem ersten Anlegen — immer, in beiden Szenarien.

---

## Dateien

```
backends/
├── __init__.py       Exporte: AbstractWorldBackend, WeltenhubBackend, LocalWorldBackend
├── base.py           AbstractWorldBackend Protocol + WorldResult, CharacterResult
├── weltenhub.py      WeltenhubBackend — wraps WeltenClient, schreibt in Weltenhub-DB
├── local.py          LocalWorldBackend — No-op Stub für Tests / offline Entwicklung
└── README.md         Diese Datei
```

---

## Klassen-Übersicht

### `WorldResult` / `CharacterResult`

Unveränderliche Rückgabe-Typen (frozen dataclass):

```python
@dataclass(frozen=True)
class WorldResult:
    id: str           # Weltenhub UUID — leerer String bei Fehler
    name: str
    description: str = ""
    setting_era: str = ""
    genre_name: str = ""
    backend: str = "unknown"   # "weltenhub" | "local"
    error: str | None = None

    @property
    def ok(self) -> bool:
        return bool(self.id) and self.error is None
```

### `AbstractWorldBackend` (Protocol)

Alle Backends implementieren dieses Interface via structural subtyping.
Kein `isinstance`-Check nötig — Duck Typing.

```python
class AbstractWorldBackend(Protocol):
    def create_world(self, name, description="", setting_era="", **kw) -> WorldResult: ...
    def get_world(self, world_id: str) -> WorldResult: ...
    def list_worlds(self, search="", page=1) -> WorldPage: ...
    def update_world(self, world_id: str, **fields) -> WorldResult: ...
    def create_character(self, world_id, name, personality="", ...) -> CharacterResult: ...
    def get_character(self, character_id: str) -> CharacterResult: ...
    def list_characters(self, world_id: str, page=1) -> CharacterPage: ...
    def provision_user(self, username: str, email: str) -> str | None: ...
```

### `WeltenhubBackend`

Konkretes Backend — wraps `WeltenClient`. **Schreibt immer in Weltenhub-DB.**

```python
from weltenfw import WeltenhubBackend

# Szenario A: User-Token
backend = WeltenhubBackend(
    base_url="https://weltenforger.com/api/v1",
    token=user.weltenhub_token,
)

# Szenario B: Service-Token (aus settings.WELTENHUB_API_KEY)
backend = WeltenhubBackend(
    base_url=settings.WELTENHUB_API_URL,
    token=settings.WELTENHUB_API_KEY,
)
```

**Idempotenz:** `create_world()` sucht zuerst nach einer Welt mit demselben Namen
im Tenant. Existiert sie, wird sie zurückgegeben statt dupliziert.

**User-Provisioning** (classmethod, kein Backend-Objekt nötig):
```python
token = WeltenhubBackend.provision_user(
    username="bf_hugo",
    email="hugo@example.com",
    base_url=settings.WELTENHUB_API_URL,
    service_token=settings.WELTENHUB_API_KEY,
)
# → per-user Token für Szenario A
# → idempotent: existierender User wird nicht dupliziert
```

### `LocalWorldBackend`

No-op Backend. Gibt leere-aber-ok Ergebnisse zurück.
Nützlich für Tests und Apps ohne Weltenhub-Verbindung.

```python
from weltenfw import LocalWorldBackend

backend = LocalWorldBackend()
result = backend.create_world(name="Test")
# result.id = ""  (Caller verwaltet lokale DB selbst)
# result.ok = True  (kein Fehler — nur kein Weltenhub)
# result.backend = "local"
```

---

## Vollständiges Nutzungsbeispiel

```python
from weltenfw import WeltenhubBackend

# 1. Backend initialisieren (Szenario A oder B)
user_token = getattr(user, "weltenhub_token", None)
token = user_token or settings.WELTENHUB_API_KEY

backend = WeltenhubBackend(
    base_url=settings.WELTENHUB_API_URL,
    token=token,
)

# 2. Welt anlegen (idempotent)
world = backend.create_world(
    name="Drachenwelt",
    description="Ein Königreich aus Feuer und Stein.",
    setting_era="medieval-fantasy",
)
if not world.ok:
    logger.error("Weltenhub create_world failed: %s", world.error)
    # Fallback: lokal speichern, später nachregistrieren

# 3. UUID lokal speichern — NUR Referenz, keine Kopie
local_world.weltenhub_world_id = world.id
local_world.save(update_fields=["weltenhub_world_id"])

# 4. Charaktere anlegen
hero = backend.create_character(
    world_id=world.id,
    name="Elara",
    personality="Neugierig und furchtlos",
    is_protagonist=True,
)

# 5. Live lesen (kein lokaler Cache)
chars = backend.list_characters(world_id=world.id)
for c in chars.results:
    print(c.name, c.role_name)

# 6. Weltenhub-UI Status prüfen
ui_available = bool(user_token)
if not ui_available:
    # Zeige Hinweis: "Weltenhub-Account verknüpfen für erweiterte Features"
    pass
```

---

## Django-Integration (bfagent Pattern)

Das `WeltenhubService` in `apps/writing_hub/services/weltenhub_sync.py`
kapselt den Backend-Zugriff für bfagent:

```python
from apps.writing_hub.services.weltenhub_sync import WeltenhubService

svc = WeltenhubService(request.user)

# Projekt registrieren (Szenario A oder B automatisch)
result = svc.ensure_world_registered(project)
if result.ok:
    # result.world_id     → Weltenhub UUID
    # result.ui_available → True wenn User-Account verknüpft
    # result.created      → True wenn neu angelegt
```

---

## Eigenes Backend implementieren

```python
from weltenfw.backends.base import AbstractWorldBackend, WorldResult, CharacterResult
from weltenfw.backends.base import WorldPage, CharacterPage

class MyCustomBackend:
    """Beispiel: Backend das in eine andere API schreibt."""

    def create_world(self, name: str, description: str = "", **kw) -> WorldResult:
        # ... eigene Logik ...
        return WorldResult(id="custom-uuid", name=name, backend="my-backend")

    def get_world(self, world_id: str) -> WorldResult:
        return WorldResult(id=world_id, name="", backend="my-backend")

    def list_worlds(self, search: str = "", page: int = 1) -> WorldPage:
        return WorldPage()

    def update_world(self, world_id: str, **fields) -> WorldResult:
        return WorldResult(id=world_id, name="", backend="my-backend")

    def create_character(self, world_id, name, **kw) -> CharacterResult:
        return CharacterResult(id="char-uuid", name=name, world_id=world_id, backend="my-backend")

    def get_character(self, character_id: str) -> CharacterResult:
        return CharacterResult(id=character_id, name="", backend="my-backend")

    def list_characters(self, world_id: str, page: int = 1) -> CharacterPage:
        return CharacterPage()

    def provision_user(self, username: str, email: str) -> str | None:
        return None
```

Duck Typing — kein `AbstractWorldBackend` in der Klassendefinition nötig.
Optionaler Runtime-Check: `isinstance(backend, AbstractWorldBackend)`.

---

## Settings-Referenz

| Setting | Zweck | Default |
|---------|-------|---------|
| `WELTENHUB_API_URL` | Weltenhub API Base URL | `https://weltenforger.com/api/v1` |
| `WELTENHUB_API_KEY` | Service-Token für S2S (Szenario B) | `""` |
| `WELTENHUB_TIMEOUT` | HTTP-Timeout in Sekunden | `30` |

---

## Tests

```python
# In Tests: LocalWorldBackend nutzen (kein HTTP)
from weltenfw import LocalWorldBackend

def test_world_registration(monkeypatch):
    from weltenfw import WeltenhubBackend
    monkeypatch.setattr(
        "apps.writing_hub.services.weltenhub_sync.WeltenhubBackend",
        lambda **kw: LocalWorldBackend(),
    )
    svc = WeltenhubService(user)
    result = svc.ensure_world_registered(project)
    assert result.ok is False  # LocalWorldBackend gibt id="" zurück
```

Oder direkt mit `respx` mocken (WeltenClient uses httpx):

```python
import respx
import httpx

@respx.mock
def test_create_world():
    respx.post("https://weltenforger.com/api/v1/worlds/worlds/").mock(
        return_value=httpx.Response(201, json={"id": "uuid-xyz", "name": "Test"})
    )
    backend = WeltenhubBackend(base_url="https://weltenforger.com/api/v1", token="tok")
    result = backend.create_world(name="Test")
    assert result.ok
    assert result.id == "uuid-xyz"
```

---

## Verwandte Dokumente

- [ADR-117](https://github.com/achimdehnert/platform/blob/main/docs/adr/ADR-117-shared-world-layer-worldfw.md) — Architektur-Entscheidung
- [weltenfw README](../../README.md) — Package-Übersicht
- [bfagent WELTENHUB_INTEGRATION.md](https://github.com/achimdehnert/bfagent/blob/main/docs/WELTENHUB_INTEGRATION.md) — Implementierungs-Guide
- [platform CROSS_APP_INTEGRATION.md](https://github.com/achimdehnert/platform/blob/main/docs/patterns/CROSS_APP_INTEGRATION.md) — Wiederverwendbares Pattern
