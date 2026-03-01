"""
Tests fuer weltenfw.pagination
"""

import pytest

from weltenfw.exceptions import PaginationError
from weltenfw.pagination import PageResult, iter_all
from weltenfw.schema.base import BaseSchema


class Item(BaseSchema):
    id: int
    name: str


def _make_pages(items_per_page: int, total: int) -> list:
    all_items = [Item(id=i, name=f"item-{i}") for i in range(total)]
    pages = []
    for i in range(0, total, items_per_page):
        chunk = all_items[i : i + items_per_page]
        has_next = (i + items_per_page) < total
        pages.append(
            PageResult(
                count=total,
                next="https://example.com/?page=2" if has_next else None,
                previous=None,
                results=chunk,
            )
        )
    return pages


def test_should_page_result_report_has_next() -> None:
    page = PageResult(count=10, next="https://example.com/?page=2", results=[])
    assert page.has_next is True


def test_should_page_result_report_no_next() -> None:
    page = PageResult(count=5, next=None, results=[])
    assert page.has_next is False


def test_should_iter_all_collect_single_page() -> None:
    pages = _make_pages(items_per_page=10, total=3)
    call_count = 0

    def fetch(page_num: int) -> PageResult:
        nonlocal call_count
        call_count += 1
        return pages[page_num - 1]

    items = list(iter_all(fetch))
    assert len(items) == 3
    assert call_count == 1


def test_should_iter_all_collect_multiple_pages() -> None:
    pages = _make_pages(items_per_page=2, total=5)

    def fetch(page_num: int) -> PageResult:
        return pages[page_num - 1]

    items = list(iter_all(fetch))
    assert len(items) == 5


def test_should_iter_all_raise_on_max_pages_exceeded() -> None:
    def infinite_fetch(page_num: int) -> PageResult:
        return PageResult(
            count=999,
            next=f"https://example.com/?page={page_num + 1}",
            results=[Item(id=page_num, name=f"item-{page_num}")],
        )

    with pytest.raises(PaginationError) as exc_info:
        list(iter_all(infinite_fetch, max_pages=3))
    assert exc_info.value.max_pages == 3


def test_should_iter_all_work_unlimited_with_none() -> None:
    pages = _make_pages(items_per_page=1, total=10)

    def fetch(page_num: int) -> PageResult:
        return pages[page_num - 1]

    items = list(iter_all(fetch, max_pages=None))
    assert len(items) == 10
