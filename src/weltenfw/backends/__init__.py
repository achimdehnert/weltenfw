"""
weltenfw.backends — Storage-Backend Pattern (ADR-117)

Konfigurierbare Backends für Welt/Charakter-Operationen:
    - WeltenhubBackend  → schreibt via REST-API in Weltenhub (Premium)
    - LocalWorldBackend → kein Backend; Caller verwaltet lokale DB selbst (Basis)

Auswahl via WORLD_STORAGE_BACKEND in Django-Settings (optional).
"""

from weltenfw.backends.base import (
    AbstractWorldBackend,
    CharacterPage,
    CharacterResult,
    LocationPage,
    LocationResult,
    ScenePage,
    SceneResult,
    WorldPage,
    WorldResult,
)
from weltenfw.backends.weltenhub import WeltenhubBackend

__all__ = [
    "AbstractWorldBackend",
    "WorldResult",
    "WorldPage",
    "CharacterResult",
    "CharacterPage",
    "LocationResult",
    "LocationPage",
    "SceneResult",
    "ScenePage",
    "WeltenhubBackend",
]
