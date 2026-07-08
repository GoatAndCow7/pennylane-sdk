from __future__ import annotations

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk._models import PennylaneModel

from .conftest import BASE_URL


class Product(PennylaneModel):
    id: int


def _page(ids: list[int], next_cursor: str | None) -> dict[str, object]:
    return {
        "items": [{"id": i} for i in ids],
        "has_more": next_cursor is not None,
        "next_cursor": next_cursor,
    }


class TestSyncPagination:
    @respx.mock
    def test_single_page(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(200, json=_page([1, 2], None))
        )
        page = sync_client.request_page("/products", item_type=Product)
        assert [p.id for p in page.items] == [1, 2]
        assert page.has_more is False
        assert page.next_page() is None
        assert len(page) == 2

    @respx.mock
    def test_auto_iteration_walks_all_pages(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/products")
        route.side_effect = [
            httpx.Response(200, json=_page([1, 2], "cur2")),
            httpx.Response(200, json=_page([3, 4], "cur3")),
            httpx.Response(200, json=_page([5], None)),
        ]
        page = sync_client.request_page("/products", item_type=Product, params={"limit": 2})
        assert [p.id for p in page] == [1, 2, 3, 4, 5]
        assert route.call_count == 3

    @respx.mock
    def test_next_page_resends_original_params_with_cursor(
        self, sync_client: SyncAPIClient
    ) -> None:
        """The cursor does not encode filters: they must be re-sent each page."""
        route = respx.get(f"{BASE_URL}/products")
        route.side_effect = [
            httpx.Response(200, json=_page([1], "cur2")),
            httpx.Response(200, json=_page([2], None)),
        ]
        page = sync_client.request_page(
            "/products",
            item_type=Product,
            params={"filter": '[{"field":"id","operator":"gteq","value":1}]', "sort": "-id"},
        )
        list(page)
        second = route.calls[1].request
        assert second.url.params["cursor"] == "cur2"
        assert second.url.params["sort"] == "-id"
        assert "filter" in second.url.params

    @respx.mock
    def test_iter_pages(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/products")
        route.side_effect = [
            httpx.Response(200, json=_page([1], "cur2")),
            httpx.Response(200, json=_page([2], None)),
        ]
        page = sync_client.request_page("/products", item_type=Product)
        sizes = [len(p) for p in page.iter_pages()]
        assert sizes == [1, 1]

    @respx.mock
    def test_included_side_loading_is_exposed(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(
                200,
                json={
                    "items": [{"id": 1}],
                    "has_more": False,
                    "next_cursor": None,
                    "included": [{"type": "invoice_line", "id": 9}],
                },
            )
        )
        page = sync_client.request_page("/products", item_type=Product)
        assert page.included == [{"type": "invoice_line", "id": 9}]


class TestAsyncPagination:
    @respx.mock
    async def test_auto_iteration_walks_all_pages(self, async_client: AsyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/products")
        route.side_effect = [
            httpx.Response(200, json=_page([1, 2], "cur2")),
            httpx.Response(200, json=_page([3], None)),
        ]
        page = await async_client.request_page("/products", item_type=Product)
        collected = [product.id async for product in page]
        assert collected == [1, 2, 3]
        assert route.call_count == 2

    @respx.mock
    async def test_manual_next_page(self, async_client: AsyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/products")
        route.side_effect = [
            httpx.Response(200, json=_page([1], "cur2")),
            httpx.Response(200, json=_page([2], None)),
        ]
        page = await async_client.request_page("/products", item_type=Product)
        assert [p.id for p in page.items] == [1]
        next_page = await page.next_page()
        assert next_page is not None
        assert [p.id for p in next_page.items] == [2]
        assert await next_page.next_page() is None


class TestSyncNumberedPagination:
    @respx.mock
    def test_auto_iteration_increments_page(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/companies")
        route.side_effect = [
            httpx.Response(
                200, json={"items": [{"id": 1}], "total_pages": 3, "current_page": 1}
            ),
            httpx.Response(
                200, json={"items": [{"id": 2}], "total_pages": 3, "current_page": 2}
            ),
            httpx.Response(
                200, json={"items": [{"id": 3}], "total_pages": 3, "current_page": 3}
            ),
        ]
        page = sync_client.request_numbered_page(
            "/companies", item_type=Product, params={"per_page": 1}
        )
        assert [p.id for p in page] == [1, 2, 3]
        assert route.call_count == 3
        second = route.calls[1].request
        assert second.url.params["page"] == "2"
        assert second.url.params["per_page"] == "1"

    @respx.mock
    def test_single_page_has_no_next(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/companies").mock(
            return_value=httpx.Response(
                200, json={"items": [{"id": 1}], "total_pages": 1, "current_page": 1}
            )
        )
        page = sync_client.request_numbered_page("/companies", item_type=Product)
        assert page.has_more is False
        assert page.next_page() is None

    @respx.mock
    def test_missing_pagination_fields_stop_iteration(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/companies").mock(
            return_value=httpx.Response(200, json={"items": [{"id": 1}]})
        )
        page = sync_client.request_numbered_page("/companies", item_type=Product)
        assert [p.id for p in page] == [1]


class TestAsyncNumberedPagination:
    @respx.mock
    async def test_auto_iteration(self, async_client: AsyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/companies")
        route.side_effect = [
            httpx.Response(
                200, json={"items": [{"id": 1}], "total_pages": 2, "current_page": 1}
            ),
            httpx.Response(
                200, json={"items": [{"id": 2}], "total_pages": 2, "current_page": 2}
            ),
        ]
        page = await async_client.request_numbered_page("/companies", item_type=Product)
        assert [p.id async for p in page] == [1, 2]
