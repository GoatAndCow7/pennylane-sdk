from __future__ import annotations

import json

import httpx
import respx

from pennylane_sdk._base_client import AsyncAPIClient, SyncAPIClient
from pennylane_sdk.resources.company.suppliers import AsyncSuppliers, Suppliers

from ..conftest import BASE_URL

SUPPLIER = {
    "id": 7,
    "name": "Office Supplies Co",
    "establishment_no": "12345678900012",
    "reg_no": "123456789",
    "vat_number": "FR987654321",
    "ledger_account": {"id": 3},
    "emails": ["billing@supplier.example"],
    "iban": "FR1420041010050500013M02606",
    "postal_address": {
        "address": "2 avenue des Champs",
        "postal_code": "75008",
        "city": "Paris",
        "country_alpha2": "FR",
    },
    "supplier_payment_method": "automatic_transfer",
    "supplier_due_date_delay": 30,
    "supplier_due_date_rule": "days",
    "external_reference": "SUP-1",
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}

CATEGORY = {
    "id": 421,
    "label": "Office supplies",
    "weight": "1.0",
    "category_group": {"id": 9},
    "analytical_code": None,
    "created_at": "2026-01-05T09:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z",
}


class TestSuppliers:
    @respx.mock
    def test_list(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/suppliers").mock(
            return_value=httpx.Response(
                200, json={"items": [SUPPLIER], "has_more": False, "next_cursor": None}
            )
        )
        page = Suppliers(sync_client).list(limit=50, sort="-id")
        assert route.calls.last.request.url.params["limit"] == "50"
        supplier = page.items[0]
        assert supplier.id == 7
        assert supplier.ledger_account is not None
        assert supplier.ledger_account.id == 3
        assert supplier.postal_address is not None
        assert supplier.postal_address.city == "Paris"

    @respx.mock
    def test_create(self, sync_client: SyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/suppliers").mock(
            return_value=httpx.Response(201, json=SUPPLIER)
        )
        supplier = Suppliers(sync_client).create(
            name="Office Supplies Co",
            postal_address={
                "address": "2 avenue des Champs",
                "postal_code": "75008",
                "city": "Paris",
                "country_alpha2": "FR",
            },
            vat_number="FR987654321",
        )
        body = json.loads(route.calls.last.request.content)
        assert body == {
            "name": "Office Supplies Co",
            "postal_address": {
                "address": "2 avenue des Champs",
                "postal_code": "75008",
                "city": "Paris",
                "country_alpha2": "FR",
            },
            "vat_number": "FR987654321",
        }
        assert supplier.id == 7

    @respx.mock
    def test_get(self, sync_client: SyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/suppliers/7").mock(
            return_value=httpx.Response(200, json=SUPPLIER)
        )
        supplier = Suppliers(sync_client).get(7)
        assert supplier.name == "Office Supplies Co"

    @respx.mock
    def test_update(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/suppliers/7").mock(
            return_value=httpx.Response(200, json=SUPPLIER)
        )
        Suppliers(sync_client).update(7, name="New name")
        assert json.loads(route.calls.last.request.content) == {"name": "New name"}

    @respx.mock
    def test_list_categories(self, sync_client: SyncAPIClient) -> None:
        route = respx.get(f"{BASE_URL}/suppliers/7/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = Suppliers(sync_client).list_categories(7, limit=10)
        assert route.calls.last.request.url.params["limit"] == "10"
        assert page.items[0].id == 421

    @respx.mock
    def test_categorize(self, sync_client: SyncAPIClient) -> None:
        route = respx.put(f"{BASE_URL}/suppliers/7/categories").mock(
            return_value=httpx.Response(200, json=[CATEGORY])
        )
        result = Suppliers(sync_client).categorize(7, categories=[{"id": 421, "weight": "1.0"}])
        assert json.loads(route.calls.last.request.content) == [{"id": 421, "weight": "1.0"}]
        assert result is None


class TestAsyncSuppliers:
    @respx.mock
    async def test_list(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/suppliers").mock(
            return_value=httpx.Response(
                200, json={"items": [SUPPLIER], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncSuppliers(async_client).list()
        assert page.items[0].id == 7

    @respx.mock
    async def test_create(self, async_client: AsyncAPIClient) -> None:
        route = respx.post(f"{BASE_URL}/suppliers").mock(
            return_value=httpx.Response(201, json=SUPPLIER)
        )
        supplier = await AsyncSuppliers(async_client).create(name="Office Supplies Co")
        assert supplier.id == 7
        body = json.loads(route.calls.last.request.content)
        assert body == {"name": "Office Supplies Co"}

    @respx.mock
    async def test_get(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/suppliers/7").mock(
            return_value=httpx.Response(200, json=SUPPLIER)
        )
        supplier = await AsyncSuppliers(async_client).get(7)
        assert supplier.id == 7

    @respx.mock
    async def test_update(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/suppliers/7").mock(
            return_value=httpx.Response(200, json=SUPPLIER)
        )
        supplier = await AsyncSuppliers(async_client).update(7, vat_number="FR000000000")
        assert supplier.id == 7

    @respx.mock
    async def test_list_categories(self, async_client: AsyncAPIClient) -> None:
        respx.get(f"{BASE_URL}/suppliers/7/categories").mock(
            return_value=httpx.Response(
                200, json={"items": [CATEGORY], "has_more": False, "next_cursor": None}
            )
        )
        page = await AsyncSuppliers(async_client).list_categories(7)
        assert page.items[0].id == 421

    @respx.mock
    async def test_categorize(self, async_client: AsyncAPIClient) -> None:
        respx.put(f"{BASE_URL}/suppliers/7/categories").mock(
            return_value=httpx.Response(200, json=[CATEGORY])
        )
        result = await AsyncSuppliers(async_client).categorize(
            7, categories=[{"id": 421, "weight": "1.0"}]
        )
        assert result is None
