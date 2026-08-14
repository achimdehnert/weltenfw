"""Antwort-Schemas muessen die API beschreiben, wie sie IST (weltenhub, main-fa00e9c).

Realfall 2026-08-14 (writing-hub, Kanon-Strang #593): der erste echte
``worlds.create()``-Lauf gegen weltenforger.com scheiterte in der
Response-Validierung — die Welt war auf dem Server laengst angelegt. Ursache:

* Das ``WorldViewSet`` nutzt fuer ``list`` UND ``create`` den
  ``WorldListSerializer`` — ohne ``tenant`` und ohne ``updated_at``.
* ``WorldListSchema``/``WorldSchema`` fuehrten beide Felder als Pflicht.

Vorher fiel das nie auf, weil jede Messung gegen LEERE Listen lief
(vacuous green). Die Payloads unten sind woertlich die Feldmengen der
deployten Serializer — nicht nachgebaute Wunschformen. ``tenant`` und
``updated_at`` sind Server-Metadaten; kein Konsument im Bestand liest sie,
darum duerfen sie fehlen (Postel), statt jeden Lauf zu killen.
"""

import uuid

from weltenfw.schema.character import CharacterSchema
from weltenfw.schema.location import LocationSchema
from weltenfw.schema.world import WorldListSchema, WorldSchema

WELT_LIST_ITEM = {
    # Feldmenge des deployten WorldListSerializer (list UND create) — ohne tenant.
    "id": str(uuid.uuid4()),
    "name": "Das Erwachen — Band 1: Der Funke",
    "slug": "das-erwachen-band-1-der-funke",
    "genre": None,
    "genre_name": None,
    "setting_era": "",
    "is_public": False,
    "is_template": False,
    "created_at": "2026-08-14T13:36:30.814050Z",
}


def test_should_accept_a_world_list_item_without_tenant():
    welt = WorldListSchema.model_validate(WELT_LIST_ITEM)
    assert welt.tenant is None
    assert welt.name.startswith("Das Erwachen")


def test_should_accept_the_create_response_that_is_list_shaped():
    # create() parst mit dem vollen WorldSchema — die Antwort kommt aber vom
    # ListSerializer: ohne tenant, ohne updated_at.
    welt = WorldSchema.model_validate(WELT_LIST_ITEM)
    assert welt.tenant is None and welt.updated_at is None
    assert str(welt.id)


def test_should_accept_character_and_location_payloads_without_server_metadata():
    basis = {
        "id": str(uuid.uuid4()),
        "world": str(uuid.uuid4()),
        "name": "Lena",
        "slug": "lena",
        "created_at": "2026-08-14T13:36:30Z",
    }
    figur = CharacterSchema.model_validate(basis)
    ort = LocationSchema.model_validate({**basis, "name": "Klinik", "slug": "klinik"})
    assert figur.tenant is None and figur.updated_at is None
    assert ort.tenant is None and ort.updated_at is None
