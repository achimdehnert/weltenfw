"""
Tests fuer weltenfw.schema.base
"""

import pytest

from weltenfw.schema.base import BaseInput, BaseSchema


class SampleSchema(BaseSchema):
    name: str
    value: int = 0


class SampleInput(BaseInput):
    name: str | None = None
    value: int | None = None


def test_should_base_schema_be_frozen() -> None:
    obj = SampleSchema(name="test", value=42)
    with pytest.raises(Exception):
        obj.name = "other"  # type: ignore[misc]


def test_should_base_input_be_mutable() -> None:
    obj = SampleInput(name="initial")
    obj.name = "changed"
    assert obj.name == "changed"


def test_should_base_schema_validate_from_dict() -> None:
    obj = SampleSchema.model_validate({"name": "hello", "value": 7})
    assert obj.name == "hello"
    assert obj.value == 7


def test_should_base_input_allow_none_fields() -> None:
    obj = SampleInput()
    assert obj.name is None
    assert obj.value is None


def test_should_base_schema_and_input_have_independent_configs() -> None:
    assert SampleSchema.model_config["frozen"] is True
    assert SampleInput.model_config["frozen"] is False
