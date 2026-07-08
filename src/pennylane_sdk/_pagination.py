"""Cursor pagination with transparent auto-fetching.

Every list endpoint returns a page object. Iterating over the page yields the
items of ALL pages, fetching the next ones lazily (under the client throttle):

    for invoice in client.customer_invoices.list(limit=100):
        ...  # seamlessly walks every page

To handle pages manually, use ``.items`` (current page only),
``.next_page()`` / ``await .next_page()``, or ``.iter_pages()``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from ._models import PennylaneModel

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

    from ._base_client import AsyncAPIClient, SyncAPIClient

__all__ = ["AsyncCursorPage", "AsyncNumberedPage", "SyncCursorPage", "SyncNumberedPage"]

T = TypeVar("T", bound=PennylaneModel)


class BasePage(Generic[T]):
    """State shared by the sync and async page implementations."""

    items: list[T]
    has_more: bool
    next_cursor: str | None
    included: list[Any] | None

    def _load(self, item_type: type[T], data: dict[str, Any]) -> None:
        raw_items = data.get("items") or []
        self.items = [item_type.model_validate(item) for item in raw_items]
        self.has_more = bool(data.get("has_more"))
        cursor = data.get("next_cursor")
        self.next_cursor = cursor if isinstance(cursor, str) else None
        included = data.get("included")
        self.included = included if isinstance(included, list) else None

    def __len__(self) -> int:
        return len(self.items)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(items={len(self.items)}, has_more={self.has_more}, "
            f"next_cursor={self.next_cursor!r})"
        )


class SyncCursorPage(BasePage[T]):
    """One page of results from the sync client."""

    def __init__(
        self,
        *,
        client: SyncAPIClient,
        item_type: type[T],
        path: str,
        params: dict[str, Any],
        data: dict[str, Any],
    ) -> None:
        self._client = client
        self._item_type = item_type
        self._path = path
        self._params = params
        self._load(item_type, data)

    def next_page(self) -> SyncCursorPage[T] | None:
        """Fetch the next page, or return ``None`` on the last page.

        The original filter/sort parameters are re-sent alongside the cursor,
        as required by the API (the cursor does not encode them).
        """
        if not self.has_more or self.next_cursor is None:
            return None
        params = {**self._params, "cursor": self.next_cursor}
        return self._client.request_page(self._path, item_type=self._item_type, params=params)

    def iter_pages(self) -> Iterator[SyncCursorPage[T]]:
        """Iterate page by page, starting with this one."""
        page: SyncCursorPage[T] | None = self
        while page is not None:
            yield page
            page = page.next_page()

    def __iter__(self) -> Iterator[T]:
        """Iterate over the items of every page (auto-pagination)."""
        for page in self.iter_pages():
            yield from page.items


class AsyncCursorPage(BasePage[T]):
    """One page of results from the async client."""

    def __init__(
        self,
        *,
        client: AsyncAPIClient,
        item_type: type[T],
        path: str,
        params: dict[str, Any],
        data: dict[str, Any],
    ) -> None:
        self._client = client
        self._item_type = item_type
        self._path = path
        self._params = params
        self._load(item_type, data)

    async def next_page(self) -> AsyncCursorPage[T] | None:
        """Fetch the next page, or return ``None`` on the last page."""
        if not self.has_more or self.next_cursor is None:
            return None
        params = {**self._params, "cursor": self.next_cursor}
        return await self._client.request_page(
            self._path, item_type=self._item_type, params=params
        )

    async def iter_pages(self) -> AsyncIterator[AsyncCursorPage[T]]:
        """Iterate page by page, starting with this one."""
        page: AsyncCursorPage[T] | None = self
        while page is not None:
            yield page
            page = await page.next_page()

    def __aiter__(self) -> AsyncIterator[T]:
        """Iterate over the items of every page (auto-pagination)."""
        return self._iter_items()

    async def _iter_items(self) -> AsyncIterator[T]:
        async for page in self.iter_pages():
            for item in page.items:
                yield item


class BaseNumberedPage(Generic[T]):
    """State shared by the sync and async page-number implementations.

    A few Firm API endpoints (companies, fiscal years, trial balance)
    paginate with ``page`` / ``per_page`` instead of a cursor.
    """

    items: list[T]
    total_pages: int | None
    current_page: int | None

    def _load(self, item_type: type[T], data: dict[str, Any]) -> None:
        raw_items = data.get("items") or []
        self.items = [item_type.model_validate(item) for item in raw_items]
        total = data.get("total_pages")
        self.total_pages = total if isinstance(total, int) else None
        current = data.get("current_page")
        self.current_page = current if isinstance(current, int) else None

    @property
    def has_more(self) -> bool:
        if self.total_pages is None or self.current_page is None:
            return False
        return self.current_page < self.total_pages

    def __len__(self) -> int:
        return len(self.items)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(items={len(self.items)}, "
            f"current_page={self.current_page}, total_pages={self.total_pages})"
        )


class SyncNumberedPage(BaseNumberedPage[T]):
    """One page of results from a page-number paginated endpoint (sync)."""

    def __init__(
        self,
        *,
        client: SyncAPIClient,
        item_type: type[T],
        path: str,
        params: dict[str, Any],
        data: dict[str, Any],
    ) -> None:
        self._client = client
        self._item_type = item_type
        self._path = path
        self._params = params
        self._load(item_type, data)

    def next_page(self) -> SyncNumberedPage[T] | None:
        """Fetch the next page, or return ``None`` on the last page."""
        if not self.has_more or self.current_page is None:
            return None
        params = {**self._params, "page": self.current_page + 1}
        return self._client.request_numbered_page(
            self._path, item_type=self._item_type, params=params
        )

    def iter_pages(self) -> Iterator[SyncNumberedPage[T]]:
        """Iterate page by page, starting with this one."""
        page: SyncNumberedPage[T] | None = self
        while page is not None:
            yield page
            page = page.next_page()

    def __iter__(self) -> Iterator[T]:
        """Iterate over the items of every page (auto-pagination)."""
        for page in self.iter_pages():
            yield from page.items


class AsyncNumberedPage(BaseNumberedPage[T]):
    """One page of results from a page-number paginated endpoint (async)."""

    def __init__(
        self,
        *,
        client: AsyncAPIClient,
        item_type: type[T],
        path: str,
        params: dict[str, Any],
        data: dict[str, Any],
    ) -> None:
        self._client = client
        self._item_type = item_type
        self._path = path
        self._params = params
        self._load(item_type, data)

    async def next_page(self) -> AsyncNumberedPage[T] | None:
        """Fetch the next page, or return ``None`` on the last page."""
        if not self.has_more or self.current_page is None:
            return None
        params = {**self._params, "page": self.current_page + 1}
        return await self._client.request_numbered_page(
            self._path, item_type=self._item_type, params=params
        )

    async def iter_pages(self) -> AsyncIterator[AsyncNumberedPage[T]]:
        """Iterate page by page, starting with this one."""
        page: AsyncNumberedPage[T] | None = self
        while page is not None:
            yield page
            page = await page.next_page()

    def __aiter__(self) -> AsyncIterator[T]:
        """Iterate over the items of every page (auto-pagination)."""
        return self._iter_items()

    async def _iter_items(self) -> AsyncIterator[T]:
        async for page in self.iter_pages():
            for item in page.items:
                yield item
