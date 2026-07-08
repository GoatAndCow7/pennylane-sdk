from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.products import AsyncProducts, Products

from ..conftest import BASE_URL

PRODUCT = {
    "id": 42,
    "label": "Consulting day",
    "description": "One day of consulting",
    "external_reference": "CONS-1",
    "price_before_tax": "500.00",
    "vat_rate": "FR_200",
    "price": "600.00",
    "unit": "day",
    "currency": "EUR",
    "reference": None,
    "ledger_account": {"id": 7},
    "archived_at": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestProducts:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(
                200, json={"items": [PRODUCT], "has_more": False, "next_cursor": None}
            )
        )
        page = Products(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        assert route.calls.last.request.url.params["sort"] == "-id"
        product = page.items[0]
        assert product.id == 42
        assert product.price_before_tax == Decimal("500.00")
        assert product.ledger_account is not None
        assert product.ledger_account.id == 7

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/products/42").mock(
            return_value=httpx.Response(200, json=PRODUCT)
        )
        product = Products(sync_client).get(42)
        assert product.label == "Consulting day"

    @respx.mock
    def test_create_sends_money_as_string_and_drops_none(
        self, sync_client: SyncAPIClient
    ) -> None:
        route = respx.post(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(201, json=PRODUCT)
        )
        Products(sync_client).create(
            label="Consulting day",
            price_before_tax=Decimal("500.00"),
            vat_rate="FR_200",
            unit="day",
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "label": "Consulting day",
            "price_before_tax": "500.00",
            "vat_rate": "FR_200",
            "unit": "day",
        }

    @respx.mock
    def test_update_sends_only_provided_fields(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/products/42").mock(
            return_value=httpx.Response(200, json=PRODUCT)
        )
        Products(sync_client).update(42, label="New label")
        assert json.loads(route.calls.last.request.content) == {"label": "New label"}


class TestAsyncProducts:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(
                200, json={"items": [PRODUCT], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncProducts(async_client).list()
        assert page.items[0].id == 42

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/products").mock(
            return_value=httpx.Response(201, json=PRODUCT)
        )
        product = await AsyncProducts(async_client).create(
            label="Consulting day",
            price_before_tax="500.00",
            vat_rate="FR_200",
        )
        assert product.id == 42
        body = json.loads(route.calls.last.request.content)
        assert body["price_before_tax"] == "500.00"

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/products/42").mock(
            return_value=httpx.Response(200, json=PRODUCT)
        )
        product = await AsyncProducts(async_client).update(42, vat_rate="FR_100")
        assert product.id == 42
