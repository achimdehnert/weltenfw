"""Tests fuer die Item-Ressource — Gegenstaende, die ueber Baende tragen.

weltenhub#58 hat den Typ eingefuehrt; ohne diese Ressource kann kein Aufrufer
ihn benutzen. Der Client ist das fehlende Stueck zwischen writing-hub und
weltenhub (achimdehnert/writing-hub#693).

Gesichert ist hier vor allem eins: der Verbleib darf leer sein. Ein Gegenstand,
dessen Aufenthalt Teil der Handlung ist, hat weder Traeger noch Ort — ein
Schema, das darauf besteht, macht genau diesen Fall unmoeglich.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import httpx
import respx

from weltenfw.client import WeltenClient
from weltenfw.schema.item import ItemCreateInput, ItemSchema

BASE_URL = "https://test.weltenforger.com/api/v1"
NOW = datetime(2026, 3, 1, 12, 0, 0, tzinfo=UTC).isoformat()


def _item_data(name: str = "Die Berger-Akte", **abweichend) -> dict:
    daten = {
        "id": str(uuid4()),
        "tenant": str(uuid4()),
        "world": str(uuid4()),
        "name": name,
        "slug": "die-berger-akte",
        "item_type": 1,
        "item_type_name": "Dokument",
        "description": "Messreihen zum Grundwasserstand.",
        "held_by": None,
        "kept_at": None,
        "whereabouts": "",
        "is_unique": True,
        "is_public": False,
        "order": 0,
        "created_at": NOW,
        "updated_at": NOW,
    }
    daten.update(abweichend)
    return daten


def _client() -> WeltenClient:
    return WeltenClient(base_url=BASE_URL, token="test-token-not-a-secret")


@respx.mock
def test_should_client_list_items() -> None:
    respx.get(f"{BASE_URL}/items/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [_item_data()]}
        )
    )

    seite = _client().items.list()

    assert len(seite.results) == 1
    assert seite.results[0].name == "Die Berger-Akte"


@respx.mock
def test_should_client_get_an_item() -> None:
    daten = _item_data()
    respx.get(f"{BASE_URL}/items/{daten['id']}/").mock(return_value=httpx.Response(200, json=daten))

    objekt = _client().items.get(daten["id"])

    assert isinstance(objekt, ItemSchema)
    assert objekt.item_type_name == "Dokument"


@respx.mock
def test_should_client_create_an_item() -> None:
    daten = _item_data()
    respx.post(f"{BASE_URL}/items/").mock(return_value=httpx.Response(201, json=daten))

    objekt = _client().items.create(
        ItemCreateInput(world=daten["world"], name="Die Berger-Akte", item_type=1),
    )

    assert objekt.name == "Die Berger-Akte"


def test_should_accept_an_item_without_any_whereabouts() -> None:
    """Weder Traeger noch Ort — der haeufigste Fall, solange der Verbleib Handlung ist."""
    objekt = ItemSchema.model_validate(_item_data(held_by=None, kept_at=None, whereabouts=None))

    assert objekt.held_by is None
    assert objekt.kept_at is None


def test_should_accept_an_item_held_by_a_character() -> None:
    figur = str(uuid4())

    objekt = ItemSchema.model_validate(_item_data(held_by=figur, whereabouts="held by Lena Voigt"))

    assert str(objekt.held_by) == figur
    assert objekt.whereabouts == "held by Lena Voigt"


def test_should_expose_items_on_the_client() -> None:
    """Ohne Verdrahtung im Client bliebe die Ressource unerreichbar."""
    mandant = _client()

    assert hasattr(mandant, "items"), "WeltenClient.items fehlt"
    assert mandant.items._base_path == "/items"
