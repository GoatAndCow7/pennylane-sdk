"""Base classes for API resources.

Resource classes (``client.customer_invoices``, ``client.products``...) are
thin wrappers around the HTTP engine. They inherit these bases and use the
``_get / _get_page / _post / _put / _delete`` helpers with the endpoint path
as a string literal: a convention audited by ``scripts/check_coverage.py``.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, overload

from ._models import PennylaneModel

if TYPE_CHECKING:
    from ._base_client import AsyncAPIClient, SyncAPIClient
    from ._pagination import AsyncCursorPage, SyncCursorPage

__all__ = ["AsyncAPIResource", "SyncAPIResource"]

T = TypeVar("T", bound=PennylaneModel)


class SyncAPIResource:
    """Base class for synchronous resources."""

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client

    def _get_page(
        self,
        path: str,
        *,
        item_type: type[T],
        params: Mapping[str, Any] | None = None,
    ) -> SyncCursorPage[T]:
        return self._client.request_page(path, item_type=item_type, params=params)

    def _get(
        self,
        path: str,
        *,
        cast_to: type[T],
        params: Mapping[str, Any] | None = None,
    ) -> T:
        return self._client.request("GET", path, cast_to=cast_to, params=params)

    @overload
    def _post(
        self,
        path: str,
        *,
        cast_to: type[T],
        body: Any = None,
        params: Mapping[str, Any] | None = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> T: ...

    @overload
    def _post(
        self,
        path: str,
        *,
        cast_to: None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> None: ...

    def _post(
        self,
        path: str,
        *,
        cast_to: type[T] | None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> T | None:
        return self._client.request(
            "POST", path, cast_to=cast_to, body=body, params=params, files=files, data=data
        )

    @overload
    def _put(
        self,
        path: str,
        *,
        cast_to: type[T],
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> T: ...

    @overload
    def _put(
        self,
        path: str,
        *,
        cast_to: None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> None: ...

    def _put(
        self,
        path: str,
        *,
        cast_to: type[T] | None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> T | None:
        return self._client.request("PUT", path, cast_to=cast_to, body=body, params=params)

    @overload
    def _delete(
        self,
        path: str,
        *,
        cast_to: type[T],
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> T: ...

    @overload
    def _delete(
        self,
        path: str,
        *,
        cast_to: None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> None: ...

    def _delete(
        self,
        path: str,
        *,
        cast_to: type[T] | None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> T | None:
        return self._client.request("DELETE", path, cast_to=cast_to, body=body, params=params)


class AsyncAPIResource:
    """Base class for asynchronous resources."""

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client

    async def _get_page(
        self,
        path: str,
        *,
        item_type: type[T],
        params: Mapping[str, Any] | None = None,
    ) -> AsyncCursorPage[T]:
        return await self._client.request_page(path, item_type=item_type, params=params)

    async def _get(
        self,
        path: str,
        *,
        cast_to: type[T],
        params: Mapping[str, Any] | None = None,
    ) -> T:
        return await self._client.request("GET", path, cast_to=cast_to, params=params)

    @overload
    async def _post(
        self,
        path: str,
        *,
        cast_to: type[T],
        body: Any = None,
        params: Mapping[str, Any] | None = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> T: ...

    @overload
    async def _post(
        self,
        path: str,
        *,
        cast_to: None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> None: ...

    async def _post(
        self,
        path: str,
        *,
        cast_to: type[T] | None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
        files: Any = None,
        data: Mapping[str, Any] | None = None,
    ) -> T | None:
        return await self._client.request(
            "POST", path, cast_to=cast_to, body=body, params=params, files=files, data=data
        )

    @overload
    async def _put(
        self,
        path: str,
        *,
        cast_to: type[T],
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> T: ...

    @overload
    async def _put(
        self,
        path: str,
        *,
        cast_to: None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> None: ...

    async def _put(
        self,
        path: str,
        *,
        cast_to: type[T] | None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> T | None:
        return await self._client.request("PUT", path, cast_to=cast_to, body=body, params=params)

    @overload
    async def _delete(
        self,
        path: str,
        *,
        cast_to: type[T],
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> T: ...

    @overload
    async def _delete(
        self,
        path: str,
        *,
        cast_to: None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> None: ...

    async def _delete(
        self,
        path: str,
        *,
        cast_to: type[T] | None = None,
        body: Any = None,
        params: Mapping[str, Any] | None = None,
    ) -> T | None:
        return await self._client.request(
            "DELETE", path, cast_to=cast_to, body=body, params=params
        )
