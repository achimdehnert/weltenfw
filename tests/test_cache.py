"""
Tests fuer weltenfw.cache
"""

import pytest

from weltenfw.cache import CacheBackend, MemoryCache, NullCache


def test_should_null_cache_always_return_none() -> None:
    cache = NullCache()
    cache.set("key", [1, 2, 3], ttl=60)
    assert cache.get("key") is None


def test_should_null_cache_clear_is_noop() -> None:
    cache = NullCache()
    cache.clear()


def test_should_memory_cache_store_and_retrieve() -> None:
    cache = MemoryCache(ttl=60)
    cache.set("genres", [{"id": 1, "name": "Fantasy"}], ttl=60)
    result = cache.get("genres")
    assert result == [{"id": 1, "name": "Fantasy"}]


def test_should_memory_cache_expire_with_zero_ttl() -> None:
    cache = MemoryCache()
    cache.set("key", ["value"], ttl=0)
    assert cache.get("key") is None


def test_should_memory_cache_delete_entry() -> None:
    cache = MemoryCache()
    cache.set("key", ["value"], ttl=60)
    cache.delete("key")
    assert cache.get("key") is None


def test_should_memory_cache_clear_all_entries() -> None:
    cache = MemoryCache()
    cache.set("genres", ["fantasy"], ttl=60)
    cache.set("moods", ["dark"], ttl=60)
    cache.clear()
    assert cache.get("genres") is None
    assert cache.get("moods") is None


def test_should_null_cache_implement_protocol() -> None:
    assert isinstance(NullCache(), CacheBackend)


def test_should_memory_cache_implement_protocol() -> None:
    assert isinstance(MemoryCache(), CacheBackend)
