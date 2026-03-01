"""
Tests fuer weltenfw.exceptions
"""

import pytest

from weltenfw.exceptions import (
    AuthError,
    NotFoundError,
    PaginationError,
    RateLimitError,
    ServerError,
    ValidationError,
    WeltenError,
)


def test_should_create_welt_error_with_status_code() -> None:
    err = WeltenError("test", status_code=500)
    assert err.status_code == 500
    assert err.message == "test"
    assert str(err) == "test"


def test_should_create_not_found_error() -> None:
    err = NotFoundError()
    assert err.status_code == 404
    assert isinstance(err, WeltenError)


def test_should_create_auth_error() -> None:
    err = AuthError()
    assert err.status_code == 401


def test_should_create_rate_limit_error() -> None:
    err = RateLimitError()
    assert err.status_code == 429


def test_should_create_validation_error_with_detail() -> None:
    err = ValidationError("bad input", detail={"field": "required"})
    assert err.status_code == 400
    assert err.detail == {"field": "required"}


def test_should_create_server_error() -> None:
    err = ServerError(status_code=503)
    assert err.status_code == 503


def test_should_create_pagination_error() -> None:
    err = PaginationError(max_pages=1000)
    assert err.max_pages == 1000
    assert "1000" in str(err)
