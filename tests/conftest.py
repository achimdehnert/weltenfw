"""
weltenfw test conftest - Fixtures und Helpers
"""

from __future__ import annotations

import pytest


@pytest.fixture
def base_url() -> str:
    return "https://test.weltenforger.com/api/v1"


@pytest.fixture
def test_token() -> str:
    return "test-token-abc123"
